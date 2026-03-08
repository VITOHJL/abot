FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install Python package metadata first (cached layer)
COPY pyproject.toml README.md LICENSE ./
RUN mkdir -p abot && touch abot/__init__.py && \
    uv pip install --system --no-cache . && \
    rm -rf abot

# Copy source and install
COPY abot/ abot/
RUN uv pip install --system --no-cache .

# Create runtime config directory
RUN mkdir -p /root/.abot

# Gateway default port
EXPOSE 18790

ENTRYPOINT ["abot"]
CMD ["status"]
