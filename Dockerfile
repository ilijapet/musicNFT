# Use an official Python runtime as the base image
FROM python:3.10.4-buster

# Set the working directory in the container from where all command will be running
WORKDIR /opt/project

# Tells Python to not write .pyc files to disk. 
# This can make your Docker build slightly faster and can also 
#  avoid some permission issues in certain cases.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# This adds the current directory (.) to the Python path. This means that 
# Python will be able to import modules from the current directory.
ENV PYTHONPATH .
ENV BACKENDSETTINGS_IN_DOCKER true

# Install dependencies
RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install virtualenvwrapper poetry==1.4.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root

# Copy project files
COPY ["README.rst", "Makefile", "./"]
COPY backend backend
COPY local local

# Expose port 8000
EXPOSE 8000

COPY var var
# Set up the entrypoint (this script is executed when the container starts)
COPY ["gunicorn.dev.py", "./"]
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
