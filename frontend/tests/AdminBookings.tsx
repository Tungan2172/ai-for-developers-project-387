import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { type PropsWithChildren } from 'react';
import { MemoryRouter } from 'react-router';
import { afterEach, describe, expect, it } from 'vitest';

import { AdminBookings } from '../src/pages/AdminBookings.tsx';
import { bookings } from './mocks/handlers.ts';

const initialBookings = structuredClone(bookings);

afterEach(() => {
  bookings.length = 0;
  bookings.push(...initialBookings);
});

function renderWithProviders() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });

  function Providers({ children }: PropsWithChildren) {
    return (
      <QueryClientProvider client={queryClient}>
        <MantineProvider>
          <MemoryRouter>{children}</MemoryRouter>
        </MantineProvider>
      </QueryClientProvider>
    );
  }

  return render(<AdminBookings />, { wrapper: Providers });
}

describe('AdminBookings', () => {
  it('отображает заголовок страницы', async () => {
    renderWithProviders();

    expect(await screen.findByRole('heading', { name: 'Предстоящие встречи' })).toBeInTheDocument();
  });

  it('отображает список броней', async () => {
    renderWithProviders();

    expect(await screen.findByText('Анна')).toBeInTheDocument();
    expect(screen.getByText('anna@test.com')).toBeInTheDocument();
    expect(screen.getByText('Борис')).toBeInTheDocument();
    expect(screen.getByText('boris@test.com')).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: 'Отменить' })).toHaveLength(2);
  });

  it('отменяет бронь по клику', async () => {
    renderWithProviders();

    await screen.findByText('Анна');

    const [firstDelete] = screen.getAllByRole('button', { name: 'Отменить' });
    const user = userEvent.setup();
    await user.click(firstDelete);

    expect(await screen.findByText('Борис')).toBeInTheDocument();
    expect(screen.getByText('boris@test.com')).toBeInTheDocument();
    expect(screen.queryByText('Анна')).not.toBeInTheDocument();
  });
});
