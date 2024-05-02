FROM python:alpine as base

EXPOSE 8000
RUN apk add --no-cache \
    curl \
    npm \
    nodejs
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /code
COPY /package.json /code
COPY /package-lock.json /code
COPY /poetry.toml /code
COPY /poetry.lock /code
COPY /pyproject.toml /code
COPY /tailwind.config.js /code
RUN poetry install
RUN npm install

FROM base as production

COPY /todo_app /code/todo_app
RUN npx tailwindcss -i ./todo_app/tailwind.css -o ./todo_app/static/css/index.css

CMD poetry run gunicorn -w=4 --bind 0.0.0.0 "todo_app.app:create_app()"

FROM base as development

CMD npm run dev