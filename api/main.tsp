import "@typespec/http";
import "@typespec/openapi";
import "@typespec/openapi3";
import "./models.tsp";
import "./routes.tsp";

using TypeSpec.Http;
using TypeSpec.OpenAPI;

/**
 * Контракт API сервиса бронирования встреч (единственный источник правды).
 *
 * Роли без авторизации: владелец календаря (один профиль "owner") и гости.
 * Время в TZ владельца Europe/Moscow (+03:00). Слоты: пн-пт 09:00-17:00,
 * окно 14 дней, шаг сетки равен длительности типа события.
 *
 * Пути даны без префикса /api: его добавляет обратный прокси (vite в dev,
 * nginx в prod), а бэкенд обслуживает маршруты от корня.
 */
@service(#{ title: "Meeting Scheduler API" })
@info(#{ version: "0.1.0" })
@server("http://localhost:8000", "Локальный backend")
namespace Scheduler;
