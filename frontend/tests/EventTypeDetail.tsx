import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import { type PropsWithChildren } from 'react';
import { createMemoryRouter, RouterProvider } from 'react-router';
import { describe, expect, it } from 'vitest';

import { EventTypeDetail } from '../src/pages/EventTypeDetail.tsx';
import { eventTypes } from './mocks/handlers.ts';

function renderWithRouter(initialEntry: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  function Providers({ children }: PropsWithChildren) {
    return (
      <QueryClientProvider client={queryClient}>
        <MantineProvider>{children}</MantineProvider>
      </QueryClientProvider>
    );
  }

  const router = createMemoryRouter([{ path: '/event-types/:id', element: <EventTypeDetail /> }], {
    initialEntries: [initialEntry],
  });

  return render(<RouterProvider router={router} />, { wrapper: Providers });
}

describe('EventTypeDetail', () => {
  it('отображает информацию о типе события', async () => {
    const et = eventTypes[0];
    renderWithRouter('/event-types/1');

    expect(await screen.findByRole('heading', { name: et.title })).toBeInTheDocument();
    expect(screen.getByText(`${String(et.durationMinutes)} мин`)).toBeInTheDocument();
    expect(screen.getByText(et.description)).toBeInTheDocument();
  });

  it('отображает кнопку «Забронировать»', async () => {
    renderWithRouter('/event-types/1');

    expect(await screen.findByRole('button', { name: 'Забронировать' })).toBeInTheDocument();
  });

  it('отображает ошибку при неверном ID', () => {
    renderWithRouter('/event-types/not-a-number');

    expect(screen.getByText('Тип события не найден')).toBeInTheDocument();
  });

  it('отображает ошибку 404 при неизвестном ID', async () => {
    renderWithRouter('/event-types/999');

    expect(await screen.findByText('Тип события не найден')).toBeInTheDocument();
  });
});
