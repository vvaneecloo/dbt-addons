import logging

RESET  = "\033[0m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"

class _ColorFormatter(logging.Formatter):
    def format(self, record):
        prefix = f"{YELLOW}[WARN]{RESET} " if record.levelno == logging.WARNING else ""
        record.msg = f"{prefix}{CYAN}{record.msg}{RESET}"
        return super().format(record)

_handler = logging.StreamHandler()
_handler.setFormatter(_ColorFormatter(fmt="%(asctime)s  %(message)s", datefmt="%H:%M:%S"))

log = logging.getLogger("dbta")
log.setLevel(logging.INFO)
log.addHandler(_handler)
log.propagate = False
