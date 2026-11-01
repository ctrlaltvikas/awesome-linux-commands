# Contributing to Awesome Linux Commands

Thank you for your interest in contributing! This repository maintains strict quality standards to ensure every command is practical, understandable, safety-tiered, and useful for production engineers.

---

## 🎯 Contribution Principles

1. **Practical Production Value:** We prioritize commands that solve real operational headaches, improve terminal ergonomics, or diagnose incidents.
2. **Every Flag Dissected:** No command should include cryptic switches (like `-tulpn` or `+L1`) without an accompanying explanation table.
3. **Safety First:** Always assign the correct risk indicator (`🟢 Safe`, `🟡 Mutating`, `🔴 Destructive`) and privilege requirement (`Normal` vs `Sudo`).
4. **Modern CLI Alternatives:** When proposing a tool replacement, ensure it is actively maintained and delivers clear advantages over coreutils (speed, syntax highlighting, ergonomics).

---

## 📝 Command Format Specification

When adding a new command to a file in `commands/`, use this exact schema:

```markdown
### N. `tool` — Brief Hook Describing Purpose

<!-- @id: unique-kebab-case-id -->
<!-- @name: tool-short-name -->
<!-- @category: Modern CLI | Incident Response | Networking | Storage | Security | Text & Streams -->
<!-- @risk: Safe | Mutating | Destructive -->
<!-- @privilege: Normal | Sudo -->
<!-- @replaces: legacy-tool (optional) -->
<!-- @tags: tag1, tag2, tag3 -->

\`\`\`bash
tool -flag1 -flag2 argument
\`\`\`

#### Flag Breakdown
| Flag | Description |
| :--- | :--- |
| `-flag1` | What this flag accomplishes |
| `-flag2` | What this flag accomplishes |

#### Why / When to Use
Concise 1-2 sentence real-world explanation of when an engineer needs this command.
```

---

## 🛠️ Validation Workflow

Before submitting a Pull Request, validate that your new command parses correctly into `metadata.json`:

```bash
# 1. Run the catalog compiler
python3 scripts/build_catalog.py

# 2. Verify git status
git status
```

The script will validate your tags and output the updated `metadata.json`. Commit both your markdown edits and the generated `metadata.json`.

Thank you for helping make the Linux terminal experience safer and more powerful for everyone!
