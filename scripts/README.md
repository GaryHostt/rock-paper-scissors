# Utility Scripts

This directory contains helper scripts for common development and validation tasks.

## Scripts

### `start_server.sh`
Quick start script for the Flask development server.

**Usage:**
```bash
./scripts/start_server.sh
```

**What it does:**
1. Changes to project root directory
2. Activates the virtual environment
3. Starts the Flask server on port 5000

**Alternative:** Run directly from project root:
```bash
python app.py
```

---

### `validate.sh`
Comprehensive validation script that checks if all game components are properly configured.

**Usage:**
```bash
./scripts/validate.sh
```

**What it validates:**
- ✓ Flask backend files (app.py)
- ✓ Streak visualization HTML
- ✓ CSS animations
- ✓ JavaScript streak logic
- ✓ AI difficulty levels
- ✓ Testing framework
- ✓ MCP server implementation
- ✓ Documentation files
- ✓ Configuration files
- ✓ Python dependencies

**Output:**
- Green ✓ for passed checks
- Red ✗ for failed checks
- Summary with pass/fail counts

---

## Making Scripts Executable

If you get a "permission denied" error, make the scripts executable:

```bash
chmod +x scripts/start_server.sh
chmod +x scripts/validate.sh
```

## Creating New Scripts

When adding new utility scripts:

1. **Add to this directory** (`scripts/`)
2. **Use proper shebang**: `#!/bin/bash`
3. **Navigate to project root**: `cd "$(dirname "$0")/.."`
4. **Make executable**: `chmod +x scripts/your_script.sh`
5. **Document here**: Add description to this README

## Related Files

- `../testing/run_tests.sh` - Test execution script (in testing directory)
- `../app.py` - Main Flask application
- `../integrations/mcp_server.py` - MCP server for Claude Desktop

