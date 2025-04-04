import logging
import os
import colorlog
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggerSingleton:
    _instance = None
    _initialized = False
    _base_dir = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_basic_logger()
        return cls._instance
    
    @classmethod
    def set_base_dir(cls, base_dir):
        """Configure a base directory for logs after initialization"""
        cls._base_dir = base_dir
        if cls._instance and not cls._initialized:
            cls._configure_file_handler()
            cls._initialized = True
    
    @classmethod
    def _create_basic_logger(cls):
        """Create a basic logger with console output only"""
        logger = colorlog.getLogger("app_logger")
        
        # Default to INFO level, can be changed later
        logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        logger.handlers = [] 
        
        # Add console handler
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(bold)s%(levelname)-8s%(reset)s "
            "%(blue)s%(message)s %(yellow)s(%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    @classmethod
    def _configure_file_handler(cls):
        """Add file handler to logger once base_dir is known"""
        if not cls._base_dir:
            return
            
        logger = cls.get_instance()
        
        # Create log directory
        log_dir = Path(cls._base_dir) / "log"
        log_dir.mkdir(exist_ok=True, parents=True)
        
        # Configure file handler
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-8s %(message)s (%(filename)s:%(lineno)d)",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"app_{current_date}.log")
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)


class Logger:
    @staticmethod
    def debug(message):
        LoggerSingleton.get_instance().debug(message)

    @staticmethod
    def info(message):
        LoggerSingleton.get_instance().info(message)

    @staticmethod
    def warning(message):
        LoggerSingleton.get_instance().warning(message)

    @staticmethod
    def error(message):
        LoggerSingleton.get_instance().error(message, exc_info=True)

    @staticmethod
    def critical(message):
        LoggerSingleton.get_instance().critical(message)

    @staticmethod
    def set_level(level):
        LoggerSingleton.get_instance().setLevel(level)
        
    @staticmethod
    def configure(base_dir=None, log_level=None):
        """Configure logger with base directory and log level"""
        if base_dir:
            LoggerSingleton.set_base_dir(base_dir)
        if log_level:
            LoggerSingleton.get_instance().setLevel(log_level)

    @staticmethod
    def get_logger():
        return LoggerSingleton.get_instance()