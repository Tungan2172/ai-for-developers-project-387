import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';
import timezone from 'dayjs/plugin/timezone.js';
import { http, HttpResponse } from 'msw';

import type { components } from '../../src/api/schema.d.ts';

dayjs.extend(utc);
dayjs.extend(timezone);

const TZ = 'Europe/Moscow';

interface SlotData {
  start: string;
  end: string;
  status: 'free' | 'busy';
}

function generateSlots(durationMinutes: number): SlotData[] {
  const slots: SlotData[] = [];
  const now = dayjs().tz(TZ);
  const startOfToday = now.startOf('day');

  for (let dayOffset = 0; dayOffset < 14; dayOffset++) {
    const day = startOfToday.add(dayOffset, 'day');
    const dayOfWeek = day.day();

    if (dayOfWeek === 0 || dayOfWeek === 6) continue;

    const dayStart = day.hour(9).minute(0).second(0).millisecond(0);
    const dayEnd = day.hour(17).minute(0).second(0).millisecond(0);

    let slotStart = dayStart;
    while (slotStart.isBefore(dayEnd)) {
      const slotEnd = slotStart.add(durationMinutes, 'minute');
      if (slotEnd.isAfter(dayEnd)) break;

      const isPast = now.isAfter(slotStart);
      const isBusy =
        dayOffset === 0 && (dayOfWeek === 1 || dayOfWeek === 3) && slotStart.hour() === 10;

      slots.push({
        start: slotStart.toISOString(),
        end: slotEnd.toISOString(),
        status: isPast ? 'busy' : isBusy ? 'busy' : 'free',
      });

      slotStart = slotEnd;
    }
  }

  return slots;
}

export const owner = {
  name: 'owner',
  title: 'Host',
  description: 'Забронируйте встречу в удобное время.',
};

export const eventTypes = [
  {
    id: 1,
    title: '15-минутная встреча',
    description: 'Быстрая синхронизация',
    durationMinutes: 15,
  },
  {
    id: 2,
    title: 'Часовая консультация',
    description: 'Подробное обсуждение проекта',
    durationMinutes: 60,
  },
];

let nextBookingId = 1;

export const bookings: components['schemas']['Booking'][] = [
  {
    id: 1,
    eventTypeId: 1,
    eventTypeTitle: '15-минутная встреча',
    durationMinutes: 15,
    start: '2026-06-16T09:00:00.000Z',
    end: '2026-06-16T09:15:00.000Z',
    guestName: 'Анна',
    guestEmail: 'anna@test.com',
    createdAt: '2026-06-14T20:00:00.000Z',
  },
  {
    id: 2,
    eventTypeId: 2,
    eventTypeTitle: 'Часовая консультация',
    durationMinutes: 60,
    start: '2026-06-17T10:00:00.000Z',
    end: '2026-06-17T11:00:00.000Z',
    guestName: 'Борис',
    guestEmail: 'boris@test.com',
    note: 'Обсудить архитектуру',
    createdAt: '2026-06-14T21:00:00.000Z',
  },
];

export const handlers = [
  http.get('/api/health', () => HttpResponse.json({ status: 'ok' })),

  http.get('/api/owner', () => HttpResponse.json(owner)),

  http.get('/api/event-types', () => HttpResponse.json(eventTypes)),

  http.get('/api/event-types/:id', ({ params }) => {
    const et = eventTypes.find((e) => e.id === Number(params.id));
    if (!et) {
      return HttpResponse.json(
        { code: 'event_type_not_found', message: 'Тип события не найден' },
        { status: 404 },
      );
    }
    return HttpResponse.json(et);
  }),

  http.get('/api/event-types/:id/slots', ({ params }) => {
    const et = eventTypes.find((e) => e.id === Number(params.id));
    if (!et) {
      return HttpResponse.json(
        { code: 'event_type_not_found', message: 'Тип события не найден' },
        { status: 404 },
      );
    }
    const slots = generateSlots(et.durationMinutes);
    return HttpResponse.json(slots);
  }),

  http.get('/api/bookings', () => HttpResponse.json(bookings)),

  http.delete('/api/bookings/:id', ({ params }) => {
    const idx = bookings.findIndex((b) => b.id === Number(params.id));
    if (idx === -1) {
      return HttpResponse.json(
        { code: 'booking_not_found', message: 'Бронь не найдена' },
        { status: 404 },
      );
    }
    bookings.splice(idx, 1);
    return new HttpResponse(null, { status: 204 });
  }),

  http.post('/api/bookings', async ({ request }) => {
    const body = (await request.json()) as {
      eventTypeId: number;
      start: string;
      guestName: string;
      guestEmail: string;
      note?: string;
    };

    if (!body.guestName || !body.guestEmail) {
      return HttpResponse.json(
        { code: 'validation_error', message: 'Имя и email обязательны' },
        { status: 422 },
      );
    }

    const et = eventTypes.find((e) => e.id === body.eventTypeId);
    if (!et) {
      return HttpResponse.json(
        { code: 'event_type_not_found', message: 'Тип события не найден' },
        { status: 404 },
      );
    }

    const slotStart = dayjs(body.start);
    const slotEnd = slotStart.add(et.durationMinutes, 'minute');
    const id = nextBookingId++;

    return HttpResponse.json(
      {
        id,
        eventTypeId: et.id,
        eventTypeTitle: et.title,
        durationMinutes: et.durationMinutes,
        start: slotStart.toISOString(),
        end: slotEnd.toISOString(),
        guestName: body.guestName,
        guestEmail: body.guestEmail,
        note: body.note,
        createdAt: dayjs().toISOString(),
      },
      { status: 201 },
    );
  }),
];
