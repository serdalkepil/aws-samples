# Node.js 22 LTS on Alpine. Pulled from ECR Public to avoid Docker Hub rate limits.
FROM public.ecr.aws/docker/library/node:22-alpine

WORKDIR /app
ENV NODE_ENV=production

COPY package.json .
RUN npm install --omit=dev

COPY app.js .

# Run as the unprivileged "node" user that the official image provides
USER node

EXPOSE 8080
CMD [ "node", "app.js" ]
