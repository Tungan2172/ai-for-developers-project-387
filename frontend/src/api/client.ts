import createClient from 'openapi-fetch';

import type { paths } from './schema.d.ts';

const baseUrl = typeof window !== 'undefined' ? `${window.location.origin}/api` : '/api';

export const client = createClient<paths>({
  baseUrl,
  fetch: (...args) => globalThis.fetch(...args),
});
