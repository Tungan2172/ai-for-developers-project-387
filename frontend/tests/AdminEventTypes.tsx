import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { type PropsWithChildren } from 'react';
import { MemoryRouter } from 'react-router';
import { beforeEach, describe, expect, it } from 'vitest';

import { AdminEventTypes } from '../src/pages/AdminEventTypes.tsx';
import { eventTypes } from './mocks/handlers.ts';

beforeEach(() => {
  eventTypes.splice(
    0,
    eventTypes.length,
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
  );
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

  return render(<AdminEventTypes />, { wrapper: Providers });
}

describe('AdminEventTypes', () => {
  it('отображает заголовок страницы', async () => {
    renderWithProviders();

    expect(await screen.findByRole('heading', { name: 'Типы событий' })).toBeInTheDocument();
  });

  it('отображает список типов событий', async () => {
    renderWithProviders();

    expect(await screen.findByText('15-минутная встреча')).toBeInTheDocument();
    expect(screen.getByText('Часовая консультация')).toBeInTheDocument();
  });

  it('создаёт новый тип события', async () => {
    const user = userEvent.setup();
    renderWithProviders();

    await screen.findByText('15-минутная встреча');

    await user.click(screen.getByRole('button', { name: 'Создать тип события' }));

    await user.type(screen.getByRole('textbox', { name: 'Название' }), 'Тестовый тип');
    await user.type(screen.getByRole('textbox', { name: 'Описание' }), 'Описание тестового типа');
    await user.type(screen.getByRole('textbox', { name: 'Длительность (мин)' }), '30');

    await user.click(screen.getByRole('button', { name: 'Создать' }));

    expect(await screen.findByText('Тестовый тип')).toBeInTheDocument();
  });

  it('редактирует существующий тип события', async () => {
    const user = userEvent.setup();
    renderWithProviders();

    await screen.findByText('15-минутная встреча');

    await user.click(screen.getAllByRole('button', { name: 'Редактировать' })[0]);

    const nameInput = screen.getByRole('textbox', { name: 'Название' });
    await user.clear(nameInput);
    await user.type(nameInput, 'Изменённая встреча');

    await user.click(screen.getByRole('button', { name: 'Сохранить' }));

    expect(await screen.findByText('Изменённая встреча')).toBeInTheDocument();
  });

  it('удаляет тип события', async () => {
    const user = userEvent.setup();
    renderWithProviders();

    await screen.findByText('15-минутная встреча');

    const deleteButtons = screen.getAllByRole('button', { name: 'Удалить' });
    await user.click(deleteButtons[0]);

    await waitFor(() => {
      expect(screen.queryByText('15-минутная встреча')).not.toBeInTheDocument();
    });
    expect(screen.getByText('Часовая консультация')).toBeInTheDocument();
  });
});
