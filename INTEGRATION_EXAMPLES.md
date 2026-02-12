# ProjForge - Integration Examples

> Copy-paste-ready code examples for common integration patterns.

---

## Table of Contents

1. [Pattern 1: ProjForge + ToolRegistry](#pattern-1-projforge--toolregistry)
2. [Pattern 2: ProjForge + SynapseLink](#pattern-2-projforge--synapselink)
3. [Pattern 3: ProjForge + GitFlow](#pattern-3-projforge--gitflow)
4. [Pattern 4: ProjForge + ToolSentinel](#pattern-4-projforge--toolsentinel)
5. [Pattern 5: ProjForge + BatchRunner](#pattern-5-projforge--batchrunner)
6. [Pattern 6: ProjForge + AgentHealth](#pattern-6-projforge--agenthealth)
7. [Pattern 7: ProjForge + SessionReplay](#pattern-7-projforge--sessionreplay)
8. [Pattern 8: ProjForge + TaskQueuePro](#pattern-8-projforge--taskqueuepro)
9. [Pattern 9: Multi-Tool Build Pipeline](#pattern-9-multi-tool-build-pipeline)
10. [Pattern 10: Full Team Brain Workflow](#pattern-10-full-team-brain-workflow)

---

## Pattern 1: ProjForge + ToolRegistry

**Use Case:** Auto-register newly created tools in the central registry.

**Code:**
```python
from pathlib import Path
from projforge import ProjForge

# Step 1: Scaffold the project
forge = ProjForge()
result = forge.create_project(
    template_name="teambrain-standard",
    project_name="SmartCache",
    variables={"description": "Intelligent caching layer"},
    init_git=True,
)

# Step 2: Register in ToolRegistry
if result.success:
    # Import ToolRegistry
    import sys
    sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects/ToolRegistry"))
    from toolregistry import ToolRegistry

    registry = ToolRegistry()
    registry.register_tool(
        name="SmartCache",
        path=str(result.project_path),
        description="Intelligent caching layer",
        status="in_progress",
        builder="ATLAS",
    )
    print(f"[OK] Registered SmartCache in ToolRegistry")
```

**Result:** New tool scaffolded AND registered in central catalog.

---

## Pattern 2: ProjForge + SynapseLink

**Use Case:** Announce new project creation to Team Brain.

**Code:**
```python
from pathlib import Path
from projforge import ProjForge

forge = ProjForge()
result = forge.create_project("teambrain-standard", "DataEngine",
    variables={"description": "Smart data processing engine"})

if result.success:
    import sys
    sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects/SynapseLink"))
    from synapselink import quick_send

    quick_send(
        "TEAM",
        "New Project Scaffolded: DataEngine",
        f"Tool: DataEngine\n"
        f"Template: teambrain-standard\n"
        f"Files: {result.files_created}\n"
        f"Path: {result.project_path}\n"
        f"Status: Ready for implementation\n"
        f"Scaffolded by: ATLAS via ProjForge",
        priority="NORMAL",
    )
```

**Result:** Team stays informed of new project creation automatically.

---

## Pattern 3: ProjForge + GitFlow

**Use Case:** Scaffold, init git, and make first commit.

**Code (CLI):**
```bash
# Scaffold with git
projforge create python-cli MyTool --var "description=Useful tool" --git

# Use GitFlow for conventional commit
cd MyTool
python ../GitFlow/gitflow.py commit "feat: initial scaffold from ProjForge"
```

**Code (Python):**
```python
from pathlib import Path
from projforge import ProjForge
import subprocess

forge = ProjForge()
result = forge.create_project("python-cli", "MyTool",
    variables={"description": "Useful tool"}, init_git=True)

if result.success:
    # Add and commit all files
    subprocess.run(["git", "add", "."], cwd=str(result.project_path))
    subprocess.run(["git", "commit", "-m",
        "feat: initial scaffold from ProjForge"],
        cwd=str(result.project_path))
```

**Result:** Project scaffolded with proper git history from day one.

---

## Pattern 4: ProjForge + ToolSentinel

**Use Case:** Verify scaffolded project meets Holy Grail Protocol.

**Code:**
```python
from projforge import ProjForge

forge = ProjForge()

# Always use teambrain-standard to guarantee compliance
result = forge.create_project("teambrain-standard", "CompliantTool",
    variables={"description": "Fully compliant tool"})

if result.success:
    # ToolSentinel can verify all required files exist
    required_files = [
        "compliant_tool.py", "test_compliant_tool.py",
        "README.md", "EXAMPLES.md", "CHEAT_SHEET.txt",
        "BUILD_COVERAGE_PLAN.md", "ARCHITECTURE.md",
        "INTEGRATION_PLAN.md", "LICENSE", "setup.py",
    ]

    all_present = all(
        (result.project_path / f).exists() for f in required_files
    )
    print(f"Holy Grail compliance: {'PASS' if all_present else 'FAIL'}")
```

**Result:** Guaranteed compliance with all protocol requirements.

---

## Pattern 5: ProjForge + BatchRunner

**Use Case:** Create multiple projects in a batch pipeline.

**Code:**
```python
from projforge import ProjForge

forge = ProjForge()

# Batch project creation
projects = [
    ("ToolA", "First batch tool"),
    ("ToolB", "Second batch tool"),
    ("ToolC", "Third batch tool"),
]

results = []
for name, desc in projects:
    result = forge.create_project("python-cli", name,
        variables={"description": desc}, init_git=True)
    results.append((name, result.success))
    print(f"  {name}: {'[OK]' if result.success else '[X]'}")

# Summary
success = sum(1 for _, s in results if s)
print(f"\nBatch complete: {success}/{len(projects)} projects created")
```

**Result:** Multiple projects scaffolded efficiently in one session.

---

## Pattern 6: ProjForge + AgentHealth

**Use Case:** Track scaffolding activity in agent health monitoring.

**Code:**
```python
from projforge import ProjForge

forge = ProjForge()

# Log scaffolding as agent activity
activity_log = []

result = forge.create_project("teambrain-standard", "HealthTool",
    variables={"description": "Health monitoring integration"})

activity_log.append({
    "action": "scaffold",
    "tool": "HealthTool",
    "success": result.success,
    "files": result.files_created,
    "template": "teambrain-standard",
})

# AgentHealth can track this activity
print(f"Activity logged: {activity_log[-1]}")
```

**Result:** Scaffolding activity tracked alongside other agent metrics.

---

## Pattern 7: ProjForge + SessionReplay

**Use Case:** Record scaffolding decisions for debugging and review.

**Code:**
```python
from projforge import ProjForge

forge = ProjForge()

# Record what was scaffolded for session replay
session_events = []

session_events.append({
    "event": "scaffold_start",
    "template": "teambrain-standard",
    "project": "ReplayTool",
})

result = forge.create_project("teambrain-standard", "ReplayTool",
    variables={"description": "Session replay integration"})

session_events.append({
    "event": "scaffold_complete",
    "success": result.success,
    "files": result.files_created,
    "path": str(result.project_path),
})

# SessionReplay can record these events
for event in session_events:
    print(f"  [{event['event']}] {event}")
```

**Result:** Full audit trail of project scaffolding decisions.

---

## Pattern 8: ProjForge + TaskQueuePro

**Use Case:** Create tasks for each phase after scaffolding.

**Code:**
```python
from projforge import ProjForge

forge = ProjForge()
result = forge.create_project("teambrain-standard", "QueuedTool",
    variables={"description": "Task queue integration"})

if result.success:
    # Create tasks for each build phase
    phases = [
        "Phase 1: Fill BUILD_COVERAGE_PLAN.md",
        "Phase 2: Fill BUILD_AUDIT.md",
        "Phase 3: Fill ARCHITECTURE.md",
        "Phase 4: Implement queued_tool.py",
        "Phase 5: Extend test_queued_tool.py",
        "Phase 6: Enhance README, EXAMPLES, CHEAT_SHEET",
        "Phase 7: Complete integration docs",
        "Phase 8: Fill BUILD_REPORT.md",
        "Phase 9: Deploy to GitHub",
    ]

    for i, phase in enumerate(phases, 1):
        print(f"  Task {i}: {phase}")

    # TaskQueuePro could auto-create these tasks
    print(f"\n9 build tasks created for QueuedTool")
```

**Result:** Automated task creation from scaffold structure.

---

## Pattern 9: Multi-Tool Build Pipeline

**Use Case:** Complete workflow using ProjForge with multiple tools.

**Code:**
```python
from pathlib import Path
from projforge import ProjForge

forge = ProjForge()

# Step 1: Scaffold
print("Step 1: Scaffolding...")
result = forge.create_project("teambrain-standard", "PipelineTool",
    variables={
        "description": "Multi-tool pipeline integration",
        "builder": "ATLAS",
        "requested_by": "FORGE",
    }, init_git=True)

if result.success:
    print(f"  [OK] Created {result.files_created} files")

    # Step 2: Verify scaffold quality
    print("Step 2: Verifying quality...")
    proj = result.project_path
    checks = {
        "Main script": (proj / "pipeline_tool.py").exists(),
        "Test suite": (proj / "test_pipeline_tool.py").exists(),
        "README": (proj / "README.md").exists(),
        "Integration docs": (proj / "INTEGRATION_PLAN.md").exists(),
        "Branding": (proj / "branding" / "BRANDING_PROMPTS.md").exists(),
    }
    for check, passed in checks.items():
        print(f"  {'[OK]' if passed else '[X]'} {check}")

    # Step 3: Run generated tests
    print("Step 3: Running tests...")
    import subprocess, sys
    test_result = subprocess.run(
        [sys.executable, str(proj / "test_pipeline_tool.py")],
        capture_output=True, text=True)
    print(f"  Tests: {'PASS' if test_result.returncode == 0 else 'FAIL'}")

    # Step 4: Summary
    print(f"\nPipeline complete!")
    print(f"  Project: {proj}")
    print(f"  Files: {result.files_created}")
    print(f"  Tests: {'Passing' if test_result.returncode == 0 else 'Failing'}")
```

**Result:** Full automated pipeline from scaffold to verification.

---

## Pattern 10: Full Team Brain Workflow

**Use Case:** End-to-end: receive request, scaffold, build, test, announce.

**Code:**
```python
from pathlib import Path
from projforge import ProjForge

# Simulated tool request
request = {
    "tool_name": "DataValidator",
    "description": "Validate data formats and schemas",
    "requested_by": "FORGE",
    "builder": "ATLAS",
    "priority": "HIGH",
}

print(f"Received tool request: {request['tool_name']}")
print(f"Requested by: {request['requested_by']}")
print(f"Builder: {request['builder']}")

# Step 1: Scaffold
forge = ProjForge()
result = forge.create_project(
    template_name="teambrain-standard",
    project_name=request["tool_name"],
    variables={
        "description": request["description"],
        "builder": request["builder"],
        "requested_by": request["requested_by"],
    },
    init_git=True,
)

if result.success:
    print(f"\n[OK] Project scaffolded: {result.project_path}")
    print(f"    Files: {result.files_created}")
    print(f"    Template: teambrain-standard")
    print(f"    Git: Initialized")
    print(f"\n    Ready for {request['builder']} to begin implementation!")
    print(f"    All 9-phase build protocol files are pre-created.")
else:
    print(f"[X] Scaffold failed: {result.errors}")
```

**Result:** Seamless end-to-end workflow from request to ready-to-build project.

---

## Recommended Integration Priority

**Week 1 (Essential):**
1. ToolRegistry - Auto-register new projects
2. GitFlow - First commit automation
3. SynapseLink - Team notifications

**Week 2 (Productivity):**
4. TaskQueuePro - Auto-create build tasks
5. BatchRunner - Pipeline automation
6. ToolSentinel - Compliance verification

**Week 3 (Advanced):**
7. AgentHealth - Activity tracking
8. SessionReplay - Audit trail
9. Full stack integration

---

## Troubleshooting Integrations

**Import Errors:**
```python
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))
from projforge import ProjForge
```

**Version Conflicts:**
```bash
cd AutoProjects/ProjForge
git pull origin main
python projforge.py --version
```

---

**Last Updated:** February 12, 2026  
**Maintained By:** ATLAS (Team Brain)
