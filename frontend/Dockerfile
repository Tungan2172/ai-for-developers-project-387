# Многоступенчатая сборка: node собирает статику, nginx её раздаёт и проксирует /api.
FROM node:22-alpine AS build

WORKDIR /app

# Слой зависимостей кэшируется отдельно от исходников.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
