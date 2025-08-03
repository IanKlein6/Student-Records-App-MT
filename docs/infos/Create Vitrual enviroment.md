Step-by-Step Setup for .venv

🟩 1. Create the virtual environment in your project root
From your terminal in the root of your project:

python3 -m venv .venv
This creates a hidden .venv/ folder.

🟩 2. Activate the environment
source .venv/bin/activate
Your terminal prompt will change to something like:

(.venv) ianklein@MacBookAir student_records_app_mt %
Now all pip commands go into this isolated environment.

🟩 3. Install your project dependencies
pip install fastapi tortoise-orm uvicorn
pip install pytest pytest-asyncio httpx
Add anything else you use (e.g. logging libs, dotenv, etc.).

🟩 4. (Optional but best practice) Save dependencies to requirements.txt
pip freeze > requirements.txt
So anyone else (or your future self) can recreate it with:

pip install -r requirements.txt
🟩 5. (Optional) Auto-activate .venv in VSCode
VSCode should detect it and ask you to use it.

If it doesn't:

Open Command Palette: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>
Search: Python: Select Interpreter
Choose: .venv/bin/python
✅ Final Touch: Add .venv to .gitignore

You don’t want to commit your virtual environment to Git.

Add this line to .gitignore:

