# Base docker image - use Debian like the proven example
FROM debian:bullseye-slim

# Install Chrome (based on proven jess/chrome Dockerfile)
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    # Chrome dependencies from proven example
    hicolor-icon-theme \
    libcanberra-gtk3-0 \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libpulse0 \
    libv4l-0 \
    fonts-symbola \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libpango-1.0-0 \
    fonts-liberation \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python3 -m playwright install chromium

# Copy application code
COPY . .

# Expose the port
EXPOSE 8000

# Start the application
CMD ["python3", "src/server.py"]
