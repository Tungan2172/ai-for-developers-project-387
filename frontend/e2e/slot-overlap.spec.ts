import { test, expect } from '@playwright/test';

import { createEventType, deleteBooking, deleteEventType, mskDate } from './helpers';

function nextMonday(): number {
  const now = new Date();
  const d = now.getDate() + ((1 + 7 - now.getDay()) % 7 || 7);
  return d;
}

test.describe('Slot overlap prevention', () => {
  let longEventTypeId: number;
  let quickEventTypeId: number;
  const createdBookingIds: number[] = [];

  test.beforeAll(async ({ request }) => {
    longEventTypeId = await createEventType(request, 'Long meeting', '30 min meeting', 30);
    quickEventTypeId = await createEventType(request, 'Quick meeting', '15 min sync', 15);
  });

  test.afterAll(async ({ request }) => {
    for (const id of createdBookingIds) {
      await deleteBooking(request, id).catch(() => {});
    }
    await deleteEventType(request, longEventTypeId).catch(() => {});
    await deleteEventType(request, quickEventTypeId).catch(() => {});
  });

  const day = nextMonday();
  const YEAR = 2026;
  const MONTH = 6;

  test('Step 1: first booking 09:00–09:30 succeeds', async ({ request }) => {
    const start = mskDate(YEAR, MONTH, day, 9, 0);
    const resp = await request.post('http://localhost:8000/bookings', {
      data: { eventTypeId: longEventTypeId, start, guestName: 'User A', guestEmail: 'a@test.com' },
    });
    expect(resp.status()).toBe(201);
    const body = (await resp.json()) as { id: number };
    createdBookingIds.push(body.id);
  });

  test('Step 2: second booking 09:30–10:00 succeeds (adjacent)', async ({ request }) => {
    const start = mskDate(YEAR, MONTH, day, 9, 30);
    const resp = await request.post('http://localhost:8000/bookings', {
      data: { eventTypeId: longEventTypeId, start, guestName: 'User B', guestEmail: 'b@test.com' },
    });
    expect(resp.status()).toBe(201);
    const body = (await resp.json()) as { id: number };
    createdBookingIds.push(body.id);
  });

  test('Step 3: third booking 09:00–09:15 rejected (overlap with step 1)', async ({ request }) => {
    const start = mskDate(YEAR, MONTH, day, 9, 0);
    const resp = await request.post('http://localhost:8000/bookings', {
      data: { eventTypeId: quickEventTypeId, start, guestName: 'User C', guestEmail: 'c@test.com' },
    });
    expect(resp.status()).toBe(409);
    const body = (await resp.json()) as { code: string };
    expect(body.code).toBe('slot_busy');
  });

  test('Step 4: fourth booking 10:00–10:15 succeeds (no overlap)', async ({ request }) => {
    const start = mskDate(YEAR, MONTH, day, 10, 0);
    const resp = await request.post('http://localhost:8000/bookings', {
      data: { eventTypeId: quickEventTypeId, start, guestName: 'User D', guestEmail: 'd@test.com' },
    });
    expect(resp.status()).toBe(201);
    const body = (await resp.json()) as { id: number };
    createdBookingIds.push(body.id);
  });
});
