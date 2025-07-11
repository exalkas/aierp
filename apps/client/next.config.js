/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  transpilePackages: [
    "@erp/shared-auth",
    "@erp/shared-ui",
    "@erp/shared-voice",
    "@erp/shared-ai",
    "@erp/standard-dashboard",
    "@erp/standard-crm",
    "@erp/standard-erp",
    "@erp/standard-reports",
  ],
};

module.exports = nextConfig;
