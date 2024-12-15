 # Use the official lightweight Python image
FROM python:3.8-slim


# Set the working directory
WORKDIR /app

# Download latest listing of available packages:
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade
# Install a new package:
RUN apt-get -y install syslog-ng vim net-tools 

# Define environment variable

ENV APP_ROOT_PATH="/app"
ENV APP_ROOT_HOST="${APP_ROOT_PATH}/host"
ENV APP_COSM_PATH="${APP_ROOT_PATH}/CosmBot"
ENV APPLOGS="${APP_ROOT_HOST}/logs"
ENV RESOURCE_PATH="${APP_ROOT_HOST}/resources"

# Create a new directory under /app
RUN mkdir -p ${APP_COSM_PATH}
RUN mkdir -p ${RESOURCE_PATH}
RUN mkdir -p ${APPLOGS}

# Make port 80 available to the world outside this container
EXPOSE 80

# Install any needed packages specified in requirements.txt
# If you don't have any additional packages, you can skip this step
RUN pip install --no-cache-dir atlassian-python-api python-jenkins pyaml Flask
RUN pip install --no-cache-dir "fastapi[standard]" webex-bot[proxy]

# Copy the system files
COPY .enviroment ${APP_ROOT_PATH}
COPY run.sh ${APP_ROOT_PATH}

# Copy the current directory contents into the container at /app
COPY app       ${APP_COSM_PATH}
COPY resources ${RESOURCE_PATH}

# Make sure the script is executable
RUN chmod +x ${APP_ROOT_PATH}/run.sh

# Run app.py when the container launches
CMD ["/app/run.sh"]
