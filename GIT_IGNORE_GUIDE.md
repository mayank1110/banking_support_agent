# 🚫 Files to Exclude from Git - Complete Guide

## ✅ Quick Answer

**NO, do NOT upload `.gradio` folder to GitHub!**

The `.gradio` folder contains:
- ❌ Temporary SSL certificates
- ❌ Runtime cache files
- ❌ Machine-specific configurations
- ❌ Auto-generated files (recreated on every run)

---

## 📋 Complete List: What to Exclude

### **1. Runtime & Cache Folders** ❌

```
.gradio/              # Gradio temporary files and certificates
__pycache__/          # Python bytecode cache
.ipynb_checkpoints/   # Jupyter auto-save checkpoints
.gradio_cached_examples/  # Gradio cached examples
.tmp/                 # Temporary files
```

**Why exclude:**
- Generated automatically at runtime
- Specific to your local machine
- Not needed for the project to work
- Can be recreated instantly

---

### **2. Virtual Environments** ❌

```
.venv/
venv/
env/
ENV/
```

**Why exclude:**
- Contains installed Python packages (large)
- Platform-specific binaries
- Recreated with `pip install -r requirements.txt`
- Typically 200MB-1GB in size

---

### **3. Compiled Python Files** ❌

```
*.py[cod]
*$py.class
*.so
.Python
```

**Why exclude:**
- Bytecode compiled from `.py` files
- Platform-specific
- Automatically generated
- Not human-readable

---

### **4. Build & Distribution** ❌

```
build/
dist/
*.egg-info/
eggs/
wheels/
downloads/
```

**Why exclude:**
- Generated during package building
- Not source code
- Can be rebuilt anytime

---

### **5. IDE & Editor Files** ❌

```
.vscode/              # VS Code settings (unless team-shared)
.idea/                # IntelliJ/PyCharm settings
*.swp                 # Vim swap files
*.swo
*~                    # Editor backup files
```

**Why exclude:**
- Personal editor preferences
- Machine-specific paths
- Not part of the project

**Exception:** Share `.vscode/settings.json` if team has agreed on common settings

---

### **6. Model Files** ❌

```
models/*.bin          # PyTorch model weights (~268MB each)
models/*.pth
models/*.pt
models/*.onnx
models/*.safetensors
```

**Why exclude:**
- Very large files (100MB-1GB+)
- Can be retrained from code
- Should be stored separately (Hugging Face, S3, etc.)

**What to include instead:**
- Training code
- Model architecture definitions
- Instructions to download/load pre-trained models

---

### **7. Data Files** ❌

```
data/support_tickets.csv    # Runtime data (user-generated)
data/*.tmp
```

**Why exclude:**
- Contains user/customer data (privacy!)
- Generated at runtime
- Should be empty or contain sample data only

**What to include:**
- `data/banking_support_dataset_train_model.csv` (training data)
- Sample/placeholder CSV files with example structure

---

### **8. Logs & Environment** ❌

```
*.log                 # Application logs
logs/
.env                  # Environment variables (SECRETS!)
.env.local
```

**Why exclude:**
- **Security risk**: May contain API keys, passwords
- Machine-specific paths
- Sensitive configuration

**What to include instead:**
- `.env.example` with placeholder values
- Documentation about required environment variables

---

## ✅ What TO Upload to GitHub

### **Source Code** ✅

```
src/
├── __init__.py
├── classifier.py
├── agents.py
├── handlers.py
├── ticket_manager.py
└── ui.py
```

### **Configuration Files** ✅

```
config.py
requirements.txt
setup.py
.gitignore
```

### **Documentation** ✅

```
README.md
QUICKSTART.md
DEPLOYMENT.md
GITHUB_GUIDE.md
PROJECT_SUMMARY.md
LICENSE
```

### **Notebooks** ✅

```
Capstone_1_Banking_Customer_Support.ipynb
Banking_Customer_Support.ipynb
```

### **Training Data** ✅

```
data/banking_support_dataset_train_model.csv
```

### **Tests** ✅

```
tests/
├── __init__.py
└── test_agent.py
```

### **Scripts** ✅

```
app.py
train_model.py
```

---

## 🔍 Your Current `.gitignore` (Updated)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Jupyter Notebook
.ipynb_checkpoints/

# Gradio (temporary files and caches)
.gradio/
gradio_cached_examples/
.tmp/

# Model outputs
models/
*.bin
*.pt
*.pth
*.onnx
*.safetensors

# Data
data/support_tickets.csv
data/*.tmp

# Logs and runtime files
*.log
logs/
.env
.env.local
```

---

## 🛠️ Commands to Clean Up Git

### **If you accidentally committed files that should be ignored:**

```bash
# Remove .gradio from tracking (keeps local file)
git rm --cached -r .gradio/

# Remove all __pycache__ directories
git rm --cached -r __pycache__/

# Remove virtual environment
git rm --cached -r .venv/

# Remove model files
git rm --cached models/*.bin

# Commit the cleanup
git commit -m "Remove files that should be in .gitignore"
```

### **Verify what's tracked:**

```bash
# See all tracked files
git ls-files

# See what will be committed
git status

# Preview what .gitignore excludes
git check-ignore -v .gradio/
```

---

## 📊 File Size Comparison

| File/Folder | Size | Upload? |
|-------------|------|---------|
| `.gradio/` | 10-50 KB | ❌ No |
| `.venv/` | 200-800 MB | ❌ No |
| `models/*.bin` | 268 MB each | ❌ No |
| `__pycache__/` | 5-20 MB | ❌ No |
| `src/` | 50-100 KB | ✅ Yes |
| `tests/` | 10-20 KB | ✅ Yes |
| `data/*.csv` (training) | 1-10 MB | ✅ Yes |
| Documentation | 100-500 KB | ✅ Yes |

---

## 🔐 Security Checklist

Before pushing to GitHub, verify:

- [ ] No `.env` files with secrets
- [ ] No API keys in code
- [ ] No passwords in configuration
- [ ] No customer/user data in CSV files
- [ ] No private certificates or keys
- [ ] `.gradio/` folder excluded
- [ ] `.venv/` folder excluded
- [ ] Model binary files excluded

**Scan for secrets:**

```bash
# Search for common secret patterns
grep -r "api_key.*=" src/
grep -r "password.*=" src/
grep -r "secret.*=" src/
grep -r "AWS_ACCESS_KEY" src/
```

---

## 🎯 Best Practices

### **1. Use `.gitignore` from Start**

Create `.gitignore` before your first commit to avoid accidental uploads.

### **2. Review Before Each Commit**

```bash
git status
git diff --cached
```

### **3. Use `.gitignore` Templates**

GitHub provides templates:
- Go to: https://github.com/github/gitignore
- Use: `Python.gitignore`

### **4. Add `.gitignore` Rules Immediately**

When you create a new file that shouldn't be tracked, add it to `.gitignore` right away.

### **5. Use `.env.example`**

```bash
# .env.example (safe to commit)
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=your_api_key_here

# .env (NEVER commit)
DATABASE_URL=postgresql://user:pass@prod-server:5432/mydb
API_KEY=sk-1234567890abcdef
```

---

## 📚 Resources

- [GitHub's .gitignore templates](https://github.com/github/gitignore)
- [Git - Book: Git Basics - Recording Changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
- [Atlassian Git Tutorial - .gitignore](https://www.atlassian.com/git/tutorials/saving-changes/gitignore)

---

## ✅ Summary

**Upload to GitHub:**
- ✅ Source code (`.py` files)
- ✅ Documentation (`.md` files)
- ✅ Configuration (`.txt`, `.py` configs)
- ✅ Tests
- ✅ Notebooks
- ✅ Training data (non-sensitive)

**DO NOT upload:**
- ❌ `.gradio/` folder
- ❌ `.venv/` or virtual environments
- ❌ Model binary files
- ❌ `__pycache__/`
- ❌ `.env` files with secrets
- ❌ User/customer data
- ❌ IDE settings (personal)
- ❌ Logs and temp files

---

**Your repository is now clean and ready for GitHub!** 🚀
