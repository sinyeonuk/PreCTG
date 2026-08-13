# Git

This document defines how agents should inspect and modify Git repositories.

## General Principles

- Respect the repository's existing Git workflow and ignore rules.
- Do not assume a branching strategy.
- Do not modify repository or global Git configuration unless authorized.
- Use relevant read-only commands such as `status`, `diff`, and `log` without separate approval.
- Treat existing modifications and untracked files as user-owned unless clear evidence shows they were created by the current task.

## Working Tree

- Inspect relevant working-tree state before editing.
- Preserve unrelated changes without reverting, overwriting, staging, or deleting them.
- When edits overlap with existing user changes, understand and preserve both intents where safely possible.
- Ask only when overlapping changes cannot be reconciled confidently or would materially change the user's work.
- Do not stage files unless staging or committing is authorized.
- Do not use `git reset --hard`, `git clean`, forced checkout, or equivalent destructive operations unless the user explicitly authorizes the exact action.
- When an operation fails partway, complete or safely revert only changes made by the current task.

## Commits

- Do not create commits unless authorized.
- Keep each commit focused on one logical change.
- Do not combine unrelated changes in a commit.
- Before creating a commit, verify that only intended files and changes will be included.

## Branches

- Do not create, rename, merge, or delete branches unless authorized.
- Switch branches only when authorized or clearly required by an authorized workflow.
- Do not discard working-tree changes to make a branch operation succeed.

## History

- Do not rewrite commit history unless authorized.
- Do not rebase, squash, or cherry-pick unless authorized.
- Do not force-push unless the user explicitly requests the exact operation and target.

## Remote Repositories

- Do not push to a remote repository unless authorized.
- Do not pull, fetch-and-merge, or otherwise integrate remote changes unless authorized.
- Perform a fetch only when the task requires current remote state, because it still changes local repository metadata.
- Confirm the intended remote and branch before a consequential remote operation when they are not already unambiguous.

## Conflict Resolution

- Resolve conflicts only when the intended result is clear from the task, surrounding code, and repository history.
- Preserve both user work and requested changes where possible.
- Ask for clarification when a consequential conflict cannot be resolved confidently.
- Do not choose a conflict side merely because it is labeled current, incoming, ours, or theirs.

## Line Endings

- When Git reports an LF/CRLF conversion warning, inspect the affected file, the repository's attributes and editor settings, and the effective Git configuration before changing files or configuration.
- Resolve the underlying mismatch so the warning does not recur while preserving the repository's declared line-ending policy.
- Do not suppress the warning or change global Git configuration merely to remove it.
- Use targeted normalization or an authorized repository-scoped configuration change only when required to align affected files with the declared policy.
- Ask before broad normalization when it would change files outside the current task, and inspect the resulting diff before retaining any normalization changes.

## Ignored and Generated Files

- Do not inspect or modify `.gitignore` on every task by default.
- Review ignore rules when the current task introduces a new generated, temporary, local-only, machine-specific, or environment-specific artifact that is likely to pollute the working tree.
- Also review ignore rules when changing a build tool, test tool, generator, development environment, or workflow that produces new local artifacts.
- Do not update `.gitignore` because unrelated untracked files already exist.
- When the current task introduces an artifact that clearly should not be tracked, update the repository's `.gitignore` without requiring separate approval.
- Limit new ignore rules to artifacts introduced or made relevant by the current task.
- Reuse existing `.gitignore` organization and avoid duplicate or overlapping patterns.
- Add the narrowest practical pattern and verify that it does not hide nearby legitimate files.
- Do not ignore a file merely to make the working tree appear clean or conceal an unexplained file.
- Do not ignore source files, required configuration, lockfiles, migrations, fixtures, tracked generated source, or deployment artifacts without a clear project convention.
- Do not commit generated files unless the project already tracks them or the task explicitly requires them.
- If a sensitive file is already tracked, do not present `.gitignore` as a complete fix.
- Do not remove a tracked sensitive file, rewrite history, or rotate credentials unless authorized; report the issue to the user.
- Do not run unrelated project checks solely for an ignore-rule change.

## Final Review

- Review the final diff and working-tree state after making changes.
- Distinguish current-task changes from pre-existing user changes.
- Ensure unrelated changes remain untouched and are excluded from any proposed commit.
