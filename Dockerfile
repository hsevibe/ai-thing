FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y binutils && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .
RUN poetry run pyinstaller --onefile main.py

FROM python:3.12-slim AS runner

COPY --from=builder /app/dist/main /usr/local/bin/main
CMD ["/usr/local/bin/main"]
