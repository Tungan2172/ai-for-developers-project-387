import { Alert, Button, Container, Skeleton, Stack, Table, Text, Title } from '@mantine/core';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import dayjs from 'dayjs';

import { client } from '../api/client.ts';
import type { components } from '../api/schema.d.ts';

type Booking = components['schemas']['Booking'];

export function AdminBookings() {
  const queryClient = useQueryClient();

  const bookingsQuery = useQuery({
    queryKey: ['bookings'],
    queryFn: () => client.GET('/bookings'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => client.DELETE('/bookings/{id}', { params: { path: { id } } }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['bookings'] });
    },
  });

  if (bookingsQuery.isLoading) {
    return (
      <Container size="md" py="xl">
        <Stack gap="lg">
          <Skeleton height={30} width="40%" radius="md" />
          <Skeleton height={200} radius="md" />
        </Stack>
      </Container>
    );
  }

  const bookingsData = bookingsQuery.data;
  const errorMessage = bookingsQuery.error instanceof Error ? bookingsQuery.error.message : null;

  if (errorMessage) {
    return (
      <Container size="md" py="xl">
        <Alert color="red">{errorMessage}</Alert>
      </Container>
    );
  }

  const bookings: Booking[] = bookingsData?.data ?? [];

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Title order={2}>Предстоящие встречи</Title>

        {bookings.length === 0 ? (
          <Text c="dimmed">Нет предстоящих встреч</Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Время</Table.Th>
                <Table.Th>Тип</Table.Th>
                <Table.Th>Гость</Table.Th>
                <Table.Th>Email</Table.Th>
                <Table.Th>Длит.</Table.Th>
                <Table.Th />
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {bookings.map((b) => (
                <Table.Tr key={b.id}>
                  <Table.Td>{dayjs(b.start).format('DD.MM.YYYY HH:mm')}</Table.Td>
                  <Table.Td>{b.eventTypeTitle}</Table.Td>
                  <Table.Td>{b.guestName}</Table.Td>
                  <Table.Td>{b.guestEmail}</Table.Td>
                  <Table.Td>{b.durationMinutes} мин</Table.Td>
                  <Table.Td>
                    <Button
                      size="xs"
                      color="red"
                      loading={deleteMutation.isPending}
                      onClick={() => {
                        deleteMutation.mutate(b.id);
                      }}
                    >
                      Отменить
                    </Button>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Stack>
    </Container>
  );
}
