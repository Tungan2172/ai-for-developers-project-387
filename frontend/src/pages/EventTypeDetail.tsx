import { Alert, Button, Container, Skeleton, Stack, Text, Title } from '@mantine/core';
import { useQuery } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router';

import { client } from '../api/client.ts';
import { useRoleContext } from '../RoleContext.tsx';

export function EventTypeDetail() {
  const { isAdmin } = useRoleContext();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const eventTypeId = Number(id);

  const query = useQuery({
    queryKey: ['event-type', eventTypeId],
    queryFn: () => client.GET('/event-types/{id}', { params: { path: { id: eventTypeId } } }),
    enabled: !Number.isNaN(eventTypeId),
  });

  if (Number.isNaN(eventTypeId)) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red">Тип события не найден</Alert>
      </Container>
    );
  }

  if (query.isLoading) {
    return (
      <Container size="sm" py="xl">
        <Stack gap="lg">
          <Skeleton height={40} width="60%" radius="md" />
          <Skeleton height={20} width="40%" radius="md" />
          <Skeleton height={100} radius="md" />
          <Skeleton height={44} width={200} radius="md" />
        </Stack>
      </Container>
    );
  }

  const errorMessage =
    query.data?.error?.message ?? (query.error instanceof Error ? query.error.message : null);

  if (errorMessage || !query.data?.data) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red">{errorMessage ?? 'Не удалось загрузить тип события'}</Alert>
      </Container>
    );
  }

  const eventType = query.data.data;

  return (
    <Container size="sm" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={1}>{eventType.title}</Title>
          <Text c="dimmed" size="sm">
            {eventType.durationMinutes} мин
          </Text>
        </div>

        <Text>{eventType.description}</Text>

        {!isAdmin && (
          <Button
            size="lg"
            fullWidth
            onClick={() => {
              void navigate(`/event-types/${String(eventType.id)}/book`);
            }}
          >
            Забронировать
          </Button>
        )}
      </Stack>
    </Container>
  );
}
