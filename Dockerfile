FROM python:alpine as base

EXPOSE 8080
RUN apk add --no-cache \
    curl \
    npm \
    nodejs
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /code
COPY /package.json /package-lock.json /code/
COPY /poetry.toml /poetry.lock /pyproject.toml /code/
COPY /tailwind.config.js /code
RUN poetry install --no-root
RUN npm install

FROM base AS test

COPY / /code
ENTRYPOINT poetry run pytest

FROM base AS development

ENTRYPOINT npm run dev

FROM base AS production

COPY /todo_app /code/todo_app
RUN npx tailwindcss -i ./todo_app/tailwind.css -o ./todo_app/static/css/index.css
ENTRYPOINT poetry run gunicorn -w=4 --bind 0.0.0.0:8080 "todo_app.app:create_app()"