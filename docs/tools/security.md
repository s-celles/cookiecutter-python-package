# Security Tools

Security tools help identify vulnerabilities, scan dependencies, and ensure your code follows security best practices.

## 🔒 Bandit

**What it is**: Security linter for Python

**Why important**:
- Finds common security vulnerabilities
- Catches hardcoded passwords, SQL injection risks
- Industry compliance requirements
- Proactive security approach

### What Bandit Detects

#### Hardcoded Secrets
```python
# ❌ Bad - Hardcoded password (B105)
password = "my_secret_password"

# ✅ Good - Environment variable
import os
password = os.getenv("PASSWORD")
```

#### SQL Injection Risks
```python
# ❌ Bad - SQL injection risk (B608)
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Good - Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

#### Insecure Random
```python
# ❌ Bad - Insecure random (B311)
import random
token = random.randint(1000, 9999)

# ✅ Good - Cryptographically secure
import secrets
token = secrets.randbelow(10000)
```

#### Shell Injection
```python
# ❌ Bad - Shell injection risk (B602)
import os
os.system(f"rm {filename}")

# ✅ Good - Safe subprocess
import subprocess
subprocess.run(["rm", filename], check=True)
```

#### Unsafe YAML Loading
```python
# ❌ Bad - Arbitrary code execution (B506)
import yaml
data = yaml.load(user_input)

# ✅ Good - Safe loading
import yaml
data = yaml.safe_load(user_input)
```

### Configuration (pyproject.toml)
```toml
[tool.bandit]
exclude_dirs = ["tests", "build", "dist"]
skips = ["B101", "B601"]

[tool.bandit.assert_used]
skips = ["*_test.py", "*test_*.py"]
```

### Configuration (.bandit)
```ini
[bandit]
exclude: /tests
skips: B101,B601

[bandit.assert_used]
skips: *_test.py,*test_*.py
```

### Usage
```bash
# Scan all Python files
bandit -r src/

# Generate report
bandit -r src/ -f json -o security_report.json

# Exclude specific tests
bandit -r src/ -x B101,B601

# Confidence levels
bandit -r src/ -i  # Show only medium/high confidence
bandit -r src/ -l  # Show only medium/high severity
```

### Common Bandit Rules

| Rule | Description | Example |
|------|-------------|---------|
| B101 | Assert used | `assert condition` |
| B102 | Exec used | `exec(user_input)` |
| B103 | Set bad file permissions | `os.chmod(file, 0o777)` |
| B104 | Hardcoded bind all interfaces | `host="0.0.0.0"` |
| B105 | Hardcoded password string | `password = "secret"` |
| B106 | Hardcoded password funcarg | `login("user", "pass")` |
| B107 | Hardcoded password default | `def func(pass="secret")` |
| B108 | Hardcoded tmp directory | `tmp_dir = "/tmp"` |
| B110 | Try except pass | `except: pass` |
| B112 | Try except continue | `except: continue` |

## 🛡️ Safety

**What it is**: Checks dependencies for known vulnerabilities

**Why important**:
- Dependencies often have security flaws
- Automated vulnerability scanning
- Alerts for critical security updates
- Supply chain security

### Installation and Usage
```bash
# Install safety
pip install safety

# Check installed packages
safety check

# Check requirements file
safety check -r requirements.txt

# JSON output
safety check --json

# Only show critical vulnerabilities
safety check --severity critical
```

### Configuration (.safety-policy.json)
```json
{
    "security": {
        "ignore-cvs": [],
        "ignore-severity-rules": {
            "ignore-cvss-severity-below": 7.0,
            "ignore-cvss-unknown-severity": false
        },
        "continue-on-vulnerability-error": false
    },
    "alert": {
        "ignore-cvs": [],
        "ignore-severity-rules": {
            "ignore-cvss-severity-below": 0.0,
            "ignore-cvss-unknown-severity": false
        },
        "continue-on-vulnerability-error": true
    },
    "filename": {
        "ignore-cvs": [],
        "ignore-severity-rules": {
            "ignore-cvss-severity-below": 0.0,
            "ignore-cvss-unknown-severity": false
        },
        "continue-on-vulnerability-error": true
    }
}
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Safety Check
  run: |
    pip install safety
    safety check --json --output safety-report.json
  continue-on-error: true
```

### Example Vulnerability Report
```json
{
    "report_meta": {
        "scan_target": "environment",
        "timestamp": "2023-10-01T12:00:00Z"
    },
    "vulnerabilities": [
        {
            "vulnerability_id": "12345",
            "package_name": "requests",
            "installed_version": "2.25.1",
            "affected_versions": "<2.26.0",
            "analyzed_version": "2.25.1",
            "advisory": "Requests library has a security vulnerability...",
            "cve": "CVE-2023-12345",
            "id": "12345",
            "more_info_url": "https://pyup.io/v/12345"
        }
    ]
}
```

## 🚨 Dependency Confusion Protection

### Dependency Pinning
```toml
# pyproject.toml - Pin dependencies
[project]
dependencies = [
    "requests==2.31.0",  # Exact version
    "click>=8.0.0,<9.0.0",  # Range
    "pydantic~=2.0.0",  # Compatible release
]
```

### Private Package Index
```toml
# pip.conf or pyproject.toml
[tool.pip]
index-url = "https://your-private-index.com/simple/"
extra-index-url = [
    "https://pypi.org/simple/",
]
```

## 🔐 Secrets Management

### Environment Variables
```python
import os
from pathlib import Path

# ✅ Good - Environment variables
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# ✅ Good - .env files (with python-dotenv)
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
```

### Secrets Detection in CI
```yaml
# GitHub Actions - Detect secrets
name: Security Scan
on: [push, pull_request]

jobs:
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trufflehog
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: main
          head: HEAD
```

### .gitignore for Secrets
```gitignore
# Secrets and credentials
.env
.env.local
.env.*.local
secrets.json
*.pem
*.key
config/secrets.yml

# IDE files that might contain secrets
.vscode/settings.json
.idea/

# OS files
.DS_Store
Thumbs.db
```

## 🛠️ Security-First Development

### Secure Coding Practices

#### Input Validation
```python
import re
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_filename(filename: str) -> str:
    """Remove potentially dangerous characters from filename."""
    # Remove path traversal attempts
    filename = filename.replace('..', '')
    # Allow only alphanumeric, dash, underscore, and dot
    return re.sub(r'[^a-zA-Z0-9._-]', '', filename)
```

#### Safe File Operations
```python
from pathlib import Path
import tempfile
import os

def safe_file_write(content: str, directory: str, filename: str) -> Path:
    """Safely write content to file."""
    # Validate directory
    base_dir = Path(directory).resolve()

    # Sanitize filename
    safe_filename = sanitize_filename(filename)

    # Ensure file is within expected directory
    file_path = (base_dir / safe_filename).resolve()
    if not str(file_path).startswith(str(base_dir)):
        raise ValueError("Path traversal attempt detected")

    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write with secure permissions
    file_path.write_text(content, encoding='utf-8')
    file_path.chmod(0o644)

    return file_path
```

#### Secure API Calls
```python
import requests
from urllib.parse import urljoin
import ssl

class SecureAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'MyApp/1.0.0'
        })

        # Verify SSL certificates
        self.session.verify = True

        # Set timeouts
        self.timeout = (5, 30)  # (connect, read)

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a secure GET request."""
        url = urljoin(self.base_url, endpoint)

        # Validate URL scheme
        if not url.startswith(('https://', 'http://localhost')):
            raise ValueError("Only HTTPS URLs allowed (except localhost)")

        response = self.session.get(
            url,
            timeout=self.timeout,
            **kwargs
        )
        response.raise_for_status()
        return response
```

## 🔍 Security Testing

### Penetration Testing
```python
# tests/test_security.py
import pytest
import requests
from unittest.mock import patch

def test_sql_injection_protection():
    """Test that SQL injection attempts are blocked."""
    malicious_input = "'; DROP TABLE users; --"

    with pytest.raises(ValueError):
        user_service.get_user_by_name(malicious_input)

def test_xss_protection():
    """Test that XSS attempts are sanitized."""
    malicious_script = "<script>alert('xss')</script>"

    sanitized = html_sanitizer.clean(malicious_script)
    assert "<script>" not in sanitized

def test_path_traversal_protection():
    """Test that path traversal is blocked."""
    malicious_path = "../../../etc/passwd"

    with pytest.raises(ValueError):
        file_service.read_file(malicious_path)

@patch('requests.get')
def test_api_timeout(mock_get):
    """Test that API calls have proper timeouts."""
    mock_get.side_effect = requests.Timeout()

    with pytest.raises(requests.Timeout):
        api_client.get_data()
```

## 📋 Security Checklist

### Code Review Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Input validation for all user inputs
- [ ] Proper error handling (no sensitive info in errors)
- [ ] Secure file operations (no path traversal)
- [ ] SQL queries use parameterization
- [ ] API calls use HTTPS and timeouts
- [ ] Dependencies are up-to-date and secure
- [ ] Proper authentication and authorization
- [ ] Logging doesn't include sensitive data
- [ ] Cryptographically secure random number generation

### Deployment Security
- [ ] Environment variables for secrets
- [ ] Proper file permissions
- [ ] SSL/TLS configuration
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Input size limits set
- [ ] Error pages don't leak information
- [ ] Regular security scans scheduled

This comprehensive security setup helps protect your application from common vulnerabilities and ensures you follow security best practices throughout development.
