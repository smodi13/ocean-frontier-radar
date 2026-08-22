import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',          // fully static; no server, no runtime deps
  reactStrictMode: true,
  images: { unoptimized: true },
  trailingSlash: true,
  // A stray package-lock.json in the home directory otherwise confuses root inference.
  turbopack: { root: __dirname },
};
export default nextConfig;
