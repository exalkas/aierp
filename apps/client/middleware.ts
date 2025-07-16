import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Define public routes that don't require authentication
const PUBLIC_ROUTES = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/api/auth/login",
  "/api/auth/register",
  "/api/auth/refresh",
  "/api/auth/forgot-password",
  "/api/auth/reset-password",
  "/_next",
  "/favicon.ico",
  "/public",
];

// Define protected routes that require authentication
const PROTECTED_ROUTES = [
  "/dashboard",
  "/customers",
  "/products",
  "/invoices",
  "/reports",
  "/settings",
  "/profile",
  "/crm",
  "/erp",
  "/api/protected",
];

// Check if route is public
function isPublicRoute(pathname: string): boolean {
  return PUBLIC_ROUTES.some((route) => pathname.startsWith(route));
}

// Check if route is protected
function isProtectedRoute(pathname: string): boolean {
  return PROTECTED_ROUTES.some((route) => pathname.startsWith(route));
}

// Get token from request
function getTokenFromRequest(request: NextRequest): string | null {
  // Check Authorization header
  const authHeader = request.headers.get("Authorization");
  if (authHeader && authHeader.startsWith("Bearer ")) {
    return authHeader.substring(7);
  }

  // Check cookie
  const tokenCookie = request.cookies.get("auth_token");
  if (tokenCookie) {
    return tokenCookie.value;
  }

  return null;
}

// Validate token using the auth service
async function validateToken(token: string): Promise<boolean> {
  if (!token) return false;

  try {
    // Use the proxy endpoint for auth service
    const response = await fetch(
      `${
        process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || "http://localhost:8001"
      }/auth/validate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (response.ok) {
      const result = await response.json();
      return result.valid === true;
    }

    return false;
  } catch (error) {
    console.error("Token validation error:", error);
    return false;
  }
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip middleware for static files and Next.js internal routes
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api/_next") ||
    pathname.includes("favicon") ||
    pathname.includes("public")
  ) {
    return NextResponse.next();
  }

  // Allow public routes
  if (isPublicRoute(pathname)) {
    return NextResponse.next();
  }

  // For protected routes, check authentication
  if (isProtectedRoute(pathname) || pathname === "/") {
    const token = getTokenFromRequest(request);

    if (!token) {
      // No token, redirect to login
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }

    // Validate token
    const isValid = await validateToken(token);

    if (!isValid) {
      // Invalid token, redirect to login
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }

    // Token is valid, allow access
    return NextResponse.next();
  }

  // For root path, redirect to dashboard if authenticated, login if not
  if (pathname === "/") {
    const token = getTokenFromRequest(request);

    if (token) {
      const isValid = await validateToken(token);
      if (isValid) {
        return NextResponse.redirect(new URL("/dashboard", request.url));
      }
    }

    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Allow all other routes
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
