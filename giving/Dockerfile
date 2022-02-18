FROM node:12.18.3 AS builder
ARG google_client_id=""

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
RUN npm install
COPY . ./
RUN mkdir env && echo "VITE_GOOGLE_CLIENT_ID=${google_client_id}" > env/.env
RUN npm run build

FROM nginx:1.17-alpine
RUN apk --no-cache add curl
COPY ./nginx.conf /etc/nginx/nginx.template
COPY --from=builder /app/dist/ /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]