import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Greek ERP/CRM - Business Management System",
  description:
    "Revolutionary Greek ERP/CRM system that eliminates traditional silos",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
