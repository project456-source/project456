# Dockerfile — For project456 container
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgbm1 \
    libasound2 \
    libpangossm1 \
    libdrm2 \
    libxcomposite1 \
    libxkbcommon0 \
    libxext6 \
    libx11-6 \
    libxcursor1 \
    libxinerama1 \
    libxrandr2 \
    libxiner de 6 \
    libxrender1 \
    libX11-6 \
    libXext6 \
    libXdamage6 \
    libXpresent0 \
    libXrandr2 \
    libXrandr2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright chromium browser
RUN playwright install chromium

# Copy all app files
COPY . .

# Set environment variables
ENV PATH="/home/container/.local/bin:${PATH}"
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "main.py"]
