# Usage Examples

This guide provides real-world examples of creating different types of Python packages using this template.

## Basic Library Package

Let's create a simple math utilities library:

```bash
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
```

**Configuration:**
```
full_name [Your Name]: Jane Smith
email [your.email@example.com]: jane.smith@example.com
github_username [yourusername]: janesmith
project_name [My Python Package]: Math Utilities
project_slug [math_utilities]:
project_short_description [A modern Python package with best practices built-in.]: A collection of mathematical utility functions
version [0.1.0]:
python_requires [>=3.9]:
license [MIT]:
build_backend [setuptools]:
use_ruff [y]:
use_mypy [y]:
use_pytest [y]:
use_coverage [y]:
use_pre_commit [y]:
use_bandit [n]:
use_safety [n]:
use_github_actions [y]:
command_line_interface [none]:
use_mkdocs [y]:
```

**Generated structure:**
```
math_utilities/
├── src/
│   └── math_utilities/
│       ├── __init__.py
│       ├── core.py
│       └── py.typed
├── tests/
│   ├── test_core.py
│   └── test_math_utilities.py
├── docs/
├── pyproject.toml
├── README.md
└── .github/workflows/ci.yml
```

**Example implementation (src/math_utilities/core.py):**
```python
"""Core mathematical utilities."""

from typing import List, Union

Number = Union[int, float]


def factorial(n: int) -> int:
    """Calculate the factorial of a number.

    Args:
        n: A non-negative integer

    Returns:
        The factorial of n

    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")

    if n <= 1:
        return 1
    return n * factorial(n - 1)


def mean(numbers: List[Number]) -> float:
    """Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: List of numbers

    Returns:
        The arithmetic mean

    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")

    return sum(numbers) / len(numbers)


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: Integer to check

    Returns:
        True if n is prime, False otherwise
    """
    if not isinstance(n, int):
        return False
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
```

## CLI Application

Creating a file processing tool with a command-line interface:

```bash
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git
```

**Configuration:**
```
project_name: File Processor
project_slug: file_processor
project_short_description: A command-line tool for processing text files
command_line_interface: typer
use_ruff: y
use_mypy: y
use_pytest: y
use_coverage: y
use_pre_commit: y
use_bandit: y
use_safety: y
```

**Example CLI implementation (src/file_processor/cli.py):**
```python
"""Command-line interface for file processor."""

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress

from .core import FileProcessor

app = typer.Typer(help="Process text files with various operations")
console = Console()


@app.command()
def count_words(
    file_path: Path = typer.Argument(..., help="Path to the text file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
) -> None:
    """Count words in a text file."""
    if not file_path.exists():
        console.print(f"[red]Error: File {file_path} does not exist[/red]")
        raise typer.Exit(1)

    try:
        processor = FileProcessor(file_path)
        word_count = processor.count_words()

        result = f"Word count: {word_count}"

        if output:
            output.write_text(result)
            console.print(f"[green]Results saved to {output}[/green]")
        else:
            console.print(result)

        if verbose:
            console.print(f"[blue]Processed file: {file_path}[/blue]")

    except Exception as e:
        console.print(f"[red]Error processing file: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def find_duplicates(
    directory: Path = typer.Argument(..., help="Directory to search"),
    pattern: str = typer.Option("*.txt", "--pattern", "-p", help="File pattern to match"),
    output_format: str = typer.Option("table", "--format", "-f", help="Output format (table, json, csv)")
) -> None:
    """Find duplicate lines across multiple files."""
    if not directory.is_dir():
        console.print(f"[red]Error: {directory} is not a directory[/red]")
        raise typer.Exit(1)

    files = list(directory.glob(pattern))
    if not files:
        console.print(f"[yellow]No files found matching pattern {pattern}[/yellow]")
        return

    with Progress() as progress:
        task = progress.add_task("Processing files...", total=len(files))

        processor = FileProcessor()
        duplicates = processor.find_duplicates(files)

        progress.update(task, completed=len(files))

    if output_format == "json":
        import json
        console.print(json.dumps(duplicates, indent=2))
    elif output_format == "csv":
        # CSV output implementation
        pass
    else:
        # Table output (default)
        from rich.table import Table
        table = Table(title="Duplicate Lines")
        table.add_column("Line")
        table.add_column("Files")

        for line, file_list in duplicates.items():
            table.add_row(line, ", ".join(file_list))

        console.print(table)


if __name__ == "__main__":
    app()
```

## Data Science Package

Creating a package for data analysis with Jupyter notebook support:

**Configuration:**
```
project_name: Data Analysis Toolkit
project_slug: data_analysis_toolkit
project_short_description: Tools for data analysis and visualization
use_jupyter: y
use_pandas: y
use_numpy: y
use_matplotlib: y
```

**Example core module (src/data_analysis_toolkit/core.py):**
```python
"""Core data analysis functions."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
from pathlib import Path


class DataAnalyzer:
    """Main class for data analysis operations."""

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """Initialize with optional data."""
        self.data = data

    def load_csv(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Load data from CSV file.

        Args:
            file_path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv

        Returns:
            Loaded DataFrame
        """
        self.data = pd.read_csv(file_path, **kwargs)
        return self.data

    def basic_stats(self) -> Dict[str, Any]:
        """Generate basic statistics for the dataset.

        Returns:
            Dictionary containing basic statistics
        """
        if self.data is None:
            raise ValueError("No data loaded")

        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum(),
            'numeric_summary': self.data.describe().to_dict()
        }

    def plot_missing_values(self, figsize: tuple = (12, 6)) -> plt.Figure:
        """Create visualization of missing values.

        Args:
            figsize: Figure size for the plot

        Returns:
            Matplotlib figure object
        """
        if self.data is None:
            raise ValueError("No data loaded")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Missing values by column
        missing_counts = self.data.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=False)

        if len(missing_counts) > 0:
            missing_counts.plot(kind='bar', ax=ax1)
            ax1.set_title('Missing Values by Column')
            ax1.set_ylabel('Count')

            # Missing values heatmap
            missing_matrix = self.data.isnull()
            ax2.imshow(missing_matrix, cmap='viridis', aspect='auto')
            ax2.set_title('Missing Values Pattern')
            ax2.set_xlabel('Columns')
            ax2.set_ylabel('Rows')
        else:
            ax1.text(0.5, 0.5, 'No missing values', ha='center', va='center')
            ax2.text(0.5, 0.5, 'No missing values', ha='center', va='center')

        plt.tight_layout()
        return fig

    def correlation_analysis(self, method: str = 'pearson') -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns.

        Args:
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            Correlation matrix
        """
        if self.data is None:
            raise ValueError("No data loaded")

        numeric_data = self.data.select_dtypes(include=[np.number])
        return numeric_data.corr(method=method)
```

## Web API Package

Creating a FastAPI-based web service:

**Configuration:**
```
project_name: Task API
project_slug: task_api
project_short_description: RESTful API for task management
use_fastapi: y
use_sqlalchemy: y
use_alembic: y
use_pydantic: y
```

**Example API implementation (src/task_api/api.py):**
```python
"""FastAPI application for task management."""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .models import Task
from .schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(
    title="Task API",
    description="A simple task management API",
    version="0.1.0"
)


@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=List[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all tasks."""
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
```

## Machine Learning Package

Creating a scikit-learn compatible estimator:

**Configuration:**
```
project_name: ML Estimators
project_slug: ml_estimators
project_short_description: Custom machine learning estimators
use_sklearn: y
use_numpy: y
use_pandas: y
use_jupyter: y
```

**Example estimator (src/ml_estimators/estimators.py):**
```python
"""Custom machine learning estimators."""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from typing import Optional


class SimpleScaler(BaseEstimator, TransformerMixin):
    """A simple feature scaler that normalizes features to [0, 1] range."""

    def __init__(self):
        """Initialize the scaler."""
        self.min_: Optional[np.ndarray] = None
        self.scale_: Optional[np.ndarray] = None

    def fit(self, X, y=None):
        """Fit the scaler to the data.

        Args:
            X: Training data
            y: Ignored (for compatibility)

        Returns:
            self
        """
        X = check_array(X)

        self.min_ = np.min(X, axis=0)
        self.scale_ = np.max(X, axis=0) - self.min_

        # Handle case where max == min (constant features)
        self.scale_[self.scale_ == 0] = 1

        return self

    def transform(self, X):
        """Transform the data.

        Args:
            X: Data to transform

        Returns:
            Transformed data
        """
        check_is_fitted(self, ['min_', 'scale_'])
        X = check_array(X)

        return (X - self.min_) / self.scale_

    def inverse_transform(self, X):
        """Inverse transform the data.

        Args:
            X: Transformed data

        Returns:
            Original scale data
        """
        check_is_fitted(self, ['min_', 'scale_'])
        X = check_array(X)

        return X * self.scale_ + self.min_


class KNearestCentroid(BaseEstimator, ClassifierMixin):
    """K-Nearest Centroid classifier."""

    def __init__(self, n_neighbors: int = 3):
        """Initialize the classifier.

        Args:
            n_neighbors: Number of neighbors to consider
        """
        self.n_neighbors = n_neighbors

    def fit(self, X, y):
        """Fit the classifier.

        Args:
            X: Training features
            y: Training labels

        Returns:
            self
        """
        X, y = check_X_y(X, y)

        self.classes_ = np.unique(y)
        self.centroids_ = np.array([
            np.mean(X[y == class_label], axis=0)
            for class_label in self.classes_
        ])

        return self

    def predict(self, X):
        """Predict class labels.

        Args:
            X: Features to predict

        Returns:
            Predicted labels
        """
        check_is_fitted(self, ['classes_', 'centroids_'])
        X = check_array(X)

        # Calculate distances to all centroids
        distances = np.sqrt(((X[:, np.newaxis, :] - self.centroids_[np.newaxis, :, :]) ** 2).sum(axis=2))

        # Find nearest centroids
        nearest_indices = np.argmin(distances, axis=1)

        return self.classes_[nearest_indices]

    def predict_proba(self, X):
        """Predict class probabilities.

        Args:
            X: Features to predict

        Returns:
            Class probabilities
        """
        check_is_fitted(self, ['classes_', 'centroids_'])
        X = check_array(X)

        # Calculate distances to all centroids
        distances = np.sqrt(((X[:, np.newaxis, :] - self.centroids_[np.newaxis, :, :]) ** 2).sum(axis=2))

        # Convert distances to probabilities (inverse distance weighting)
        probabilities = 1 / (distances + 1e-8)  # Add small epsilon to avoid division by zero
        probabilities = probabilities / probabilities.sum(axis=1, keepdims=True)

        return probabilities
```

## Testing Examples

Each package type should include comprehensive tests:

**Test for library package (tests/test_core.py):**
```python
"""Tests for core math utilities."""

import pytest
from math_utilities.core import factorial, mean, is_prime


class TestFactorial:
    """Tests for factorial function."""

    def test_factorial_base_cases(self):
        """Test factorial base cases."""
        assert factorial(0) == 1
        assert factorial(1) == 1

    def test_factorial_positive_integers(self):
        """Test factorial with positive integers."""
        assert factorial(5) == 120
        assert factorial(10) == 3628800

    def test_factorial_negative_input(self):
        """Test factorial with negative input."""
        with pytest.raises(ValueError, match="non-negative"):
            factorial(-1)

    def test_factorial_non_integer_input(self):
        """Test factorial with non-integer input."""
        with pytest.raises(TypeError, match="integer"):
            factorial(3.14)


class TestMean:
    """Tests for mean function."""

    def test_mean_integers(self):
        """Test mean with integers."""
        assert mean([1, 2, 3, 4, 5]) == 3.0

    def test_mean_floats(self):
        """Test mean with floats."""
        assert mean([1.5, 2.5, 3.5]) == 2.5

    def test_mean_empty_list(self):
        """Test mean with empty list."""
        with pytest.raises(ValueError, match="empty list"):
            mean([])


@pytest.mark.parametrize("number,expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (25, False),
    (1, False),
    (0, False),
    (-1, False),
])
def test_is_prime(number, expected):
    """Test is_prime function with various inputs."""
    assert is_prime(number) == expected
```

These examples demonstrate how to create different types of Python packages using this template, from simple libraries to complex applications with web APIs and machine learning components.
