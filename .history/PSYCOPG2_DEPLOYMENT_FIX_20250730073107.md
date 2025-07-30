# psycopg2 Deployment Fix for Render

## Problem
The application was failing to deploy on Render with the following error:
```
ImportError: /opt/render/project/src/.venv/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-x86_64-linux-gnu.so: undefined symbol: _PyInterpreterState_Get
```

This error occurs due to Python version mismatch - the deployment environment was using Python 3.13, but the configuration was set for Python 3.11.9, causing psycopg2 binary compatibility issues.

## Solution Applied

### 1. Updated requirements.txt
- **Changed**: Updated `psycopg2-binary` from version `2.9.7` to `2.9.9`
- **Removed**: Redundant `psycopg2` dependency (keeping only `psycopg2-binary`)
- **Reason**: `psycopg2-binary` includes pre-compiled binaries and doesn't require system PostgreSQL libraries

### 2. Updated Python Version Configuration
- **Updated**: Python version from `3.11.9` to `3.13.0` in both `runtime.txt` and `render.yaml`
- **Fixed**: Version consistency across all configuration files
- **Reason**: Match the actual Python version being used in the deployment environment

### 3. Updated render.yaml
- **Updated**: Python version to `3.13.0` for consistency
- **Maintained**: Proper database configuration with connection string environment variable
- **Kept**: Simplified build command to avoid unnecessary system package installations
- **Maintained**: Production environment variables for Flask

### 4. Configuration Files Status
- ✅ `config.py` - Already properly configured to handle PostgreSQL URLs
- ✅ `runtime.txt` - Updated to specify Python 3.13.0
- ✅ `render.yaml` - Updated with Python 3.13.0 configuration
- ✅ `requirements.txt` - Updated with latest psycopg2-binary version (2.9.10)

## Key Changes Made

### requirements.txt
```diff
- psycopg2-binary==2.9.9
+ psycopg2-binary==2.9.10
+ # Alternative option for Python 3.13 compatibility (uncomment if psycopg2 fails):
+ # psycopg[binary]==3.1.18
```

### runtime.txt
```diff
- python-3.11.9
+ python-3.13.0
```

### render.yaml
```yaml
services:
  - type: web
    name: sacco-management
    env: python
    runtime: python
    pythonVersion: "3.13.0"
    buildCommand: |
      echo "Python version:"
      python --version
      echo "Upgrading pip..."
      pip install --upgrade pip
      echo "Installing Python dependencies..."
      pip install -r requirements.txt
      echo "Build completed successfully"
    startCommand: gunicorn run:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.13.0"
      - key: DATABASE_URL
        fromDatabase:
          name: sacco-db
          property: connectionString
      - key: FLASK_ENV
        value: production
      - key: FLASK_APP
        value: run.py
    
databases:
  - name: sacco-db
    databaseName: sacco_management
    user: sacco_user
```

## Verification

A deployment verification script (`verify_deployment.py`) has been created to help troubleshoot future deployment issues. Run it locally with:

```bash
python verify_deployment.py
```

## Expected Results After Fix

1. **Build Phase**: Should complete without psycopg2 import errors
2. **Runtime**: Application should connect to PostgreSQL database successfully
3. **Database**: Migrations should run properly with PostgreSQL

## Alternative Solutions (if issues persist)

If the above solution doesn't work, try these alternatives:

### Option 1: Use psycopg2-binary with specific version
```txt
psycopg2-binary==2.9.5
```

### Option 2: Add system dependencies (if needed)
```yaml
buildCommand: |
  apt-get update && apt-get install -y libpq-dev
  pip install --upgrade pip
  pip install -r requirements.txt
```

### Option 3: Use psycopg (modern alternative) - Recommended for Python 3.13
```txt
# Replace psycopg2-binary with:
psycopg[binary]==3.1.18
```

This is the recommended approach for Python 3.13 as psycopg3 has better support for newer Python versions.

## Troubleshooting Steps

1. **Check Build Logs**: Look for specific error messages during pip install
2. **Verify Python Version**: Ensure consistency between runtime.txt and render.yaml
3. **Test Locally**: Run `verify_deployment.py` to check dependencies
4. **Database Connection**: Verify DATABASE_URL environment variable is set
5. **Migration Issues**: Run migrations manually if needed

## Files Modified
- `requirements.txt` - Updated psycopg2-binary version
- `render.yaml` - Complete configuration update
- `verify_deployment.py` - New verification script (created)
- `PSYCOPG2_DEPLOYMENT_FIX.md` - This documentation (created)

## Next Steps
1. Commit these changes to your repository
2. Push to trigger a new deployment on Render
3. Monitor the build logs for successful psycopg2 installation
4. Verify the application starts and connects to the database