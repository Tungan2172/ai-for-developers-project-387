import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import { type PropsWithChildren } from 'react';
import { createMemoryRouter, RouterProvider } from 'react-router';
import { describe, expect, it } from 'vitest';

import { RoleProvider } from '../src/RoleContext.tsx';
import { BookSlot } from '../src/pages/BookSlot.tsx';
import { eventTypes } from './mocks/handlers.ts';

function renderWithRouter(initialEntry: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  function Providers({ children }: PropsWithChildren) {
    return (
      <QueryClientProvider client={queryClient}>
        <MantineProvider>
          <RoleProvider>{children}</RoleProvider>
        </MantineProvider>
      </QueryClientProvider>
    );
  }

  const router = createMemoryRouter([{ path: '/event-types/:id/book', element: <BookSlot /> }], {
    initialEntries: [initialEntry],
  });

  return render(<RouterProvider router={router} />, { wrapper: Providers });
}

describe('BookSlot', () => {
  it('отображает название и длительность типа события', async () => {
    const et = eventTypes[0];
    renderWithRouter('/event-types/1/book');

    expect(await screen.findByRole('heading', { name: et.title })).toBeInTheDocument();
    expect(screen.getByText(`${String(et.durationMinutes)} мин`)).toBeInTheDocument();
  });

  it('отображает календарь', async () => {
    renderWithRouter('/event-types/1/book');

    const table = await screen.findByRole('table');
    expect(table).toBeInTheDocument();
  });

  it('отображает календарь после загрузки данных', async () => {
    renderWithRouter('/event-types/1/book');

    await screen.findByRole('heading', { name: eventTypes[0].title });
    expect(screen.getByRole('table')).toBeInTheDocument();
  });

  it('отображает ошибку при неверном ID', () => {
    renderWithRouter('/event-types/not-a-number/book');

    expect(screen.getByText('Тип события не найден')).toBeInTheDocument();
  });

  it('отображает ошибку 404 при неизвестном ID', async () => {
    renderWithRouter('/event-types/999/book');

    expect(await screen.findByText('Тип события не найден')).toBeInTheDocument();
  });
});
