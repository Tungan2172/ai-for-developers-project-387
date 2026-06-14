import { Container, Title, Text } from '@mantine/core';

export function Welcome() {
  return (
    <Container size="sm" py="xl">
      <Title order={1}>Calendar</Title>
      <Text c="dimmed">Скелет приложения. Экраны добавляются на этапах F-welcome…F5.</Text>
    </Container>
  );
}
