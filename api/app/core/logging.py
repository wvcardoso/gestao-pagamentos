import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

# Apenas este módulo em DEBUG
logging.getLogger("app.core.utils").setLevel(logging.DEBUG)
logging.getLogger("app.services.processador").setLevel(logging.DEBUG)
logging.getLogger("app.services.parser.orchestrator").setLevel(logging.DEBUG)
logging.getLogger("app.services.parser.neoenergia").setLevel(logging.INFO)
