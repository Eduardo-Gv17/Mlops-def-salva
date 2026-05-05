FROM node:20-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY package*.json ./
RUN npm install --omit=dev
COPY . .
EXPOSE 8003
CMD ["node", "index.js"]
