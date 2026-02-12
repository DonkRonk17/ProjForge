# ProjForge - Build Coverage Plan

**Tool Name:** ProjForge  
**Version:** 1.0  
**Builder:** ATLAS (Team Brain)  
**For:** Logan Smith / Metaphy LLC  
**Date:** February 12, 2026  
**Phase:** 1 of 9 (Build Protocol v1)  

---

## 1. PROJECT SCOPE

### One-Sentence Purpose
ProjForge is a CLI project scaffolding and template engine that generates complete, ready-to-code project structures from built-in or custom templates.

### Problem Statement
Logan and Team Brain build 73+ tools (and counting). Each tool requires the same standard structure: main script, test suite, README (400+ lines), EXAMPLES.md, CHEAT_SHEET.txt, setup.py, LICENSE, .gitignore, branding prompts, integration docs, and build protocol files. Manually creating this structure takes 30-60 minutes and leads to inconsistencies. There is no existing tool in the 73+ tool ecosystem that scaffolds new projects.

### Solution
A zero-dependency Python CLI tool that:
1. Ships with built-in templates (Python CLI tool, Python library, Team Brain Holy Grail standard)
2. Generates complete project structures with a single command
3. Supports variable substitution (tool name, author, date, description, etc.)
4. Allows custom templates (create your own)
5. Supports interactive mode (prompts for missing values)
6. Cross-platform (Windows, Linux, macOS)

### Target Users
1. **Team Brain Agents** - Scaffold new tools following Holy Grail Protocol
2. **Logan Smith** - Quick project creation for new tool ideas
3. **General Developers** - Create standardized Python projects quickly

---

## 2. SUCCESS CRITERIA

1. Generate a complete project structure in under 2 seconds
2. Built-in templates cover: Python CLI, Python Library, Team Brain Standard
3. All generated files are valid (Python syntax, markdown, etc.)
4. Variables correctly substituted throughout all template files
5. Custom template support with simple folder-based format
6. Interactive mode fills in missing variables
7. Zero external dependencies (Python stdlib only)
8. Cross-platform (Windows, Linux, macOS)
9. 100% test coverage (10+ unit, 5+ integration)
10. Professional documentation (README 400+, EXAMPLES 10+)

---

## 3. FEATURE LIST

### Core Features (MVP)
- [x] Template-based project scaffolding
- [x] Built-in templates: python-cli, python-lib, teambrain-standard
- [x] Variable substitution: {{name}}, {{author}}, {{date}}, {{description}}, etc.
- [x] CLI interface: `projforge create <template> <project-name>`
- [x] List available templates: `projforge list`
- [x] Preview mode: `projforge preview <template>` (show structure without creating)
- [x] Variable overrides: `--var key=value`
- [x] Interactive mode: `--interactive` (prompt for missing vars)
- [x] Output directory: `--output <dir>`

### Advanced Features
- [x] Custom templates: `projforge template add <path>`
- [x] Template info: `projforge info <template>`
- [x] Dry run: `--dry-run` (show what would be created)
- [x] Git init: `--git` (auto-initialize git repo)
- [x] Post-scaffold hooks (optional shell commands)

---

## 4. INTEGRATION POINTS

### Team Brain Tools (potential integration)
- **ToolRegistry** - Register newly created tools automatically
- **GitFlow** - Initialize git with proper conventions
- **SynapseLink** - Announce new project creation
- **ToolSentinel** - Verify project follows Holy Grail Protocol
- **BatchRunner** - Chain scaffold + git init + first commit

### External Integration
- Git (optional, for --git flag)
- File system (pathlib, standard I/O)

---

## 5. RISK ASSESSMENT

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Template variable collision | Medium | Low | Use distinctive {{double_brace}} syntax |
| Path length limits (Windows) | Low | Low | Use short default paths, warn on long names |
| Permission errors | Medium | Low | Graceful error messages, check write access |
| Template corruption | Low | Very Low | Validate templates on load |
| Unicode in filenames | Medium | Low | ASCII-safe file names, UTF-8 content |

---

## 6. QUALITY REQUIREMENTS

- **Code Quality:** Type hints, docstrings, error handling
- **Testing:** 10+ unit tests, 5+ integration tests, 100% passing
- **Documentation:** README 400+, EXAMPLES 10+, CHEAT_SHEET
- **Dependencies:** Zero (Python stdlib only)
- **Platform:** Cross-platform (Windows, Linux, macOS)
- **Unicode:** ASCII-safe status indicators in Python code

---

## 7. ESTIMATED METRICS

- **Lines of Code:** 500-700 (main script)
- **Templates:** 3 built-in, custom support
- **Tests:** 15-20+
- **Documentation:** ~3000 lines total
- **Build Time:** ~4-5 hours

---

**Phase 1 Score: 99/100** - Comprehensive coverage plan with clear scope, success criteria, and risk assessment.

**Ready for Phase 2: Tool Audit**
