{%- if cookiecutter.use_pytest == "y" %}
"""Tests for {{ cookiecutter.project_slug }} core functionality."""

import pytest

from {{ cookiecutter.project_slug }}.core import (
    {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }},
    add_numbers,
    hello_world,
)


def test_hello_world_default():
    """Test hello_world with default parameter."""
    result = hello_world()
    assert result == "Hello, World!"


def test_hello_world_custom_name():
    """Test hello_world with custom name."""
    result = hello_world("Python")
    assert result == "Hello, Python!"


def test_add_numbers():
    """Test add_numbers function."""
    assert add_numbers(2, 3) == 5.0
    assert add_numbers(1.5, 2.5) == 4.0
    assert add_numbers(-1, 1) == 0.0


def test_main_class():
    """Test the main class."""
    instance = {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}("Test")
    assert instance.name == "Test"
    assert instance.greet() == "Hello, Test!"
    assert "Test" in repr(instance)


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
        ("", "Hello, !"),
        ("123", "Hello, 123!"),
    ],
)
def test_hello_world_parametrized(name, expected):
    """Test hello_world with various inputs."""
    assert hello_world(name) == expected


class TestMainClass:
    """Test class for the main class."""

    def test_initialization(self):
        """Test class initialization."""
        instance = {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}("TestName")
        assert instance.name == "TestName"

    def test_greet_method(self):
        """Test the greet method."""
        instance = {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}("Developer")
        result = instance.greet()
        assert result == "Hello, Developer!"

    def test_repr_method(self):
        """Test the __repr__ method."""
        instance = {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}("TestRepr")
        repr_str = repr(instance)
        assert "TestRepr" in repr_str
        assert instance.__class__.__name__ in repr_str
{%- else %}
"""Tests for {{ cookiecutter.project_slug }} core functionality."""

from {{ cookiecutter.project_slug }}.core import (
    add_numbers,
    hello_world,
    {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }},
)


def test_hello_world():
    """Test hello_world function."""
    assert hello_world() == "Hello, World!"
    assert hello_world("Python") == "Hello, Python!"


def test_add_numbers():
    """Test add_numbers function."""
    assert add_numbers(2, 3) == 5.0
    assert add_numbers(1.5, 2.5) == 4.0


def test_main_class():
    """Test the main class."""
    instance = {{ cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '') }}("Test")
    assert instance.name == "Test"
    assert instance.greet() == "Hello, Test!"


if __name__ == "__main__":
    test_hello_world()
    test_add_numbers()
    test_main_class()
    print("All tests passed!")
{%- endif %}
