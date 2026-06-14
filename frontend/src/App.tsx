import { Anchor, AppShell, Group, Switch } from '@mantine/core';
import { useState } from 'react';
import { Link, Outlet } from 'react-router';

export function AppLayout() {
  const [isAdmin, setIsAdmin] = useState(false);

  return (
    <AppShell header={{ height: 50 }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Group>
            <Anchor component={Link} to="/">Главная</Anchor>
            {isAdmin && (
              <>
                <Anchor component={Link} to="/admin/bookings">Брони</Anchor>
                <Anchor component={Link} to="/admin/event-types">Типы событий</Anchor>
              </>
            )}
          </Group>
          <Switch
            label="Режим владельца"
            checked={isAdmin}
            onChange={(e) => { setIsAdmin(e.currentTarget.checked); }}
          />
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
