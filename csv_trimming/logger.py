import sys
import logging

# Create the logger
logger = logging.getLogger(__name__)
# Change the levels names to that they are 4 chars long
logging.addLevelName(logging.DEBUG, 'DEBG')
logging.addLevelName(logging.WARNING, 'WARN')
logging.addLevelName(logging.ERROR, 'ERRO')
logging.addLevelName(logging.CRITICAL, 'CRIT')
# Set the default log level
logger.setLevel(logging.INFO)
# Set the format of the loger
formatter = logging.Formatter("[%(levelname)s] %(asctime)-15s : %(message)s")

# Setup a stdout logger
shandler = logging.StreamHandler(sys.stdout)
shandler.setLevel(logging.INFO)
shandler.setFormatter(formatter)
logger.addHandler(shandler)
