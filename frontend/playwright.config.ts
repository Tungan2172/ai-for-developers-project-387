import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  timeout: 30_000,
  expect: { timeout: 10_000 },

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },

  webServer: [
    {
      command: './entrypoint.sh',
      port: 8000,
      cwd: '../backend',
      reuseExistingServer: !process.env.CI,
      env: {
        APP_DATABASE_URL:
          process.env.APP_DATABASE_URL ||
          'postgresql+psycopg://scheduler:scheduler@localhost:5432/scheduler',
      },
    },
    {
      command: 'npm run dev',
      port: 5173,
      reuseExistingServer: !process.env.CI,
      env: {
        VITE_E2E: 'true',
      },
    },
  ],

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
