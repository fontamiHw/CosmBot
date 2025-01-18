 # Use the official lightweight Python image
FROM cosm-pythontool-base:latest
 

# Install any needed packages specified in requirements.txt
# If you don't have any additional packages, you can skip this step
RUN pip install --no-cache-dir --force-reinstall -v atlassian-python-api==3.41.16 python-jenkins==1.8.2 schedule==1.2.2
RUN pip install --no-cache-dir --force-reinstall -v webex-bot[proxy]==0.5.2 webexteamssdk==1.6.1


ENV APP_COSM_PATH="${APP_ROOT_PATH}/CosmBot"
ENV PYTHONPATH="${APP_COSM_PATH}"


# Copy the logrotate configuration file
COPY CosmWebex-logrotate /etc/logrotate.d/cosmwebex
RUN chmod 0444 /etc/logrotate.d/cosmwebex

# Add a cron job to run logrotate at 2:00 AM every day
RUN echo "0 2 * * * /usr/sbin/logrotate /etc/logrotate.d/cosmwebex" > /etc/cron.d/logrotate

# Give execution rights on the cron job
RUN chmod 0444 /etc/cron.d/logrotate

# Apply cron job
RUN crontab /etc/cron.d/logrotate

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf 

# Copy the system files. Make sure the script is executable
COPY run.sh ${APP_ROOT_PATH}
COPY app-run.sh ${APP_ROOT_PATH}
RUN chmod +x ${APP_ROOT_PATH}/run.sh
RUN chmod +x ${APP_ROOT_PATH}/app-run.sh

# Copy the current directory contents into the container at /app
COPY app       ${APP_COSM_PATH}
COPY host/resources ${TMP_RESOURCE_PATH} 

# Start supervisor from the script
CMD ["/app/run.sh"]
