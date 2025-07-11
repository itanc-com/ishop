import logging
from enum import StrEnum

# ? use this file to create a logger for each service in your application for future debugging to separate logs


class ServiceName(StrEnum):
    EMAIL_SERVICE = "email_service"
    AUTH_SERVICE = "auth_service"
    API_ROUTERS = "api_routers"
    REDIS_SERVICE = "redis_service"
    # Add more services as needed


def get_logger(service: ServiceName) -> logging.Logger:
    logger = logging.getLogger(service.value)  # Creates a named logger
    return logger
