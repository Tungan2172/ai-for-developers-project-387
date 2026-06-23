---
name: "code-review"
description: "Review code changes following project standards; check only changed files via git diff, verify naming conventions, test coverage, absence of hardcoded config, and collect structured feedback."
---

## Что проверять

1. Найди все измененные файлы через git diff
2. Ревью проводи только по файлам, найденным из пункта 1
3. Для каждого файла проверь:
   - соответствие naming conventions проекта
   - наличие тестов для новой логики
   - отсутствие хардкода конфигурации
4. Собери замечания в структурированный список
5. Если замечаний нет, напиши короткое подтверждение

## Чего не делать

- Не предлагай стилистические правки, которые покрывает линтер
- Не переписывай код, только укажи на проблему
