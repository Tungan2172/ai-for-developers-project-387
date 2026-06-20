import { test, expect } from '@playwright/test';

import { createBooking, createEventType, mskDate } from './helpers';

const TODAY = new Date(2026, 5, 20); // Saturday
const MONDAY = 22; // June 22 (Monday)

test.describe('Guest booking flow', () => {
  let eventTypeId: number;
  let bookingId: number;

  test.beforeAll(async ({ request }) => {
    eventTypeId = await createEventType(request, 'Consultation', '30 min meeting', 30);
    const start = mskDate(2026, 6, MONDAY, 10, 0);
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
      `http://localhost:8000/event-types/${eventTypeId}/slots?from=2026-06-22&to=2026-06-22`,
    );
    expect(slotsResp.status()).toBe(200);
    const slots = (await slotsResp.json()) as Array<{ start: string; end: string; status: string }>;
    console.log('SLOT_COUNT:', slots.length, 'FIRST_START:', slots[0]?.start, 'FIRST_STATUS:', slots[0]?.status);
    const Slot10 = slots.find((s) => s.start.includes('10:00') || s.start.includes('07:00'));
    expect(Slot10).toBeDefined();
    expect(Slot10!.status).toBe('busy');

    await page.goto(`/event-types/${eventTypeId}/book`);

    await expect(page.getByRole('heading', { level: 2, name: 'Consultation' })).toBeVisible();

    const day22 = page.locator('.mantine-Calendar-day').filter({ hasText: String(MONDAY) });
    await day22.click();

    const enDash = '\u2013';
    const freeSlot = page.getByRole('button', { name: `10:30${enDash}11:00` });
    await expect(freeSlot).not.toBeDisabled();
  });

  test('Guest books a free slot', async ({ page }) => {
    const start = mskDate(2026, 6, MONDAY, 10, 30);
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
