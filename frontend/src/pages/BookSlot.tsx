import { Button, Container, SimpleGrid, Skeleton, Stack, Text, Title } from '@mantine/core';
import { Calendar } from '@mantine/dates';
import { useQuery } from '@tanstack/react-query';
import dayjs from 'dayjs';
import { useState } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router';

import { client } from '../api/client.ts';
import { useRoleContext } from '../RoleContext.tsx';
import type { components } from '../api/schema.d.ts';

type Slot = components['schemas']['Slot'];

function formatTime(iso: string) {
  return dayjs(iso).format('HH:mm');
}

function isSameDay(a: dayjs.Dayjs, b: dayjs.Dayjs) {
  return a.format('YYYY-MM-DD') === b.format('YYYY-MM-DD');
}

export function BookSlot() {
  const { isAdmin } = useRoleContext();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const eventTypeId = Number(id);
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());

  const slotsQuery = useQuery({
    queryKey: ['slots', eventTypeId],
    queryFn: () => client.GET('/event-types/{id}/slots', { params: { path: { id: eventTypeId } } }),
    enabled: !Number.isNaN(eventTypeId),
  });

  const eventTypeQuery = useQuery({
    queryKey: ['event-type', eventTypeId],
    queryFn: () => client.GET('/event-types/{id}', { params: { path: { id: eventTypeId } } }),
    enabled: !Number.isNaN(eventTypeId),
  });

  if (isAdmin) return <Navigate to="/" replace />;

  if (Number.isNaN(eventTypeId)) {
    return (
      <Container size="sm" py="xl">
        <Text c="red">Тип события не найден</Text>
      </Container>
    );
  }

  if (slotsQuery.isLoading || eventTypeQuery.isLoading) {
    return (
      <Container size="sm" py="xl">
        <Stack gap="lg">
          <Skeleton height={40} width="60%" radius="md" />
          <Skeleton height={300} radius="md" />
          <Skeleton height={100} radius="md" />
        </Stack>
      </Container>
    );
  }

  const slotsData = slotsQuery.data;
  const eventTypeData = eventTypeQuery.data;

  const errorMessage =
    slotsData?.error?.message ??
    eventTypeData?.error?.message ??
    (slotsQuery.error instanceof Error ? slotsQuery.error.message : null) ??
    (eventTypeQuery.error instanceof Error ? eventTypeQuery.error.message : null);

  if (errorMessage || !slotsData?.data || !eventTypeData?.data) {
    return (
      <Container size="sm" py="xl">
        <Text c="red">{errorMessage ?? 'Не удалось загрузить данные'}</Text>
      </Container>
    );
  }

  const eventType = eventTypeData.data;
  const allSlots = slotsData.data;

  const slotsByDate = allSlots.reduce<Record<string, Slot[]>>((acc, slot) => {
    const dateKey = dayjs(slot.start).format('YYYY-MM-DD');
    (acc[dateKey] ??= []).push(slot);
    return acc;
  }, {});

  const selectedDateKey = selectedDate ? dayjs(selectedDate).format('YYYY-MM-DD') : '';
  const selectedSlots = selectedDate ? (slotsByDate[selectedDateKey] ?? []) : [];

  const hasFreeSlots = (date: Date) => {
    const key = dayjs(date).format('YYYY-MM-DD');
    return key in slotsByDate && slotsByDate[key].some((s) => s.status === 'free');
  };

  return (
    <Container size="sm" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={2}>{eventType.title}</Title>
          <Text c="dimmed" size="sm">
            {eventType.durationMinutes} мин
          </Text>
        </div>

        <Calendar
          getDayProps={(date) => ({
            selected: selectedDate ? isSameDay(dayjs(date), dayjs(selectedDate)) : false,
            onClick: () => {
              setSelectedDate(date);
            },
            style: hasFreeSlots(date) ? undefined : { opacity: 0.4 },
          })}
        />

        {selectedSlots.length > 0 ? (
          <SimpleGrid cols={{ base: 2, sm: 3 }}>
            {selectedSlots.map((slot) => (
              <Button
                key={slot.start}
                variant={slot.status === 'free' ? 'filled' : 'light'}
                color={slot.status === 'free' ? 'blue' : 'gray'}
                disabled={slot.status === 'busy'}
                fullWidth
                onClick={
                  slot.status === 'free'
                    ? () => {
                        void navigate(
                          `/event-types/${String(eventTypeId)}/book/confirm?start=${encodeURIComponent(slot.start)}`,
                        );
                      }
                    : undefined
                }
              >
                {formatTime(slot.start)}–{formatTime(slot.end)}
              </Button>
            ))}
          </SimpleGrid>
        ) : selectedDate ? (
          <Text c="dimmed">На этот день нет доступных слотов</Text>
        ) : null}
      </Stack>
    </Container>
  );
}
