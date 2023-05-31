
from logging.config import dictConfig
import logging

dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        }
    },
    'handlers': {
        'myapp_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/logsContainer.log',
            'when': 'd',
            'interval': 1,
            'backupCount': 30,
            'level': 'DEBUG',
            "encoding": "utf8",
            'formatter': 'standard'
        },
    },
    'loggers': {
        'simple': {
            'level': 'DEBUG',
            'handlers': ['myapp_handler']
        }
    },
})

def initLogger():
    logger = logging.getLogger("simple")

    logger.info("Logger Started")