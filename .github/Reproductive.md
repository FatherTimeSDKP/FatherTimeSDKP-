I'll produce the ZIP contents assuming repo URL https://github.com/FatherTimeSDKP/FatherTimeSDKP-.git. Below are the files I'll create (you can copy these into a folder and zip them), with exact contents.

1) reproduce.sh
```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_URL="https://github.com/FatherTimeSDKP/FatherTimeSDKP-.git"
WORKDIR="$(pwd)/fathertime-repro"
RESULTS_DIR="$WORKDIR/results"
PYTHON=python3

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR" "$RESULTS_DIR"
cd "$WORKDIR"

# Clone specific repo
git clone --depth 1 "$REPO_URL" repo
cd repo

# Create venv
$PYTHON -m venv ../venv
source ../venv/bin/activate
pip install --upgrade pip
pip install -r requirements-repro.txt || true

# Fallback installs (safe set)
pip install numpy scipy matplotlib pandas sympy requests

# Ensure run_configs exists
cd ..
mkdir -p run_configs

# Run scripts with fixed seeds and capture outputs
cd repo

# qcc0_bias_repro.py
if [ -f qcc0_bias_repro.py ]; then
  echo "Running qcc0_bias_repro.py"
  PYTHONHASHSEED=0 python qcc0_bias_repro.py --seed 0 > "$RESULTS_DIR/qcc0_bias_repro.log" 2>&1 || true
fi

# Digital_Crystal_Protocal.py
if [ -f Digital_Crystal_Protocal.py ]; then
  echo "Running Digital_Crystal_Protocal.py"
  PYTHONHASHSEED=0 python Digital_Crystal_Protocal.py --test --seed 0 > "$RESULTS_DIR/Digital_Crystal_Protocal.log" 2>&1 || true
fi

# vibration-Field-equations-VFE.py
if [ -f vibration-Field-equations-VFE.py ]; then
  echo "Running vibration-Field-equations-VFE.py"
  PYTHONHASHSEED=0 python vibration-Field-equations-VFE.py --test --seed 0 > "$RESULTS_DIR/vibration-Field-equations-VFE.log" 2>&1 || true
fi

# Collect environment info
pip freeze > "$RESULTS_DIR/pip-freeze.txt"
python -V > "$RESULTS_DIR/python-version.txt"
git rev-parse --short HEAD > "$RESULTS_DIR/repo-commit.txt"

echo "Reproduction run complete. Results in: $RESULTS_DIR"
```

2) requirements-repro.txt
```
numpy==1.26.4
scipy==1.11.3
matplotlib==3.8.1
pandas==2.2.2
sympy==1.12
requests==2.31.0
```

3) run_configs/qcc0_bias_repro.json
```json
{
  "script": "qcc0_bias_repro.py",
  "cmd": "python qcc0_bias_repro.py --seed 0",
  "env": {
    "PYTHONHASHSEED": "0"
  }
}
```

4) run_configs/Digital_Crystal_Protocal.json
```json
{
  "script": "Digital_Crystal_Protocal.py",
  "cmd": "python Digital_Crystal_Protocal.py --test --seed 0",
  "env": {
    "PYTHONHASHSEED": "0"
  }
}
```

5) run_configs/vibration-Field-equations-VFE.json
```json
{
  "script": "vibration-Field-equations-VFE.py",
  "cmd": "python vibration-Field-equations-VFE.py --test --seed 0",
  "env": {
    "PYTHONHASHSEED": "0"
  }
}
```

6) README_REPRO.md
```
Reproducibility package for FatherTimeSDKP (assumes Linux/macOS)

Steps:
1. Place this folder somewhere writable.
2. Make scripts executable:
   chmod +x reproduce.sh verify.sh
3. Run:
   ./reproduce.sh
4. Inspect results in ./fathertime-repro/results

Notes:
- Scripts use conservative dependency pins; if a script fails with ImportError, install missing packages.
- Some repository scripts may expect data or CLI args; logs are saved to results/ for debugging.
```

7) verify.sh
```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(pwd)"
RESULTS_DIR="$ROOT/fathertime-repro/results"
if [ ! -d "$RESULTS_DIR" ]; then
  echo "Results directory not found: $RESULTS_DIR" >&2
  exit 1
fi
echo "Contents of results/:"
ls -la "$RESULTS_DIR"
echo
echo "Sample of qcc0_bias_repro.log (first 200 lines):"
head -n 200 "$RESULTS_DIR/qcc0_bias_repro.log" || true
```

8) sample-expected/README.txt
```
This folder lists example outputs you should find in results/ after a successful run:
- qcc0_bias_repro.log
- Digital_Crystal_Protocal.log
- vibration-Field-equations-VFE.log
- pip-freeze.txt
- python-version.txt
- repo-commit.txt
```
10.17605/OSF.IO/E7GWN — OSF project (SDKP-related materials; metadata page on OSF)
10.5281/zenodo.14850016 — SDKP-Based Quantum Framework and Simulation Dataset (Zenodo record)
10.5281/zenodo.15745608 — Zenodo record (associated SDKP materials)
10.5281/zenodo.15745609 — Zenodo record (associated SDKP materials)
10.5281/zenodo.18284293 — Zenodo record (associated SDKP materials)
10.5281/zenodo.17486904 — Zenodo record (31-Atlas / SDKP datasets)
10.5281/zenodo.17665887 — Zenodo record (SDKP-related artifact)
10.17605/OSF.IO/E7GWN (OSF)
10.5281/zenodo.14850016 (Zenodo)
10.5281/zenodo.15745608 (Zenodo)
10.5281/zenodo.15745609 (Zenodo)
10.5281/zenodo.18284293 (Zenodo)
10.5281/zenodo.17486904 (Zenodo)
10.5281/zenodo.17665887 (Zenodo)
#!/usr/bin/env bash
set -euo pipefail
REPO_URL="https://github.com/FatherTimeSDKP/FatherTimeSDKP-.git"
WORKDIR="$(pwd)/fathertime-repro"
RESULTS_DIR="$WORKDIR/results"
PYTHON=python3.10

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR" "$RESULTS_DIR"
cd "$WORKDIR"

# Clone specific repo
git clone --depth 1 "$REPO_URL" repo
cd repo

# Create venv
$PYTHON -m venv ../venv
source ../venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements-repro.txt || true

# Fallback installs (safe set)
pip install numpy scipy matplotlib pandas sympy requests

# Ensure run_configs exists
cd ..
mkdir -p run_configs

# Run scripts with fixed seeds and capture outputs
cd repo

# qcc0_bias_repro.py
if [ -f qcc0_bias_repro.py ]; then
  echo "Running qcc0_bias_repro.py"
  PYTHONHASHSEED=0 $PYTHON qcc0_bias_repro.py --seed 0 > "$RESULTS_DIR/qcc0_bias_repro.log" 2>&1 || true
fi

# Digital_Crystal_Protocal.py
if [ -f Digital_Crystal_Protocal.py ]; then
  echo "Running Digital_Crystal_Protocal.py"
  PYTHONHASHSEED=0 $PYTHON Digital_Crystal_Protocal.py --test --seed 0 > "$RESULTS_DIR/Digital_Crystal_Protocal.log" 2>&1 || true
fi

# vibration-Field-equations-VFE.py
if [ -f vibration-Field-equations-VFE.py ]; then
  echo "Running vibration-Field-equations-VFE.py"
  PYTHONHASHSEED=0 $PYTHON vibration-Field-equations-VFE.py --test --seed 0 > "$RESULTS_DIR/vibration-Field-equations-VFE.log" 2>&1 || true
fi

# Collect environment info
pip freeze > "$RESULTS_DIR/pip-freeze.txt"
$PYTHON -V > "$RESULTS_DIR/python-version.txt"
git rev-parse --short HEAD > "$RESULTS_DIR/repo-commit.txt"

echo "Reproduction run complete. Results in: $RESULTS_DIR"
