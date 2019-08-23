#!python
import logging
import sys
import traceback

from PyQt5.QtWidgets import QApplication

from hdfinspect.display.view import HDFInspectMain


def initialise_logging(default_level=logging.DEBUG):
    global _log_formatter
    _log_formatter = logging.Formatter(
        "%(asctime)s [%(name)s:L%(lineno)d] %(levelname)s: %(message)s")

    # Add a very verbose logging level
    logging.addLevelName(5, 'TRACE')

    # Capture all warnings
    logging.captureWarnings(True)

    # Remove default handlers
    root_logger = logging.getLogger()
    root_logger.handlers = []

    # Stdout handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(_log_formatter)
    root_logger.addHandler(console_handler)

    # Default log level
    root_logger.setLevel(default_level)

    # Don't ever print all the debug logging from Qt
    logging.getLogger('PyQt5').setLevel(logging.INFO)


def main():
    initialise_logging(logging.DEBUG)

    log = logging.getLogger(__name__)
    sys.excepthook = lambda exc_type, exc_value, exc_traceback: log.error(
        "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

    app = QApplication(sys.argv)
    view = HDFInspectMain()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
