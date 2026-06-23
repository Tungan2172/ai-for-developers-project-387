import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { createTestWrapper } from './testWrapper.tsx';
import { Welcome } from '../src/pages/Welcome.tsx';
import { eventTypes, owner } from './mocks/handlers.ts';

describe('App', () => {
  it('отображает заголовок и описание владельца', async () => {
    render(<Welcome />, { wrapper: createTestWrapper() });

    expect(await screen.findByRole('heading', { name: owner.title })).toBeInTheDocument();
    expect(screen.getByText(owner.description)).toBeInTheDocument();
  });

  it('отображает список типов событий', async () => {
    render(<Welcome />, { wrapper: createTestWrapper() });

    for (const et of eventTypes) {
      expect(await screen.findByRole('heading', { name: et.title })).toBeInTheDocument();
    }
  });

  it('отображает длительность в минутах', async () => {
    render(<Welcome />, { wrapper: createTestWrapper() });

    for (const et of eventTypes) {
      expect(await screen.findByText(`${String(et.durationMinutes)} мин`)).toBeInTheDocument();
    }
  });
});
