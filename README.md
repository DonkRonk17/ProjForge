# 🏗️ ProjForge

> **Project Scaffolding & Template Engine** - Generate complete, ready-to-code project structures from built-in or custom templates in seconds.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/DonkRonk17/ProjForge)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-77%20passing-brightgreen.svg)](#testing)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)](#dependencies)

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Built-in Templates](#-built-in-templates)
- [Custom Templates](#-custom-templates)
- [Python API](#-python-api)
- [Real-World Results](#-real-world-results)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Use Cases](#-use-cases)
- [Testing](#-testing)
- [Integration](#-integration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Credits](#-credits)
- [License](#-license)

---

## 🚨 The Problem

When starting a new project, you have to:

- Manually create folder structures (5-10 minutes)
- Write boilerplate setup.py, requirements.txt, .gitignore from scratch
- Copy-paste test suite templates and adapt them
- Create README with proper sections (20-30 minutes for a good one)
- Remember all the standard files (LICENSE, setup.py, .gitignore)
- For Team Brain tools: create 17+ files across 9 build phases

**Result:** 30-60 minutes wasted on repetitive setup before writing a single line of real code. Inconsistencies creep in across projects. Files get forgotten.

### The Scale of the Problem

With 73+ tools in the Team Brain ecosystem, each requiring identical structure:
- **73 x 30 minutes = 36+ hours** wasted on project setup alone
- Inconsistent README formats across tools
- Missing LICENSE files, .gitignore variations
- Forgotten test suite templates
- No standardized Holy Grail Protocol structure

---

## ✅ The Solution

ProjForge generates complete project structures with a single command:

```bash
projforge create python-cli MyAwesomeTool --var "description=A really useful tool"
```

**That's it.** In under 2 seconds, you get:
- Main script with argparse CLI and class interface
- Complete test suite (ready to run)
- README.md with proper structure
- setup.py, requirements.txt, LICENSE, .gitignore
- All variables substituted (name, date, author, etc.)

### Real Impact

| Metric | Before ProjForge | After ProjForge |
|--------|-----------------|-----------------|
| Project setup time | 30-60 minutes | **2 seconds** |
| Files created manually | 7-17 per project | **0** |
| Consistency | Variable | **100% standardized** |
| Forgotten files | Common | **Impossible** |
| Test suite creation | 15-20 minutes | **Instant** |

---

## ✨ Features

- 🏗️ **3 Built-in Templates** - Python CLI, Python Library, Team Brain Standard
- 📝 **Smart Variable Substitution** - `{{name}}`, `{{name_lower}}`, auto-derived variants
- 🔄 **Custom Templates** - Create and reuse your own project templates
- 👁️ **Preview Mode** - See what will be created before committing (`--dry-run`)
- 💬 **Interactive Mode** - Prompts for missing variables (`--interactive`)
- 📊 **Template Info** - Detailed variable descriptions and file counts
- 🔧 **Git Integration** - Auto-initialize git repo (`--git`)
- 🖥️ **Cross-Platform** - Works on Windows, Linux, and macOS
- 📦 **Zero Dependencies** - Python standard library only
- ⚡ **Fast** - Projects generated in under 2 seconds
- 🧪 **Generated Tests Pass** - All generated test suites are immediately runnable
- 🎯 **Holy Grail Protocol** - Team Brain standard template includes all 9-phase files

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/ProjForge.git
cd ProjForge

# Verify it works
python projforge.py list
```

No installation required! No dependencies to install! Just clone and run.

### Your First Project

```bash
# Create a Python CLI tool
python projforge.py create python-cli MyCoolTool --var "description=A fantastic utility"

# See what was created
cd MyCoolTool
ls
```

**Output:**
```
[OK] Project created at ./MyCoolTool
  Files: 7
  Directories: 1
```

### Run the Generated Tests

```bash
cd MyCoolTool
python test_my_cool_tool.py
```

```
======================================================================
TESTING: MyCoolTool v1.0.0
======================================================================
test_initialization ... ok
test_run ... ok
test_config_defaults ... ok
test_invalid_config_path ... ok
----------------------------------------------------------------------
Ran 4 tests in 0.001s
OK
======================================================================
RESULTS: 4 tests | Passed: 4
======================================================================
```

**That's it! Your project is ready to code.**

---

## 📘 Usage

### CLI Commands

#### `create` - Create a New Project

```bash
projforge create <template> <name> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `--var KEY=VALUE` | Set template variable (repeatable) |
| `--output DIR` | Output directory (default: current) |
| `--interactive` | Prompt for missing variables |
| `--git` | Initialize git repository |
| `--dry-run` | Preview without creating files |

**Examples:**
```bash
# Basic creation
projforge create python-cli MyTool --var "description=Useful tool"

# Team Brain standard (full Holy Grail)
projforge create teambrain-standard DataEngine --var "description=Smart data processor"

# Python library
projforge create python-lib MyUtils --var "description=Utility library"

# Interactive mode (prompts for missing vars)
projforge create python-cli MyTool --interactive

# Preview what would be created
projforge create python-cli MyTool --var "description=Preview" --dry-run

# With git initialization
projforge create python-cli MyTool --var "description=Git ready" --git

# Custom output directory
projforge create python-cli MyTool --var "description=Custom dir" --output /tmp/projects
```

#### `list` - List Available Templates

```bash
projforge list           # Basic list
projforge list --verbose # Include variable details
```

#### `preview` - Preview Template Structure

```bash
projforge preview python-cli
projforge preview teambrain-standard
```

#### `info` - Detailed Template Information

```bash
projforge info python-cli
projforge info teambrain-standard
```

#### `template add` - Add Custom Template

```bash
projforge template add /path/to/my-template
```

---

## 📦 Built-in Templates

### 1. `python-cli` - Python CLI Tool

Standard Python CLI tool with argparse interface.

**Files created (7):**
```
MyTool/
  my_tool.py              # Main script with argparse CLI + class
  test_my_tool.py         # Unittest test suite (4 tests)
  README.md               # Standard README
  requirements.txt        # Dependencies (stdlib only)
  setup.py                # Package setup
  LICENSE                 # MIT License
  .gitignore              # Python gitignore
```

**Best for:** CLI utilities, automation scripts, standalone tools

### 2. `python-lib` - Python Library

Python library with package structure.

**Files created (9):**
```
MyLib/
  my_lib/
    __init__.py           # Package init with exports
    core.py               # Core module with main class
  tests/
    __init__.py
    test_core.py          # Test suite (4 tests)
  README.md
  requirements.txt
  setup.py
  LICENSE
  .gitignore
```

**Best for:** Reusable libraries, shared modules, pip packages

### 3. `teambrain-standard` - Full Holy Grail Protocol

Complete Team Brain tool with all 9-phase documentation.

**Files created (17):**
```
MyTool/
  my_tool.py              # Main script with CLI + class
  test_my_tool.py         # Comprehensive test suite (11 tests)
  README.md               # Professional README template
  EXAMPLES.md             # Usage examples template
  CHEAT_SHEET.txt         # Quick reference template
  BUILD_COVERAGE_PLAN.md  # Phase 1
  BUILD_AUDIT.md          # Phase 2
  ARCHITECTURE.md         # Phase 3
  BUILD_REPORT.md         # Phase 8
  INTEGRATION_PLAN.md     # Phase 7
  QUICK_START_GUIDES.md   # Phase 7
  INTEGRATION_EXAMPLES.md # Phase 7
  requirements.txt
  setup.py
  LICENSE
  .gitignore
  branding/
    BRANDING_PROMPTS.md   # DALL-E branding prompts
```

**Best for:** Team Brain tools, professional production tools, Holy Grail Protocol

---

## 🔧 Custom Templates

### Creating a Custom Template

1. Create a template directory:
```
my-template/
  template.json     # Metadata and variables
  files/            # Template files
    main.py
    tests/
      test_main.py
    README.md
```

2. Define `template.json`:
```json
{
  "name": "my-template",
  "description": "My custom project template",
  "version": "1.0",
  "author": "Your Name",
  "variables": {
    "name": {"description": "Project name", "required": true},
    "description": {"description": "Project description", "required": true},
    "author": {"description": "Author", "default": "Your Name"}
  }
}
```

3. Use `{{variable}}` placeholders in template files.

4. Register the template:
```bash
projforge template add /path/to/my-template
```

### Variable Syntax

| Syntax | Description |
|--------|-------------|
| `{{name}}` | Project name as provided |
| `{{name_lower}}` | snake_case version |
| `{{name_upper}}` | UPPER_CASE version |
| `{{name_snake}}` | snake_case version |
| `{{name_title}}` | Title Case version |
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{year}}` | Current year |
| `{{month}}` | Current month name |
| `{{var:default}}` | Variable with default value |

---

## 🐍 Python API

ProjForge provides a clean Python API for programmatic use:

```python
from projforge import ProjForge

# Initialize
forge = ProjForge()

# Create a project
result = forge.create_project(
    template_name="python-cli",
    project_name="MyTool",
    variables={"description": "A useful tool"},
    output_dir=Path("./projects"),
    init_git=True,
)

print(f"Success: {result.success}")
print(f"Files: {result.files_created}")
print(f"Path: {result.project_path}")
```

### API Reference

```python
# List templates
templates = forge.list_templates(verbose=True)

# Preview template structure
preview = forge.preview_template("python-cli")

# Get template info
info = forge.get_template_info("teambrain-standard")

# Add custom template
success, msg = forge.add_template(Path("/path/to/template"))
```

---

## 📊 Real-World Results

### Team Brain Impact

ProjForge was built specifically to address the scaffolding needs of the 73+ tool Team Brain ecosystem:

| Scenario | Before | After |
|----------|--------|-------|
| New Python CLI tool | 30 min setup | **2 sec** |
| Holy Grail Protocol tool | 60+ min setup | **2 sec** |
| Test suite creation | 15 min | **Instant** |
| README template | 10 min copy/paste | **Pre-filled** |
| Consistency across 73 tools | Variable | **Guaranteed** |

### Time Savings Calculator

```
Projects per month:     ~4 new tools
Time saved per project: 30-60 minutes
Monthly savings:        2-4 hours
Annual savings:         24-48 hours
```

---

## ⚙️ How It Works

### Architecture

```
CLI Interface (argparse)
    |
ProjForge Orchestrator
    |
+---+---+
|       |
Template    File
Engine      Generator
|
Template Store
(built-in + custom)
```

### Process Flow

1. **Parse** - CLI arguments parsed, variables collected
2. **Resolve** - Template loaded, variables resolved (auto-derived + user + defaults)
3. **Render** - Template strings processed with `{{variable}}` substitution
4. **Generate** - Files and directories created on disk
5. **Post-process** - Optional git init

### Variable Resolution Order

1. Auto-derived from project name (name_lower, name_upper, etc.)
2. Auto-generated (date, year, month)
3. Template defaults
4. Config file defaults
5. User-provided `--var` overrides (highest priority)

---

## ⚙️ Configuration

**Config file:** `~/.projforge/config.json`

```json
{
  "default_author": "Logan Smith",
  "default_org": "Metaphy LLC",
  "default_license": "MIT",
  "default_template": "python-cli",
  "auto_git": false
}
```

**Custom templates directory:** `~/.projforge/templates/`

---

## 🎯 Use Cases

### 1. Quick Prototype
```bash
projforge create python-cli QuickProto --var "description=Fast prototype"
cd QuickProto && python quick_proto.py run
```

### 2. Team Brain Tool Build
```bash
projforge create teambrain-standard NewTool --var "description=Cool new tool" --git
# All 17 files created, git initialized, ready for 9-phase build
```

### 3. Library Development
```bash
projforge create python-lib SharedUtils --var "description=Shared utilities"
# Package structure with __init__.py, core.py, tests ready
```

### 4. Batch Project Creation (with BatchRunner)
```bash
# Create multiple projects in sequence
projforge create python-cli ToolA --var "description=Tool A"
projforge create python-cli ToolB --var "description=Tool B"
projforge create python-cli ToolC --var "description=Tool C"
```

### 5. Explore Before Committing
```bash
# Preview what would be created
projforge preview teambrain-standard
projforge create teambrain-standard BigProject --var "description=Big" --dry-run
```

---

## 🧪 Testing

### Run the Test Suite

```bash
python test_projforge.py
```

### Test Coverage

| Category | Tests | Status |
|----------|-------|--------|
| Snake Case Conversion | 9 | Passing |
| Name Validation | 8 | Passing |
| Variable Parsing | 6 | Passing |
| Template Engine | 9 | Passing |
| Template Store | 6 | Passing |
| File Generator | 5 | Passing |
| ProjForge Core | 16 | Passing |
| CLI Interface | 5 | Passing |
| Data Classes | 5 | Passing |
| Template Quality | 8 | Passing |
| **TOTAL** | **77** | **100% Passing** |

### What's Tested

- Core variable substitution and rendering
- All 3 built-in templates (end-to-end creation)
- Edge cases (empty names, invalid names, reserved names)
- Error handling (missing templates, existing directories)
- CLI argument parsing
- Dry-run mode
- Generated tests actually pass
- No Unicode emojis in Python templates
- Cross-platform path handling

---

## 🔗 Integration

### With ToolRegistry
```python
from projforge import ProjForge
from toolregistry import ToolRegistry

forge = ProjForge()
registry = ToolRegistry()

# Create project
result = forge.create_project("python-cli", "NewTool",
    variables={"description": "New tool"})

# Register it
if result.success:
    registry.register(result.project_path)
```

### With GitFlow
```bash
# Create and git-initialize
projforge create python-cli MyTool --var "description=Tool" --git
cd MyTool
gitflow commit "Initial scaffold from ProjForge"
```

### With SynapseLink
```python
from projforge import ProjForge
from synapselink import quick_send

forge = ProjForge()
result = forge.create_project("teambrain-standard", "CoolTool",
    variables={"description": "A cool tool"})

if result.success:
    quick_send("TEAM", "New Project Scaffolded",
               f"CoolTool created with {result.files_created} files")
```

**See:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for complete integration guide.

---

## 🔍 Troubleshooting

### Common Issues

**"Directory already exists and is not empty"**
```bash
# The target directory already has files. Either:
# 1. Choose a different name
# 2. Delete the existing directory
# 3. Use --output to specify a different location
projforge create python-cli MyTool --output /new/location
```

**"Template not found"**
```bash
# Check available templates
projforge list

# Verify template name (case-sensitive)
projforge info python-cli
```

**"Invalid project name"**
```bash
# Names must:
# - Start with a letter
# - Contain only letters, numbers, hyphens, underscores
# - Not be Windows reserved names (CON, PRN, etc.)
# - Be under 100 characters

# Good: MyTool, data-processor, tool_v2
# Bad: 123tool, my tool!, con
```

**Generated tests fail on Windows**
```bash
# If temp file tests fail, ensure you have write permissions
# to the system temp directory
python -c "import tempfile; print(tempfile.gettempdir())"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python test_projforge.py` (must be 100% passing)
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create a Pull Request

### Code Style

- Type hints on all public functions
- Docstrings with Args/Returns/Example
- No Unicode emojis in Python code (use [OK], [X], [!])
- Cross-platform path handling (use pathlib)

---

## 📝 Credits

**Built by:** ATLAS (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Requested by:** Self-initiated (Identified gap in 73+ tool ecosystem)  
**Why:** Save 30-60 minutes per project, ensure consistency across all tools  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** February 12, 2026  

**Special Thanks:**
- Logan Smith for the vision of standardized, professional-quality tools
- Forge for the Holy Grail Protocol and Build Protocol v1 methodology
- The Team Brain collective for building 73+ tools that demonstrated the need

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

Copyright (c) 2026 Logan Smith / Metaphy LLC

---

## 📚 Additional Resources

- **Examples:** [EXAMPLES.md](EXAMPLES.md) - 10+ working examples
- **Quick Reference:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt) - Printable cheat sheet
- **Integration:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Team Brain integration guide
- **Quick Starts:** [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md) - Agent-specific guides
- **GitHub:** [https://github.com/DonkRonk17/ProjForge](https://github.com/DonkRonk17/ProjForge)
- **Issues:** [https://github.com/DonkRonk17/ProjForge/issues](https://github.com/DonkRonk17/ProjForge/issues)

---

**Built with precision, deployed with pride.**  
**Team Brain Standard: 99%+ Quality, Every Time.**  
**For the Maximum Benefit of Life. One World. One Family. One Love.** 🔆
