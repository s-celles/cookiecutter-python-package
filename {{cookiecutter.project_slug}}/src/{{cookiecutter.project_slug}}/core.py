"""Main module for {{ cookiecutter.project_name }}."""

from __future__ import annotations


def hello_world(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message.

    Example:
        >>> hello_world()
        'Hello, World!'
        >>> hello_world("Python")
        'Hello, Python!'
    """
    return f"Hello, {name}!"


def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b

    Example:
        >>> add_numbers(2, 3)
        5.0
        >>> add_numbers(1.5, 2.5)
        4.0
    """
    return a + b


class {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}:
    """Main class for {{ cookiecutter.project_name }}."""

    def __init__(self, name: str) -> None:
        """Initialize the class.

        Args:
            name: The name for this instance
        """
        self.name = name

    def greet(self) -> str:
        """Return a greeting from this instance.

        Returns:
            A personalized greeting
        """
        return hello_world(self.name)

    def __repr__(self) -> str:
        """Return string representation of the instance."""
        return f"{self.__class__.__name__}(name='{self.name}')"
