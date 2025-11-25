# Configuration Files

This directory contains configuration templates and examples for the Rock Paper Scissors game.

## Files

### `env.example`
Template for environment variables.

**Usage:**
```bash
# Copy to project root and rename to .env
cp config/env.example .env

# Edit .env with your actual values
nano .env  # or your preferred editor
```

**Contents:**
```bash
# OpenAI API Key for ChatGPT Commentary
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration (optional)
# FLASK_ENV=development
# FLASK_DEBUG=1
```

**Security:**
- ✅ `.env` is in `.gitignore` and will NOT be committed to git
- ✅ Never share your actual `.env` file
- ✅ Get your OpenAI API key from: https://platform.openai.com/api-keys

---

## Environment Variables

### Required for OpenAI Commentary Feature

**`OPENAI_API_KEY`**
- Required for: AI-powered gameplay commentary
- Get from: https://platform.openai.com/api-keys
- Cost: Uses GPT-4o-mini model (very affordable)
- Feature: "View OpenAI Commentary" button in web interface

Without this key:
- Game still works fully
- OpenAI commentary button will show error
- All other features (AI opponents, statistics, etc.) work normally

### Optional Flask Configuration

**`FLASK_ENV`**
- Values: `development` or `production`
- Default: `production`
- Effect: Controls debug mode and error messages

**`FLASK_DEBUG`**
- Values: `0` (off) or `1` (on)
- Default: `0`
- Effect: Auto-reloading and detailed error pages

**`PORT`**
- Values: Any valid port number
- Default: `5000`
- Effect: Which port Flask runs on

---

## Setup Instructions

### Local Development

1. **Create your .env file:**
   ```bash
   cp config/env.example .env
   ```

2. **Add your OpenAI API key:**
   ```bash
   echo "OPENAI_API_KEY=sk-..." >> .env
   ```

3. **Verify it's ignored by git:**
   ```bash
   git status  # Should NOT show .env
   ```

### Production Deployment

For production platforms (Heroku, Railway, etc.), set environment variables through the platform:

**Heroku:**
```bash
heroku config:set OPENAI_API_KEY=your_key_here
```

**Railway:**
Use the Railway dashboard → Variables section

**Docker:**
```bash
docker run -e OPENAI_API_KEY=your_key_here ...
```

---

## Adding New Configuration

If you add new environment variables:

1. **Add to `env.example`** with placeholder value
2. **Document in this README**
3. **Update** `../docs/OPENAI_SETUP.md` if relevant
4. **Update deployment docs** in `../deployment/`

---

## Related Files

- `../.gitignore` - Ensures `.env` is not committed
- `../deployment/HEROKU_DEPLOYMENT.md` - Production config guide
- `../docs/OPENAI_SETUP.md` - OpenAI API setup details
- `../docs/SECURE_API_KEYS.md` - Security best practices
- `../app.py` - Reads environment variables

---

## Security Best Practices

✅ **DO:**
- Use `env.example` as a template
- Keep your `.env` file in the project root (where `.gitignore` protects it)
- Use different API keys for development and production
- Rotate API keys periodically
- Set appropriate API usage limits

❌ **DON'T:**
- Commit `.env` to git (it's in `.gitignore`)
- Share your actual API keys
- Hardcode API keys in source code
- Use production keys in development
- Expose `.env` file via web server

---

## Troubleshooting

**"API key not found" error:**
1. Verify `.env` exists in project root
2. Check `.env` contains `OPENAI_API_KEY=sk-...`
3. Restart the Flask server
4. Check file isn't named `.env.txt` or similar

**OpenAI API errors:**
1. Verify key is valid at platform.openai.com
2. Check you have API credits
3. Ensure key has proper permissions
4. Review rate limits

For more help, see `../docs/OPENAI_SETUP.md`

