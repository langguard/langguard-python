"""Core functionality for LangGuard."""


def hello(name: str = "World") -> str:
    """
    Return a hello message.
    
    Args:
        name: The name to greet (default: "World")
    
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to LangGuard!"


class LangGuard:
    """Main LangGuard class for library usage."""
    
    def __init__(self, config: dict = None):
        """
        Initialize LangGuard instance.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
    
    def greet(self, name: str = "World") -> str:
        """
        Generate a greeting message.
        
        Args:
            name: The name to greet
            
        Returns:
            A greeting message
        """
        return hello(name)