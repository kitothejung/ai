# Shared AI Memory System

This repository is a scaffold for a shared memory workflow that can be used by both Claude and Codex.

## What This Is

The repository does not contain application code yet. It only defines the project structure, shared instructions, and memory files that future AI sessions can use as durable context.

## Repository Layout

- `AGENTS.md` - shared operating instructions for AI agents.
- `CLAUDE.md` - Claude-specific guidance.
- `memory/` - the durable project memory.
- `.claude/` - Claude-local support files and placeholders.
- `.codex/` - Codex-local support files and placeholders.
- `.vscode/` - editor configuration for the workspace.

## Workflow

1. Start by reading `README.md`.
2. Read `memory/00-index.md` to find the most important context files.
3. Check `memory/01-project-brief.md` for the current project definition.
4. Review `memory/02-decisions.md` before changing behavior or structure.
5. Use `memory/03-active-context.md` for current tasks and open questions.
6. After completing work, update the relevant memory files with anything durable.

## Memory File Roles

- `memory/00-index.md` - entry point and file map.
- `memory/01-project-brief.md` - project purpose and scope.
- `memory/02-decisions.md` - stable decisions and rationale.
- `memory/03-active-context.md` - current focus, open questions, and short-term notes.
- `memory/04-session-log.md` - dated session notes.
- `memory/05-patterns.md` - recurring implementation or workflow patterns.
- `memory/06-prompts.md` - reusable prompts and instructions.

## Expected Behavior

- Keep notes short and factual.
- Update memory when context changes.
- Do not add application logic until requested.
- Preserve user work and avoid unrelated edits.

