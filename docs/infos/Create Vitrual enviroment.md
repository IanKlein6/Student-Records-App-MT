# Virtual Environment Setup

## 1. Create the virtual environment
From your terminal in the project root:
```bash
python3 -m venv .venv
```
This creates a hidden .venv/ folder.

## 2. Activate the environment
```bash
source .venv/bin/activate
```
Your terminal prompt will change to something like:
```
(.venv) ianklein@MacBookAir student_records_app_mt %
```
Now all pip commands go into this isolated environment.

## 3. Install project dependencies
```bash
pip install fastapi tortoise-orm uvicorn
pip install pytest pytest-asyncio httpx
```
Add anything else you use (logging libs, dotenv, etc.).

## 4. Save dependencies to requirements.txt
```bash
pip freeze > requirements.txt
```
So anyone else (or your future self) can recreate it with:
```bash
pip install -r requirements.txt
```

## 5. Auto-activate in VSCode
VSCode should detect it and ask you to use it.

If it doesn't:
- Open Command Palette: Cmd + Shift + P
- Search: Python: Select Interpreter
- Choose: .venv/bin/python

## Final Touch: Add .venv to .gitignore
You don't want to commit your virtual environment to Git.

Add this line to .gitignore:
```
.venv/
```
