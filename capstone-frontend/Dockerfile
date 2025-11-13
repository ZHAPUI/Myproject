# ---- build ----
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---- serve ----
FROM nginx:alpine
# 若你提供了 SPA 回退的 nginx.conf，解开下一行并确保文件存在
# COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
