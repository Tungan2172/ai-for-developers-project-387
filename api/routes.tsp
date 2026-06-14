import "@typespec/http";
import "./models.tsp";

using TypeSpec.Http;

namespace Scheduler;

@route("/event-types")
@tag("Event Types")
namespace EventTypes {
  @doc("Список типов событий (гость и владелец)")
  @get
  op list(): EventType[];

  @doc("Получить тип события по идентификатору")
  @get
  op read(@path id: int64): EventType | NotFoundResponse;

  @doc("Создать тип события (владелец)")
  @post
  op create(@body body: EventTypeCreate): {
    @statusCode statusCode: 201;
    @body created: EventType;
  } | ValidationErrorResponse;

  @doc("Частично обновить тип события (владелец)")
  @patch
  op update(@path id: int64, @body body: EventTypeUpdate):
    | EventType
    | NotFoundResponse
    | ValidationErrorResponse;

  @doc("Удалить тип события (владелец). 409, если есть предстоящие брони")
  @delete
  op delete(@path id: int64): {
    @statusCode statusCode: 204;
  } | NotFoundResponse | ConflictResponse;

  @doc("Слоты типа события на 14 дней вперёд со статусом free/busy")
  @route("/{id}/slots")
  @get
  op slots(
    @path id: int64,
    @doc("Начало диапазона (по умолчанию текущая дата)")
    @query
    from?: plainDate,

    @doc("Конец диапазона (по умолчанию текущая дата + 14 дней)")
    @query
    to?: plainDate,
  ): Slot[] | NotFoundResponse;
}

@route("/bookings")
@tag("Bookings")
namespace Bookings {
  @doc("Список предстоящих броней всех типов (владелец), сортировка по времени")
  @get
  op list(): Booking[];

  @doc("Создать бронь на свободный слот (гость)")
  @post
  op create(@body body: BookingCreate): {
    @statusCode statusCode: 201;
    @body created: Booking;
  } | ConflictResponse | ValidationErrorResponse | NotFoundResponse;

  @doc("Отменить бронь (владелец)")
  @delete
  op cancel(@path id: int64): {
    @statusCode statusCode: 204;
  } | NotFoundResponse;
}

@route("/owner")
@tag("Owner")
namespace OwnerRoutes {
  @doc("Публичный профиль владельца календаря")
  @get
  op read(): Owner;
}

@route("/health")
@tag("Service")
namespace HealthRoutes {
  @doc("Проверка живости сервиса")
  @get
  op check(): HealthStatus;
}
