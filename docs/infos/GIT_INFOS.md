# Git Quick Reference

## Daily Workflow

### Start new feature
```bash
git checkout main
git pull --ff-only
git checkout -b feature/my-feature
```

### Commit and push
```bash
git add -A
git commit -m "feat(scope): message"
git push -u origin feature/my-feature
```

### Merge feature into main
```bash
git checkout main
git pull --ff-only
git merge --no-ff feature/my-feature
git push
```

---

## Common Commands

### Check status
```bash
git status
git branch --show-current
git log --oneline --graph -n 10
```

### Pull updates
```bash
git pull --ff-only
git fetch --all --prune
```

### Undo changes
```bash
git restore --staged <file>    # unstage
git restore <file>              # discard changes
git revert <hash>               # revert commit
```

### Delete branch
```bash
git branch -d branch-name       # safe delete
git branch -D branch-name       # force delete
```

---

## Merge Conflicts

```bash
git status                      # see conflicted files
# fix conflicts in files (remove <<<<<<, =======, >>>>>> markers)
git add <files>
git merge --continue
```

Abort merge if needed:
```bash
git merge --abort
```

---

## Cherry-pick

```bash
git log --oneline
git cherry-pick <hash>
```

If conflict:
```bash
git add <paths>
git cherry-pick --continue
```

Abort:
```bash
git cherry-pick --abort
```

---

## Commit Message Format

### Types
- `feat` - new feature
- `fix` - bug fix
- `chore` - build or tooling changes
- `docs` - documentation only
- `refactor` - code change without new features or fixes
- `test` - adding or updating tests
- `style` - formatting only
- `perf` - performance improvement

### Scope Examples
students, groups, api, appointments, calendar, email, schema, devlog

### Examples
```
feat(appointments): add slot-booking logic with email trigger
fix(groups): prevent group creation without semester
docs(devlog): log database schema decisions
refactor(schema): rename trials to exam_attempt_evaluation
test(api): add test for student creation endpoint
```

---

## Branch Strategy

```
main (production-ready)
  └── dev (integration branch)
       └── feature/my-feature (your work)
```

### Workflow
1. Create feature branch from dev
2. Work and commit on feature branch
3. Merge feature into dev
4. Test on dev
5. Merge dev into main for release
