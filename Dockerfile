FROM python:3.10-slim as base

# Install Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /usr/src/app

COPY src/ poetry.lock pyproject.toml /usr/src/app/

FROM base as dev

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y gcc

RUN npm install -g nodemon

RUN poetry install

CMD ["nodemon", "--exec", "poetry", "run", "python", "src/main.py", "--watch", "."]

FROM base as prod

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "src/main.py"]