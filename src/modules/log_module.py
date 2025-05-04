from rich.console import Console
from rich.theme import Theme

custom_theme: Theme = Theme({"success": "bold green", "error": "bold red"})
console: Console = Console(theme=custom_theme)

class Log(Console):
    """
    A class that extends the Console class to provide a more user-friendly logging system.
    """
    def __init__(self):
        super().__init__(theme=custom_theme)


    def log_success(self, message: str) -> None:
        console.log(f"[success]{message}[/success]")


    def log_error(self, message: str) -> None:
        console.log(f"[error]{message}[/error]")


    def log_info(self, message: str, args: str = "") -> None:
        if args:
            console.log(f"[bold white]{message}[/bold white] [underline]{args}[/underline]")
        else:
            console.log(f"[bold white]{message}[/bold white]")
