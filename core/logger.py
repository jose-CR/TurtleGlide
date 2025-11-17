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
    _MAGENTA = "\033[95m"
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
    
    # 📁 Función original mejorada
    @staticmethod
    def folder(message: str, color: str = None) -> None:
        chosen_color = color if color else Logger._MAGENTA
        print(f"{chosen_color}📁📂 {Logger._BOLD}Creando directorio: {message}{Logger._RESET}")


    # 📁➡️📂 Variante 3: Animación
    @staticmethod
    def carpet_anim(message: str, color: str = None) -> None:
        import time
        chosen_color = color if color else Logger._YELLOW
        frames = ["📁", "📁➡️", "📁➡️📂", "📂"]
        for frame in frames:
            print(f"{chosen_color}{frame} {Logger._BOLD}{message}{Logger._RESET}", end="\r")
            time.sleep(0.15)
        print()
