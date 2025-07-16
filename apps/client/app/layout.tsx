import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { TranslationProvider, AuthProvider } from "@erp/shared-ui";
import { AppName } from "@erp/shared-ui/constants";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Greek ERP/CRM System",
  description:
    "Greek Business Management System with multi-tenant architecture and AADE compliance",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="el">
      <body className={inter.className}>
        <TranslationProvider>
          <AuthProvider app={AppName.CLIENT}>{children}</AuthProvider>
        </TranslationProvider>
      </body>
    </html>
  );
}
