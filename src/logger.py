import logging

log = logging.getLogger("builderProcess")
log.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('../logfile.log')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
log.addHandler(handler)


def getLogger():
    return log