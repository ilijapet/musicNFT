LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # how to format the output
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        },
    },
    # how to handle log messages
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    # what do we want to log
    "loggers": {
        logger_name: {
            "level": "WARNING",
            "propagate": True,
        } for logger_name in (
            "django",
            "django.request",
            "django.db.backends",
            "django.template",
            "backend",
        )
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}
