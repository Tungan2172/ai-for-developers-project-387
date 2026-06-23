import '@testing-library/jest-dom/vitest';

import { beforeAll, afterAll, afterEach } from 'vitest';

import { server } from './mocks/server.ts';

beforeAll(() => {
  server.listen({ onUnhandledRequest: 'warn' });

  window.matchMedia = (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  });
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
