FROM node
WORKDIR /usr/src/app
COPY ./monitoring/package*.json ./
RUN npm install
COPY ./monitoring .
EXPOSE 8080
CMD ["npm", "index.js"]