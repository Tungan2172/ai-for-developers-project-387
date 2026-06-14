import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

// В dev все запросы /api/* проксируются на backend, а префикс /api срезается:
// браузер ходит на один origin (нет CORS), в коде путь всегда /api (см. AGENTS.md).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setupTests.ts',
    include: ['tests/**/*.tsx'],
    exclude: ['tests/setupTests.ts', 'tests/testWrapper.tsx', 'tests/mocks/**'],
  },
});
