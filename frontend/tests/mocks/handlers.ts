import { http, HttpResponse } from 'msw';

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
];
