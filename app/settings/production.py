# flake8: noqa
from .base import *

STATIC_ROOT = os.environ.get("STATIC_ROOT", "/var/www/static")
STATICFILES_DIRS = [BASE_DIR.parent.joinpath("static")]


LOG_DIR = BASE_DIR.parent.joinpath("log")

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s",
            },
            "verbose": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            },
            "simple": {
                "format": "%(asctime)s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "celery": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("celery.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "django": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("django.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "block": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("block.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "crm": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("crm.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "dashboard": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("dashboard.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "protocol": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("protocol.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "rate": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("rate.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "transaction": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("transaction.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "wallet": {
                "level": LOGLEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_DIR.joinpath("wallet.log"),
                "maxBytes": 1024 * 1024 * 100,  # 100MB
                "backupCount": 10,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "app": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "django",
                ],
            },
            "celery": {
                "level": "DEBUG",
                "propagate": True,
                "handlers": [
                    "console",
                    "celery",
                ],
            },
            "django": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "django",
                ],
            },
            "app": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "django",
                ],
            },
            "block": {
                "level": "DEBUG",
                "propagate": True,
                "handlers": [
                    "console",
                    "block",
                ],
            },
            "crm": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "crm",
                ],
            },
            "dashboard": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "dashboard",
                ],
            },
            "protocol": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "protocol",
                ],
            },
            "rate": {
                "level": LOGLEVEL,
                "propagate": True,
                "handlers": [
                    "console",
                    "rate",
                ],
            },
            "transaction": {
                "level": "DEBUG",
                "propagate": True,
                "handlers": [
                    "console",
                    "transaction",
                ],
            },
            "wallet": {
                "level": "DEBUG",
                "propagate": True,
                "handlers": [
                    "console",
                    "wallet",
                ],
            },
        },
    }
)
