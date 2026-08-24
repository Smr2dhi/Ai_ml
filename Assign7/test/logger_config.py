import logging


def get_loggger(name):
    logger=logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        file_handler= logging.FileHandler("registration.log")

        formatter=logging.Formatter(
            "%(asctime)s- %(name)s -%(levelname)s -%(message)s"

        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
