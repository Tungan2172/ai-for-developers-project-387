import "@typespec/http";

using TypeSpec.Http;

namespace Scheduler;

// --- Ошибки -----------------------------------------------------------------

// Единый формат тела ошибки для всех кодов (404/409/422).
// Почему единый: фронт разбирает ошибки одной функцией, а контракт не зависит
// от внутреннего формата валидации FastAPI (см. AGENTS.md, решение A3).
@doc("Единое тело ошибки")
@error
model ApiError {
  @doc("Машиночитаемый код, например slot_busy, out_of_window, event_type_not_found")
  code: string;

  @doc("Человекочитаемое сообщение")
  message: string;
}

@doc("Ресурс не найден")
model NotFoundResponse {
  @statusCode statusCode: 404;
  @body body: ApiError;
}

@doc("Конфликт: время занято или удаление невозможно")
model ConflictResponse {
  @statusCode statusCode: 409;
  @body body: ApiError;
}

@doc("Ошибка валидации: слот вне окна/часов или некорректные данные")
model ValidationErrorResponse {
  @statusCode statusCode: 422;
  @body body: ApiError;
}

// --- Тип события ------------------------------------------------------------

@doc("Тип события, создаётся владельцем календаря")
model EventType {
  @doc("Идентификатор")
  id: int64;

  @doc("Название")
  @maxLength(200)
  title: string;

  @doc("Описание")
  description: string;

  // Длительность задаёт владелец произвольно (не кратна 30). Верхняя граница 480
  // равна длине рабочего окна 09:00-17:00: тип длиннее окна не имел бы слотов.
  @doc("Длительность в минутах (1..480)")
  @minValue(1)
  @maxValue(480)
  durationMinutes: int32;
}

@doc("Данные для создания типа события")
model EventTypeCreate {
  @maxLength(200)
  title: string;

  description: string;

  @minValue(1)
  @maxValue(480)
  durationMinutes: int32;
}

@doc("Данные для частичного обновления типа события")
model EventTypeUpdate {
  @maxLength(200)
  title?: string;

  description?: string;

  @minValue(1)
  @maxValue(480)
  durationMinutes?: int32;
}

// --- Слоты ------------------------------------------------------------------

@doc("Статус слота")
enum SlotStatus {
  free,
  busy,
}

@doc("Временной слот для типа события. Шаг сетки равен длительности типа.")
model Slot {
  @doc("Начало слота (TZ владельца, +03:00)")
  start: offsetDateTime;

  @doc("Конец слота")
  end: offsetDateTime;

  @doc("Свободен или занят")
  status: SlotStatus;
}

// --- Бронирование -----------------------------------------------------------

@doc("Бронирование встречи")
model Booking {
  @doc("Идентификатор")
  id: int64;

  @doc("Идентификатор типа события")
  eventTypeId: int64;

  // Денормализация: название и длительность встроены, чтобы список предстоящих
  // встреч рисовался одним запросом без джойна на клиенте (решение A2).
  @doc("Название типа события на момент брони")
  eventTypeTitle: string;

  @doc("Длительность типа события в минутах")
  durationMinutes: int32;

  @doc("Начало встречи")
  start: offsetDateTime;

  @doc("Конец встречи (вычисляется сервером из длительности)")
  end: offsetDateTime;

  @doc("Имя гостя")
  guestName: string;

  @doc("Email гостя")
  guestEmail: string;

  @doc("Заметка/тема встречи")
  note?: string;

  @doc("Момент создания брони")
  createdAt: offsetDateTime;
}

@doc("Данные для создания брони гостем")
model BookingCreate {
  @doc("Идентификатор выбранного типа события")
  eventTypeId: int64;

  // Гость передаёт только начало; конец сервер вычисляет из длительности типа.
  @doc("Начало выбранного слота")
  start: offsetDateTime;

  @maxLength(200)
  guestName: string;

  @format("email")
  guestEmail: string;

  @maxLength(2000)
  note?: string;
}

// --- Владелец и служебное ---------------------------------------------------

@doc("Публичный профиль владельца календаря")
model Owner {
  @doc("Имя владельца")
  name: string;

  @doc("Подзаголовок/роль, например Host")
  title: string;

  @doc("Описание")
  description: string;
}

@doc("Состояние сервиса")
model HealthStatus {
  status: string;
}
