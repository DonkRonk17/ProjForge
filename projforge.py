#!/usr/bin/env python3
"""
ProjForge - Project Scaffolding & Template Engine

Generate complete, ready-to-code project structures from built-in or custom
templates. Ships with templates for Python CLI tools, Python libraries, and
the Team Brain Holy Grail standard. Supports variable substitution, interactive
mode, custom templates, dry-run preview, and optional git initialization.

Author: ATLAS (Team Brain)
For: Logan Smith / Metaphy LLC
Version: 1.0.0
Date: February 12, 2026
License: MIT
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# CONSTANTS
# ============================================================================

VERSION = "1.0.0"
APP_NAME = "ProjForge"
CONFIG_DIR = Path.home() / ".projforge"
CONFIG_FILE = CONFIG_DIR / "config.json"
CUSTOM_TEMPLATE_DIR = CONFIG_DIR / "templates"
VARIABLE_PATTERN = re.compile(r"\{\{(\w+)(?::([^}]*))?\}\}")

DEFAULT_CONFIG = {
    "default_author": "Logan Smith",
    "default_org": "Metaphy LLC",
    "default_license": "MIT",
    "default_template": "python-cli",
    "auto_git": False,
}


# ============================================================================
# DATA CLASSES (stdlib-only, no dataclasses for max compat)
# ============================================================================

class TemplateInfo:
    """Metadata about a project template."""

    def __init__(self, name: str, description: str, version: str,
                 author: str, variables: Dict[str, dict],
                 file_count: int, dir_count: int, is_builtin: bool = True):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.variables = variables
        self.file_count = file_count
        self.dir_count = dir_count
        self.is_builtin = is_builtin

    def __repr__(self) -> str:
        return f"TemplateInfo(name={self.name!r})"


class CreateResult:
    """Result of a project creation operation."""

    def __init__(self, success: bool, project_path: Optional[Path] = None,
                 files_created: int = 0, dirs_created: int = 0,
                 errors: Optional[List[str]] = None,
                 message: str = ""):
        self.success = success
        self.project_path = project_path
        self.files_created = files_created
        self.dirs_created = dirs_created
        self.errors = errors or []
        self.message = message


# ============================================================================
# BUILT-IN TEMPLATES
# ============================================================================

def _get_current_date() -> str:
    """Get current date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def _get_current_year() -> str:
    """Get current year."""
    return str(datetime.now().year)


def _get_current_month() -> str:
    """Get current month name."""
    return datetime.now().strftime("%B")


BUILTIN_TEMPLATES: Dict[str, dict] = {}


def _register_python_cli_template() -> dict:
    """Python CLI tool template."""
    return {
        "name": "python-cli",
        "description": "Standard Python CLI tool with argparse, tests, and documentation",
        "version": "1.0",
        "author": "Team Brain",
        "variables": {
            "name": {"description": "Project name (PascalCase)", "required": True},
            "description": {"description": "One-line project description", "required": True},
            "author": {"description": "Author name", "default": "Logan Smith"},
            "org": {"description": "Organization", "default": "Metaphy LLC"},
            "year": {"description": "Copyright year", "default": "auto"},
        },
        "directories": [],
        "files": {
            "{{name_lower}}.py": '''#!/usr/bin/env python3
"""
{{name}} - {{description}}

A professional CLI tool built with Python standard library.

Author: {{author}} / {{org}}
Version: 1.0.0
Date: {{date}}
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "1.0.0"


class {{name}}:
    """
    Main interface for {{name}} functionality.

    Example:
        >>> tool = {{name}}()
        >>> tool.run()
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize {{name}} with optional config."""
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Load configuration from file or defaults."""
        defaults = {}
        if config_path and config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return {**defaults, **json.load(f)}
        return defaults

    def run(self) -> dict:
        """Execute main functionality."""
        return {"status": "success", "message": "{{name}} executed successfully"}


def main():
    """CLI entry point."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="{{name}} - {{description}}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run            # Run main functionality
  %(prog)s --version      # Show version

For more information: https://github.com/DonkRonk17/{{name}}
        """,
    )

    parser.add_argument("command", nargs="?", default="run",
                        choices=["run"],
                        help="Command to execute")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {VERSION}")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")

    args = parser.parse_args()

    tool = {{name}}()

    if args.command == "run":
        result = tool.run()
        if args.verbose:
            print(json.dumps(result, indent=2))
        else:
            print(f"[OK] {result.get('message', 'Done')}")


if __name__ == "__main__":
    main()
''',
            "test_{{name_lower}}.py": '''#!/usr/bin/env python3
"""
Comprehensive test suite for {{name}}.

Run: python test_{{name_lower}}.py
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from {{name_lower}} import {{name}}


class Test{{name}}Core(unittest.TestCase):
    """Test core functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = {{name}}()

    def test_initialization(self):
        """Test tool initializes correctly."""
        tool = {{name}}()
        self.assertIsNotNone(tool)

    def test_run(self):
        """Test basic run works."""
        result = self.tool.run()
        self.assertEqual(result["status"], "success")

    def test_config_defaults(self):
        """Test default configuration."""
        self.assertIsInstance(self.tool.config, dict)


class Test{{name}}EdgeCases(unittest.TestCase):
    """Test edge cases."""

    def test_invalid_config_path(self):
        """Test with non-existent config path."""
        tool = {{name}}(config_path=Path("/nonexistent/config.json"))
        self.assertIsNotNone(tool)


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print(f"TESTING: {{name}} v1.0.0")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(Test{{name}}Core))
    suite.addTests(loader.loadTestsFromTestCase(Test{{name}}EdgeCases))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\\n" + "=" * 70)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"RESULTS: {result.testsRun} tests | Passed: {passed}")
    print("=" * 70)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
''',
            "README.md": '''# {{name}}

> {{description}}

**Version:** 1.0.0
**Author:** {{author}} / {{org}}
**License:** MIT
**Date:** {{date}}

---

## Installation

```bash
git clone https://github.com/DonkRonk17/{{name}}.git
cd {{name}}
python {{name_lower}}.py --help
```

## Usage

```bash
# Run main functionality
python {{name_lower}}.py run

# Verbose output
python {{name_lower}}.py run --verbose
```

## Testing

```bash
python test_{{name_lower}}.py
```

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built by:** {{author}} / {{org}}
**Scaffolded with:** ProjForge (Team Brain)
''',
            "requirements.txt": '''# {{name}} - Dependencies
# Zero external dependencies (Python stdlib only)
''',
            "setup.py": '''from setuptools import setup, find_packages

setup(
    name="{{name_lower}}",
    version="1.0.0",
    description="{{description}}",
    author="{{author}}",
    author_email="",
    url="https://github.com/DonkRonk17/{{name}}",
    py_modules=["{{name_lower}}"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "{{name_lower}}={{name_lower}}:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
''',
            "LICENSE": '''MIT License

Copyright (c) {{year}} {{author}} / {{org}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
            ".gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
venv/
.env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Testing
.pytest_cache/
.coverage
htmlcov/

# Data
*.db
*.sqlite3
*.log
''',
        },
    }


def _register_python_lib_template() -> dict:
    """Python library package template."""
    return {
        "name": "python-lib",
        "description": "Python library package with module structure, tests, and docs",
        "version": "1.0",
        "author": "Team Brain",
        "variables": {
            "name": {"description": "Package name (PascalCase)", "required": True},
            "description": {"description": "One-line package description", "required": True},
            "author": {"description": "Author name", "default": "Logan Smith"},
            "org": {"description": "Organization", "default": "Metaphy LLC"},
            "year": {"description": "Copyright year", "default": "auto"},
        },
        "directories": ["{{name_lower}}", "tests"],
        "files": {
            "{{name_lower}}/__init__.py": '''"""
{{name}} - {{description}}

Author: {{author}} / {{org}}
Version: 1.0.0
"""

from .core import {{name}}

__version__ = "1.0.0"
__all__ = ["{{name}}"]
''',
            "{{name_lower}}/core.py": '''"""
{{name}} core module.

This module contains the main {{name}} class.
"""

from typing import Any, Dict, Optional


class {{name}}:
    """
    Main interface for {{name}}.

    Example:
        >>> from {{name_lower}} import {{name}}
        >>> obj = {{name}}()
        >>> obj.process("data")
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize with optional config."""
        self.config = config or {}

    def process(self, data: Any) -> Dict[str, Any]:
        """
        Process input data.

        Args:
            data: Input data to process.

        Returns:
            Dictionary with processing results.
        """
        return {"status": "success", "input": str(data)}
''',
            "tests/__init__.py": "",
            "tests/test_core.py": '''"""Tests for {{name}} core module."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from {{name_lower}} import {{name}}


class Test{{name}}(unittest.TestCase):
    """Test {{name}} core functionality."""

    def test_init(self):
        """Test initialization."""
        obj = {{name}}()
        self.assertIsNotNone(obj)

    def test_init_with_config(self):
        """Test initialization with config."""
        obj = {{name}}(config={"key": "value"})
        self.assertEqual(obj.config["key"], "value")

    def test_process(self):
        """Test basic processing."""
        obj = {{name}}()
        result = obj.process("test")
        self.assertEqual(result["status"], "success")

    def test_process_returns_input(self):
        """Test process returns input data."""
        obj = {{name}}()
        result = obj.process("hello")
        self.assertEqual(result["input"], "hello")


if __name__ == "__main__":
    unittest.main(verbosity=2)
''',
            "README.md": '''# {{name}}

> {{description}}

**Version:** 1.0.0
**Author:** {{author}} / {{org}}
**License:** MIT

## Installation

```bash
pip install -e .
```

## Usage

```python
from {{name_lower}} import {{name}}

obj = {{name}}()
result = obj.process("data")
print(result)
```

## Testing

```bash
python -m pytest tests/ -v
```

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built by:** {{author}} / {{org}}
**Scaffolded with:** ProjForge (Team Brain)
''',
            "requirements.txt": "# {{name}} - Dependencies\n# Zero external dependencies\n",
            "setup.py": '''from setuptools import setup, find_packages

setup(
    name="{{name_lower}}",
    version="1.0.0",
    description="{{description}}",
    author="{{author}}",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
''',
            "LICENSE": '''MIT License

Copyright (c) {{year}} {{author}} / {{org}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
            ".gitignore": '''__pycache__/\n*.py[cod]\n*.egg-info/\ndist/\nbuild/\n.eggs/\nvenv/\n.env/\n.venv/\n.vscode/\n.idea/\n.DS_Store\nThumbs.db\n.pytest_cache/\n.coverage\nhtmlcov/\n*.db\n*.log\n''',
        },
    }


def _register_teambrain_template() -> dict:
    """Team Brain Holy Grail Protocol standard template."""
    return {
        "name": "teambrain-standard",
        "description": "Full Holy Grail Protocol standard - complete Team Brain tool with all 9-phase files",
        "version": "1.0",
        "author": "Team Brain",
        "variables": {
            "name": {"description": "Tool name (PascalCase)", "required": True},
            "description": {"description": "One-line tool description", "required": True},
            "author": {"description": "Author/builder name", "default": "ATLAS (Team Brain)"},
            "org": {"description": "Organization", "default": "Metaphy LLC"},
            "year": {"description": "Copyright year", "default": "auto"},
            "builder": {"description": "Builder agent name", "default": "ATLAS"},
            "requested_by": {"description": "Who requested this tool", "default": "Self-initiated"},
        },
        "directories": ["branding"],
        "files": {
            "{{name_lower}}.py": '''#!/usr/bin/env python3
"""
{{name}} - {{description}}

Professional production-quality tool built following the Holy Grail Protocol.
Zero external dependencies (Python stdlib only). Cross-platform compatible.

Author: {{author}}
For: Logan Smith / {{org}}
Version: 1.0.0
Date: {{date}}
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "1.0.0"


class {{name}}:
    """
    Main interface for {{name}} functionality.

    Example:
        >>> tool = {{name}}()
        >>> result = tool.run()
        >>> print(result["status"])
        success
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize {{name}}.

        Args:
            config_path: Optional path to JSON config file.
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[Path]) -> dict:
        """Load configuration from file or return defaults."""
        defaults = {}
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return {**defaults, **json.load(f)}
        return defaults

    def run(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute main functionality.

        Args:
            **kwargs: Additional arguments.

        Returns:
            Dictionary with status and results.
        """
        return {
            "status": "success",
            "message": "{{name}} executed successfully",
            "version": VERSION,
        }


def main():
    """CLI entry point for {{name}}."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="{{name}} - {{description}}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run                 # Run main functionality
  %(prog)s run --verbose       # Verbose output
  %(prog)s --version           # Show version

Built by: {{author}}
For: Logan Smith / {{org}}
GitHub: https://github.com/DonkRonk17/{{name}}
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    run_parser = subparsers.add_parser("run", help="Run main functionality")
    run_parser.add_argument("--verbose", "-v", action="store_true",
                            help="Verbose output")

    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    tool = {{name}}()

    if args.command == "run":
        result = tool.run()
        if getattr(args, "verbose", False):
            print(json.dumps(result, indent=2))
        else:
            print(f"[OK] {result.get('message', 'Done')}")


if __name__ == "__main__":
    main()
''',
            "test_{{name_lower}}.py": '''#!/usr/bin/env python3
"""
Comprehensive test suite for {{name}}.

Tests cover:
- Core functionality
- Edge cases
- Error handling
- Integration scenarios

Run: python test_{{name_lower}}.py
"""

import unittest
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from {{name_lower}} import {{name}}, VERSION


class Test{{name}}Core(unittest.TestCase):
    """Test core functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = {{name}}()

    def test_initialization(self):
        """Test tool initializes correctly."""
        tool = {{name}}()
        self.assertIsNotNone(tool)
        self.assertIsInstance(tool.config, dict)

    def test_run_returns_success(self):
        """Test run returns success status."""
        result = self.tool.run()
        self.assertEqual(result["status"], "success")

    def test_run_includes_version(self):
        """Test run result includes version."""
        result = self.tool.run()
        self.assertEqual(result["version"], VERSION)

    def test_run_includes_message(self):
        """Test run result includes message."""
        result = self.tool.run()
        self.assertIn("message", result)

    def test_config_default(self):
        """Test default configuration."""
        self.assertEqual(self.tool.config, {})

    def test_config_from_file(self):
        """Test loading config from file."""
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                          delete=False)
        try:
            json.dump({"key": "value"}, tmp)
            tmp.close()
            tool = {{name}}(config_path=Path(tmp.name))
            self.assertEqual(tool.config["key"], "value")
        finally:
            Path(tmp.name).unlink(missing_ok=True)


class Test{{name}}EdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def test_invalid_config_path(self):
        """Test with non-existent config path."""
        tool = {{name}}(config_path=Path("/nonexistent/config.json"))
        self.assertIsNotNone(tool)
        self.assertEqual(tool.config, {})

    def test_run_with_kwargs(self):
        """Test run accepts keyword arguments."""
        tool = {{name}}()
        result = tool.run(extra="data")
        self.assertEqual(result["status"], "success")

    def test_version_format(self):
        """Test version string format."""
        self.assertRegex(VERSION, r"^\\d+\\.\\d+\\.\\d+$")

    def test_multiple_runs(self):
        """Test tool can run multiple times."""
        tool = {{name}}()
        for _ in range(10):
            result = tool.run()
            self.assertEqual(result["status"], "success")


class Test{{name}}Integration(unittest.TestCase):
    """Test integration scenarios."""

    def test_json_serializable(self):
        """Test output is JSON serializable."""
        tool = {{name}}()
        result = tool.run()
        serialized = json.dumps(result)
        self.assertIsInstance(serialized, str)


def run_tests():
    """Run all tests with summary output."""
    print("=" * 70)
    print(f"TESTING: {{name}} v{VERSION}")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(Test{{name}}Core))
    suite.addTests(loader.loadTestsFromTestCase(Test{{name}}EdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(Test{{name}}Integration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\\n" + "=" * 70)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"RESULTS: {result.testsRun} tests | Passed: {passed} | "
          f"Failed: {len(result.failures)} | Errors: {len(result.errors)}")
    print("=" * 70)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
''',
            "README.md": '''# {{name}}

> {{description}}

**Version:** 1.0.0  
**Author:** {{author}}  
**For:** Logan Smith / {{org}}  
**License:** MIT  
**Date:** {{date}}  
**Requested By:** {{requested_by}}  

---

## The Problem

[Describe the problem this tool solves]

## The Solution

[Describe how this tool solves it]

---

## Quick Start

```bash
git clone https://github.com/DonkRonk17/{{name}}.git
cd {{name}}
python {{name_lower}}.py --help
```

## Usage

```bash
# Run main functionality
python {{name_lower}}.py run

# Verbose output
python {{name_lower}}.py run --verbose
```

## Python API

```python
from {{name_lower}} import {{name}}

tool = {{name}}()
result = tool.run()
print(result)
```

## Testing

```bash
python test_{{name_lower}}.py
```

---

## Credits

**Built by:** {{author}}  
**For:** Logan Smith / {{org}}  
**Requested by:** {{requested_by}}  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** {{date}}  

---

**Scaffolded with ProjForge (Team Brain)**
''',
            "EXAMPLES.md": '''# {{name}} - Usage Examples

## Example 1: Basic Usage

```bash
python {{name_lower}}.py run
```

**Expected Output:**
```
[OK] {{name}} executed successfully
```

## Example 2: Verbose Output

```bash
python {{name_lower}}.py run --verbose
```

## Example 3: Python API

```python
from {{name_lower}} import {{name}}

tool = {{name}}()
result = tool.run()
print(result["status"])  # "success"
```

---

**More examples to be added as features are built.**
''',
            "CHEAT_SHEET.txt": '''================================================================================
{{name_upper}} CHEAT SHEET
================================================================================

QUICK START
-----------
1. Clone: git clone https://github.com/DonkRonk17/{{name}}.git
2. Run:   python {{name_lower}}.py run
3. Test:  python test_{{name_lower}}.py

================================================================================
COMMANDS
--------------------------------------------------------------------------------

Run:
  python {{name_lower}}.py run
  python {{name_lower}}.py run --verbose

Help:
  python {{name_lower}}.py --help
  python {{name_lower}}.py --version

================================================================================
PYTHON API
--------------------------------------------------------------------------------

Import:
  from {{name_lower}} import {{name}}

Basic Usage:
  tool = {{name}}()
  result = tool.run()

With Config:
  tool = {{name}}(config_path=Path("config.json"))

================================================================================
RESOURCES
--------------------------------------------------------------------------------

Documentation: README.md
Examples:      EXAMPLES.md
GitHub:        https://github.com/DonkRonk17/{{name}}

================================================================================
''',
            "BUILD_COVERAGE_PLAN.md": "# {{name}} - Build Coverage Plan\\n\\n**Tool:** {{name}}\\n**Date:** {{date}}\\n**Builder:** {{builder}}\\n\\n[Fill in during Phase 1]\\n",
            "BUILD_AUDIT.md": "# {{name}} - Build Audit\\n\\n**Date:** {{date}}\\n**Builder:** {{builder}}\\n\\n[Fill in during Phase 2]\\n",
            "ARCHITECTURE.md": "# {{name}} - Architecture\\n\\n**Date:** {{date}}\\n**Builder:** {{builder}}\\n\\n[Fill in during Phase 3]\\n",
            "BUILD_REPORT.md": "# {{name}} - Build Report\\n\\n**Date:** {{date}}\\n**Builder:** {{builder}}\\n\\n[Fill in during Phase 8]\\n",
            "INTEGRATION_PLAN.md": "# {{name}} - Integration Plan\\n\\n**Date:** {{date}}\\n\\n[Fill in during Phase 7]\\n",
            "QUICK_START_GUIDES.md": "# {{name}} - Quick Start Guides\\n\\n**Date:** {{date}}\\n\\n[Fill in during Phase 7]\\n",
            "INTEGRATION_EXAMPLES.md": "# {{name}} - Integration Examples\\n\\n**Date:** {{date}}\\n\\n[Fill in during Phase 7]\\n",
            "requirements.txt": "# {{name}} - Dependencies\\n# Zero external dependencies (Python stdlib only)\\n",
            "setup.py": '''from setuptools import setup

setup(
    name="{{name_lower}}",
    version="1.0.0",
    description="{{description}}",
    author="{{author}}",
    url="https://github.com/DonkRonk17/{{name}}",
    py_modules=["{{name_lower}}"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "{{name_lower}}={{name_lower}}:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
''',
            "LICENSE": '''MIT License

Copyright (c) {{year}} {{author}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
            ".gitignore": '''__pycache__/\n*.py[cod]\n*.egg-info/\ndist/\nbuild/\n.eggs/\nvenv/\n.env/\n.venv/\n.vscode/\n.idea/\n.DS_Store\nThumbs.db\n.pytest_cache/\n.coverage\nhtmlcov/\n*.db\n*.sqlite3\n*.log\n''',
            "branding/BRANDING_PROMPTS.md": '''# {{name}} - Branding Prompts

## 1. TITLE CARD (16:9 - 1920x1080px)

**DALL-E Prompt:**
Create a sleek title card for "{{name}}" - {{description}}.
Dark navy background (#0a0e27), bright cyan accents (#00d4ff).
Large bold title centered. Subtle tech patterns in background.
Professional, cutting-edge, Team Brain ecosystem.

## 2. LOGO MARK (1:1 - 1024x1024px)

**DALL-E Prompt:**
Minimalist logo icon for "{{name}}" tool.
Simple geometric shape. Cyan (#00d4ff) on dark navy (#0a0e27).
Clean, recognizable at small sizes. No text.

## 3. HORIZONTAL LOGO (3:1 - 1800x600px)

**DALL-E Prompt:**
Horizontal logo banner for "{{name}}".
Dark navy background, cyan text and accents.
Icon on left, tool name center-left.

## 4. APP ICON (1:1 - 512x512px)

**DALL-E Prompt:**
Simplified app icon for "{{name}}".
Maximum 2 colors: cyan + white on dark background.
Bold shapes, readable at 32x32px. Flat design.
''',
        },
    }


# Register all built-in templates
BUILTIN_TEMPLATES["python-cli"] = _register_python_cli_template()
BUILTIN_TEMPLATES["python-lib"] = _register_python_lib_template()
BUILTIN_TEMPLATES["teambrain-standard"] = _register_teambrain_template()


# ============================================================================
# TEMPLATE ENGINE
# ============================================================================

class TemplateEngine:
    """
    Load, parse, and render templates with variable substitution.

    Supports {{variable}} and {{variable:default}} syntax.
    Auto-generates derived variables (name_lower, name_upper, etc.).
    """

    @staticmethod
    def resolve_variables(name: str, user_vars: Dict[str, str],
                          template_vars: Dict[str, dict]) -> Dict[str, str]:
        """
        Resolve all template variables including derived ones.

        Args:
            name: Project name as provided by user.
            user_vars: User-provided variable overrides.
            template_vars: Template variable definitions.

        Returns:
            Complete dictionary of resolved variables.
        """
        resolved: Dict[str, str] = {}

        # Auto-derived from project name
        resolved["name"] = name
        resolved["name_lower"] = _to_snake_case(name).lower()
        resolved["name_upper"] = name.upper().replace("-", "_").replace(" ", "_")
        resolved["name_snake"] = _to_snake_case(name)
        resolved["name_title"] = name.replace("_", " ").replace("-", " ").title()

        # Auto-generated date/time vars
        resolved["date"] = _get_current_date()
        resolved["year"] = _get_current_year()
        resolved["month"] = _get_current_month()

        # Apply template defaults
        for var_name, var_def in template_vars.items():
            if var_name not in resolved:
                default = var_def.get("default", "")
                if default == "auto":
                    if var_name == "year":
                        default = _get_current_year()
                    elif var_name == "date":
                        default = _get_current_date()
                    else:
                        default = ""
                resolved[var_name] = default

        # Apply user overrides (highest priority)
        for key, value in user_vars.items():
            resolved[key] = value

        # Re-derive name variants if user overrode name
        if "name" in user_vars:
            resolved["name_lower"] = _to_snake_case(user_vars["name"]).lower()
            resolved["name_upper"] = user_vars["name"].upper().replace("-", "_").replace(" ", "_")
            resolved["name_snake"] = _to_snake_case(user_vars["name"])
            resolved["name_title"] = user_vars["name"].replace("_", " ").replace("-", " ").title()

        return resolved

    @staticmethod
    def render_string(template_str: str, variables: Dict[str, str]) -> str:
        """
        Render a template string by substituting variables.

        Supports {{var}} and {{var:default}} syntax.

        Args:
            template_str: String with {{variable}} placeholders.
            variables: Dictionary of variable values.

        Returns:
            Rendered string with all variables substituted.
        """
        def replace_var(match: re.Match) -> str:
            var_name = match.group(1)
            default = match.group(2)
            if var_name in variables:
                return str(variables[var_name])
            elif default is not None:
                return default
            return match.group(0)  # Leave unreplaced

        return VARIABLE_PATTERN.sub(replace_var, template_str)

    @staticmethod
    def get_required_variables(template: dict) -> List[str]:
        """
        Get list of required variables that have no default.

        Args:
            template: Template definition dict.

        Returns:
            List of required variable names.
        """
        required = []
        for var_name, var_def in template.get("variables", {}).items():
            if var_def.get("required", False) and "default" not in var_def:
                required.append(var_name)
        return required

    @staticmethod
    def get_missing_variables(template: dict,
                              provided: Dict[str, str]) -> List[str]:
        """
        Find required variables not yet provided.

        Args:
            template: Template definition dict.
            provided: Variables already provided.

        Returns:
            List of missing required variable names.
        """
        missing = []
        for var_name, var_def in template.get("variables", {}).items():
            if var_def.get("required", False):
                if var_name not in provided and var_name != "name":
                    missing.append(var_name)
        return missing


# ============================================================================
# TEMPLATE STORE
# ============================================================================

class TemplateStore:
    """
    Manage built-in and custom templates.

    Built-in templates are Python dicts defined above.
    Custom templates are folders in ~/.projforge/templates/.
    """

    def __init__(self) -> None:
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Create config and template directories if needed."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CUSTOM_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass  # May fail in restricted environments

    def list_all(self) -> List[TemplateInfo]:
        """
        List all available templates (built-in + custom).

        Returns:
            List of TemplateInfo objects.
        """
        templates = []

        # Built-in templates
        for name, tmpl in BUILTIN_TEMPLATES.items():
            templates.append(TemplateInfo(
                name=tmpl["name"],
                description=tmpl["description"],
                version=tmpl["version"],
                author=tmpl["author"],
                variables=tmpl.get("variables", {}),
                file_count=len(tmpl.get("files", {})),
                dir_count=len(tmpl.get("directories", [])),
                is_builtin=True,
            ))

        # Custom templates
        if CUSTOM_TEMPLATE_DIR.exists():
            for entry in sorted(CUSTOM_TEMPLATE_DIR.iterdir()):
                if entry.is_dir():
                    meta_file = entry / "template.json"
                    if meta_file.exists():
                        try:
                            with open(meta_file, "r", encoding="utf-8") as f:
                                meta = json.load(f)
                            templates.append(TemplateInfo(
                                name=meta.get("name", entry.name),
                                description=meta.get("description", "Custom template"),
                                version=meta.get("version", "1.0"),
                                author=meta.get("author", "Unknown"),
                                variables=meta.get("variables", {}),
                                file_count=meta.get("file_count", 0),
                                dir_count=meta.get("dir_count", 0),
                                is_builtin=False,
                            ))
                        except (json.JSONDecodeError, OSError):
                            pass

        return templates

    def get_template(self, name: str) -> Optional[dict]:
        """
        Get a template by name.

        Args:
            name: Template name.

        Returns:
            Template dict or None if not found.
        """
        # Check built-in first
        if name in BUILTIN_TEMPLATES:
            return BUILTIN_TEMPLATES[name]

        # Check custom templates
        custom_path = CUSTOM_TEMPLATE_DIR / name
        if custom_path.exists() and custom_path.is_dir():
            return self._load_custom_template(custom_path)

        return None

    def _load_custom_template(self, path: Path) -> Optional[dict]:
        """
        Load a custom template from a directory.

        Custom template format:
            template_dir/
                template.json    # Metadata and variable definitions
                files/           # Template files (directory structure)

        Args:
            path: Path to template directory.

        Returns:
            Template dict or None.
        """
        meta_file = path / "template.json"
        files_dir = path / "files"

        if not meta_file.exists():
            return None

        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

        template = {
            "name": meta.get("name", path.name),
            "description": meta.get("description", "Custom template"),
            "version": meta.get("version", "1.0"),
            "author": meta.get("author", "Unknown"),
            "variables": meta.get("variables", {}),
            "directories": [],
            "files": {},
        }

        # Load files from files/ directory
        if files_dir.exists():
            for file_path in files_dir.rglob("*"):
                if file_path.is_file():
                    relative = file_path.relative_to(files_dir)
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        template["files"][str(relative).replace("\\", "/")] = content
                    except (OSError, UnicodeDecodeError):
                        pass
                elif file_path.is_dir():
                    relative = file_path.relative_to(files_dir)
                    template["directories"].append(str(relative).replace("\\", "/"))

        return template

    def add_custom_template(self, source_path: Path) -> Tuple[bool, str]:
        """
        Add a custom template from a directory.

        The source must contain a template.json and files/ directory.

        Args:
            source_path: Path to template source directory.

        Returns:
            Tuple of (success, message).
        """
        source = Path(source_path)

        if not source.exists() or not source.is_dir():
            return False, f"Source directory not found: {source}"

        meta_file = source / "template.json"
        if not meta_file.exists():
            return False, f"Missing template.json in {source}"

        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            return False, f"Invalid template.json: {e}"

        name = meta.get("name", source.name)
        dest = CUSTOM_TEMPLATE_DIR / name

        if dest.exists():
            return False, f"Template '{name}' already exists at {dest}"

        try:
            shutil.copytree(source, dest)
            return True, f"Template '{name}' added successfully to {dest}"
        except OSError as e:
            return False, f"Failed to copy template: {e}"

    def template_exists(self, name: str) -> bool:
        """Check if a template exists (built-in or custom)."""
        if name in BUILTIN_TEMPLATES:
            return True
        custom_path = CUSTOM_TEMPLATE_DIR / name
        return custom_path.exists() and (custom_path / "template.json").exists()


# ============================================================================
# FILE GENERATOR
# ============================================================================

class FileGenerator:
    """Generate files and directories from a rendered template."""

    @staticmethod
    def generate(template: dict, variables: Dict[str, str],
                 output_dir: Path, dry_run: bool = False) -> CreateResult:
        """
        Generate a project from a template.

        Args:
            template: Template definition dict.
            variables: Resolved variable values.
            output_dir: Directory to create project in.
            dry_run: If True, report what would be created without writing.

        Returns:
            CreateResult with details of what was created.
        """
        engine = TemplateEngine()
        files_created = 0
        dirs_created = 0
        errors: List[str] = []
        created_paths: List[str] = []

        # Create project root directory
        project_dir = output_dir
        if not dry_run:
            try:
                project_dir.mkdir(parents=True, exist_ok=True)
                dirs_created += 1
            except OSError as e:
                return CreateResult(
                    success=False,
                    errors=[f"Cannot create project directory: {e}"],
                )
        else:
            dirs_created += 1
            created_paths.append(str(project_dir) + "/")

        # Create explicit directories
        for dir_path in template.get("directories", []):
            rendered_path = engine.render_string(dir_path, variables)
            full_path = project_dir / rendered_path
            if not dry_run:
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    dirs_created += 1
                except OSError as e:
                    errors.append(f"Cannot create directory {rendered_path}: {e}")
            else:
                dirs_created += 1
                created_paths.append(str(full_path) + "/")

        # Create files
        for file_path, content in template.get("files", {}).items():
            rendered_path = engine.render_string(file_path, variables)
            rendered_content = engine.render_string(content, variables)
            full_path = project_dir / rendered_path

            if not dry_run:
                try:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(rendered_content, encoding="utf-8")
                    files_created += 1
                except OSError as e:
                    errors.append(f"Cannot create file {rendered_path}: {e}")
            else:
                files_created += 1
                created_paths.append(str(full_path))

        message = ""
        if dry_run:
            message = "DRY RUN - No files created. Would create:\n"
            for p in sorted(created_paths):
                message += f"  {p}\n"
        else:
            message = (
                f"Project created at {project_dir}\n"
                f"  Files: {files_created}\n"
                f"  Directories: {dirs_created}"
            )

        return CreateResult(
            success=len(errors) == 0,
            project_path=project_dir,
            files_created=files_created,
            dirs_created=dirs_created,
            errors=errors,
            message=message,
        )


# ============================================================================
# PROJFORGE (MAIN ORCHESTRATOR)
# ============================================================================

class ProjForge:
    """
    Main ProjForge interface for project scaffolding.

    Combines TemplateStore, TemplateEngine, and FileGenerator
    into a simple, cohesive API.

    Example:
        >>> forge = ProjForge()
        >>> result = forge.create_project("python-cli", "MyTool",
        ...     variables={"description": "A useful tool"})
        >>> print(result.success)
        True
    """

    def __init__(self) -> None:
        """Initialize ProjForge with default store and config."""
        self.store = TemplateStore()
        self.engine = TemplateEngine()
        self.generator = FileGenerator()
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load config from file or return defaults."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except (json.JSONDecodeError, OSError):
                pass
        return dict(DEFAULT_CONFIG)

    def save_config(self) -> None:
        """Save current config to file."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except OSError:
            pass

    def create_project(self, template_name: str, project_name: str,
                       variables: Optional[Dict[str, str]] = None,
                       output_dir: Optional[Path] = None,
                       dry_run: bool = False,
                       init_git: bool = False,
                       interactive: bool = False) -> CreateResult:
        """
        Create a new project from a template.

        Args:
            template_name: Name of the template to use.
            project_name: Name of the new project.
            variables: Optional variable overrides.
            output_dir: Output directory (defaults to cwd/project_name).
            dry_run: Preview only, don't create files.
            init_git: Initialize git repo after creation.
            interactive: Prompt for missing variables.

        Returns:
            CreateResult with details.
        """
        variables = variables or {}

        # Validate project name
        if not project_name or not project_name.strip():
            return CreateResult(success=False,
                                errors=["Project name cannot be empty"])

        if not _is_valid_name(project_name):
            return CreateResult(
                success=False,
                errors=[f"Invalid project name: '{project_name}'. "
                        "Use alphanumeric characters, hyphens, and underscores."],
            )

        # Get template
        template = self.store.get_template(template_name)
        if template is None:
            available = ", ".join(t.name for t in self.store.list_all())
            return CreateResult(
                success=False,
                errors=[f"Template '{template_name}' not found. "
                        f"Available: {available}"],
            )

        # Handle interactive mode for missing variables
        if interactive:
            missing = self.engine.get_missing_variables(template, variables)
            for var_name in missing:
                var_def = template["variables"].get(var_name, {})
                desc = var_def.get("description", var_name)
                default = var_def.get("default", "")
                prompt_str = f"  {var_name} ({desc})"
                if default:
                    prompt_str += f" [{default}]"
                prompt_str += ": "
                value = input(prompt_str).strip()
                if not value and default:
                    value = default
                if value:
                    variables[var_name] = value

        # Apply config defaults
        if "author" not in variables and self.config.get("default_author"):
            variables.setdefault("author", self.config["default_author"])
        if "org" not in variables and self.config.get("default_org"):
            variables.setdefault("org", self.config["default_org"])

        # Resolve all variables
        resolved = self.engine.resolve_variables(
            project_name, variables, template.get("variables", {})
        )

        # Determine output directory
        if output_dir is None:
            output_dir = Path.cwd() / project_name
        else:
            output_dir = Path(output_dir) / project_name

        # Check if output exists
        if output_dir.exists() and not dry_run:
            contents = list(output_dir.iterdir())
            if contents:
                return CreateResult(
                    success=False,
                    errors=[f"Directory already exists and is not empty: {output_dir}"],
                )

        # Generate the project
        result = self.generator.generate(template, resolved, output_dir, dry_run)

        # Initialize git if requested
        if init_git and result.success and not dry_run:
            git_result = _init_git(output_dir)
            if git_result:
                result.message += f"\n  Git: Initialized"
            else:
                result.message += f"\n  Git: Failed to initialize (git may not be installed)"

        return result

    def list_templates(self, verbose: bool = False) -> str:
        """
        List all available templates as formatted string.

        Args:
            verbose: Include variable details.

        Returns:
            Formatted string of available templates.
        """
        templates = self.store.list_all()
        if not templates:
            return "No templates available."

        lines = ["Available Templates:", "=" * 60]

        for tmpl in templates:
            tag = "[built-in]" if tmpl.is_builtin else "[custom]"
            lines.append(f"\n  {tmpl.name} {tag}")
            lines.append(f"    {tmpl.description}")
            lines.append(f"    Files: {tmpl.file_count} | Dirs: {tmpl.dir_count}")

            if verbose:
                lines.append("    Variables:")
                for var_name, var_def in tmpl.variables.items():
                    req = " (required)" if var_def.get("required") else ""
                    default = var_def.get("default", "")
                    default_str = f" [default: {default}]" if default else ""
                    desc = var_def.get("description", "")
                    lines.append(f"      {{{{  {var_name}  }}}} - {desc}{default_str}{req}")

        lines.append(f"\n{'=' * 60}")
        lines.append(f"Total: {len(templates)} templates")
        return "\n".join(lines)

    def preview_template(self, template_name: str) -> str:
        """
        Show the file structure a template would create.

        Args:
            template_name: Name of the template.

        Returns:
            Formatted tree of files and directories.
        """
        template = self.store.get_template(template_name)
        if template is None:
            return f"Template '{template_name}' not found."

        lines = [
            f"Template: {template['name']}",
            f"Description: {template['description']}",
            "",
            "File Structure:",
            f"  {{{{name}}}}/",
        ]

        # Collect all paths
        all_paths: List[str] = []
        for dir_path in template.get("directories", []):
            all_paths.append(dir_path + "/")
        for file_path in template.get("files", {}).keys():
            all_paths.append(file_path)

        for path in sorted(all_paths):
            indent = "    " + "  " * path.count("/")
            name = path.rstrip("/").split("/")[-1]
            if path.endswith("/"):
                lines.append(f"{indent}{name}/")
            else:
                lines.append(f"{indent}{name}")

        lines.append(f"\nTotal: {len(template.get('files', {}))} files, "
                      f"{len(template.get('directories', []))} directories")
        return "\n".join(lines)

    def get_template_info(self, template_name: str) -> Optional[TemplateInfo]:
        """
        Get detailed info about a template.

        Args:
            template_name: Name of the template.

        Returns:
            TemplateInfo or None.
        """
        template = self.store.get_template(template_name)
        if template is None:
            return None

        return TemplateInfo(
            name=template["name"],
            description=template["description"],
            version=template.get("version", "1.0"),
            author=template.get("author", "Unknown"),
            variables=template.get("variables", {}),
            file_count=len(template.get("files", {})),
            dir_count=len(template.get("directories", [])),
            is_builtin=template["name"] in BUILTIN_TEMPLATES,
        )

    def add_template(self, source_path: Path) -> Tuple[bool, str]:
        """
        Add a custom template from a directory.

        Args:
            source_path: Path to template directory.

        Returns:
            Tuple of (success, message).
        """
        return self.store.add_custom_template(source_path)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _to_snake_case(name: str) -> str:
    """
    Convert a name to snake_case.

    Args:
        name: Input name (PascalCase, camelCase, kebab-case, etc.)

    Returns:
        snake_case version.

    Examples:
        >>> _to_snake_case("MyTool")
        'my_tool'
        >>> _to_snake_case("HTTPClient")
        'http_client'
        >>> _to_snake_case("my-cool-tool")
        'my_cool_tool'
    """
    # Replace hyphens and spaces with underscores
    name = name.replace("-", "_").replace(" ", "_")

    # Insert underscore before uppercase letters (handle CamelCase)
    result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    result = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", result)

    # Clean up multiple underscores and lowercase
    result = re.sub(r"_+", "_", result).strip("_").lower()
    return result


def _is_valid_name(name: str) -> bool:
    """
    Check if a project name is valid for filesystem use.

    Args:
        name: Project name to validate.

    Returns:
        True if valid.
    """
    if not name or not name.strip():
        return False

    # Only allow alphanumeric, hyphens, underscores
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        return False

    # Check length
    if len(name) > 100:
        return False

    # Check reserved names
    reserved = {"con", "prn", "aux", "nul", "com1", "com2", "com3",
                "com4", "lpt1", "lpt2", "lpt3", ".", ".."}
    if name.lower() in reserved:
        return False

    return True


def _init_git(project_dir: Path) -> bool:
    """
    Initialize a git repository in the project directory.

    Args:
        project_dir: Path to initialize git in.

    Returns:
        True if successful.
    """
    try:
        subprocess.run(
            ["git", "init"],
            cwd=str(project_dir),
            capture_output=True,
            timeout=30,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return False


# ============================================================================
# CLI INTERFACE
# ============================================================================

def _build_parser() -> argparse.ArgumentParser:
    """Build the argparse CLI parser."""
    parser = argparse.ArgumentParser(
        prog="projforge",
        description="ProjForge - Project Scaffolding & Template Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  projforge create python-cli MyTool --var description="A useful tool"
  projforge create teambrain-standard DataWrangler --interactive
  projforge list --verbose
  projforge preview python-lib
  projforge info teambrain-standard

Built by: ATLAS (Team Brain)
For: Logan Smith / Metaphy LLC
GitHub: https://github.com/DonkRonk17/ProjForge
        """,
    )

    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # CREATE command
    create_parser = subparsers.add_parser(
        "create", help="Create a new project from template",
        description="Scaffold a new project directory from a template.",
    )
    create_parser.add_argument("template", help="Template name (use 'list' to see options)")
    create_parser.add_argument("name", help="Project name (PascalCase recommended)")
    create_parser.add_argument("--var", action="append", default=[],
                               metavar="KEY=VALUE",
                               help="Set template variable (can repeat)")
    create_parser.add_argument("--output", "-o", type=Path, default=None,
                               help="Output directory (default: current dir)")
    create_parser.add_argument("--interactive", "-i", action="store_true",
                               help="Prompt for missing variables")
    create_parser.add_argument("--git", action="store_true",
                               help="Initialize git repository")
    create_parser.add_argument("--dry-run", action="store_true",
                               help="Preview without creating files")

    # LIST command
    list_parser = subparsers.add_parser(
        "list", help="List available templates",
    )
    list_parser.add_argument("--verbose", "-v", action="store_true",
                             help="Show variable details")

    # PREVIEW command
    preview_parser = subparsers.add_parser(
        "preview", help="Preview template file structure",
    )
    preview_parser.add_argument("template", help="Template name")

    # INFO command
    info_parser = subparsers.add_parser(
        "info", help="Show detailed template information",
    )
    info_parser.add_argument("template", help="Template name")

    # TEMPLATE command
    template_parser = subparsers.add_parser(
        "template", help="Manage custom templates",
    )
    template_sub = template_parser.add_subparsers(dest="template_action")
    add_parser = template_sub.add_parser("add", help="Add custom template")
    add_parser.add_argument("path", type=Path, help="Path to template directory")

    return parser


def _parse_vars(var_list: List[str]) -> Dict[str, str]:
    """
    Parse KEY=VALUE pairs from --var arguments.

    Args:
        var_list: List of "KEY=VALUE" strings.

    Returns:
        Dictionary of key-value pairs.
    """
    result: Dict[str, str] = {}
    for item in var_list:
        if "=" in item:
            key, _, value = item.partition("=")
            result[key.strip()] = value.strip()
    return result


def main() -> None:
    """CLI entry point for ProjForge."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    forge = ProjForge()

    if args.command == "create":
        variables = _parse_vars(args.var)
        result = forge.create_project(
            template_name=args.template,
            project_name=args.name,
            variables=variables,
            output_dir=args.output,
            dry_run=args.dry_run,
            init_git=args.git,
            interactive=args.interactive,
        )

        if result.success:
            print(f"[OK] {result.message}")
        else:
            for err in result.errors:
                print(f"[X] Error: {err}")
            sys.exit(1)

    elif args.command == "list":
        print(forge.list_templates(verbose=getattr(args, "verbose", False)))

    elif args.command == "preview":
        print(forge.preview_template(args.template))

    elif args.command == "info":
        info = forge.get_template_info(args.template)
        if info is None:
            print(f"[X] Template '{args.template}' not found.")
            sys.exit(1)

        tag = "[built-in]" if info.is_builtin else "[custom]"
        print(f"Template: {info.name} {tag}")
        print(f"Description: {info.description}")
        print(f"Version: {info.version}")
        print(f"Author: {info.author}")
        print(f"Files: {info.file_count}")
        print(f"Directories: {info.dir_count}")
        print(f"\nVariables:")
        for var_name, var_def in info.variables.items():
            req = " (REQUIRED)" if var_def.get("required") else ""
            default = var_def.get("default", "")
            default_str = f" [default: {default}]" if default else ""
            desc = var_def.get("description", "")
            print(f"  {var_name}: {desc}{default_str}{req}")

    elif args.command == "template":
        if getattr(args, "template_action", None) == "add":
            success, msg = forge.add_template(args.path)
            if success:
                print(f"[OK] {msg}")
            else:
                print(f"[X] {msg}")
                sys.exit(1)
        else:
            parser.parse_args(["template", "--help"])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
