/** @type {import('next').NextConfig} */
const nextConfig = {
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
  experimental: {
    externalDir: true,
  },
  env: {
    NEXT_PUBLIC_AUTH_SERVICE_URL: process.env.NEXT_PUBLIC_AUTH_SERVICE_URL,
    NEXT_PUBLIC_API_SERVICE_URL: process.env.NEXT_PUBLIC_API_SERVICE_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_ENVIRONMENT: process.env.NEXT_PUBLIC_ENVIRONMENT,
  },
  async rewrites() {
    return [
      {
        source: "/api/auth/:path*",
        destination: `${
          process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || "http://localhost:8001"
        }/auth/:path*`,
      },
      {
        source: "/api/v1/:path*",
        destination: `${
          process.env.NEXT_PUBLIC_API_SERVICE_URL || "http://localhost:8000"
        }/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
