FROM python:3.9-slim

# Create non-root user
RUN useradd -m ctfuser

# Install only essential tools
RUN apt-get update && apt-get install -y \
    coreutils \
    && rm -rf /var/lib/apt/lists/*

# Set up the application directory
WORKDIR /app

# Copy and install Python requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a custom restricted shell
COPY restricted_shell.py /usr/local/bin/restricted_shell
RUN chmod +x /usr/local/bin/restricted_shell

# Copy application code
COPY . .

# Create the flag files and set ownership BEFORE removing chown/chmod
RUN echo "BMCTF{pretty_lil_baby_you_say_that_maybe_youll_be_thinking_of_me_and_try_to_H4CK_me}" > /app/flag.txt && \
    chmod 644 /app/flag.txt && \
    chown -R ctfuser:ctfuser /app

# Remove other Python interpreters but keep python3.9
RUN find /usr/local/bin -name "*python*" ! -name "python3.9" -delete 2>/dev/null || true

# Remove dangerous binaries (keep /bin/sh for now as Docker needs it)
RUN rm -f /bin/bash /usr/bin/wget /usr/bin/curl /usr/bin/nc* /usr/bin/netcat \
    /usr/bin/python /usr/bin/python2* /usr/bin/pip /usr/bin/pip2* \
    /bin/chmod /bin/chown /usr/bin/sudo \
    /usr/bin/vim /usr/bin/nano /usr/bin/less /usr/bin/more \
    /usr/bin/vi /usr/bin/emacs /usr/bin/find

# Switch to non-root user
USER ctfuser

# Expose Django port
EXPOSE 8000

# Start Django application
CMD ["python3.9", "manage.py", "runserver", "0.0.0.0:8000"]