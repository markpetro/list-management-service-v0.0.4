import logging
import os
from logging.handlers import TimedRotatingFileHandler

class LoggingService:
    def __init__(self, log_file_name="app.log", log_level=logging.INFO):
        self.logger = logging.getLogger("list_management_service")
        self.logger.setLevel(log_level)

        # Define format for logs
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # File handler (logs rotate daily)
        if log_file_name:
            log_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_file_path = os.path.join(log_dir, log_file_name)
            file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1)
            file_handler.setFormatter(log_format)
            file_handler.suffix = "%Y%m%d"  # Filename suffix for rotating logs
            self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_exception(self, message):
        self.logger.exception(message)

# Initialize a global logger instance to use across the app
logger = LoggingService()