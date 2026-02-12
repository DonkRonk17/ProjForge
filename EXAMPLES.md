# ProjForge - Usage Examples

> 10+ working examples from basic to advanced, covering all features.

---

## Quick Navigation

1. [Example 1: Your First Project](#example-1-your-first-project)
2. [Example 2: Team Brain Standard Tool](#example-2-team-brain-standard-tool)
3. [Example 3: Python Library Package](#example-3-python-library-package)
4. [Example 4: Exploring Templates](#example-4-exploring-templates)
5. [Example 5: Dry Run Preview](#example-5-dry-run-preview)
6. [Example 6: Interactive Mode](#example-6-interactive-mode)
7. [Example 7: Custom Variables](#example-7-custom-variables)
8. [Example 8: Git Integration](#example-8-git-integration)
9. [Example 9: Python API Usage](#example-9-python-api-usage)
10. [Example 10: Custom Output Directory](#example-10-custom-output-directory)
11. [Example 11: Generated Tests Verification](#example-11-generated-tests-verification)
12. [Example 12: Full Production Workflow](#example-12-full-production-workflow)

---

## Example 1: Your First Project

**Scenario:** You need a new Python CLI tool quickly.

**Steps:**
```bash
# Create a Python CLI project
python projforge.py create python-cli FileOrganizer --var "description=Smart file organization tool"
```

**Expected Output:**
```
[OK] Project created at ./FileOrganizer
  Files: 7
  Directories: 1
```

**Verify:**
```bash
cd FileOrganizer
python file_organizer.py run
```

**Output:**
```
[OK] FileOrganizer executed successfully
```

**What You Learned:**
- Basic `create` syntax: `projforge create <template> <name> --var "KEY=VALUE"`
- ProjForge auto-derives `file_organizer` from `FileOrganizer` for filenames

---

## Example 2: Team Brain Standard Tool

**Scenario:** You need a full Holy Grail Protocol tool with all 9-phase documentation.

**Steps:**
```bash
python projforge.py create teambrain-standard SmartCache \
  --var "description=Intelligent caching layer for Team Brain" \
  --var "builder=ATLAS" \
  --var "requested_by=FORGE"
```

**Expected Output:**
```
[OK] Project created at ./SmartCache
  Files: 17
  Directories: 2
```

**Files Created:**
```
SmartCache/
  smart_cache.py              # Main script
  test_smart_cache.py         # 11 tests
  README.md                   # Professional template
  EXAMPLES.md                 # Usage examples
  CHEAT_SHEET.txt             # Quick reference
  BUILD_COVERAGE_PLAN.md      # Phase 1
  BUILD_AUDIT.md              # Phase 2
  ARCHITECTURE.md             # Phase 3
  BUILD_REPORT.md             # Phase 8
  INTEGRATION_PLAN.md         # Phase 7
  QUICK_START_GUIDES.md       # Phase 7
  INTEGRATION_EXAMPLES.md     # Phase 7
  requirements.txt
  setup.py
  LICENSE
  .gitignore
  branding/BRANDING_PROMPTS.md
```

**What You Learned:**
- The `teambrain-standard` template creates ALL documentation files
- Multiple `--var` flags can be used
- Build protocol files are pre-created (fill in during each phase)

---

## Example 3: Python Library Package

**Scenario:** You need a reusable library with proper package structure.

**Steps:**
```bash
python projforge.py create python-lib DataUtils --var "description=Shared data utility functions"
```

**Expected Output:**
```
[OK] Project created at ./DataUtils
  Files: 9
  Directories: 3
```

**Package Structure:**
```
DataUtils/
  data_utils/
    __init__.py     # Package with exports
    core.py         # Main module
  tests/
    __init__.py
    test_core.py    # Test suite
  README.md
  setup.py
  ...
```

**Test immediately:**
```bash
cd DataUtils
python -m pytest tests/ -v
```

---

## Example 4: Exploring Templates

**Scenario:** You want to see what templates are available and what they contain.

**Steps:**
```bash
# List all templates
python projforge.py list

# List with variable details
python projforge.py list --verbose

# Preview a template structure
python projforge.py preview teambrain-standard

# Get detailed info about a template
python projforge.py info python-cli
```

**Expected Output (list --verbose):**
```
Available Templates:
============================================================

  python-cli [built-in]
    Standard Python CLI tool with argparse, tests, and documentation
    Files: 7 | Dirs: 0
    Variables:
      {{  name  }} - Project name (PascalCase) (required)
      {{  description  }} - One-line project description (required)
      {{  author  }} - Author name [default: Logan Smith]
      ...

  python-lib [built-in]
    Python library package with module structure, tests, and docs
    ...

  teambrain-standard [built-in]
    Full Holy Grail Protocol standard
    ...

============================================================
Total: 3 templates
```

---

## Example 5: Dry Run Preview

**Scenario:** You want to see what would be created without actually creating anything.

**Steps:**
```bash
python projforge.py create python-cli PreviewTool --var "description=Just checking" --dry-run
```

**Expected Output:**
```
[OK] DRY RUN - No files created. Would create:
  ./PreviewTool/
  ./PreviewTool/.gitignore
  ./PreviewTool/LICENSE
  ./PreviewTool/README.md
  ./PreviewTool/requirements.txt
  ./PreviewTool/setup.py
  ./PreviewTool/test_preview_tool.py
  ./PreviewTool/preview_tool.py
```

**What You Learned:**
- `--dry-run` shows exact files that would be created
- No files are written to disk
- Great for verifying before committing

---

## Example 6: Interactive Mode

**Scenario:** You want to be prompted for missing variables.

**Steps:**
```bash
python projforge.py create python-cli InteractiveTool --interactive
```

**Expected Interaction:**
```
  description (One-line project description): A tool built interactively
  author (Author name) [Logan Smith]: Jane Doe
  org (Organization) [Metaphy LLC]:

[OK] Project created at ./InteractiveTool
  Files: 7
  Directories: 1
```

**What You Learned:**
- `--interactive` prompts for all required variables
- Defaults are shown in [brackets]
- Press Enter to accept defaults

---

## Example 7: Custom Variables

**Scenario:** You want to override default author and organization.

**Steps:**
```bash
python projforge.py create python-cli ClientTool \
  --var "description=Client project tool" \
  --var "author=Jane Doe" \
  --var "org=Acme Corp" \
  --var "year=2026"
```

**Verify in generated LICENSE:**
```
MIT License
Copyright (c) 2026 Jane Doe / Acme Corp
```

**What You Learned:**
- Any variable can be overridden with `--var`
- Variables propagate to all generated files

---

## Example 8: Git Integration

**Scenario:** You want your project git-ready from the start.

**Steps:**
```bash
python projforge.py create python-cli GitReadyTool \
  --var "description=Ready for version control" \
  --git
```

**Expected Output:**
```
[OK] Project created at ./GitReadyTool
  Files: 7
  Directories: 1
  Git: Initialized
```

**Verify:**
```bash
cd GitReadyTool
git status
```

```
On branch main
Untracked files:
  .gitignore
  LICENSE
  README.md
  ...
```

---

## Example 9: Python API Usage

**Scenario:** You want to create projects programmatically.

**Code:**
```python
from pathlib import Path
from projforge import ProjForge

# Initialize ProjForge
forge = ProjForge()

# Create a project
result = forge.create_project(
    template_name="python-cli",
    project_name="AutoCreated",
    variables={"description": "Created via Python API"},
    output_dir=Path("./output"),
)

# Check result
if result.success:
    print(f"Created at: {result.project_path}")
    print(f"Files: {result.files_created}")
    print(f"Dirs: {result.dirs_created}")
else:
    print(f"Errors: {result.errors}")
```

**API Methods:**
```python
# List templates
print(forge.list_templates(verbose=True))

# Preview structure
print(forge.preview_template("teambrain-standard"))

# Get template info
info = forge.get_template_info("python-cli")
print(f"Template: {info.name}, Files: {info.file_count}")

# Add custom template
success, msg = forge.add_template(Path("/path/to/template"))
```

---

## Example 10: Custom Output Directory

**Scenario:** You want to create the project in a specific location.

**Steps:**
```bash
# Create in specific directory
python projforge.py create python-cli RemoteTool \
  --var "description=Remote management tool" \
  --output "D:\Projects\SpecialTools"
```

**Expected Output:**
```
[OK] Project created at D:\Projects\SpecialTools\RemoteTool
  Files: 7
  Directories: 1
```

---

## Example 11: Generated Tests Verification

**Scenario:** Verify that ALL generated templates produce working code.

**Steps:**
```bash
# Test python-cli generated code
python projforge.py create python-cli TestA --var "description=Test A" --output /tmp/verify
cd /tmp/verify/TestA
python test_test_a.py

# Test teambrain-standard generated code
python projforge.py create teambrain-standard TestB --var "description=Test B" --output /tmp/verify
cd /tmp/verify/TestB
python test_test_b.py
```

**All generated tests should pass 100%.**

---

## Example 12: Full Production Workflow

**Scenario:** Complete end-to-end workflow for building a Team Brain tool.

**Steps:**
```bash
# Step 1: Scaffold the project
python projforge.py create teambrain-standard SmartAnalyzer \
  --var "description=Intelligent code analysis tool" \
  --var "builder=ATLAS" \
  --var "requested_by=FORGE" \
  --git

# Step 2: Verify structure
cd SmartAnalyzer
ls

# Step 3: Run generated tests (should pass)
python test_smart_analyzer.py

# Step 4: Start implementing! Edit smart_analyzer.py
# - All boilerplate is ready
# - Test suite is ready to extend
# - Build protocol files ready to fill in
# - Integration docs ready for Phase 7

# Step 5: Build following the protocol
# Phase 1: Fill in BUILD_COVERAGE_PLAN.md
# Phase 2: Fill in BUILD_AUDIT.md
# Phase 3: Fill in ARCHITECTURE.md
# Phase 4: Implement smart_analyzer.py (already has skeleton!)
# Phase 5: Extend test_smart_analyzer.py
# Phase 6: Enhance README.md, EXAMPLES.md, CHEAT_SHEET.txt
# Phase 7: Complete INTEGRATION_PLAN.md, QUICK_START_GUIDES.md
# Phase 8: Fill in BUILD_REPORT.md
# Phase 9: Push to GitHub
```

**What You Learned:**
- ProjForge eliminates all setup time
- You can immediately focus on implementation
- All build protocol files are pre-created
- The workflow is standardized and repeatable

---

## 📚 More Resources

- **README:** [README.md](README.md) - Full documentation
- **Cheat Sheet:** [CHEAT_SHEET.txt](CHEAT_SHEET.txt) - Quick reference
- **Integration:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Team Brain integration

---

**Built by:** ATLAS (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Date:** February 12, 2026
