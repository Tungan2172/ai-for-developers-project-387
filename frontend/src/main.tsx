import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { Router } from './router.tsx';

import '@mantine/core/styles.css';
import '@mantine/dates/styles.css';

async function start() {
  if (import.meta.env.DEV) {
    const { worker } = await import('../tests/mocks/browser.ts');
    await worker.start({ onUnhandledRequest: 'warn' });
  }

  const queryClient = new QueryClient();

  const rootElement = document.getElementById('root');
  if (!rootElement) {
    throw new Error('Root element #root not found');
  }

  createRoot(rootElement).render(
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <MantineProvider>
          <Router />
        </MantineProvider>
      </QueryClientProvider>
    </StrictMode>,
  );
}

start().catch(console.error);
