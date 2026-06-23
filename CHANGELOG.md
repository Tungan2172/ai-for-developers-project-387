# Changelog

## [1.2.0](https://github.com/Tungan2172/ai-for-developers-project-387/compare/v1.1.0...v1.2.0) (2026-06-23)


### Features

* add nightly audit workflow (build + e2e + lighthouse + issue) ([621f04f](https://github.com/Tungan2172/ai-for-developers-project-387/commit/621f04ffd17fd306188a96b74f7764c71d6d37db))
* add nightly audit workflow (build + e2e + lighthouse + issue) ([26858dc](https://github.com/Tungan2172/ai-for-developers-project-387/commit/26858dc5d5307d4e3f2aa2bc3b65042a8d54438f))
* remove EventTypeDetail page, navigate Welcome → /event-types/{id}/book ([c20fbd5](https://github.com/Tungan2172/ai-for-developers-project-387/commit/c20fbd5e5678123f182b8123acaaadd523b513f3))


### Bug Fixes

* change nightly audit schedule to 01:30 MSK ([35fba61](https://github.com/Tungan2172/ai-for-developers-project-387/commit/35fba6106d0352837ae34c118da45563aad9fa34))
* change nightly audit schedule to 01:30 MSK ([7645bd8](https://github.com/Tungan2172/ai-for-developers-project-387/commit/7645bd8effc5ecba96019efbeb5fee14dbecff42))
* change nightly audit schedule to 01:45 MSK ([9966543](https://github.com/Tungan2172/ai-for-developers-project-387/commit/9966543ca2d54f222770541f0d9463c67ee6a1ab))
* change nightly audit schedule to 02:00 MSK ([39d06ac](https://github.com/Tungan2172/ai-for-developers-project-387/commit/39d06ac3c464707b350bc849ac395fcf68c7ab71))
* change nightly audit schedule to 02:30 MSK ([951f4e3](https://github.com/Tungan2172/ai-for-developers-project-387/commit/951f4e3cb4744c3558d6fc64e8c2e8ddd4542dfb))
* change nightly audit schedule to 06:00 MSK ([2d97896](https://github.com/Tungan2172/ai-for-developers-project-387/commit/2d9789681070cabcda8bfd2d40841502b1960ce3))
* change nightly audit schedule to 06:00 MSK ([b1864a8](https://github.com/Tungan2172/ai-for-developers-project-387/commit/b1864a8d9556968506b7eef9360267447968c8e7))
* correct nightly audit cron to 00:55 MSK and fix YAML block scala… ([71cc990](https://github.com/Tungan2172/ai-for-developers-project-387/commit/71cc99027ab7419c44d0f07334d1484fd852a989))
* correct nightly audit cron to 00:55 MSK and fix YAML block scalar in issue body ([f38ae8a](https://github.com/Tungan2172/ai-for-developers-project-387/commit/f38ae8a2901423c46b747c4ff1cb2041ec1ffd21))
* pass GITHUB_TOKEN explicitly to release-please-action ([5e4c78a](https://github.com/Tungan2172/ai-for-developers-project-387/commit/5e4c78a58c8d154935a588a0d957fd5da8751c84))
* quote pg_isready health check in postgres service ([fd52090](https://github.com/Tungan2172/ai-for-developers-project-387/commit/fd5209014c46c315ff518ba5723de26923d908dc))
* quote pg_isready health check in postgres service ([af19e73](https://github.com/Tungan2172/ai-for-developers-project-387/commit/af19e7321a27b3630a9822b64225a0bf021e5d99))
* remove dead code and fix now/today ordering in slot generation ([e47154c](https://github.com/Tungan2172/ai-for-developers-project-387/commit/e47154c5c37411658c78dba094d7f373773ad065))
* remove manual server start, let Playwright webServer manage lifecycle ([e7944b0](https://github.com/Tungan2172/ai-for-developers-project-387/commit/e7944b0e9183cdd53b8aeef7c9d8d3bde0e7ce5c))
* restrict /oc triggers to explain/fix/comment and add bot-actor guard ([ad7e513](https://github.com/Tungan2172/ai-for-developers-project-387/commit/ad7e5137651a9bc8fe77cefec458064c612831fc))
* use PAT for release-please to bypass PR creation restriction ([f70a677](https://github.com/Tungan2172/ai-for-developers-project-387/commit/f70a677d364b1b8230ed158cf856161140866d58))
* use PAT for release-please to bypass PR creation restriction ([e874fac](https://github.com/Tungan2172/ai-for-developers-project-387/commit/e874fac843a847785a4f06f3c12ad23fb59b0ec9))

## [1.1.0](https://github.com/Tungan2172/ai-for-developers-project-386/compare/v1.0.0...v1.1.0) (2026-06-23)


### Features

* root Dockerfile + deploy configs for Render ([e166273](https://github.com/Tungan2172/ai-for-developers-project-386/commit/e166273fe9e94bf459bd7d8b4e0f80b2fdd8cc8e))
* root Dockerfile + deploy configs for Render ([e166273](https://github.com/Tungan2172/ai-for-developers-project-386/commit/e166273fe9e94bf459bd7d8b4e0f80b2fdd8cc8e))
* root Dockerfile + deploy configs for Render ([b6a91fc](https://github.com/Tungan2172/ai-for-developers-project-386/commit/b6a91fc239cd9a7bdc5cb734d0080b03d6d989d3))


### Bug Fixes

* auto-detect psycopg v3 driver for postgresql:// URLs ([ce7cd90](https://github.com/Tungan2172/ai-for-developers-project-386/commit/ce7cd90cb0e11d4b8fd96bbc980f130aa3c01415))
* graceful DB init fallback + DB-aware health check ([106d36e](https://github.com/Tungan2172/ai-for-developers-project-386/commit/106d36e9f0671e706ec06f425060f8ea63d1916e))
* graceful DB init fallback + DB-aware health check ([458b640](https://github.com/Tungan2172/ai-for-developers-project-386/commit/458b64065978feb450bf3aa61835badf8c8f9a6f))
* install gettext-base for envsubst in Dockerfile ([1b31dad](https://github.com/Tungan2172/ai-for-developers-project-386/commit/1b31dad967eb4bd1a950b446a574d79692ba5b0d))
* name EXCLUDE constraint in ensure_db DO block ([29adb29](https://github.com/Tungan2172/ai-for-developers-project-386/commit/29adb290e188f505cd39ff156e19f65f3a29d8a6))
* name EXCLUDE constraint in ensure_db DO block ([e5adce8](https://github.com/Tungan2172/ai-for-developers-project-386/commit/e5adce860012f038a51aabe7d701eedd53c988cd))
* register ORM models in ensure_db and fix alembic psycopg v3 URL ([8e60586](https://github.com/Tungan2172/ai-for-developers-project-386/commit/8e60586f3c8e09d3317a4ff0a14b8118741109c9))
* use $PORT without default value syntax for envsubst compatibility ([9b61ee6](https://github.com/Tungan2172/ai-for-developers-project-386/commit/9b61ee6984bcfaa3d53a2466eee2521ab590876d))
* use dynamic future dates in e2e booking test and fix ruff import order ([4528e92](https://github.com/Tungan2172/ai-for-developers-project-386/commit/4528e9203cf5640c971cb3c8dd6fcf6a90a036a7))

## 1.0.0 (2026-06-21)


### Features

* CRUD типов событий администратора (F5) ([fb24317](https://github.com/Tungan2172/ai-for-developers-project-386/commit/fb243174e0aadeb1ad65a78f80c33b6ee1d5696c))
* e2e tests with Playwright + real backend ([dc68457](https://github.com/Tungan2172/ai-for-developers-project-386/commit/dc6845732bc17b61797772d9482b3fefe06783d9))
* e2e tests with Playwright + real backend (E2E) ([0fd1844](https://github.com/Tungan2172/ai-for-developers-project-386/commit/0fd18449e233a1f464fb94eb3f61c12cffd3f4df))
* entrypoint.sh, make deploy/smoke, compose cleanup (S-fin) ([63b6c51](https://github.com/Tungan2172/ai-for-developers-project-386/commit/63b6c51e0a934cc46d83cdc6310ae9b9470e433a))
* entrypoint.sh, make deploy/smoke, compose cleanup (S-fin) ([c948567](https://github.com/Tungan2172/ai-for-developers-project-386/commit/c9485670a93360feec77cc9709c5c7e0537fa750))
* GET/DELETE bookings и GET /owner (B6) ([31547e7](https://github.com/Tungan2172/ai-for-developers-project-386/commit/31547e7a7054997be42387c53b8b19dea9c25430))
* GET/POST/DELETE bookings и GET /owner (B6) ([a6d9e53](https://github.com/Tungan2172/ai-for-developers-project-386/commit/a6d9e530525049dde8a47cbd2065cd5e31d2d886))
* PATCH и DELETE /event-types/{id} с проверкой 409 при бронях (B3) ([7fc77d0](https://github.com/Tungan2172/ai-for-developers-project-386/commit/7fc77d00bdc93c9b0386f3845be54e8ef4b9c09d))
* PATCH и DELETE /event-types/{id} с проверкой 409 при бронях (B3) ([6424497](https://github.com/Tungan2172/ai-for-developers-project-386/commit/6424497d6b5fcaa8aec0a7f268bda4630f6ec092))
* Playwright E2E tests and CI pipeline fixes ([dc68457](https://github.com/Tungan2172/ai-for-developers-project-386/commit/dc6845732bc17b61797772d9482b3fefe06783d9))
* POST /bookings с валидацией слотов и проверкой занятости (B5) ([89cd745](https://github.com/Tungan2172/ai-for-developers-project-386/commit/89cd745e37d94ca0ef94b0f749e5d3f433527a4e))
* POST /bookings с валидацией слотов и проверкой занятости (B5) ([56fadea](https://github.com/Tungan2172/ai-for-developers-project-386/commit/56fadea27ac81e5a940736b604b541472522e087))
* release-please workflow and Conventional Commits ([641efeb](https://github.com/Tungan2172/ai-for-developers-project-386/commit/641efebc224bdb5162c0fad3d241642503aa18c3))
* release-please workflow and Conventional Commits docs ([afe4bba](https://github.com/Tungan2172/ai-for-developers-project-386/commit/afe4bba61d4d44934947f3bb2e81608fb754ffe8))
* schemathesis контракт-тест (B7) ([2a8d462](https://github.com/Tungan2172/ai-for-developers-project-386/commit/2a8d46297576668f94ec2fbcad5ae30aaa7827b3))
* schemathesis контракт-тест (B7) ([0065149](https://github.com/Tungan2172/ai-for-developers-project-386/commit/006514903aaba068a8e531995bd507df525d454c))
* test coverage tools (pytest-cov + @vitest/coverage-v8) + CI ([0c5c01e](https://github.com/Tungan2172/ai-for-developers-project-386/commit/0c5c01e5fe17e0e582c3939c0034e6e9ba190dd4))
* test coverage tools (pytest-cov + @vitest/coverage-v8) + CI ([2a01536](https://github.com/Tungan2172/ai-for-developers-project-386/commit/2a01536fdb6c3d3da44ecf927d76d6c57c1e196d))
* TypeSpec-контракт API (S0a) ([f49a1ad](https://github.com/Tungan2172/ai-for-developers-project-386/commit/f49a1ad8a897aa8b57c7e2b5b16f520bdbf6655f))
* база данных, доменное ядро, Alembic, сид владельца (B1) ([db068d5](https://github.com/Tungan2172/ai-for-developers-project-386/commit/db068d5132e567c03722959f429c8ecaff470513))
* база данных, доменное ядро, репозитории, Alembic, сид владельца (B1) ([f48d5f1](https://github.com/Tungan2172/ai-for-developers-project-386/commit/f48d5f193c402024d229da5b28bd0995884cde12))
* генерация слотов и GET /event-types/{id}/slots (B4) ([d2b70c1](https://github.com/Tungan2172/ai-for-developers-project-386/commit/d2b70c1f86ef3037a23186c1c708d79e287b0087))
* генерация слотов и GET /event-types/{id}/slots (B4) ([e7a2e56](https://github.com/Tungan2172/ai-for-developers-project-386/commit/e7a2e568edd20fc10a7e339c9f89b275416d88dd))
* добавлен TypeSpec-контракт API календаря бронирования ([2707f33](https://github.com/Tungan2172/ai-for-developers-project-386/commit/2707f339c116c8ae60231d4d7f86387acf26d3c5))
* защита бронирования по роли через RoleContext ([a8b7544](https://github.com/Tungan2172/ai-for-developers-project-386/commit/a8b75445fab875763b54740bcb32ecce44819f5e))
* карточки событий некликабельны для владельца ([ea8a53b](https://github.com/Tungan2172/ai-for-developers-project-386/commit/ea8a53bce1a033033e8380d992280882bb880804))
* переключатель режима гостя/владельца ([64bc500](https://github.com/Tungan2172/ai-for-developers-project-386/commit/64bc5005e4129047f1866d873a12a521bf398c54))
* скелет фронта Mantine + React Router + MSW + кодген (F0) ([c0949ba](https://github.com/Tungan2172/ai-for-developers-project-386/commit/c0949ba330a9c93ca16b068ef0a8f01031963c60))
* скелет фронта Mantine + React Router + MSW + кодген (F0) ([48f36b5](https://github.com/Tungan2172/ai-for-developers-project-386/commit/48f36b59f94b94b21e2336f35af5f1cae2dcdaeb))
* страница деталей типа события с навигацией и кнопкой бронирования (F1) ([9b58a70](https://github.com/Tungan2172/ai-for-developers-project-386/commit/9b58a70055836c08777dad7e291fad812eaab4b9))
* страница деталей типа события с навигацией и кнопкой бронирования (F1) ([e049b42](https://github.com/Tungan2172/ai-for-developers-project-386/commit/e049b4209bdc42931e9b8153719a45532feaf502))
* страница календаря и выбора слотов с интеграцией Mantine Calendar (F2) ([ff72779](https://github.com/Tungan2172/ai-for-developers-project-386/commit/ff72779ffbd337496604ae2dc709bf138c048983))
* страница календаря и выбора слотов с интеграцией Mantine Calendar (F2) ([ab1f859](https://github.com/Tungan2172/ai-for-developers-project-386/commit/ab1f859783c4187ed96a4ba16a7a2402d2df0d34))
* страница приветствия с профилем владельца и списком типов событий (F-welcome) ([c68c74e](https://github.com/Tungan2172/ai-for-developers-project-386/commit/c68c74ef828c8be7f82da4f237dacb36b3a8d0dd))
* страница приветствия с профилем владельца и списком типов событий (F-welcome) ([1e40196](https://github.com/Tungan2172/ai-for-developers-project-386/commit/1e40196eab07e00e4fa296d3e9d3540b79893e6c))
* страница списка броней администратора (F4) ([4d07439](https://github.com/Tungan2172/ai-for-developers-project-386/commit/4d074397c303280e083071b638dcf0e210170bd7))
* страница списка броней администратора с отменой (F4) ([8678c00](https://github.com/Tungan2172/ai-for-developers-project-386/commit/8678c00a960d381f250e56d54609193fcdce5cdf))
* форма бронирования (F3) ([f6ca38b](https://github.com/Tungan2172/ai-for-developers-project-386/commit/f6ca38b636e14ecb662b96d93fcbeba6f98bf2e8))
* форма бронирования с полями guestName/guestEmail/note (F3) ([bf6e0ea](https://github.com/Tungan2172/ai-for-developers-project-386/commit/bf6e0ea30292debf345909fae806ae4e37470be1))
* эндпоинты GET/POST event-types (B2) ([d2a116d](https://github.com/Tungan2172/ai-for-developers-project-386/commit/d2a116d2f68b68a3214ce6cce7f88b033a56fec3))
* эндпоинты GET/POST event-types с Pydantic-DTO и обработкой ошибок (B2) ([4df8dca](https://github.com/Tungan2172/ai-for-developers-project-386/commit/4df8dca2f991b0b3b984c2c912d37542f0cd029c))


### Bug Fixes

* add postgres port mapping in CI; format e2e/helpers.ts ([cd0d271](https://github.com/Tungan2172/ai-for-developers-project-386/commit/cd0d271c23451a476c9a122dd0b0877504df949c))
* commit session after each request in get_session() ([4d06f8d](https://github.com/Tungan2172/ai-for-developers-project-386/commit/4d06f8d52fa8c804dbe760d36b93277b2e695a73))
* disable MSW in e2e mode (VITE_E2E=true) ([b3ea83a](https://github.com/Tungan2172/ai-for-developers-project-386/commit/b3ea83af34573e9111810f9fbde9a4f2e6f091af))
* e2e test alignments (30/15min) and selector robustness ([e2f1025](https://github.com/Tungan2172/ai-for-developers-project-386/commit/e2f1025db396263569d3bed719fee89c78ead763))
* postgres health-cmd quoting in CI; ignore playwright.config.ts in eslint ([7f3ee59](https://github.com/Tungan2172/ai-for-developers-project-386/commit/7f3ee590820caa1afa304ecca212e08c713b9bb5))
* slot start format check; remove debug logging ([0fa007a](https://github.com/Tungan2172/ai-for-developers-project-386/commit/0fa007a3da5f4904ac37d57fc72b3bb8ce84c751))
* slots query date range to &lt; to_date (exclusive) ([aa0e424](https://github.com/Tungan2172/ai-for-developers-project-386/commit/aa0e424535b35f0330c12179405d12fbe9b72b92))
* verify slot busy via API; simplify calendar test ([abfb48c](https://github.com/Tungan2172/ai-for-developers-project-386/commit/abfb48c26d582fa1c680574e27edbdee2bfbe8a5))
