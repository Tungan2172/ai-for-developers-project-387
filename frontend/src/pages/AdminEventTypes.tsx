import {
  Alert,
  Button,
  Card,
  Container,
  Group,
  NumberInput,
  Skeleton,
  Stack,
  Table,
  Text,
  TextInput,
  Textarea,
  Title,
} from '@mantine/core';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';

import { client } from '../api/client.ts';
import type { components } from '../api/schema.d.ts';

type EventType = components['schemas']['EventType'];
type EventTypeCreate = components['schemas']['EventTypeCreate'];
type EventTypeUpdate = components['schemas']['EventTypeUpdate'];

interface FormState {
  title: string;
  description: string;
  durationMinutes: string;
}

const emptyForm: FormState = { title: '', description: '', durationMinutes: '' };

function formToCreate(f: FormState): EventTypeCreate {
  return { title: f.title, description: f.description, durationMinutes: Number(f.durationMinutes) };
}

function formToUpdate(f: FormState): EventTypeUpdate {
  return {
    title: f.title || undefined,
    description: f.description || undefined,
    durationMinutes: f.durationMinutes ? Number(f.durationMinutes) : undefined,
  };
}

function eventTypeToForm(et: EventType): FormState {
  return { title: et.title, description: et.description, durationMinutes: String(et.durationMinutes) };
}

export function AdminEventTypes() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<FormState>(emptyForm);
  const [apiError, setApiError] = useState<string | null>(null);

  const isEditing = editingId !== null;

  const eventTypesQuery = useQuery({
    queryKey: ['event-types'],
    queryFn: () => client.GET('/event-types'),
  });

  const createMutation = useMutation({
    mutationFn: (data: EventTypeCreate) => client.POST('/event-types', { body: data }),
    onSuccess: () => {
      closeForm();
      void queryClient.invalidateQueries({ queryKey: ['event-types'] });
    },
    onError: (err) => {
      setApiError(err instanceof Error ? err.message : 'Ошибка создания');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: EventTypeUpdate }) =>
      client.PATCH('/event-types/{id}', { params: { path: { id } }, body: data }),
    onSuccess: () => {
      closeForm();
      void queryClient.invalidateQueries({ queryKey: ['event-types'] });
    },
    onError: (err) => {
      setApiError(err instanceof Error ? err.message : 'Ошибка обновления');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) =>
      client.DELETE('/event-types/{id}', { params: { path: { id } } }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['event-types'] });
    },
    onError: (err) => {
      const msg = err instanceof Error ? err.message : 'Ошибка удаления';
      const resp = (err as { response?: { status: number } }).response;
      if (resp?.status === 409) {
        setApiError('Нельзя удалить тип события с предстоящими бронями');
      } else {
        setApiError(msg);
      }
    },
  });

  function closeForm() {
    setShowForm(false);
    setEditingId(null);
    setForm(emptyForm);
    setApiError(null);
  }

  function openCreate() {
    setEditingId(null);
    setForm(emptyForm);
    setApiError(null);
    setShowForm(true);
  }

  function openEdit(et: EventType) {
    setEditingId(et.id);
    setForm(eventTypeToForm(et));
    setApiError(null);
    setShowForm(true);
  }

  function handleSave() {
    if (!form.title || !form.description || !form.durationMinutes) return;
    setApiError(null);
    if (isEditing) {
      updateMutation.mutate({ id: editingId, data: formToUpdate(form) });
    } else {
      createMutation.mutate(formToCreate(form));
    }
  }

  if (eventTypesQuery.isLoading) {
    return (
      <Container size="md" py="xl">
        <Stack gap="lg">
          <Skeleton height={30} width="40%" radius="md" />
          <Skeleton height={200} radius="md" />
        </Stack>
      </Container>
    );
  }

  const errorMessage = eventTypesQuery.error instanceof Error ? eventTypesQuery.error.message : null;
  if (errorMessage) {
    return (
      <Container size="md" py="xl">
        <Alert color="red">{errorMessage}</Alert>
      </Container>
    );
  }

  const items: EventType[] = eventTypesQuery.data?.data ?? [];
  const isMutating = createMutation.isPending || updateMutation.isPending;

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Group justify="space-between">
          <Title order={2}>Типы событий</Title>
          <Button onClick={openCreate}>Создать тип события</Button>
        </Group>

        {items.length === 0 ? (
          <Text c="dimmed">Нет типов событий</Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Название</Table.Th>
                <Table.Th>Описание</Table.Th>
                <Table.Th>Длит.</Table.Th>
                <Table.Th />
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {items.map((et) => (
                <Table.Tr key={et.id}>
                  <Table.Td>{et.title}</Table.Td>
                  <Table.Td>{et.description}</Table.Td>
                  <Table.Td>{et.durationMinutes} мин</Table.Td>
                  <Table.Td>
                    <Group gap="xs">
                      <Button size="xs" variant="light" onClick={() => { openEdit(et); }}>
                        Редактировать
                      </Button>
                      <Button
                        size="xs"
                        color="red"
                        loading={deleteMutation.isPending}
                        onClick={() => { deleteMutation.mutate(et.id); }}
                      >
                        Удалить
                      </Button>
                    </Group>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}

        {showForm ? (
          <Card withBorder shadow="sm" padding="lg" radius="md">
            <Stack gap="md">
              <Title order={3}>{isEditing ? 'Редактировать тип события' : 'Создать тип события'}</Title>

              {apiError ? <Alert color="red">{apiError}</Alert> : null}

              <TextInput
                label="Название"
                required
                value={form.title}
                onChange={(e) => { setForm({ ...form, title: e.currentTarget.value }); }}
              />

              <Textarea
                label="Описание"
                required
                value={form.description}
                onChange={(e) => { setForm({ ...form, description: e.currentTarget.value }); }}
              />

              <NumberInput
                label="Длительность (мин)"
                required
                min={1}
                max={480}
                value={form.durationMinutes ? Number(form.durationMinutes) : ''}
                onChange={(v) => { setForm({ ...form, durationMinutes: v === '' ? '' : String(v) }); }}
              />

              <Group>
                <Button loading={isMutating} onClick={handleSave}>
                  {isEditing ? 'Сохранить' : 'Создать'}
                </Button>
                <Button variant="light" onClick={closeForm}>Отмена</Button>
              </Group>
            </Stack>
          </Card>
        ) : null}
      </Stack>
    </Container>
  );
}
