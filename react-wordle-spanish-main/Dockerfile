FROM node:16.14.0-alpine3.14 AS node_modules
WORKDIR /app
COPY package-lock.json package.json ./
RUN npm install
COPY . .

FROM node_modules AS prod_builder
RUN npm run build

FROM nginx:1.24.0-alpine
COPY --from=prod_builder /app/build /usr/share/nginx/html
# Default HTTP port of Nginx.
EXPOSE 80
