import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';
import timezone from 'dayjs/plugin/timezone.js';
import { http, HttpResponse } from 'msw';

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
];
