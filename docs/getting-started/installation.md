# Installation

This guide covers different ways to install and use the Cookiecutter Python Package template.

## Prerequisites

Before using this template, ensure you have the following installed:

### Python Requirements
- **Python 3.9 or higher** (3.11+ recommended for best performance)
- **pip** (Python package installer)

Check your Python version:
```bash
python --version
# or
python3 --version
```

### Git (Required)
Git is required for cloning repositories and version control:

#### Windows
Download from [git-scm.com](https://git-scm.com/download/win) or use:
```powershell
winget install Git.Git
```

#### macOS
```bash
# Using Homebrew
brew install git

# Using Xcode Command Line Tools
xcode-select --install
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

## Installing Cookiecutter

### Method 1: Using pip (Recommended)
```bash
pip install cookiecutter
```

### Method 2: Using pipx (Isolated Installation)
```bash
# Install pipx if not already installed
pip install pipx

# Install cookiecutter with pipx
pipx install cookiecutter
```

### Method 3: Using uv (Fastest)
```bash
# Install uv
pip install uv

# Install cookiecutter with uv
uv tool install cookiecutter
```

### Method 4: Using conda
```bash
conda install -c conda-forge cookiecutter
```

## Verify Installation

Check that cookiecutter is installed correctly:
```bash
cookiecutter --version
```

You should see output similar to:
```
Cookiecutter 2.5.0 from /path/to/cookiecutter (Python 3.11)
```

## Platform-Specific Notes

### Windows
If you encounter issues with long path names, enable long path support:
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### macOS
If you have issues with the default Python, consider using:
```bash
# Install Python via Homebrew
brew install python@3.11

# Use the Homebrew Python
/opt/homebrew/bin/python3.11 -m pip install cookiecutter
```

### Linux
Make sure you have the development tools installed:
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# CentOS/RHEL/Fedora
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

## Network and Firewall Considerations

### Corporate Networks
If you're behind a corporate firewall, you may need to configure proxy settings:

```bash
# Set proxy for pip
pip install --proxy http://proxy.company.com:8080 cookiecutter

# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### SSH vs HTTPS
The template can be accessed via HTTPS (default) or SSH:

```bash
# HTTPS (works everywhere)
cookiecutter https://github.com/s-celles/cookiecutter-python-package.git

# SSH (requires SSH key setup)
cookiecutter git@github.com:s-celles/cookiecutter-python-package.git
```

## Alternative Installation Methods

### Direct Download
If you can't use git, download the template directly:

1. Visit the [GitHub repository](https://github.com/s-celles/cookiecutter-python-package)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Use the local path:

```bash
cookiecutter /path/to/extracted/cookiecutter-python-package
```

### Docker (Experimental)
For completely isolated usage:

```bash
# Build the image
docker build -t cookiecutter-python-package .

# Run the template
docker run -it -v $(pwd):/output cookiecutter-python-package
```

## Troubleshooting Installation

### Common Issues

#### "cookiecutter: command not found"
**Solution**: Ensure the Python Scripts directory is in your PATH:

**Windows**:
```powershell
# Add to PATH (replace with your Python path)
$env:PATH += ";C:\Users\YourUser\AppData\Local\Programs\Python\Python311\Scripts"
```

**macOS/Linux**:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

#### Permission Errors
**Windows**: Run command prompt as Administrator
**macOS/Linux**: Use `sudo` or install in user directory:
```bash
pip install --user cookiecutter
```

#### SSL Certificate Errors
```bash
# Upgrade certificates
pip install --upgrade certifi

# Or bypass SSL (not recommended for production)
pip install --trusted-host pypi.org --trusted-host pypi.python.org cookiecutter
```

#### ImportError or Module Not Found
Ensure you're using the correct Python environment:
```bash
# Check which Python pip is using
pip --version

# Use specific Python version
python3.11 -m pip install cookiecutter
```

### Getting Help

If you encounter issues:

1. **Check the logs**: Use `cookiecutter --verbose` for detailed output
2. **Update cookiecutter**: `pip install --upgrade cookiecutter`
3. **Check GitHub Issues**: [Template Issues](https://github.com/s-celles/cookiecutter-python-package/issues)
4. **Community Support**: Python Discord, Reddit r/Python

## Next Steps

Once cookiecutter is installed, you're ready to:

1. [Create your first package](quick-start.md)
2. [Explore configuration options](../configuration/template-options.md)
3. [Learn about the tools](../tools/overview.md)

## Development Installation

If you want to contribute to the template itself:

```bash
# Clone the repository
git clone https://github.com/s-celles/cookiecutter-python-package.git
cd cookiecutter-python-package

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Test the template locally
cookiecutter .
```

This ensures you have a working cookiecutter installation and can successfully create Python packages using this template.
