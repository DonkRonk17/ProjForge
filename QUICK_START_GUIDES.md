# ProjForge - Quick Start Guides

> Each Team Brain agent has a 5-minute quick-start guide tailored to their role.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## Forge Quick Start

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to scaffold tools before assigning to builders

### Step 1: Verify ProjForge
```bash
python C:\Users\logan\OneDrive\Documents\AutoProjects\ProjForge\projforge.py list
```

### Step 2: Scaffold a Tool from a Spec
When you create a tool request, scaffold the project immediately:
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects
python ProjForge\projforge.py create teambrain-standard NewToolName \
    --var "description=Tool purpose from your spec" \
    --var "requested_by=FORGE" \
    --var "builder=ATLAS" \
    --git
```

### Step 3: Verify the Scaffold
```bash
cd NewToolName
dir
python test_new_tool_name.py
```

### Step 4: Common Forge Workflows

**Scaffold + assign to builder:**
```python
from projforge import ProjForge

forge = ProjForge()
result = forge.create_project("teambrain-standard", "RequestedTool",
    variables={
        "description": "Tool from Forge spec",
        "builder": "ATLAS",
        "requested_by": "FORGE",
    }, init_git=True)

# Now assign to Atlas/Clio with scaffold ready
```

**Preview before creating:**
```bash
projforge preview teambrain-standard
projforge create teambrain-standard ToolName --var "description=Test" --dry-run
```

### Next Steps for Forge
1. Use ProjForge for every new tool request
2. Scaffold before assigning to builders
3. Review generated structure matches spec

---

## Atlas Quick Start

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Use ProjForge at the start of every build session

### Step 1: Verify ProjForge
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects
python ProjForge\projforge.py --version
```

### Step 2: Start a Build Session
```bash
# At session start, scaffold the tool
python ProjForge\projforge.py create teambrain-standard NewTool \
    --var "description=Smart analysis tool" \
    --var "builder=ATLAS" \
    --git
```

### Step 3: Verify Generated Tests Pass
```bash
cd NewTool
python test_new_tool.py
# All 11 tests should pass
```

### Step 4: Start Building!
The scaffold gives you:
- `new_tool.py` with working skeleton (class + CLI)
- `test_new_tool.py` with 11 passing tests to extend
- All 9-phase build protocol files pre-created
- README, EXAMPLES, CHEAT_SHEET templates to fill in
- branding/BRANDING_PROMPTS.md ready

### Step 5: Follow Build Protocol
```bash
# Phase 1: Edit BUILD_COVERAGE_PLAN.md (already created!)
# Phase 2: Edit BUILD_AUDIT.md
# Phase 3: Edit ARCHITECTURE.md
# Phase 4: Implement new_tool.py (skeleton is there!)
# Phase 5: Extend test_new_tool.py
# Phase 6: Enhance README.md, EXAMPLES.md, CHEAT_SHEET.txt
# Phase 7: Complete INTEGRATION_PLAN.md, QUICK_START_GUIDES.md
# Phase 8: Fill BUILD_REPORT.md
# Phase 9: Push to GitHub
```

### Next Steps for Atlas
1. Use ProjForge for EVERY new tool build
2. Never manually create project structures again
3. Extend generated test suites during Phase 5

---

## Clio Quick Start

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Use ProjForge on Linux

### Step 1: Get ProjForge
```bash
git clone https://github.com/DonkRonk17/ProjForge.git
cd ProjForge
python3 projforge.py list
```

### Step 2: Create a Project
```bash
python3 projforge.py create python-cli LinuxTool \
    --var "description=Linux system utility"
```

### Step 3: Verify
```bash
cd LinuxTool
python3 test_linux_tool.py
python3 linux_tool.py run
```

### Step 4: Linux-Specific Notes
- Use `python3` instead of `python`
- File paths use forward slashes
- Custom templates: `~/.projforge/templates/`
- Config: `~/.projforge/config.json`

### Next Steps for Clio
1. Clone ProjForge to your Ubuntu environment
2. Create Linux-specific custom templates
3. Use for all new tool builds

---

## Nexus Quick Start

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Cross-platform project creation

### Step 1: Platform Verification
```python
import platform
from projforge import ProjForge

forge = ProjForge()
print(f"Platform: {platform.system()}")
print(f"Templates: {len(forge.store.list_all())}")
```

### Step 2: Create Cross-Platform Project
```bash
projforge create python-cli CrossPlatTool \
    --var "description=Works on Windows, Linux, and macOS"
```

### Step 3: Verify on Current Platform
```bash
cd CrossPlatTool
python test_cross_plat_tool.py
```

### Step 4: Platform Considerations
- All generated code uses `pathlib.Path` (cross-platform)
- Generated `.gitignore` covers Windows and Unix
- Generated setup.py has `Operating System :: OS Independent`
- Config stored in `Path.home()` (works everywhere)

### Next Steps for Nexus
1. Test ProjForge on all platforms
2. Create platform-specific templates if needed
3. Report any cross-platform issues

---

## Bolt Quick Start

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Quick project creation without API costs

### Step 1: Verify (No API Key Required!)
```bash
python projforge.py list
```

### Step 2: Quick Scaffold
```bash
projforge create python-cli QuickTool --var "description=Quick tool"
```

### Step 3: Batch Mode
```bash
# Create multiple projects quickly
projforge create python-cli ToolA --var "description=First tool"
projforge create python-cli ToolB --var "description=Second tool"
projforge create python-cli ToolC --var "description=Third tool"
```

### Step 4: Cost Benefits
- Zero API calls required
- Pure local execution
- No network dependency
- Instant results (< 2 seconds)

### Next Steps for Bolt
1. Use for all repetitive project creation
2. Batch create when multiple tools needed
3. Report any issues via Synapse

---

## Additional Resources

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md) (12 examples)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/ProjForge/issues
- Synapse: Post in THE_SYNAPSE/active/

---

**Last Updated:** February 12, 2026  
**Maintained By:** ATLAS (Team Brain)
