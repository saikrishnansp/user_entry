import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      // "@/components": path.resolve(__dirname, "./src/components"),
      // "@/api": path.resolve(__dirname, "./src/api"),
    },
  },
  server: {
    host: "localhost",
    port: 5173,
    hmr: {
      host: "localhost", // fixed the ws://localhost error
    },
  },
});
