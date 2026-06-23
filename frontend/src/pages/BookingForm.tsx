import {
  Alert,
  Button,
  Container,
  Skeleton,
  Stack,
  Text,
  TextInput,
  Textarea,
  Title,
} from '@mantine/core';
import { useMutation, useQuery } from '@tanstack/react-query';
import dayjs from 'dayjs';
import { useState } from 'react';
import { Navigate, useNavigate, useParams, useSearchParams } from 'react-router';

import { client } from '../api/client.ts';
import { useRoleContext } from '../RoleContext.tsx';
import type { components } from '../api/schema.d.ts';

type BookingCreate = components['schemas']['BookingCreate'];

export function BookingForm() {
  const { isAdmin } = useRoleContext();
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const eventTypeId = Number(id);
  const startIso = searchParams.get('start') ?? '';
  const [guestName, setGuestName] = useState('');
  const [guestEmail, setGuestEmail] = useState('');
  const [note, setNote] = useState('');

  const eventTypeQuery = useQuery({
    queryKey: ['event-type', eventTypeId],
    queryFn: () => client.GET('/event-types/{id}', { params: { path: { id: eventTypeId } } }),
    enabled: !Number.isNaN(eventTypeId),
  });

  const bookingMutation = useMutation({
    mutationFn: (data: BookingCreate) => client.POST('/bookings', { body: data }),
    onSuccess: () => {
      void navigate(
        `/event-types/${String(eventTypeId)}/book/confirm?start=${encodeURIComponent(startIso)}&success=1`,
      );
    },
  });

  if (isAdmin) return <Navigate to="/" replace />;

  if (searchParams.get('success') === '1') {
    return (
      <Container size="sm" py="xl">
        <Stack gap="lg">
          <Title order={2}>Бронь подтверждена</Title>
          <Text>Встреча успешно забронирована. Вы получите уведомление на email.</Text>
          <Button
            onClick={() => {
              void navigate('/');
            }}
          >
            На главную
          </Button>
        </Stack>
      </Container>
    );
  }

  if (Number.isNaN(eventTypeId) || !startIso || !dayjs(startIso).isValid()) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red">Некорректные параметры бронирования</Alert>
      </Container>
    );
  }

  if (eventTypeQuery.isLoading) {
    return (
      <Container size="sm" py="xl">
        <Stack gap="lg">
          <Skeleton height={30} width="60%" radius="md" />
          <Skeleton height={20} width="40%" radius="md" />
          <Skeleton height={200} radius="md" />
        </Stack>
      </Container>
    );
  }

  const eventTypeData = eventTypeQuery.data;
  const errorMessage =
    eventTypeData?.error?.message ??
    (eventTypeQuery.error instanceof Error ? eventTypeQuery.error.message : null);

  if (errorMessage || !eventTypeData?.data) {
    return (
      <Container size="sm" py="xl">
        <Alert color="red">{errorMessage ?? 'Не удалось загрузить данные'}</Alert>
      </Container>
    );
  }

  const eventType = eventTypeData.data;
  const formattedDate = dayjs(startIso).format('DD.MM.YYYY');
  const formattedTime = `${dayjs(startIso).format('HH:mm')}–${dayjs(startIso).add(eventType.durationMinutes, 'minute').format('HH:mm')}`;

  const apiError = bookingMutation.data?.error;

  return (
    <Container size="sm" py="xl">
      <Stack gap="lg">
        <Text c="dimmed" size="sm">
          {formattedDate}, {formattedTime}
        </Text>

        {apiError ? <Alert color="red">{apiError.message}</Alert> : null}

        <TextInput
          label="Имя"
          placeholder="Ваше имя"
          required
          value={guestName}
          onChange={(e) => {
            setGuestName(e.currentTarget.value);
          }}
        />

        <TextInput
          label="Email"
          placeholder="your@email.com"
          required
          type="email"
          value={guestEmail}
          onChange={(e) => {
            setGuestEmail(e.currentTarget.value);
          }}
        />

        <Textarea
          label="Заметка"
          placeholder="Необязательная заметка к встрече"
          value={note}
          onChange={(e) => {
            setNote(e.currentTarget.value);
          }}
        />

        <Button
          size="lg"
          fullWidth
          loading={bookingMutation.isPending}
          disabled={!guestName || !guestEmail}
          onClick={() => {
            bookingMutation.mutate({
              eventTypeId,
              start: startIso,
              guestName,
              guestEmail,
              note: note || undefined,
            });
          }}
        >
          Подтвердить бронь
        </Button>
      </Stack>
    </Container>
  );
}
