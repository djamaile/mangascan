import logging
import colorlog


def init_logger(module_name) -> logging.Logger:
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s %(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )

    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
