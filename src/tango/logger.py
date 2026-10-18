RESET = "\033[0m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def header(title: str):
    print()
    print(f"{CYAN}{'=' * 50}{RESET}")
    print(f"{BOLD}{title}{RESET}")
    print(f"{CYAN}{'=' * 50}{RESET}")


def info(message: str):
    print(f"{BLUE}ℹ{RESET}  {message}")


def success(message: str):
    print(f"{GREEN}✓{RESET}  {message}")


def warning(message: str):
    print(f"{YELLOW}⚠{RESET}  {message}")


def error(message: str):
    print(f"{RED}✗{RESET}  {message}")
