# AGENTS.md

Shared operating instructions for AI agents working in this repository.

## Purpose

This repository is a shared memory workspace for Claude and Codex. Use `config/project.yaml` as the entry point, then follow `config/agents.yaml`, `config/workflow.yaml`, `config/rules.yaml`, `skills/`, and `memory/` for durable project context, decisions, and workflow notes.

## Working Rules

- Read the memory files before making changes.
- Update memory when you learn something durable.
- Keep notes concise, factual, and current.
- Do not add application code yet unless explicitly asked.
- Preserve existing user changes and avoid overwriting unrelated work.

## Recommended Flow

1. Read `config/project.yaml`.
2. Review `config/agents.yaml`.
3. Check `config/workflow.yaml`.
4. Check `config/rules.yaml`.
5. Read the relevant files in `skills/`.
6. Review `memory/00-index.md`, then the relevant memory files.
7. Make the requested change.
8. Update the relevant memory files if anything important changed.

## Memory Hygiene

- Record decisions, constraints, and open questions.
- Prefer short entries over long narratives.
- Move stale items out of active context when they are resolved.
