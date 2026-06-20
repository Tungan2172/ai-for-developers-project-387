import type { APIRequestContext } from '@playwright/test';

const API_BASE = 'http://localhost:8000';
const MSK = '+03:00';

export function mskDate(year: number, month: number, day: number, hour: number, minute: number): string {
  const m = String(month).padStart(2, '0');
  const d = String(day).padStart(2, '0');
  const h = String(hour).padStart(2, '0');
  const min = String(minute).padStart(2, '0');
  return `${year}-${m}-${d}T${h}:${min}:00${MSK}`;
}

export async function createEventType(
  request: APIRequestContext,
  title: string,
  description: string,
  durationMinutes: number,
): Promise<number> {
  const resp = await request.post(`${API_BASE}/event-types`, {
    data: { title, description, durationMinutes },
  });
  if (resp.status() !== 201) {
    throw new Error(`createEventType failed: ${resp.status()} ${await resp.text()}`);
  }
  const body = (await resp.json()) as { id: number };
  return body.id;
}

export async function createBooking(
  request: APIRequestContext,
  eventTypeId: number,
  start: string,
  guestName?: string,
  guestEmail?: string,
): Promise<number> {
  const resp = await request.post(`${API_BASE}/bookings`, {
    data: {
      eventTypeId,
      start,
      guestName: guestName ?? 'E2E User',
      guestEmail: guestEmail ?? 'e2e@test.com',
    },
  });
  if (resp.status() !== 201) {
    throw new Error(`createBooking failed: ${resp.status()} ${await resp.text()}`);
  }
  const body = (await resp.json()) as { id: number };
  return body.id;
}

export async function deleteBooking(request: APIRequestContext, id: number): Promise<void> {
  await request.delete(`${API_BASE}/bookings/${id}`);
}

export async function deleteEventType(request: APIRequestContext, id: number): Promise<void> {
  await request.delete(`${API_BASE}/event-types/${id}`);
}

export const SLOT_TIME_REGEX = /\d{2}:\d{2}–\d{2}:\d{2}/;
