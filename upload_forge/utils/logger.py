import logging
from rich.logging import RichHandler
from rich.console import Console

# Setup Rich Console
console = Console()

def setup_logger(name: str = "upload-forge", level: int = logging.INFO):
    """
    Configures and returns a logger with RichHandler.
    """
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

# Global logger instance
logger = setup_logger()
