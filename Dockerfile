FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -m venv "$POETRY_HOME" && "$POETRY_HOME/bin/pip" install poetry==1.2.0
COPY . ./
RUN poetry install --only main --no-interaction --no-ansi -vvv


FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
CMD [ "python", "./main.py" ]