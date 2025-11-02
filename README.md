# Password Generator (CLI)

A tiny, secure password generator written in Python. Uses the `secrets` module for cryptographic randomness.

## Features
- Choose length
- Toggle lowercase, uppercase, digits, symbols
- Optionally exclude ambiguous characters like `O, 0, l, 1, |`
- Optionally prevent duplicate characters
- Generate multiple passwords at once
- Zero external dependencies

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
# No requirements needed for runtime
python -m src.password_generator --help
```

## Examples
```bash
# 1. Default: length 16 with all character classes
python -m src.password_generator

# 2. Custom length and exclude ambiguous characters
python -m src.password_generator -l 20 --exclude-ambiguous

# 3. Generate 5 passwords, no symbols
python -m src.password_generator -n 5 --no-symbols

# 4. No duplicates and only digits + uppercase (length must be <= pool size)
python -m src.password_generator -l 10 --no-lower --no-symbols --no-duplicates
```

## Output format
Plain text, one password per line. Add `--json` to get JSON output.

## Run tests
```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

## Project layout
```
password-generator/
├─ src/
│  └─ password_generator/
│     ├─ __init__.py
│     └─ __main__.py
├─ tests/
│  └─ test_password_generator.py
├─ .gitignore
├─ LICENSE
├─ README.md
└─ requirements-dev.txt
```

## Push to GitHub
```bash
git init
git add .
git commit -m "feat: add secure password generator CLI"
git branch -M main
git remote add origin https://github.com/<your-username>/password-generator.git
git push -u origin main
```
