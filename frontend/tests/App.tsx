import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { createTestWrapper } from './testWrapper.tsx';
import { Welcome } from '../src/pages/Welcome.tsx';

describe('App', () => {
  it('отображает заголовок приложения', () => {
    render(<Welcome />, { wrapper: createTestWrapper() });

    expect(screen.getByRole('heading', { name: 'Calendar' })).toBeInTheDocument();
  });
});
