"use client";

import { useTranslation, useAuth } from "@erp/shared-ui";
import { useState, useEffect } from "react";
import {
  TrendingUp,
  Users,
  FileText,
  Calendar,
  DollarSign,
  Target,
  Phone,
  Mail,
  Plus,
  ArrowUpRight,
  Activity,
  Building,
  CheckCircle,
  Package,
  BarChart3,
  Settings,
  Zap,
  Clock,
} from "lucide-react";

export default function DashboardPage() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update time every minute
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  const formatGreekTime = (date: Date) => {
    return date.toLocaleString("el-GR", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  // Mock data - In production, this would come from APIs
  const kpis = [
    {
      title: "Συνολικοί Πελάτες",
      value: "847",
      change: "+12%",
      trend: "up",
      icon: Users,
      color: "blue",
    },
    {
      title: "Μηνιαία Τιμολόγια",
      value: "156",
      change: "+18%",
      trend: "up",
      icon: FileText,
      color: "green",
    },
    {
      title: "Μηνιαίος Τζίρος",
      value: "€47.350",
      change: "+8.2%",
      trend: "up",
      icon: TrendingUp,
      color: "purple",
    },
    {
      title: "Ενεργές Ευκαιρίες",
      value: "23",
      change: "+5",
      trend: "up",
      icon: Target,
      color: "orange",
    },
  ];

  const recentActivities = [
    {
      type: "invoice",
      title: "Τιμολόγιο #2024-0087 → AADE",
      time: "πριν 1 ώρα",
      icon: FileText,
      color: "green",
    },
    {
      type: "customer",
      title: "Νέος πελάτης: Παπαδόπουλος Α.Ε.",
      time: "πριν 2 ώρες",
      icon: Building,
      color: "blue",
    },
    {
      type: "call",
      title: "Κλήση με Μαρία Κωστάκου",
      time: "πριν 4 ώρες",
      icon: Phone,
      color: "purple",
    },
    {
      type: "opportunity",
      title: "Νέα ευκαιρία: €15.000 προσφορά",
      time: "χθες",
      icon: Target,
      color: "orange",
    },
  ];

  const quickActions = [
    {
      title: "Νέο Τιμολόγιο",
      description: "Δημιουργία και αποστολή στο AADE",
      icon: FileText,
      color: "green",
      href: "/invoices/new",
    },
    {
      title: "Νέος Πελάτης",
      description: "Καταχώρηση επιχείρησης/προμηθευτή",
      icon: Users,
      color: "blue",
      href: "/customers/new",
    },
    {
      title: "Νέα Ευκαιρία",
      description: "Καταχώρηση ευκαιρίας πώλησης",
      icon: Target,
      color: "purple",
      href: "/opportunities/new",
    },
    {
      title: "Προγραμματισμός",
      description: "Νέο ραντεβού ή δραστηριότητα",
      icon: Calendar,
      color: "orange",
      href: "/activities/new",
    },
  ];

  const moduleCards = [
    {
      icon: "👥",
      title: "Διαχείριση Επιχειρήσεων",
      description: "Πελάτες, προμηθευτές, επαφές & σχέσεις",
      href: "/businesses",
      status: "active",
      phase: "milestone_1",
    },
    {
      icon: "🧾",
      title: "Ελληνική Τιμολόγηση",
      description: "16 είδη παραστατικών & AADE ενσωμάτωση",
      href: "/invoices",
      status: "active",
      phase: "milestone_1",
    },
    {
      icon: "🎯",
      title: "Πωλήσεις & Pipeline",
      description: "Ευκαιρίες, προσφορές & πρόβλεψη πωλήσεων",
      href: "/opportunities",
      status: "active",
      phase: "milestone_1",
    },
    {
      icon: "📦",
      title: "Κατάλογος Προϊόντων",
      description: "Προϊόντα, υπηρεσίες & τιμολόγηση",
      href: "/products",
      status: "developing",
      phase: "erp_core",
    },
    {
      icon: "📋",
      title: "Διαχείριση Αποθέματος",
      description: "Αποθήκες, κίνηση & αυτοματισμοί",
      href: "/inventory",
      status: "planned",
      phase: "erp_core",
    },
    {
      icon: "💰",
      title: "Οικονομική Διαχείριση",
      description: "Λογιστική, ταμείο & χρηματοροές",
      href: "/finance",
      status: "planned",
      phase: "erp_expansion",
    },
    {
      icon: "📊",
      title: "Επιχειρηματικές Αναλύσεις",
      description: "Dashboards, KPIs & προβλέψεις",
      href: "/analytics",
      status: "planned",
      phase: "erp_expansion",
    },
    {
      icon: "🏛️",
      title: "AADE Συμμόρφωση",
      description: "MyDATA, φορολογικές υποχρεώσεις",
      href: "/compliance",
      status: "developing",
      phase: "milestone_1",
    },
    {
      icon: "👨‍💼",
      title: "Διαχείριση Προσωπικού",
      description: "HR, μισθοδοσία & παρουσίες",
      href: "/hr",
      status: "planned",
      phase: "erp_expansion",
    },
  ];

  const getKpiIcon = (IconComponent: any, color: string) => {
    const colorClasses = {
      blue: "text-blue-600 bg-blue-100",
      green: "text-green-600 bg-green-100",
      purple: "text-purple-600 bg-purple-100",
      orange: "text-orange-600 bg-orange-100",
    };

    return (
      <div
        className={`p-3 rounded-full ${
          colorClasses[color as keyof typeof colorClasses]
        }`}
      >
        <IconComponent size={24} />
      </div>
    );
  };

  const getActivityIcon = (IconComponent: any, color: string) => {
    const colorClasses = {
      blue: "text-blue-600",
      green: "text-green-600",
      purple: "text-purple-600",
      orange: "text-orange-600",
    };

    return (
      <IconComponent
        size={16}
        className={colorClasses[color as keyof typeof colorClasses]}
      />
    );
  };

  const getModuleStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <CheckCircle size={20} className="text-green-600" />;
      case "developing":
        return <Zap size={20} className="text-blue-600" />;
      case "planned":
        return <Clock size={20} className="text-gray-400" />;
      default:
        return null;
    }
  };

  const getModuleStatusText = (status: string) => {
    switch (status) {
      case "active":
        return { text: "Ενεργό", className: "bg-green-100 text-green-700" };
      case "developing":
        return { text: "Ανάπτυξη", className: "bg-blue-100 text-blue-700" };
      case "planned":
        return {
          text: "Προγραμματισμένο",
          className: "bg-gray-100 text-gray-600",
        };
      default:
        return { text: "", className: "" };
    }
  };

  const getPhaseColor = (phase: string) => {
    switch (phase) {
      case "milestone_1":
        return "border-l-4 border-l-green-500 bg-green-50";
      case "erp_core":
        return "border-l-4 border-l-blue-500 bg-blue-50";
      case "erp_expansion":
        return "border-l-4 border-l-purple-500 bg-purple-50";
      default:
        return "border-l-4 border-l-gray-300 bg-gray-50";
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Welcome Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-3xl font-bold text-gray-900">
            Καλώς ήρθατε, {user?.name || "Χρήστη"}!
          </h1>
          <div className="text-sm text-gray-600">
            {formatGreekTime(currentTime)}
          </div>
        </div>
        <p className="text-gray-600">
          Επισκόπηση της επιχείρησής σας • Εταιρεία:{" "}
          {user?.name?.split("@")[0] ||
            user?.email?.split("@")[0] ||
            "Δεν έχει οριστεί"}
        </p>
      </div>

      {/* Milestone Progress */}
      <div className="mb-8 p-6 bg-gradient-to-r from-blue-50 to-green-50 rounded-xl border border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-1">
              Πρόοδος Ανάπτυξης
            </h2>
            <p className="text-gray-700">
              <strong>Milestone 1:</strong> CRM + Τιμολόγηση (Ολοκληρώθηκε 75%)
              →<strong className="ml-2">ERP Core:</strong> Αποθέματα +
              Οικονομικά (Επόμενο)
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">3/4</div>
              <div className="text-xs text-gray-600">Milestone 1</div>
            </div>
            <ArrowUpRight className="text-blue-600" size={24} />
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">0/4</div>
              <div className="text-xs text-gray-600">ERP Core</div>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {kpis.map((kpi, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 mb-1">
                  {kpi.title}
                </p>
                <p className="text-2xl font-bold text-gray-900">{kpi.value}</p>
                <div className="flex items-center mt-2">
                  <ArrowUpRight
                    size={16}
                    className={`mr-1 ${
                      kpi.trend === "up" ? "text-green-600" : "text-red-600"
                    }`}
                  />
                  <span
                    className={`text-sm font-medium ${
                      kpi.trend === "up" ? "text-green-600" : "text-red-600"
                    }`}
                  >
                    {kpi.change}
                  </span>
                </div>
              </div>
              {getKpiIcon(kpi.icon, kpi.color)}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Quick Actions */}
        <div className="lg:col-span-1">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Γρήγορες Ενέργειες
          </h2>
          <div className="space-y-3">
            {quickActions.map((action, index) => (
              <button
                key={index}
                className="w-full p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all text-left group"
              >
                <div className="flex items-center">
                  <div
                    className={`p-2 rounded-lg mr-3 group-hover:scale-110 transition-transform ${
                      action.color === "blue"
                        ? "bg-blue-100 text-blue-600"
                        : action.color === "green"
                        ? "bg-green-100 text-green-600"
                        : action.color === "purple"
                        ? "bg-purple-100 text-purple-600"
                        : "bg-orange-100 text-orange-600"
                    }`}
                  >
                    <action.icon size={20} />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{action.title}</p>
                    <p className="text-sm text-gray-600">
                      {action.description}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Recent Activities */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Πρόσφατες Δραστηριότητες
          </h2>
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-center">
                  <div className="flex-shrink-0 mr-3">
                    {getActivityIcon(activity.icon, activity.color)}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.title}
                    </p>
                    <p className="text-xs text-gray-600">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
            <button className="w-full mt-4 text-sm text-blue-600 hover:text-blue-800 font-medium">
              Δείτε όλες τις δραστηριότητες →
            </button>
          </div>
        </div>
      </div>

      {/* Module Cards - Organized by Development Phase */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-6">
          Μονάδες Συστήματος - Roadmap Ανάπτυξης
        </h2>

        {/* Phase Headers */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="font-semibold text-green-800 flex items-center">
              <CheckCircle size={16} className="mr-2" />
              Milestone 1: CRM + Τιμολόγηση
            </h3>
            <p className="text-sm text-green-700 mt-1">
              Βασικές επιχειρηματικές λειτουργίες
            </p>
          </div>
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-800 flex items-center">
              <Zap size={16} className="mr-2" />
              ERP Core: Αποθέματα + Οικονομικά
            </h3>
            <p className="text-sm text-blue-700 mt-1">
              Ολοκληρωμένη επιχειρησιακή διαχείριση
            </p>
          </div>
          <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
            <h3 className="font-semibold text-purple-800 flex items-center">
              <Clock size={16} className="mr-2" />
              ERP Expansion: Προηγμένες Λειτουργίες
            </h3>
            <p className="text-sm text-purple-700 mt-1">
              Προηγμένες αναλύσεις & αυτοματισμοί
            </p>
          </div>
        </div>

        {/* Module Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {moduleCards.map((card, index) => (
            <div
              key={index}
              className={`bg-white p-6 rounded-xl border border-gray-200 hover:shadow-md transition-all group cursor-pointer ${getPhaseColor(
                card.phase
              )}`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="text-3xl mb-3">{card.icon}</div>
                <div className="flex flex-col items-end space-y-2">
                  {getModuleStatusBadge(card.status)}
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${
                      getModuleStatusText(card.status).className
                    }`}
                  >
                    {getModuleStatusText(card.status).text}
                  </span>
                </div>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                {card.title}
              </h3>
              <p className="text-gray-600 text-sm mb-4">{card.description}</p>
              {card.status === "active" && (
                <div className="flex items-center text-blue-600 text-sm font-medium group-hover:text-blue-800">
                  Άνοιγμα μονάδας <ArrowUpRight size={16} className="ml-1" />
                </div>
              )}
              {card.status === "developing" && (
                <div className="flex items-center text-blue-600 text-sm font-medium">
                  Σε ανάπτυξη <Activity size={16} className="ml-1" />
                </div>
              )}
              {card.status === "planned" && (
                <div className="flex items-center text-gray-500 text-sm">
                  Επόμενη φάση <Clock size={16} className="ml-1" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Footer Info */}
      <div className="mt-12 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Activity className="text-blue-600 mr-3" size={24} />
            <div>
              <h3 className="font-semibold text-blue-900">
                Ελληνικό ERP/CRM - Ενοποιημένη Επιχειρηματική Διαχείριση
              </h3>
              <p className="text-blue-700 text-sm">
                Milestone 1: CRM + Τιμολόγηση • ERP Core: Αποθέματα + Οικονομικά
                • ERP Expansion: HR + Analytics
              </p>
            </div>
          </div>
          <div className="text-sm text-blue-600 font-medium">
            Πολυ-εταιρικό σύστημα ασφαλείας ✓
          </div>
        </div>
      </div>
    </div>
  );
}
