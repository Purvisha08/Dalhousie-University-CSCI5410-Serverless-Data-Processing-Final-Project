FROM node:16.17-alpine3.15 as build

RUN mkdir -p usr/src/app
WORKDIR /usr/src/app
COPY . ./
RUN npm install

RUN npm run build


# ---
FROM fholzer/nginx-brotli:v1.12.2

WORKDIR /etc/nginx
ADD nginx.conf /etc/nginx/nginx.conf


COPY --from=build /usr/src/app/build /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
