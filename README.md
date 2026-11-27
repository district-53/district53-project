Secret scanning before commit
Before every git commit, pre-commit checks your files for passwords, tokens and keys.
If it finds a secret, the commit is not created.
The config file is in .github/.pre-commit-config.yaml.
## Setup
You need Python 3.9 or newer.
### Windows
```powershell
py -m pip install pre-commit
git config --global init.templateDir "$HOME/.git-template"
pre-commit init-templatedir -c .github/.pre-commit-config.yaml "$HOME/.git-template"
```
### macOS
```bash
pip3 install pre-commit        
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir -c .github/.pre-commit-config.yaml ~/.git-template
```
### Linux
```bash
pip install --user pre-commit         
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir -c .github/.pre-commit-config.yaml ~/.git-template
```

### And
Run this once in the root folder of the repository:
```bash
pre-commit install -c .github/.pre-commit-config.yaml
```

## If gitleaks finds a secret
1. Remove the secret from the code. Put it in an environment variable or in a .env file
   (and add .env to .gitignore).
2. Run git add and git commit again.

If it is a false alarm (not a real secret), add this comment at the end of the line:
```python
API_KEY = "example-not-real-key"  # gitleaks:allow
```
