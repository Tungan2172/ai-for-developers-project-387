import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { type PropsWithChildren } from 'react';
import { createMemoryRouter, RouterProvider } from 'react-router';
import { describe, expect, it } from 'vitest';

import { BookingForm } from '../src/pages/BookingForm.tsx';
import { eventTypes } from './mocks/handlers.ts';

function renderWithRouter(initialEntry: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });

  function Providers({ children }: PropsWithChildren) {
    return (
      <QueryClientProvider client={queryClient}>
        <MantineProvider>{children}</MantineProvider>
      </QueryClientProvider>
    );
  }

  const router = createMemoryRouter(
    [{ path: '/event-types/:id/book/confirm', element: <BookingForm /> }],
    { initialEntries: [initialEntry] },
  );

  return render(<RouterProvider router={router} />, { wrapper: Providers });
}

describe('BookingForm', () => {
  it('отображает форму с полями', async () => {
    renderWithRouter('/event-types/1/book/confirm?start=2026-06-15T09:00:00.000Z');

    expect(await screen.findByRole('heading', { name: eventTypes[0].title })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Имя' })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Email' })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: 'Заметка' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Подтвердить бронь' })).toBeInTheDocument();
  });

  it('отображает время и длительность выбранного слота', async () => {
    renderWithRouter('/event-types/1/book/confirm?start=2026-06-15T09:00:00.000Z');

    expect(await screen.findByText(/\d{2}:\d{2}–\d{2}:\d{2}/)).toBeInTheDocument();
    expect(screen.getByText(/15 мин/)).toBeInTheDocument();
  });

  it('кнопка заблокирована при пустых полях', async () => {
    renderWithRouter('/event-types/1/book/confirm?start=2026-06-15T09:00:00.000Z');

    await screen.findByRole('heading', { name: eventTypes[0].title });

    const button = screen.getByRole('button', { name: 'Подтвердить бронь' });
    expect(button).toBeDisabled();
  });

  it('успешное бронирование показывает success', async () => {
    const user = userEvent.setup();
    renderWithRouter('/event-types/1/book/confirm?start=2026-06-15T09:00:00.000Z');

    await screen.findByRole('heading', { name: eventTypes[0].title });

    await user.type(screen.getByRole('textbox', { name: 'Имя' }), 'Иван');
    await user.type(screen.getByRole('textbox', { name: 'Email' }), 'ivan@test.com');

    const button = screen.getByRole('button', { name: 'Подтвердить бронь' });
    expect(button).not.toBeDisabled();

    await user.click(button);

    expect(await screen.findByText('Бронь подтверждена')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'На главную' })).toBeInTheDocument();
  });

  it('отображает ошибку при некорректных параметрах', () => {
    renderWithRouter('/event-types/not-a-number/book/confirm?start=2026-06-15T09:00:00.000Z');

    expect(screen.getByText('Некорректные параметры бронирования')).toBeInTheDocument();
  });

  it('отображает ошибку при отсутствии start', () => {
    renderWithRouter('/event-types/1/book/confirm');

    expect(screen.getByText('Некорректные параметры бронирования')).toBeInTheDocument();
  });
});
