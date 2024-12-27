 # Use the official lightweight Python image
FROM python:3.8-slim


# Set the working directory
WORKDIR /app

# Download latest listing of available packages: 
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade
# Install a new package:
RUN apt-get -y install syslog-ng vim net-tools iputils-ping logrotate cron

# Define environment variable

ENV APP_ROOT_PATH="/app"
ENV APP_ROOT_HOST="${APP_ROOT_PATH}/host"
ENV APP_COSM_PATH="${APP_ROOT_PATH}/CosmBot"
ENV APPLOGS="${APP_ROOT_HOST}/logs"
ENV RESOURCE_PATH="${APP_ROOT_HOST}/resources"
ENV TMP_RESOURCE_PATH="${APP_ROOT_PATH}/resources"
ENV PYTHONPATH="${APP_COSM_PATH}"

# Create a new directory under /app
RUN mkdir -p ${APP_COSM_PATH}
# RUN mkdir -p ${RESOURCE_PATH}
# RUN mkdir -p ${APPLOGS}
RUN mkdir -p ${TMP_RESOURCE_PATH}

# Copy the logrotate configuration file
COPY CosmWebex-logrotate /etc/logrotate.d/cosmwebex
RUN chmod 0444 /etc/logrotate.d/cosmwebex

# Add a cron job to run logrotate at 2:00 AM every day
RUN echo "0 2 * * * /usr/sbin/logrotate /etc/logrotate.d/cosmwebex" > /etc/cron.d/logrotate

# Give execution rights on the cron job
RUN chmod 0444 /etc/cron.d/logrotate

# Apply cron job
RUN crontab /etc/cron.d/logrotate
 

# Install any needed packages specified in requirements.txt
# If you don't have any additional packages, you can skip this step
RUN pip install --no-cache-dir atlassian-python-api python-jenkins pyaml
RUN pip install --no-cache-dir "fastapi[standard]" webex-bot[proxy]

# Copy the system files
COPY run.sh ${APP_ROOT_PATH}

# Copy the current directory contents into the container at /app
COPY app       ${APP_COSM_PATH}
COPY host/resources ${TMP_RESOURCE_PATH}

# Make sure the script is executable
RUN chmod +x ${APP_ROOT_PATH}/run.sh

# Run app.py when the container launches
CMD ["/app/run.sh"]
