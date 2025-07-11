// Greek ERP/CRM - Admin Users Module

// User management types
export interface AdminUser {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  permissions: string[];
  companyId: string;
  isActive: boolean;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserRole {
  id: string;
  name: string;
  description: string;
  permissions: string[];
  isSystemRole: boolean;
}

export interface UserPermission {
  id: string;
  name: string;
  description: string;
  category: string;
  resource: string;
  action: string;
}

// Admin utilities
export const createUser = (data: Partial<AdminUser>): AdminUser => {
  const now = new Date();
  return {
    id: `user_${Date.now()}`,
    email: data.email || "",
    name: data.name || "",
    role: data.role || {
      id: "user",
      name: "User",
      description: "Basic user",
      permissions: [],
      isSystemRole: true,
    },
    permissions: data.permissions || [],
    companyId: data.companyId || "",
    isActive: data.isActive !== undefined ? data.isActive : true,
    lastLogin: data.lastLogin,
    createdAt: now,
    updatedAt: now,
  };
};

export const validateEmail = (email: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const hasPermission = (user: AdminUser, permission: string): boolean => {
  return (
    user.permissions.includes(permission) ||
    user.role.permissions.includes(permission)
  );
};

export const getSystemRoles = (): UserRole[] => {
  return [
    {
      id: "admin",
      name: "Administrator",
      description: "Full system access",
      permissions: ["*"],
      isSystemRole: true,
    },
    {
      id: "manager",
      name: "Manager",
      description: "Business management access",
      permissions: ["users:read", "customers:*", "invoices:*", "reports:*"],
      isSystemRole: true,
    },
    {
      id: "user",
      name: "User",
      description: "Basic user access",
      permissions: ["customers:read", "invoices:create", "invoices:read"],
      isSystemRole: true,
    },
  ];
};
