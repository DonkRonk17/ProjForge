#!/usr/bin/env python3
"""
Comprehensive test suite for ProjForge - Project Scaffolding & Template Engine.

Tests cover:
- Core functionality (template engine, variable resolution, file generation)
- Edge cases (empty inputs, invalid names, missing templates)
- Error handling (permissions, existing dirs, bad variables)
- Integration scenarios (end-to-end project creation, all templates)
- CLI interface (argument parsing)

Run: python test_projforge.py

Author: ATLAS (Team Brain)
For: Logan Smith / Metaphy LLC
Date: February 12, 2026
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from projforge import (
    VERSION,
    CreateResult,
    FileGenerator,
    ProjForge,
    TemplateEngine,
    TemplateInfo,
    TemplateStore,
    _build_parser,
    _is_valid_name,
    _parse_vars,
    _to_snake_case,
    BUILTIN_TEMPLATES,
)


class TestSnakeCaseConversion(unittest.TestCase):
    """Test the _to_snake_case utility function."""

    def test_pascal_case(self):
        """Test PascalCase to snake_case."""
        self.assertEqual(_to_snake_case("MyTool"), "my_tool")

    def test_camel_case(self):
        """Test camelCase to snake_case."""
        self.assertEqual(_to_snake_case("myTool"), "my_tool")

    def test_kebab_case(self):
        """Test kebab-case to snake_case."""
        self.assertEqual(_to_snake_case("my-cool-tool"), "my_cool_tool")

    def test_spaces(self):
        """Test name with spaces."""
        self.assertEqual(_to_snake_case("My Cool Tool"), "my_cool_tool")

    def test_already_snake(self):
        """Test already snake_case."""
        self.assertEqual(_to_snake_case("my_tool"), "my_tool")

    def test_all_caps(self):
        """Test ALL CAPS."""
        self.assertEqual(_to_snake_case("MYTOOL"), "mytool")

    def test_acronym(self):
        """Test names with acronyms."""
        self.assertEqual(_to_snake_case("HTTPClient"), "http_client")

    def test_single_word(self):
        """Test single word."""
        self.assertEqual(_to_snake_case("Tool"), "tool")

    def test_numbers(self):
        """Test name with numbers."""
        self.assertEqual(_to_snake_case("Tool2Go"), "tool2_go")


class TestNameValidation(unittest.TestCase):
    """Test the _is_valid_name utility function."""

    def test_valid_names(self):
        """Test valid project names."""
        valid = ["MyTool", "tool", "my-tool", "my_tool", "Tool123", "A"]
        for name in valid:
            self.assertTrue(_is_valid_name(name), f"{name} should be valid")

    def test_empty_name(self):
        """Test empty name is invalid."""
        self.assertFalse(_is_valid_name(""))

    def test_none_input(self):
        """Test None-like input."""
        self.assertFalse(_is_valid_name("   "))

    def test_starts_with_number(self):
        """Test name starting with number."""
        self.assertFalse(_is_valid_name("123tool"))

    def test_special_characters(self):
        """Test names with special characters."""
        invalid = ["my tool!", "tool@home", "my.tool", "tool/test"]
        for name in invalid:
            self.assertFalse(_is_valid_name(name), f"{name} should be invalid")

    def test_reserved_names(self):
        """Test Windows reserved names."""
        reserved = ["con", "prn", "aux", "nul", "COM1", "LPT1"]
        for name in reserved:
            self.assertFalse(_is_valid_name(name), f"{name} should be invalid")

    def test_too_long_name(self):
        """Test extremely long name."""
        self.assertFalse(_is_valid_name("A" * 101))

    def test_max_valid_length(self):
        """Test name at exactly max length."""
        self.assertTrue(_is_valid_name("A" * 100))


class TestVariableParsing(unittest.TestCase):
    """Test the _parse_vars function."""

    def test_simple_pair(self):
        """Test simple KEY=VALUE."""
        result = _parse_vars(["description=A cool tool"])
        self.assertEqual(result["description"], "A cool tool")

    def test_multiple_pairs(self):
        """Test multiple KEY=VALUE pairs."""
        result = _parse_vars(["author=Logan", "org=Metaphy"])
        self.assertEqual(result["author"], "Logan")
        self.assertEqual(result["org"], "Metaphy")

    def test_empty_value(self):
        """Test KEY= with empty value."""
        result = _parse_vars(["key="])
        self.assertEqual(result["key"], "")

    def test_value_with_equals(self):
        """Test value containing equals sign."""
        result = _parse_vars(["formula=a=b+c"])
        self.assertEqual(result["formula"], "a=b+c")

    def test_empty_list(self):
        """Test empty var list."""
        result = _parse_vars([])
        self.assertEqual(result, {})

    def test_no_equals(self):
        """Test entry without equals sign (should be skipped)."""
        result = _parse_vars(["noequals"])
        self.assertEqual(result, {})


class TestTemplateEngine(unittest.TestCase):
    """Test the TemplateEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = TemplateEngine()

    def test_render_simple_variable(self):
        """Test basic variable substitution."""
        result = self.engine.render_string("Hello {{name}}!", {"name": "World"})
        self.assertEqual(result, "Hello World!")

    def test_render_multiple_variables(self):
        """Test multiple variables in one string."""
        template = "{{name}} by {{author}} ({{year}})"
        result = self.engine.render_string(template, {
            "name": "MyTool", "author": "Logan", "year": "2026"
        })
        self.assertEqual(result, "MyTool by Logan (2026)")

    def test_render_with_default(self):
        """Test variable with default value."""
        result = self.engine.render_string("{{name:Unknown}}", {})
        self.assertEqual(result, "Unknown")

    def test_render_override_default(self):
        """Test variable override takes precedence over default."""
        result = self.engine.render_string("{{name:Unknown}}", {"name": "MyTool"})
        self.assertEqual(result, "MyTool")

    def test_render_unresolved_variable(self):
        """Test unresolved variable stays as-is."""
        result = self.engine.render_string("Hello {{undefined}}!", {})
        self.assertEqual(result, "Hello {{undefined}}!")

    def test_resolve_variables_derived(self):
        """Test auto-derived variables from project name."""
        resolved = self.engine.resolve_variables(
            "MyAwesomeTool", {}, {}
        )
        self.assertEqual(resolved["name"], "MyAwesomeTool")
        self.assertEqual(resolved["name_lower"], "my_awesome_tool")
        self.assertEqual(resolved["name_upper"], "MYAWESOMETOOL")
        self.assertIn("date", resolved)
        self.assertIn("year", resolved)

    def test_resolve_variables_user_override(self):
        """Test user-provided variables override defaults."""
        resolved = self.engine.resolve_variables(
            "Tool", {"author": "TestUser"}, {"author": {"default": "Default"}}
        )
        self.assertEqual(resolved["author"], "TestUser")

    def test_resolve_variables_auto_year(self):
        """Test 'auto' year resolves to current year."""
        resolved = self.engine.resolve_variables(
            "Tool", {}, {"year": {"default": "auto"}}
        )
        import datetime
        self.assertEqual(resolved["year"], str(datetime.datetime.now().year))

    def test_get_missing_variables(self):
        """Test finding missing required variables."""
        template = {
            "variables": {
                "name": {"required": True},
                "description": {"required": True},
                "author": {"default": "Default"},
            }
        }
        missing = self.engine.get_missing_variables(template, {})
        self.assertIn("description", missing)
        self.assertNotIn("author", missing)


class TestTemplateStore(unittest.TestCase):
    """Test the TemplateStore class."""

    def setUp(self):
        """Set up test fixtures."""
        self.store = TemplateStore()

    def test_list_builtin_templates(self):
        """Test listing built-in templates."""
        templates = self.store.list_all()
        names = [t.name for t in templates]
        self.assertIn("python-cli", names)
        self.assertIn("python-lib", names)
        self.assertIn("teambrain-standard", names)

    def test_get_builtin_template(self):
        """Test getting a built-in template by name."""
        tmpl = self.store.get_template("python-cli")
        self.assertIsNotNone(tmpl)
        self.assertEqual(tmpl["name"], "python-cli")

    def test_get_nonexistent_template(self):
        """Test getting a template that doesn't exist."""
        tmpl = self.store.get_template("nonexistent-template")
        self.assertIsNone(tmpl)

    def test_template_exists_builtin(self):
        """Test checking if built-in template exists."""
        self.assertTrue(self.store.template_exists("python-cli"))
        self.assertTrue(self.store.template_exists("python-lib"))
        self.assertTrue(self.store.template_exists("teambrain-standard"))

    def test_template_not_exists(self):
        """Test checking non-existent template."""
        self.assertFalse(self.store.template_exists("fake-template"))

    def test_builtin_template_has_files(self):
        """Test that built-in templates have files defined."""
        for name in ["python-cli", "python-lib", "teambrain-standard"]:
            tmpl = self.store.get_template(name)
            self.assertGreater(len(tmpl["files"]), 0,
                               f"{name} should have files")


class TestFileGenerator(unittest.TestCase):
    """Test the FileGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = FileGenerator()
        self.test_dir = Path(tempfile.mkdtemp(prefix="projforge_test_"))

    def tearDown(self):
        """Clean up test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_basic(self):
        """Test basic file generation."""
        template = {
            "directories": [],
            "files": {
                "hello.txt": "Hello {{name}}!",
            },
        }
        variables = {"name": "World"}
        output = self.test_dir / "TestProject"

        result = self.generator.generate(template, variables, output)
        self.assertTrue(result.success)
        self.assertEqual(result.files_created, 1)

        content = (output / "hello.txt").read_text()
        self.assertEqual(content, "Hello World!")

    def test_generate_with_directories(self):
        """Test generation with subdirectories."""
        template = {
            "directories": ["src", "tests"],
            "files": {
                "src/main.py": "# main",
                "tests/test_main.py": "# tests",
            },
        }
        output = self.test_dir / "TestProject"

        result = self.generator.generate(template, {}, output)
        self.assertTrue(result.success)
        self.assertTrue((output / "src").is_dir())
        self.assertTrue((output / "tests").is_dir())

    def test_generate_dry_run(self):
        """Test dry run doesn't create files."""
        template = {
            "directories": [],
            "files": {"test.txt": "content"},
        }
        output = self.test_dir / "DryRunProject"

        result = self.generator.generate(template, {}, output, dry_run=True)
        self.assertTrue(result.success)
        self.assertFalse(output.exists())
        self.assertIn("DRY RUN", result.message)

    def test_generate_nested_directories(self):
        """Test creating files in nested subdirectories."""
        template = {
            "directories": [],
            "files": {
                "a/b/c/deep.txt": "deep content",
            },
        }
        output = self.test_dir / "DeepProject"

        result = self.generator.generate(template, {}, output)
        self.assertTrue(result.success)
        self.assertTrue((output / "a" / "b" / "c" / "deep.txt").exists())

    def test_generate_variable_in_filename(self):
        """Test variable substitution in filenames."""
        template = {
            "directories": [],
            "files": {
                "{{name_lower}}.py": "# {{name}}",
            },
        }
        variables = {"name": "MyTool", "name_lower": "my_tool"}
        output = self.test_dir / "VarProject"

        result = self.generator.generate(template, variables, output)
        self.assertTrue(result.success)
        self.assertTrue((output / "my_tool.py").exists())


class TestProjForgeCore(unittest.TestCase):
    """Test the main ProjForge orchestrator."""

    def setUp(self):
        """Set up test fixtures."""
        self.forge = ProjForge()
        self.test_dir = Path(tempfile.mkdtemp(prefix="projforge_test_"))

    def tearDown(self):
        """Clean up test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_initialization(self):
        """Test ProjForge initializes correctly."""
        forge = ProjForge()
        self.assertIsNotNone(forge)
        self.assertIsNotNone(forge.store)
        self.assertIsNotNone(forge.engine)
        self.assertIsNotNone(forge.config)

    def test_create_python_cli(self):
        """Test creating a python-cli project end-to-end."""
        result = self.forge.create_project(
            template_name="python-cli",
            project_name="TestCLI",
            variables={"description": "A test CLI tool"},
            output_dir=self.test_dir,
        )
        self.assertTrue(result.success)
        self.assertEqual(result.files_created, 7)
        self.assertTrue((self.test_dir / "TestCLI" / "test_cli.py").exists())
        self.assertTrue((self.test_dir / "TestCLI" / "test_test_cli.py").exists())
        self.assertTrue((self.test_dir / "TestCLI" / "README.md").exists())

    def test_create_python_lib(self):
        """Test creating a python-lib project end-to-end."""
        result = self.forge.create_project(
            template_name="python-lib",
            project_name="TestLib",
            variables={"description": "A test library"},
            output_dir=self.test_dir,
        )
        self.assertTrue(result.success)
        self.assertTrue((self.test_dir / "TestLib" / "test_lib" / "__init__.py").exists())
        self.assertTrue((self.test_dir / "TestLib" / "test_lib" / "core.py").exists())
        self.assertTrue((self.test_dir / "TestLib" / "tests" / "test_core.py").exists())

    def test_create_teambrain_standard(self):
        """Test creating a teambrain-standard project end-to-end."""
        result = self.forge.create_project(
            template_name="teambrain-standard",
            project_name="TestBrain",
            variables={"description": "A Team Brain tool"},
            output_dir=self.test_dir,
        )
        self.assertTrue(result.success)
        self.assertEqual(result.files_created, 17)
        # Check all expected files
        proj = self.test_dir / "TestBrain"
        expected_files = [
            "test_brain.py", "test_test_brain.py", "README.md",
            "EXAMPLES.md", "CHEAT_SHEET.txt", "BUILD_COVERAGE_PLAN.md",
            "ARCHITECTURE.md", "INTEGRATION_PLAN.md", "LICENSE",
            "setup.py", ".gitignore", "requirements.txt",
        ]
        for f in expected_files:
            self.assertTrue((proj / f).exists(), f"{f} should exist")
        self.assertTrue((proj / "branding" / "BRANDING_PROMPTS.md").exists())

    def test_create_invalid_template(self):
        """Test creating with non-existent template."""
        result = self.forge.create_project(
            template_name="nonexistent",
            project_name="Test",
            output_dir=self.test_dir,
        )
        self.assertFalse(result.success)
        self.assertTrue(any("not found" in e for e in result.errors))

    def test_create_empty_name(self):
        """Test creating with empty project name."""
        result = self.forge.create_project(
            template_name="python-cli",
            project_name="",
            output_dir=self.test_dir,
        )
        self.assertFalse(result.success)

    def test_create_invalid_name(self):
        """Test creating with invalid project name."""
        result = self.forge.create_project(
            template_name="python-cli",
            project_name="123invalid!",
            output_dir=self.test_dir,
        )
        self.assertFalse(result.success)

    def test_create_existing_directory(self):
        """Test creating in already-existing non-empty directory."""
        # Create a project first
        self.forge.create_project(
            template_name="python-cli",
            project_name="ExistingProject",
            variables={"description": "First"},
            output_dir=self.test_dir,
        )
        # Try to create in same dir
        result = self.forge.create_project(
            template_name="python-cli",
            project_name="ExistingProject",
            variables={"description": "Second"},
            output_dir=self.test_dir,
        )
        self.assertFalse(result.success)
        self.assertTrue(any("already exists" in e for e in result.errors))

    def test_create_dry_run(self):
        """Test dry run mode."""
        result = self.forge.create_project(
            template_name="python-cli",
            project_name="DryProject",
            variables={"description": "Dry run test"},
            output_dir=self.test_dir,
            dry_run=True,
        )
        self.assertTrue(result.success)
        self.assertFalse((self.test_dir / "DryProject").exists())

    def test_list_templates(self):
        """Test listing templates returns formatted string."""
        output = self.forge.list_templates()
        self.assertIn("python-cli", output)
        self.assertIn("python-lib", output)
        self.assertIn("teambrain-standard", output)

    def test_list_templates_verbose(self):
        """Test verbose template listing includes variables."""
        output = self.forge.list_templates(verbose=True)
        self.assertIn("description", output)
        self.assertIn("required", output.lower())

    def test_preview_template(self):
        """Test template preview output."""
        output = self.forge.preview_template("python-cli")
        self.assertIn("python-cli", output)
        self.assertIn("File Structure", output)
        self.assertIn(".py", output)

    def test_preview_nonexistent_template(self):
        """Test preview of non-existent template."""
        output = self.forge.preview_template("fake")
        self.assertIn("not found", output)

    def test_get_template_info(self):
        """Test getting template info."""
        info = self.forge.get_template_info("python-cli")
        self.assertIsNotNone(info)
        self.assertEqual(info.name, "python-cli")
        self.assertTrue(info.is_builtin)
        self.assertGreater(info.file_count, 0)

    def test_get_template_info_nonexistent(self):
        """Test getting info for non-existent template."""
        info = self.forge.get_template_info("fake")
        self.assertIsNone(info)

    def test_variable_substitution_in_content(self):
        """Test variables are properly substituted in file contents."""
        result = self.forge.create_project(
            template_name="python-cli",
            project_name="VarTest",
            variables={"description": "Variable substitution test"},
            output_dir=self.test_dir,
        )
        self.assertTrue(result.success)

        # Read generated README and verify substitution
        readme = (self.test_dir / "VarTest" / "README.md").read_text(encoding="utf-8")
        self.assertIn("VarTest", readme)
        self.assertIn("Variable substitution test", readme)
        self.assertNotIn("{{name}}", readme)
        self.assertNotIn("{{description}}", readme)

    def test_generated_tests_pass(self):
        """Test that generated test suites actually pass."""
        self.forge.create_project(
            template_name="python-cli",
            project_name="PassingTests",
            variables={"description": "Test passing"},
            output_dir=self.test_dir,
        )
        proj = self.test_dir / "PassingTests"
        result = subprocess.run(
            [sys.executable, str(proj / "test_passing_tests.py")],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, f"Tests failed: {result.stderr}")


class TestProjForgeCLI(unittest.TestCase):
    """Test CLI argument parsing."""

    def test_parser_creation(self):
        """Test parser builds without error."""
        parser = _build_parser()
        self.assertIsNotNone(parser)

    def test_parse_create_command(self):
        """Test parsing create command."""
        parser = _build_parser()
        args = parser.parse_args(["create", "python-cli", "MyTool",
                                   "--var", "description=test"])
        self.assertEqual(args.command, "create")
        self.assertEqual(args.template, "python-cli")
        self.assertEqual(args.name, "MyTool")
        self.assertEqual(args.var, ["description=test"])

    def test_parse_list_command(self):
        """Test parsing list command."""
        parser = _build_parser()
        args = parser.parse_args(["list", "--verbose"])
        self.assertEqual(args.command, "list")
        self.assertTrue(args.verbose)

    def test_parse_preview_command(self):
        """Test parsing preview command."""
        parser = _build_parser()
        args = parser.parse_args(["preview", "python-cli"])
        self.assertEqual(args.command, "preview")
        self.assertEqual(args.template, "python-cli")

    def test_parse_create_with_options(self):
        """Test parsing create with all options."""
        parser = _build_parser()
        args = parser.parse_args([
            "create", "python-cli", "Tool",
            "--var", "a=1", "--var", "b=2",
            "--git", "--dry-run",
        ])
        self.assertTrue(args.git)
        self.assertTrue(args.dry_run)
        self.assertEqual(len(args.var), 2)


class TestCreateResult(unittest.TestCase):
    """Test the CreateResult data class."""

    def test_success_result(self):
        """Test creating a success result."""
        result = CreateResult(success=True, files_created=5, dirs_created=2)
        self.assertTrue(result.success)
        self.assertEqual(result.files_created, 5)
        self.assertEqual(result.dirs_created, 2)
        self.assertEqual(result.errors, [])

    def test_failure_result(self):
        """Test creating a failure result."""
        result = CreateResult(success=False, errors=["Something broke"])
        self.assertFalse(result.success)
        self.assertEqual(len(result.errors), 1)

    def test_default_values(self):
        """Test default values."""
        result = CreateResult(success=True)
        self.assertEqual(result.files_created, 0)
        self.assertEqual(result.dirs_created, 0)
        self.assertIsNone(result.project_path)
        self.assertEqual(result.message, "")


class TestTemplateInfo(unittest.TestCase):
    """Test the TemplateInfo data class."""

    def test_creation(self):
        """Test creating TemplateInfo."""
        info = TemplateInfo(
            name="test", description="Test template",
            version="1.0", author="Tester",
            variables={}, file_count=5, dir_count=2,
        )
        self.assertEqual(info.name, "test")
        self.assertEqual(info.file_count, 5)
        self.assertTrue(info.is_builtin)

    def test_repr(self):
        """Test string representation."""
        info = TemplateInfo(
            name="test", description="", version="1.0",
            author="", variables={}, file_count=0, dir_count=0,
        )
        self.assertIn("test", repr(info))


class TestBuiltinTemplateQuality(unittest.TestCase):
    """Verify quality of built-in templates."""

    def test_all_templates_have_required_fields(self):
        """Test all templates have required metadata."""
        for name, tmpl in BUILTIN_TEMPLATES.items():
            self.assertIn("name", tmpl, f"{name} missing 'name'")
            self.assertIn("description", tmpl, f"{name} missing 'description'")
            self.assertIn("files", tmpl, f"{name} missing 'files'")
            self.assertIn("variables", tmpl, f"{name} missing 'variables'")

    def test_all_templates_have_readme(self):
        """Test all templates include README.md."""
        for name, tmpl in BUILTIN_TEMPLATES.items():
            self.assertIn("README.md", tmpl["files"],
                          f"{name} missing README.md")

    def test_all_templates_have_license(self):
        """Test all templates include LICENSE."""
        for name, tmpl in BUILTIN_TEMPLATES.items():
            self.assertIn("LICENSE", tmpl["files"],
                          f"{name} missing LICENSE")

    def test_all_templates_have_gitignore(self):
        """Test all templates include .gitignore."""
        for name, tmpl in BUILTIN_TEMPLATES.items():
            self.assertIn(".gitignore", tmpl["files"],
                          f"{name} missing .gitignore")

    def test_teambrain_has_all_phases(self):
        """Test teambrain-standard has all Holy Grail files."""
        tmpl = BUILTIN_TEMPLATES["teambrain-standard"]
        required = [
            "BUILD_COVERAGE_PLAN.md", "BUILD_AUDIT.md",
            "ARCHITECTURE.md", "BUILD_REPORT.md",
            "INTEGRATION_PLAN.md", "QUICK_START_GUIDES.md",
            "INTEGRATION_EXAMPLES.md", "EXAMPLES.md",
            "CHEAT_SHEET.txt",
        ]
        for f in required:
            self.assertIn(f, tmpl["files"],
                          f"teambrain-standard missing {f}")

    def test_teambrain_has_branding(self):
        """Test teambrain-standard has branding prompts."""
        tmpl = BUILTIN_TEMPLATES["teambrain-standard"]
        self.assertIn("branding/BRANDING_PROMPTS.md", tmpl["files"])

    def test_no_unicode_emojis_in_python_templates(self):
        """Test Python template code has no Unicode emojis."""
        import re
        emoji_pattern = re.compile(
            "[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]"
        )
        for name, tmpl in BUILTIN_TEMPLATES.items():
            for file_path, content in tmpl["files"].items():
                if file_path.endswith(".py"):
                    matches = emoji_pattern.findall(content)
                    self.assertEqual(
                        len(matches), 0,
                        f"Unicode emoji found in {name}/{file_path}: {matches}"
                    )


def run_tests():
    """Run all tests with summary output."""
    print("=" * 70)
    print(f"TESTING: ProjForge v{VERSION}")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestSnakeCaseConversion,
        TestNameValidation,
        TestVariableParsing,
        TestTemplateEngine,
        TestTemplateStore,
        TestFileGenerator,
        TestProjForgeCore,
        TestProjForgeCLI,
        TestCreateResult,
        TestTemplateInfo,
        TestBuiltinTemplateQuality,
    ]

    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"RESULTS: {result.testsRun} tests | Passed: {passed} | "
          f"Failed: {len(result.failures)} | Errors: {len(result.errors)}")
    print("=" * 70)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
