# Deployment Troubleshooting Guide

## psycopg2 ImportError Fix

### Problem
```
ImportError: /opt/render/project/src/.venv/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-x86_64-linux-gnu.so: undefined symbol: _PyInterpreterState_Get
```

### Root Cause
This error occurs when:
1. The deployment environment uses Python 3.13 instead of the specified version
2. psycopg2-binary wheels are incompatible with Python 3.13
3. There's a mismatch between the Python version and compiled binaries

### Solutions Applied

#### 1. Updated Python Version
- Changed `runtime.txt` from `python-3.11.9` to `python-3.11.10`
- Python 3.11.10 has better compatibility with psycopg2-binary

#### 2. Updated psycopg2 Version
- Changed from `psycopg2-binary==2.9.9` to `psycopg2-binary==2.9.7`
- Version 2.9.7 has better stability with Python 3.11.x

#### 3. Added Render Configuration
- Created `render.yaml` with explicit Python version specification
- Added build dependencies for PostgreSQL

### Alternative Solutions (if above fails)

#### Option 1: Use psycopg (version 3)
Replace in `requirements.txt`:
```
# Replace psycopg2-binary==2.9.7 with:
psycopg[binary]==3.1.18
```

#### Option 2: Force Python 3.11
In Render dashboard:
1. Go to Environment Variables
2. Add: `PYTHON_VERSION=3.11.10`

#### Option 3: Build from Source
Replace in `requirements.txt`:
```
# Replace psycopg2-binary==2.9.7 with:
psycopg2==2.9.7
```
Note: Requires PostgreSQL development headers on the build system.

### Verification Steps
1. Check deployment logs for Python version being used
2. Verify psycopg2 installation completes without errors
3. Test database connection after deployment

### Additional Notes
- Always ensure `runtime.txt` specifies the exact Python version
- psycopg2-binary is preferred for deployment simplicity
- If using PostgreSQL locally, install with: `pip install psycopg2-binary`