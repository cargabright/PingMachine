import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def get_console_logger_from_config(config: dict) -> logging.StreamHandler:
	console_handler = logging.StreamHandler()
	console_handler.setLevel(config.get("level").upper())
	console_handler.setFormatter(logging.Formatter(config.get("format")))
	return console_handler


def get_file_logger_from_config(config: dict, logpath: str) -> logging.StreamHandler:
	file_handler = logging.FileHandler(filename=logpath, mode="a")
	file_handler.setLevel(config.get("level").upper())
	file_handler.setFormatter(logging.Formatter(config.get("format")))
	return file_handler


def get_rotating_file_logger_from_config(config: dict, logpath: str) -> TimedRotatingFileHandler:
	file_handler = TimedRotatingFileHandler(filename=logpath, when=config.get("when"), interval=config.get("interval"),
											backupCount=config.get("backupCount"))
	file_handler.setLevel(config.get("level").upper())
	file_handler.setFormatter(logging.Formatter(config.get("format")))
	return file_handler


def get_plugin_logger_from_config(config: dict, logpath: str) -> logging.StreamHandler:
	file_handler = logging.FileHandler(filename=logpath, mode="w")
	file_handler.setLevel(config.get("level").upper())
	file_handler.setFormatter(logging.Formatter(config.get("format")))
	return file_handler


def initialize_logger(logger, config):
	# Check that the app_log_path exists. If not then create
	if not os.path.exists(Path(config.get("app_log_path"))):
		os.mkdir(config.get("app_log_path"))

	# Create Stream logger
	stream_log_handler = get_console_logger_from_config(config.get("loggers").get("console"))
	logger.addHandler(stream_log_handler)

	# Create App logger
	app_logpath = f'{config.get("app_log_path")}/{config.get("app_log_filename")}'
	rotating_file_log_handler = get_rotating_file_logger_from_config(config=config.get("loggers").get("rotating_file"),
																	 logpath=app_logpath)
	logger.addHandler(rotating_file_log_handler)
