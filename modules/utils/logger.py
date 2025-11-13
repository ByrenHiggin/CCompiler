#!/usr/bin/env python3
# type: ignore
"""
Global logger configuration for the C Compiler project.
Provides a centralized logging setup that can be imported and used throughout the project.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Global logger instance
_logger: Optional[logging.Logger] = None

def setup_logger(
    name: str = "CCompiler",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up and configure the global logger.
    
    Args:
        name: Logger name (default: "CCompiler")
        level: Logging level (default: INFO)
        log_file: Optional log file path
        format_string: Custom format string
    
    Returns:
        Configured logger instance
    """
    global _logger
    
    if _logger is not None:
        # Update level on existing logger
        _logger.setLevel(level)
        for handler in _logger.handlers:
            handler.setLevel(level)
        return _logger
    
    # Create logger
    _logger = logging.getLogger(name)
    _logger.setLevel(level)
    
    # Prevent duplicate handlers if logger already exists
    if _logger.handlers:
        return _logger
    
    # Default format
    if format_string is None:
        format_string = '[%(asctime)s] %(levelname)-8s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
    
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)
    
    return _logger

def get_logger() -> logging.Logger:
    """
    Get the global logger instance.
    If not initialized, creates a default logger.
    
    Returns:
        Logger instance
    """
    global _logger
    
    if _logger is None:
        _logger = setup_logger()
    
    return _logger

def set_log_level(level: int):
    """
    Set the logging level for all handlers.
    
    Args:
        level: New logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logger = get_logger()
    logger.setLevel(level)
    
    for handler in logger.handlers:
        handler.setLevel(level)

# Convenience functions for common log levels
def debug(message: str, *args, **kwargs):
    """Log a debug message"""
    get_logger().debug(message, *args, **kwargs)

def info(message: str, *args, **kwargs):
    """Log an info message"""
    get_logger().info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    """Log a warning message"""
    get_logger().warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    """Log an error message"""
    get_logger().error(message, *args, **kwargs)

def critical(message: str, *args, **kwargs):
    """Log a critical message"""
    get_logger().critical(message, *args, **kwargs) 

# Initialize with default settings when module is imported
if _logger is None:
    setup_logger()