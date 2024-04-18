# Release procedure

Prior to release create
[new release issue](https://github.com/Argmaster/pygerber/issues/new). Use it as a
scratchpad for release notes. Title should be `Release x.y.z`. Description should start
with short summary explaining agenda for the release. Then list all changes that will be
included in the release. Each change should be a separate bullet point starting with one
of "magic" words: Added, Changed, Deprecated, Removed, Fixed, Updated, Refactored.

On branch `main`:

1. Update `CHANGELOG.md` with new release notes and commit

   ```
    git commit -m "Update CHANGELOG.md"
   ```

2. Update version number in:

   - `pygerber/__init__.py`
   - `pyproject.toml`

   then commit:

   ```
    git commit -m "Bump version to x.y.z"
   ```

3. Push changes and wait for CI to finish.

   ```
    git push
   ```

4. If CI failed, fix issues, commit and push changes. Repeat until CI passes. If any of
   the changes introduced may have impact of users, update `CHANGELOG.md`.

5. Create a new tag:

   ```
    git tag vx.y.z
   ```

   And push it to the repository:

   ```
    git push --tags
   ```

6. Wait for CI to finish. It should automatically publish PyPI release files and
   documentation update.

7. Close release issue.

8. **SKIP FOR PATCH RELEASES**:

   Create `maintenance/x.y.x`, second `x` should remain in branch name, eg. for release
   `2.3.0` branch name should be `maintenance/2.3.x`

   ```
    git switch -c maintenance/x.y.x
   ```
