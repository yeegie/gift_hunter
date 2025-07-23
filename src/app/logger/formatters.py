import logging


def get_default_formatter() -> logging.Formatter:
    return logging.Formatter(
        fmt="[{asctime}] [{levelname:<8}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    )
