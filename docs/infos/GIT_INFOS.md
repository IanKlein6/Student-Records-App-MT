# SIMPLE Git — One-Page 

# New Branch
    git checkout main
    git pull --ff-only
    git checkout -b dev
    git push -u origin dev

# New Feature
    git checkout -b feature/my-feature
    git add -A
    git commit -m "feat(scope): message"
    git push -u origin feature/my-feature

# Merge Feature → dev
    git switch dev
    git pull --ff-only
    git merge --no-ff feature/my-feature
    git push

# Release dev → main
    git switch main
    git pull --ff-only
    git merge --no-ff dev
    git push

# Cherry-pick
    git log --oneline
    git cherry-pick <hash>
    # If conflict:
        git add <paths>
        git cherry-pick --continue
    # Abort:
        git cherry-pick --abort

# Conflicts
    git status
    git add <paths>
    git merge --continue
    git merge --abort

# Undo
    git restore --staged <paths>
    git restore <paths>
    git revert <hash>

# Pull / Update
    git pull --ff-only
    git fetch --all --prune

# Commit Types
    feat, fix, chore, docs, refactor, style, test, perf, ci, revert, infra

# Scope Examples
    students, groups, api, appointments, calendar-sync, email-notify, devlog, excalidraw, schema

# Examples
    feat(appointments): add slot-booking logic with email trigger
    fix(groups): prevent group creation without semester
    docs(devlog): log database schema decisions






# IN-DEPTH

# New Branch:
    # Make sure you’re on main:
        git checkout main
    # Pull the latest main just in case:
        git pull --ff-only
    # Create the dev branch from main:
        git checkout -b dev
    # Push it to GitHub (so it exists remotely too):
        git push -u origin dev

# Then Create Your Feature Branch
    git checkout -b feature/add-evaluation-models
    # Do your work...
    git add -A
    git commit -m "feat: add evaluation models"
    git push -u origin feature/add-evaluation-models

# Summary
    Task	                    Command
    Create dev from main	    git checkout -b dev
    Push dev to GitHub	        git push -u origin dev
    Start new feature branch	git checkout -b feature/your-feature

# When done:
    git add -A
    git commit -m "feat: add OralExam and ProtocolAttempt models"
    git push
    Then either:
    Open a PR on GitHub to merge into dev, or
    From CLI:
        git checkout dev
        git pull --ff-only
        git merge --no-ff feature/add-oralexam-model
        git push

---

# Basics
    # Check where you are:
        git status -sb
        git branch --show-current
    # See recent commits:
        git log --oneline --graph --decorate -n 20

# Commit changes
    # Stage everything:
        git add -A
    # Or stage interactively:
        git add -p
    # Commit (one-line):
        git commit -m "<type>(scope): message"
        # Examples:
            feat(api): add endpoint
            fix(tests): correct failing case
            docs(devlog): log progress

# Pull (get latest)
    # From current branch’s upstream:
        git pull --ff-only
    # Update tracking branches without merging:
        git fetch --all --prune

# Create & switch branches
    # New branch from current HEAD:
        git switch -c my-branch
    # New branch from another base:
        git switch -c my-branch origin/main
    # Switch to existing branch:
        git switch my-branch

# Push branches
    # First push (set upstream):
        git push -u origin feature/add-oralexam-model
    # Subsequent pushes:
        git push

# Merge feature branch into dev
    git switch dev
    git pull --ff-only
    git merge --no-ff feature/add-oralexam-model
    git push

# Merge dev into main (release)
    git switch main
    git pull --ff-only
    # (Optional) bring main into dev first to reduce conflicts:
        git switch dev && git merge origin/main && git switch main
    git merge --no-ff dev
    git push

# Cherry-pick (specific commit only)
    # Find commit hash:
        git log --oneline
    # Apply:
        git cherry-pick <hash>
    # If conflict:
        git add <paths>
        git cherry-pick --continue
    # Abort:
        git cherry-pick --abort

# Cherry-pick docs only
    git restore -s other-branch -- docs/DEVLOG.md docs/DECISIONS.md
    git add docs/*
    git commit -m "docs: import updates from other-branch"

# See differences before merging
    # Commits on feature not in main:
        git log --oneline main..feature/xyz
    # File changes:
        git diff --name-status main...feature/xyz

# Resolve merge conflicts
    git status
    # Open files with conflict markers (<<<<<<<, =======, >>>>>>>)
    # Fix content, remove markers
    git add <paths>
    git merge --continue
    # Abort merge:
        git merge --abort

# Undo safely
    git restore --staged <paths>
    git restore <paths>
    git revert <hash>

# Good habits
    - Small, focused commits
    - Clear messages (type(scope): summary)
    - Pull before push: git pull --ff-only
    - Keep branches up to date:
        git fetch && git merge origin/dev
        # Or rebase:
            git rebase origin/dev
            # If rebased, push with:
                git push --force-with-lease

# Helpful one-liners
    # Set default editor to nano:
        git config --global core.editor "nano"
    # Show staged changes:
        git diff --cached
    # Blame:
        git blame <file>

# GIT COMMITS:
## Types (prefixes):
    feat: — a new feature
    fix: — a bug fix
    chore: — build or tooling changes (e.g. Poetry, linters)
    docs: — documentation only (e.g. README, devlog)
    refactor: — code change that doesn’t add features or fix bugs
    style: — formatting only (whitespace, semicolons, etc.)
    test: — adding or updating tests
    perf: — performance improvement
    ci: — continuous integration or Docker changes
    revert: — revert a previous commit
    infra: — setup or config not covered above (e.g. .env, Docker)

## Scope examples (optional):
    students
    groups
    api
    appointments
    calendar-sync
    email-notify
    devlog
    excalidraw
    schema

### Example
        feat(appointments): add slot-booking logic with email trigger  
        fix(groups): prevent group creation without semester  
        docs(devlog): log database schema decisions  
        refactor(schema): rename trials to exam_attempt_evaluation  
        test(api): add test for student creation endpoint  
        infra(docker): add PostgreSQL service to docker-compose  
        chore(lint): add pre-commit hook for formatting  

---

# Minimal workflows

## Add + commit + push current branch
    git add -A
    git commit -m "feat(scope): message"
    git push

## Start new feature from dev
    git switch dev && git pull --ff-only
    git switch -c feature/my-feature
    git add -A && git commit -m "feat: ..."
    git push -u origin feature/my-feature

## Merge feature → dev
    git switch dev && git pull --ff-only
    git merge --no-ff feature/my-feature
    git push

## Release dev → main
    git switch main && git pull --ff-only
    git merge --no-ff dev
    git push
