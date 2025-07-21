import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import {
  TranslationProvider,
  AuthProvider,
  ThemeProvider,
  GreekLocaleProvider,
} from "@erp/shared-ui";
import { AppName } from "@erp/shared-ui/constants";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Axiologic",
  description:
    "Greek Business Management System with multi-tenant architecture and AADE compliance",
  icons: {
    icon: [
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/favicon.ico", sizes: "48x48" },
      { url: "/favicon-96x96.png", sizes: "96x96", type: "image/png" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="el">
      <body className={inter.className}>
        <ThemeProvider>
          <TranslationProvider>
            <GreekLocaleProvider enableReferenceDataFetch={true}>
              <AuthProvider app={AppName.CLIENT}>{children}</AuthProvider>
            </GreekLocaleProvider>
          </TranslationProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
