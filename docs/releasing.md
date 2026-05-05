# Releasing

This project uses git tags and GitHub Releases as stable snapshots of the assistant context. The `main` branch can move quickly as Rive docs and tool support change.

## Version Format

Use date-based tags:

```text
vYYYY.MM.DD
```

If more than one release is needed on the same date, append a patch suffix:

```text
vYYYY.MM.DD.1
```

## When to Release

Cut a release when one or more of these are true:

- Rive reference files or recipes changed meaningfully
- Tool context behavior changed
- Eval coverage changed in a way users should know about
- Upstream Rive docs drift required a public assistant update
- A maintenance change affects setup, validation, or contribution workflow

Do not release for typo-only changes unless they fix misleading technical guidance.

## Release Checklist

Before tagging:

1. Confirm the working tree is clean.

   ```bash
   git status --short
   ```

2. Run all validation commands.

   ```bash
   python3 -m unittest discover -s tests
   python3 scripts/validate_doc_paths.py
   python3 scripts/validate_tool_context_sync.py
   python3 scripts/validate_answer_evals.py
   ```

3. Review `CHANGELOG.md` and ensure the release-worthy changes are listed under `[Unreleased]`.

4. Create an annotated tag.

   ```bash
   git tag -a vYYYY.MM.DD -m "Release vYYYY.MM.DD"
   ```

5. Push the tag.

   ```bash
   git push origin vYYYY.MM.DD
   ```

6. Create a GitHub Release from the tag. Use the relevant `CHANGELOG.md` bullets as the release notes.

## User Guidance

- Use `main` for the freshest Rive docs tracking.
- Use tagged releases for stable assistant snapshots.
- Watch GitHub Releases for update notifications.

## After Release

After publishing, leave `[Unreleased]` in `CHANGELOG.md` for future changes. Do not delete historical entries.
