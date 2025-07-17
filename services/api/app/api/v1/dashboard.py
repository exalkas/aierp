"""
Dashboard API endpoints for Greek ERP/CRM System
Provides aggregated statistics for dashboard KPIs
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract, text, desc, or_
from sqlalchemy.exc import ProgrammingError
from pydantic import BaseModel
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from ...core.database import get_db
from ...models.user import User
from ...models.business_entity import BusinessEntity, BusinessEntityRole, BusinessEntityStatus, business_entity_roles
from ...models.invoice import Invoice, InvoiceType, InvoiceStatus
from ...models.opportunity import Opportunity, OpportunityStage
from ...models.activity import Activity, ActivityType, ActivityStatus
from ...models.audit_log import AuditLog, AuditAction, AuditEntityType
from ...models.contact import Contact
from ...middleware.company_isolation import get_current_user_and_company

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
logger = logging.getLogger(__name__)


def get_current_user(user_company = Depends(get_current_user_and_company)) -> User:
    """Get current authenticated user"""
    user, company_id = user_company
    return user


class DashboardStatsResponse(BaseModel):
    """Response model for dashboard statistics"""
    total_customers: int
    monthly_invoices: int
    monthly_revenue: float
    active_opportunities: int
    # Additional metrics for context
    monthly_revenue_formatted: str
    change_indicators: Dict[str, float] = {}
    last_updated: str


class DetailedDashboardStatsResponse(BaseModel):
    """Response model for detailed dashboard statistics"""
    total_customers: int
    monthly_invoices: int
    monthly_revenue: float
    active_opportunities: int
    monthly_revenue_formatted: str
    period: Dict[str, Any]
    change_indicators: Dict[str, float] = {}
    last_updated: str


class RecentActivityResponse(BaseModel):
    """Response model for a single recent activity"""
    id: str
    type: str  # "activity", "audit", "system"
    title: str
    description: Optional[str]
    time: str  # "2 hours ago", "yesterday"
    timestamp: datetime
    icon: str  # "FileText", "Users", "Phone", etc.
    color: str  # "green", "blue", "purple", etc.
    entity_type: Optional[str]  # "customer", "invoice", "opportunity"
    entity_id: Optional[str]
    user_name: Optional[str]


class RecentActivitiesResponse(BaseModel):
    """Response model for recent activities list"""
    activities: List[RecentActivityResponse]
    total_count: int
    last_updated: str


class QuickActionResponse(BaseModel):
    """Response model for quick actions with dynamic data"""
    title: str
    description: str
    icon: str
    color: str
    href: str
    count: Optional[int] = None
    status: Optional[str] = None


class QuickActionsResponse(BaseModel):
    """Response model for quick actions list"""
    actions: List[QuickActionResponse]
    last_updated: str


class DashboardService:
    """Service class for dashboard statistics calculations"""
    
    def __init__(self, db: Session, company_id: str):
        self.db = db
        self.company_id = company_id
    
    def get_total_customers(self) -> int:
        """Get total number of active customers"""
        try:
            return self.db.query(func.count(BusinessEntity.id.distinct())).join(
                business_entity_roles,
                BusinessEntity.id == business_entity_roles.c.business_entity_id
            ).filter(
                and_(
                    BusinessEntity.company_id == self.company_id,
                    business_entity_roles.c.role.in_([BusinessEntityRole.CUSTOMER]),
                    business_entity_roles.c.is_active == True,
                    BusinessEntity.status == BusinessEntityStatus.ACTIVE
                )
            ).scalar() or 0
        except Exception as e:
            logger.error(f"Error getting total customers: {e}")
            # Fallback: count all active business entities
            try:
                return self.db.query(func.count(BusinessEntity.id)).filter(
                    and_(
                        BusinessEntity.company_id == self.company_id,
                        BusinessEntity.status == BusinessEntityStatus.ACTIVE
                    )
                ).scalar() or 0
            except Exception as fallback_e:
                logger.error(f"Fallback query failed: {fallback_e}")
                return 0

    def get_monthly_invoices(self, month: int = None, year: int = None) -> int:
        """Get count of invoices for the current month"""
        if not month or not year:
            now = datetime.now()
            month = now.month
            year = now.year

        try:
            # Try with invoice_type column
            return self.db.query(func.count(Invoice.id)).filter(
                and_(
                    Invoice.company_id == self.company_id,
                    Invoice.invoice_type.in_([
                        InvoiceType.SALES_INVOICE,
                        InvoiceType.RECEIPT,
                        InvoiceType.SIMPLIFIED_INVOICE
                    ]),
                    Invoice.status != InvoiceStatus.CANCELLED,
                    extract('month', Invoice.issue_date) == month,
                    extract('year', Invoice.issue_date) == year
                )
            ).scalar() or 0
        except (ProgrammingError, Exception) as e:
            logger.warning(f"invoice_type column not found, using fallback: {e}")
            # Rollback the failed transaction before trying fallback
            self.db.rollback()
            try:
                return self.db.query(func.count(Invoice.id)).filter(
                    and_(
                        Invoice.company_id == self.company_id,
                        extract('month', Invoice.issue_date) == month,
                        extract('year', Invoice.issue_date) == year
                    )
                ).scalar() or 0
            except Exception as fallback_e:
                logger.error(f"Fallback invoice query failed: {fallback_e}")
                self.db.rollback()
                return 0

    def get_monthly_revenue(self, month: int = None, year: int = None) -> Decimal:
        """Get total revenue for the current month"""
        if not month or not year:
            now = datetime.now()
            month = now.month
            year = now.year

        try:
            # Try with invoice_type and status columns
            result = self.db.query(func.sum(Invoice.total_amount)).filter(
                and_(
                    Invoice.company_id == self.company_id,
                    Invoice.invoice_type.in_([
                        InvoiceType.SALES_INVOICE,
                        InvoiceType.RECEIPT,
                        InvoiceType.SIMPLIFIED_INVOICE
                    ]),
                    Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.PAID, InvoiceStatus.PARTIALLY_PAID]),
                    extract('month', Invoice.issue_date) == month,
                    extract('year', Invoice.issue_date) == year
                )
            ).scalar()
            return result or Decimal('0.00')
        except (ProgrammingError, Exception) as e:
            logger.warning(f"Advanced invoice filtering not available, using fallback: {e}")
            # Rollback the failed transaction before trying fallback
            self.db.rollback()
            try:
                result = self.db.query(func.sum(Invoice.total_amount)).filter(
                    and_(
                        Invoice.company_id == self.company_id,
                        extract('month', Invoice.issue_date) == month,
                        extract('year', Invoice.issue_date) == year
                    )
                ).scalar()
                return result or Decimal('0.00')
            except Exception as fallback_e:
                logger.error(f"Fallback revenue query failed: {fallback_e}")
                self.db.rollback()
                return Decimal('0.00')

    def get_active_opportunities(self) -> int:
        """Get count of active opportunities"""
        try:
            return self.db.query(func.count(Opportunity.id)).filter(
                and_(
                    Opportunity.company_id == self.company_id,
                    Opportunity.stage.notin_([OpportunityStage.CLOSED_WON, OpportunityStage.CLOSED_LOST])
                )
            ).scalar() or 0
        except Exception as e:
            logger.error(f"Error getting active opportunities: {e}")
            # Rollback the failed transaction before trying fallback
            self.db.rollback()
            try:
                return self.db.query(func.count(Opportunity.id)).filter(
                    Opportunity.company_id == self.company_id
                ).scalar() or 0
            except Exception as fallback_e:
                logger.error(f"Fallback opportunity query failed: {fallback_e}")
                self.db.rollback()
                return 0

    def calculate_change_indicators(self, month: int, year: int) -> Dict[str, float]:
        """Calculate month-over-month change indicators"""
        try:
            # Calculate previous month
            prev_month = month - 1 if month > 1 else 12
            prev_year = year if month > 1 else year - 1
            
            # Current month metrics
            current_invoices = self.get_monthly_invoices(month, year)
            current_revenue = float(self.get_monthly_revenue(month, year))
            
            # Previous month metrics
            prev_invoices = self.get_monthly_invoices(prev_month, prev_year)
            prev_revenue = float(self.get_monthly_revenue(prev_month, prev_year))
            
            # Calculate percentage changes
            invoice_change = ((current_invoices - prev_invoices) / prev_invoices * 100) if prev_invoices > 0 else 0
            revenue_change = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            
            return {
                "invoices": round(invoice_change, 1),
                "revenue": round(revenue_change, 1),
                "customers": 0.0,  # Customer count doesn't change monthly typically
                "opportunities": 0.0  # Opportunity count change would need more complex calculation
            }
        except Exception as e:
            logger.error(f"Error calculating change indicators: {e}")
            return {
                "invoices": 0.0,
                "revenue": 0.0,
                "customers": 0.0,
                "opportunities": 0.0
            }

    def get_recent_activities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities from both Activity and AuditLog models"""
        activities = []
        
        try:
            # Get recent activities from Activity model
            recent_activities = self.db.query(Activity).filter(
                Activity.company_id == self.company_id
            ).order_by(desc(Activity.created_at)).limit(limit // 2).all()
            
            for activity in recent_activities:
                # Format activity data
                icon = self._get_activity_icon(activity.activity_type)
                color = self._get_activity_color(activity.activity_type)
                time_ago = self._format_time_ago(activity.created_at)
                
                activities.append({
                    "id": str(activity.id),
                    "type": "activity",
                    "title": activity.title,
                    "description": activity.description,
                    "time": time_ago,
                    "timestamp": activity.created_at,
                    "icon": icon,
                    "color": color,
                    "entity_type": activity.activity_type.value,
                    "entity_id": str(activity.business_entity_id) if activity.business_entity_id else None,
                    "user_name": None  # Would need to join with User model
                })
                
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
        
        try:
            # Get recent audit log entries
            recent_audits = self.db.query(AuditLog).filter(
                AuditLog.entity_type.in_([
                    AuditEntityType.BUSINESS_ENTITY,
                    AuditEntityType.INVOICE,
                    AuditEntityType.PRODUCT
                ])
            ).order_by(desc(AuditLog.timestamp)).limit(limit // 2).all()
            
            for audit in recent_audits:
                # Format audit data
                icon = self._get_audit_icon(audit.entity_type, audit.action)
                color = self._get_audit_color(audit.action)
                time_ago = self._format_time_ago(audit.timestamp)
                title = self._get_audit_title(audit.entity_type, audit.action, audit.description)
                
                activities.append({
                    "id": str(audit.id),
                    "type": "audit",
                    "title": title,
                    "description": audit.description,
                    "time": time_ago,
                    "timestamp": audit.timestamp,
                    "icon": icon,
                    "color": color,
                    "entity_type": audit.entity_type.value,
                    "entity_id": str(audit.entity_id),
                    "user_name": audit.user_name
                })
                
        except Exception as e:
            logger.error(f"Error fetching audit logs: {e}")
        
        # Sort all activities by timestamp (most recent first)
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return activities[:limit]

    def _get_activity_icon(self, activity_type: ActivityType) -> str:
        """Get icon for activity type"""
        icon_map = {
            ActivityType.PHONE_CALL: "Phone",
            ActivityType.EMAIL: "Mail",
            ActivityType.MEETING: "Users",
            ActivityType.TASK: "CheckSquare",
            ActivityType.NOTE: "FileText",
            ActivityType.APPOINTMENT: "Calendar",
            ActivityType.FOLLOW_UP: "ArrowRight",
            ActivityType.DEMO: "Monitor",
            ActivityType.PRESENTATION: "Presentation",
            ActivityType.SITE_VISIT: "MapPin"
        }
        return icon_map.get(activity_type, "Activity")

    def _get_activity_color(self, activity_type: ActivityType) -> str:
        """Get color for activity type"""
        color_map = {
            ActivityType.PHONE_CALL: "purple",
            ActivityType.EMAIL: "blue",
            ActivityType.MEETING: "green",
            ActivityType.TASK: "orange",
            ActivityType.NOTE: "gray",
            ActivityType.APPOINTMENT: "blue",
            ActivityType.FOLLOW_UP: "yellow",
            ActivityType.DEMO: "purple",
            ActivityType.PRESENTATION: "green",
            ActivityType.SITE_VISIT: "red"
        }
        return color_map.get(activity_type, "gray")

    def _get_audit_icon(self, entity_type: AuditEntityType, action: AuditAction) -> str:
        """Get icon for audit action"""
        if action == AuditAction.CREATE:
            if entity_type == AuditEntityType.BUSINESS_ENTITY:
                return "UserPlus"
            elif entity_type == AuditEntityType.INVOICE:
                return "FileText"
            elif entity_type == AuditEntityType.PRODUCT:
                return "Package"
        elif action == AuditAction.UPDATE:
            return "Edit"
        elif action == AuditAction.DELETE:
            return "Trash"
        
        return "Activity"

    def _get_audit_color(self, action: AuditAction) -> str:
        """Get color for audit action"""
        color_map = {
            AuditAction.CREATE: "green",
            AuditAction.UPDATE: "blue",
            AuditAction.DELETE: "red",
            AuditAction.ACTIVATE: "green",
            AuditAction.DEACTIVATE: "orange"
        }
        return color_map.get(action, "gray")

    def _get_audit_title(self, entity_type: AuditEntityType, action: AuditAction, description: str) -> str:
        """Generate title for audit log entry"""
        entity_names = {
            AuditEntityType.BUSINESS_ENTITY: "Customer",
            AuditEntityType.INVOICE: "Invoice",
            AuditEntityType.PRODUCT: "Product",
            AuditEntityType.COMPANY: "Company",
            AuditEntityType.USER: "User"
        }
        
        action_names = {
            AuditAction.CREATE: "Created",
            AuditAction.UPDATE: "Updated", 
            AuditAction.DELETE: "Deleted",
            AuditAction.ACTIVATE: "Activated",
            AuditAction.DEACTIVATE: "Deactivated"
        }
        
        entity_name = entity_names.get(entity_type, entity_type.value)
        action_name = action_names.get(action, action.value)
        
        if description:
            return f"{action_name} {entity_name}: {description[:50]}..."
        return f"{action_name} {entity_name}"

    def _format_time_ago(self, timestamp: datetime) -> str:
        """Format timestamp as 'time ago' string"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 1:
            return f"{diff.days} days ago"
        elif diff.days == 1:
            return "yesterday"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"

    def get_quick_actions_data(self) -> List[Dict[str, Any]]:
        """Get quick actions with dynamic counts"""
        try:
            # Get counts for dynamic data
            draft_invoices = self.db.query(func.count(Invoice.id)).filter(
                and_(
                    Invoice.company_id == self.company_id,
                    Invoice.status == InvoiceStatus.DRAFT
                )
            ).scalar() or 0
            
            open_opportunities = self.db.query(func.count(Opportunity.id)).filter(
                and_(
                    Opportunity.company_id == self.company_id,
                    Opportunity.stage.notin_([OpportunityStage.CLOSED_WON, OpportunityStage.CLOSED_LOST])
                )
            ).scalar() or 0
            
            pending_activities = self.db.query(func.count(Activity.id)).filter(
                and_(
                    Activity.company_id == self.company_id,
                    Activity.status == ActivityStatus.PLANNED,
                    Activity.start_date <= datetime.now() + timedelta(days=1)
                )
            ).scalar() or 0
            
            total_customers = self.get_total_customers()
            
            return [
                {
                    "title": "new_invoice",
                    "description": "new_invoice_desc", 
                    "icon": "FileText",
                    "color": "green",
                    "href": "/invoices/new",
                    "count": draft_invoices,
                    "status": f"{draft_invoices} drafts"
                },
                {
                    "title": "new_customer",
                    "description": "new_customer_desc",
                    "icon": "Users", 
                    "color": "blue",
                    "href": "/customers/new",
                    "count": total_customers,
                    "status": f"{total_customers} total"
                },
                {
                    "title": "new_opportunity",
                    "description": "new_opportunity_desc",
                    "icon": "Target",
                    "color": "purple", 
                    "href": "/opportunities/new",
                    "count": open_opportunities,
                    "status": f"{open_opportunities} open"
                },
                {
                    "title": "schedule",
                    "description": "schedule_desc",
                    "icon": "Calendar",
                    "color": "orange",
                    "href": "/activities/new", 
                    "count": pending_activities,
                    "status": f"{pending_activities} pending"
                }
            ]
            
        except Exception as e:
            logger.error(f"Error getting quick actions data: {e}")
            # Return basic actions without counts
            return [
                {
                    "title": "new_invoice",
                    "description": "new_invoice_desc",
                    "icon": "FileText",
                    "color": "green", 
                    "href": "/invoices/new"
                },
                {
                    "title": "new_customer",
                    "description": "new_customer_desc",
                    "icon": "Users",
                    "color": "blue",
                    "href": "/customers/new"
                },
                {
                    "title": "new_opportunity", 
                    "description": "new_opportunity_desc",
                    "icon": "Target",
                    "color": "purple",
                    "href": "/opportunities/new"
                },
                {
                    "title": "schedule",
                    "description": "schedule_desc", 
                    "icon": "Calendar",
                    "color": "orange",
                    "href": "/activities/new"
                }
            ]


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    try:
        dashboard_service = DashboardService(db, current_user.company_id)
        
        now = datetime.now()
        
        # Get current statistics
        total_customers = dashboard_service.get_total_customers()
        monthly_invoices = dashboard_service.get_monthly_invoices(now.month, now.year)
        monthly_revenue = dashboard_service.get_monthly_revenue(now.month, now.year)
        active_opportunities = dashboard_service.get_active_opportunities()
        
        # Get change indicators
        change_indicators = dashboard_service.calculate_change_indicators(now.month, now.year)
        
        # Format revenue
        monthly_revenue_formatted = f"€{monthly_revenue:,.2f}"
        
        return DashboardStatsResponse(
            total_customers=total_customers,
            monthly_invoices=monthly_invoices,
            monthly_revenue=float(monthly_revenue),
            active_opportunities=active_opportunities,
            monthly_revenue_formatted=monthly_revenue_formatted,
            change_indicators=change_indicators,
            last_updated=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error calculating dashboard statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating dashboard statistics: {str(e)}"
        )


@router.get("/stats/detailed", response_model=DetailedDashboardStatsResponse)
async def get_detailed_dashboard_stats(
    month: int = Query(None, description="Month (1-12)"),
    year: int = Query(None, description="Year"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed dashboard statistics with optional month/year filtering"""
    try:
        dashboard_service = DashboardService(db, current_user.company_id)
        
        # Use current month/year if not provided
        if not month or not year:
            now = datetime.now()
            month = now.month
            year = now.year
        
        # Validate month/year
        if not (1 <= month <= 12) or year < 2020 or year > 2030:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid month or year provided"
            )
        
        # Get statistics
        total_customers = dashboard_service.get_total_customers()
        monthly_invoices = dashboard_service.get_monthly_invoices(month, year)
        monthly_revenue = dashboard_service.get_monthly_revenue(month, year)
        active_opportunities = dashboard_service.get_active_opportunities()
        
        # Get change indicators
        change_indicators = dashboard_service.calculate_change_indicators(month, year)
        
        # Format revenue
        monthly_revenue_formatted = f"€{monthly_revenue:,.2f}"
        
        stats = {
            "total_customers": total_customers,
            "monthly_invoices": monthly_invoices,
            "monthly_revenue": float(monthly_revenue),
            "active_opportunities": active_opportunities,
            "monthly_revenue_formatted": monthly_revenue_formatted,
            "period": {
                "month": month,
                "year": year,
                "month_name": datetime(year, month, 1).strftime("%B")
            },
            "change_indicators": change_indicators,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating detailed dashboard statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating dashboard statistics: {str(e)}"
        )


@router.get("/recent-activities", response_model=RecentActivitiesResponse)
async def get_recent_activities(
    limit: int = Query(10, description="Number of activities to return", ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent activities for the dashboard"""
    try:
        dashboard_service = DashboardService(db, current_user.company_id)
        activities_data = dashboard_service.get_recent_activities(limit)
        
        activities = [
            RecentActivityResponse(**activity) for activity in activities_data
        ]
        
        return RecentActivitiesResponse(
            activities=activities,
            total_count=len(activities),
            last_updated=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error fetching recent activities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching recent activities: {str(e)}"
        )


@router.get("/quick-actions", response_model=QuickActionsResponse)
async def get_quick_actions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get quick actions with dynamic data for the dashboard"""
    try:
        dashboard_service = DashboardService(db, current_user.company_id)
        actions_data = dashboard_service.get_quick_actions_data()
        
        actions = [
            QuickActionResponse(**action) for action in actions_data
        ]
        
        return QuickActionsResponse(
            actions=actions,
            last_updated=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error fetching quick actions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching quick actions: {str(e)}"
        ) 