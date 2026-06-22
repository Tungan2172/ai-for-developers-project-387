import { test, expect } from '@playwright/test';

import { createBooking, createEventType, mskDate } from './helpers';

function nextMondayDate(): Date {
  const now = new Date();
  const d = now.getDate() + ((1 + 7 - now.getDay()) % 7 || 7);
  return new Date(now.getFullYear(), now.getMonth(), d);
}

function pad(n: number): string {
  return String(n).padStart(2, '0');
}

const monday = nextMondayDate();
const year = monday.getFullYear();
const month = monday.getMonth() + 1;
const day = monday.getDate();

test.describe('Guest booking flow', () => {
  let eventTypeId: number;
  let bookingId: number;

  test.beforeAll(async ({ request }) => {
    eventTypeId = await createEventType(request, 'Consultation', '30 min meeting', 30);
    const start = mskDate(year, month, day, 10, 0);
    bookingId = await createBooking(request, eventTypeId, start);
  });

  test.afterAll(async ({ request }) => {
    await request.delete(`http://localhost:8000/bookings/${bookingId}`);
    await request.delete(`http://localhost:8000/event-types/${eventTypeId}`);
  });

  test('Welcome page shows owner and event type list', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1, name: 'Host' })).toBeVisible();

    const eventTypeCard = page.getByRole('heading', { level: 3, name: 'Consultation' });
    await expect(eventTypeCard).toBeVisible();
    await expect(page.getByText('30 мин')).toBeVisible();
  });

  test('Calendar shows free and busy slots', async ({ page, request }) => {
    // Check via API that the slot is busy
    const slotsResp = await request.get(
      `http://localhost:8000/event-types/${eventTypeId}/slots?from=${year}-${pad(month)}-${pad(day)}&to=${year}-${pad(month)}-${pad(day + 1)}`,
    );
    expect(slotsResp.status()).toBe(200);
    const slots = (await slotsResp.json()) as Array<{ start: string; end: string; status: string }>;
    const Slot10 = slots.find((s) => s.start.includes('10:00'));
    expect(Slot10).toBeDefined();
    expect(Slot10!.status).toBe('busy');

    await page.goto(`/event-types/${eventTypeId}/book`);

    await expect(page.getByRole('heading', { level: 2, name: 'Consultation' })).toBeVisible();

    const dayEl = page.locator('.mantine-Calendar-day').filter({ hasText: String(day) });
    await dayEl.click();

    const enDash = '\u2013';
    const freeSlot = page.getByRole('button', { name: `10:30${enDash}11:00` });
    await expect(freeSlot).not.toBeDisabled();
  });

  test('Guest books a free slot', async ({ page }) => {
    const start = mskDate(year, month, day, 10, 30);
    await page.goto(`/event-types/${eventTypeId}/book/confirm?start=${encodeURIComponent(start)}`);

    await expect(page.getByRole('heading', { level: 2, name: 'Consultation' })).toBeVisible();

    await page.getByLabel('Имя').fill('Анна');
    await page.getByLabel('Email').fill('anna@test.com');
    await page.getByPlaceholder('Необязательная заметка к встрече').fill('Жду встречи');

    await page.getByRole('button', { name: 'Подтвердить бронь' }).click();

    await expect(page.getByRole('heading', { name: 'Бронь подтверждена' })).toBeVisible({
      timeout: 10_000,
    });
    await expect(
      page.getByText('Встреча успешно забронирована. Вы получите уведомление на email.'),
    ).toBeVisible();

    const resp = await page.request.get('http://localhost:8000/bookings');
    const bookings = (await resp.json()) as Array<{ id: number; start: string }>;
    const created = bookings.find((b) => b.start === start);
    if (created) {
      await page.request.delete(`http://localhost:8000/bookings/${created.id}`);
    }
  });
});
