import { Card, Container, Group, SimpleGrid, Skeleton, Stack, Text, Title } from '@mantine/core';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router';

import { client } from '../api/client.ts';

export function Welcome() {
  const navigate = useNavigate();
  const ownerQuery = useQuery({
    queryKey: ['owner'],
    queryFn: () => client.GET('/owner'),
  });

  const eventTypesQuery = useQuery({
    queryKey: ['event-types'],
    queryFn: () => client.GET('/event-types'),
  });

  return (
    <Container size="sm" py="xl">
      <Stack gap="lg">
        {ownerQuery.isLoading ? (
          <Skeleton height={80} radius="md" />
        ) : ownerQuery.data?.data ? (
          <div>
            <Title order={1}>{ownerQuery.data.data.title}</Title>
            <Text c="dimmed">{ownerQuery.data.data.description}</Text>
          </div>
        ) : null}

        {eventTypesQuery.isLoading ? (
          <>
            <Skeleton height={100} radius="md" />
            <Skeleton height={100} radius="md" />
          </>
        ) : eventTypesQuery.data?.data ? (
          <SimpleGrid cols={{ base: 1, sm: 2 }}>
            {eventTypesQuery.data.data.map((et) => (
              <Card
                key={et.id}
                shadow="sm"
                padding="lg"
                radius="md"
                withBorder
                onClick={() => {
                  void navigate(`/event-types/${String(et.id)}`);
                }}
                style={{ cursor: 'pointer' }}
              >
                <Group justify="space-between" mb="xs">
                  <Title order={3}>{et.title}</Title>
                  <Text c="dimmed" fz="sm">
                    {et.durationMinutes} мин
                  </Text>
                </Group>
                <Text size="sm" c="dimmed">
                  {et.description}
                </Text>
              </Card>
            ))}
          </SimpleGrid>
        ) : null}
      </Stack>
    </Container>
  );
}
