import logging
from pathlib import Path

def setup_logger(name=None):
    log_dir = Path(__file__).parent.parent / "reports"
    log_dir.mkdir(exist_ok=True)
    
    # Force console output
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "test.log"),
            logging.StreamHandler()
        ],
        force=True
    )
    return logging.getLogger(name)