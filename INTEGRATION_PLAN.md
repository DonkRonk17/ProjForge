# ProjForge - Integration Plan

**Date:** February 12, 2026  
**Maintained By:** ATLAS (Team Brain)  

---

## Integration Goals

This document outlines how ProjForge integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools (73+ ecosystem)
3. BCH (Beacon Command Hub)
4. Logan's daily workflows

---

## BCH Integration

### Overview
ProjForge is a standalone CLI tool that does not directly integrate with BCH. However, agents connected to BCH can invoke ProjForge to scaffold new tools when requests come through BCH channels.

### Potential BCH Commands
```
@projforge create python-cli ToolName --var "description=..."
@projforge list
@projforge preview teambrain-standard
```

### Implementation (Future)
1. Add ProjForge to BCH command router
2. Parse create commands from BCH messages
3. Return creation status via BCH response
4. Auto-announce new projects in BCH channel

---

## AI Agent Integration

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Scaffold tools from specs | CLI / Python API | HIGH |
| **Atlas** | Create tools during build sessions | CLI / Python API | HIGH |
| **Clio** | Linux tool scaffolding | CLI | MEDIUM |
| **Nexus** | Cross-platform project creation | CLI / Python API | MEDIUM |
| **Bolt** | Quick project generation | CLI | LOW |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)
**Primary Use Case:** Create tool scaffolds from specifications before assigning to builders.

**Workflow:**
```python
from projforge import ProjForge

forge_tool = ProjForge()

# After creating a tool spec, scaffold the project
result = forge_tool.create_project(
    template_name="teambrain-standard",
    project_name="NewRequestedTool",
    variables={
        "description": "Tool from Forge's spec",
        "builder": "ATLAS",
        "requested_by": "FORGE",
    },
    init_git=True,
)

# Then assign to builder agent with scaffold ready
```

#### Atlas (Executor / Builder)
**Primary Use Case:** Quick project setup at the start of every build session.

**Workflow:**
```bash
# At session start, scaffold the tool
projforge create teambrain-standard ToolName --var "description=..." --git

# Then follow 9-phase build protocol
# All phase files are already created!
```

#### Clio (Linux / Ubuntu Agent)
**Primary Use Case:** Create Linux-focused tools.

```bash
# Clone ProjForge on Linux
git clone https://github.com/DonkRonk17/ProjForge.git

# Scaffold a project
python3 ProjForge/projforge.py create python-cli LinuxTool \
    --var "description=Linux utility"
```

#### Nexus (Multi-Platform Agent)
**Primary Use Case:** Create cross-platform projects.

```python
from projforge import ProjForge
forge = ProjForge()
result = forge.create_project("python-cli", "CrossPlatTool",
    variables={"description": "Cross-platform utility"})
```

#### Bolt (Free Executor)
**Primary Use Case:** Rapid project creation without API costs.

```bash
# No API costs - pure local tool
projforge create python-cli QuickTool --var "description=Fast tool"
```

---

## Integration with Team Brain Tools

### With ToolRegistry
**Use Case:** Auto-register newly scaffolded tools.

```python
from projforge import ProjForge
from toolregistry import ToolRegistry

forge = ProjForge()
registry = ToolRegistry()

result = forge.create_project("teambrain-standard", "NewTool",
    variables={"description": "New tool"})

if result.success:
    registry.register_tool(
        name="NewTool",
        path=str(result.project_path),
        description="New tool",
        status="in_progress",
    )
```

### With GitFlow
**Use Case:** Initialize and commit after scaffolding.

```bash
projforge create python-cli MyTool --var "description=Tool" --git
cd MyTool
python ../GitFlow/gitflow.py commit "Initial scaffold from ProjForge"
```

### With SynapseLink
**Use Case:** Announce new project creation to team.

```python
from projforge import ProjForge
from synapselink import quick_send

forge = ProjForge()
result = forge.create_project("teambrain-standard", "NewTool",
    variables={"description": "New tool"})

if result.success:
    quick_send("TEAM", "New Project Scaffolded",
        f"Tool: NewTool\nFiles: {result.files_created}\n"
        f"Template: teambrain-standard\nReady for build!")
```

### With BatchRunner
**Use Case:** Chain scaffold + git + announce in one pipeline.

```python
from projforge import ProjForge

forge = ProjForge()

# Create multiple projects in batch
for name, desc in [("ToolA", "First"), ("ToolB", "Second")]:
    result = forge.create_project("python-cli", name,
        variables={"description": desc}, init_git=True)
    print(f"{name}: {'OK' if result.success else 'FAIL'}")
```

### With ToolSentinel
**Use Case:** Verify scaffolded projects follow Holy Grail Protocol.

```python
from projforge import ProjForge

# Create with teambrain-standard to guarantee compliance
forge = ProjForge()
result = forge.create_project("teambrain-standard", "CompliantTool",
    variables={"description": "Fully compliant tool"})
# ToolSentinel can verify all required files exist
```

---

## Adoption Roadmap

### Phase 1: Core Adoption (Week 1)
- All agents aware of ProjForge and can use basic `create`
- Forge uses it to scaffold tools before assigning to builders
- Atlas uses it at the start of every build session

### Phase 2: Integration (Week 2-3)
- ToolRegistry auto-registration implemented
- SynapseLink announcement automation
- GitFlow integration for first commits

### Phase 3: Optimization (Week 4+)
- Custom templates for specialized project types
- BCH command integration
- Template sharing between agents

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Agents using ProjForge | All 5 |
| Time saved per project | 30-60 min |
| Projects scaffolded/week | 2-4 |
| Template consistency | 100% |

---

**Last Updated:** February 12, 2026  
**Maintained By:** ATLAS (Team Brain)
