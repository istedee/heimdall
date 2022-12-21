# syntax=docker/dockerfile:1.4
FROM node:14.4.0-alpine AS development

RUN mkdir /project
WORKDIR /project

COPY . .

RUN npm rebuild node-sass
RUN npm install -g @vue/cli
RUN npm install
ENV HOST=0.0.0.0
CMD ["npm", "run", "dev"]

FROM development as dev-envs
RUN apk update
RUN apk add git


RUN addgroup -S docker
RUN adduser -S --shell /bin/bash --ingroup docker vscode
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["npm", "run", "dev"]
