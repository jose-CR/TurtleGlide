# =================================================
#   Base de LOGGER - centraliza mensajes con emojis
# ===================================================
class Logger:
    """Clase auxiliar para mostrar mensajes con formato consistente."""

    # 🎨 Colores básicos (ANSI)
    _GREEN = "\033[92m"
    _BLUE = "\033[94m"
    _YELLOW = "\033[93m"
    _RED = "\033[91m"
    _CYAN = "\033[96m"
    _RESET = "\033[0m"
    _BOLD = "\033[1m"

    @staticmethod
    def success(message: str) -> None:
        print(f"{Logger._GREEN}✅ {Logger._BOLD}{message}{Logger._RESET}")
    
    @staticmethod
    def info(message: str) -> None:
        print(f"{Logger._BLUE}ℹ️ {message}{Logger._RESET}")
    
    @staticmethod
    def beginning(message: str, symbol: str = "─") -> None:
        """🚀 Inicio de un bloque o proceso"""
        line = symbol * (len(message) + 10)
        print(f"\n{Logger._CYAN}{Logger._BOLD}🚀 {message}{Logger._RESET}")
        print(f"{Logger._CYAN}{line}{Logger._RESET}")
    
    @staticmethod
    def ending(message: str = "Proceso finalizado", symbol: str = "─") -> None:
        """🏁 Fin de un bloque o proceso"""
        line = symbol * (len(message) + 10)
        print(f"{Logger._CYAN}{line}{Logger._RESET}")
        print(f"{Logger._CYAN}{Logger._BOLD}🏁 {message}{Logger._RESET}\n")

    @staticmethod
    def warning(message: str) -> None:
        print(f"{Logger._YELLOW}⚠️ {message}{Logger._RESET}")

    @staticmethod
    def error(message: str) -> None:
       print(f"{Logger._RED}❌ {Logger._BOLD}{message}{Logger._RESET}")
