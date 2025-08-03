# New Branch:
    #Make sure you’re on main:
        git checkout main
    #Pull the latest main just in case:
        git pull
    #Create the dev branch from main:
        git checkout -b dev
    #Push it to GitHub (so it exists remotely too):
        git push -u origin dev

# Then Create Your Feature Branch
    git checkout -b feature/add-evaluation-models
    # do your work...
    git add .
    git commit -m "feat: add evaluation models"
    git push -u origin feature/add-evaluation-models

# Summary
    Task	Command
    Create dev from main	git checkout -b dev
    Push dev to GitHub	git push -u origin dev
    Start new feature branch	git checkout -b feature/your-feature

# When done:
    git add .
    git commit -m "feat: add OralExam and ProtocolAttempt models"
    git push
    Then either:
    Open a PR on GitHub to merge into dev, or
    From CLI:
    git checkout dev
    git pull
    git merge feature/add-oralexam-model
    git push



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
