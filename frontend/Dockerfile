# Frontend Dockerfile (two-stage: build + nginx served)
FROM node:18-alpine AS builder
WORKDIR /app/frontend

# Install dependencies (lockfile assumed to exist at frontend/)
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --silent

# Copy source
COPY frontend/ ./

# Build both user/admin apps if present
RUN if [ -d packages/user-app ]; then (cd packages/user-app && npm run build); fi
RUN if [ -d packages/admin-app ]; then (cd packages/admin-app && npm run build); fi

FROM nginx:1.25-alpine
COPY --from=builder /app/frontend/packages/user-app/build /usr/share/nginx/html/user/ 2>/dev/null || true
COPY --from=builder /app/frontend/packages/admin-app/build /usr/share/nginx/html/admin/ 2>/dev/null || true
COPY infra/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
