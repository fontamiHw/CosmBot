 # Use the official lightweight Python image
FROM python:3.8-slim


# Set the working directory
WORKDIR /app

# Create a new directory under /app
RUN mkdir -p /app/resources
RUN mkdir -p /app/CosmBot

# Copy the system files
COPY .enviroment /app
COPY run.sh /app

# Copy the current directory contents into the container at /app
COPY app       /app/CosmBot
COPY resources /app/resources

# Install any needed packages specified in requirements.txt
# If you don't have any additional packages, you can skip this step
RUN pip install --no-cache-dir atlassian-python-api python-jenkins pyaml Flask
RUN pip install --no-cache-dir webex-bot[proxy]


# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Make sure the script is executable
RUN chmod +x /app/run.sh

# Run app.py when the container launches
CMD ["/app/run.sh"]
