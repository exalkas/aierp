/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: [
    "@erp/shared-ui",
    "@erp/shared-auth",
    "@erp/admin-subscriptions",
    "@erp/shared-utils",
  ],
};

module.exports = nextConfig;
