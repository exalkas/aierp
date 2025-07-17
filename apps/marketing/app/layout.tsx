import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Axiologic - Business Management System",
  description:
    "Revolutionary business management system that eliminates traditional silos",
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
