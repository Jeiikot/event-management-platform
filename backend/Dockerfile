FROM python:3.12-slim

# Set environment variables
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Install dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Copy application
COPY . /app

EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
