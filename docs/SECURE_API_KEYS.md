# 🔐 Secure API Key Management for Heroku

This guide explains how to securely manage your OpenAI API key for this Rock Paper Scissors app deployed on Heroku.

## ✅ Current Security Status

Your app is **already configured correctly** for secure API key management:

- ✅ API key is read from environment variable (`OPENAI_API_KEY`)
- ✅ No hardcoded API keys in the code
- ✅ `.env` files are in `.gitignore` (won't be committed)
- ✅ Error handling if API key is missing

## 🚀 Setting Up on Heroku

### Method 1: Using Heroku CLI (Recommended)

```bash
# Set the OpenAI API key as a Heroku config var
heroku config:set OPENAI_API_KEY=your_actual_api_key_here -a your-app-name

# Verify it was set (will show masked value)
heroku config:get OPENAI_API_KEY -a your-app-name

# View all config vars
heroku config -a your-app-name
```

### Method 2: Using Heroku Dashboard (Web UI)

1. Go to your Heroku Dashboard: https://dashboard.heroku.com/
2. Select your app (e.g., `rock-paper-scissors`)
3. Click on the **Settings** tab
4. Scroll down to **Config Vars** section
5. Click **Reveal Config Vars**
6. Add a new config var:
   - **KEY**: `OPENAI_API_KEY`
   - **VALUE**: Your actual OpenAI API key (e.g., `sk-...`)
7. Click **Add**

Your app will automatically restart and pick up the new environment variable.

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Click **Create new secret key**
5. Give it a name (e.g., "Rock Paper Scissors Heroku")
6. Copy the key immediately (you won't be able to see it again!)
7. Use this key in your Heroku config

## 💻 Local Development Setup

For local development, create a `.env` file in the project root:

```bash
# Create .env file (this will NOT be committed to git)
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

Then load it when running locally:

```bash
# Option 1: Export manually
export OPENAI_API_KEY=your_actual_api_key_here
python app.py

# Option 2: Use python-dotenv (already installed)
# The app will automatically load from .env if it exists
python app.py
```

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use environment variables for all API keys
- ✅ Keep `.env` in `.gitignore`
- ✅ Use different API keys for development and production
- ✅ Rotate API keys periodically
- ✅ Set usage limits on your OpenAI account
- ✅ Monitor API usage on OpenAI dashboard

### ❌ DON'T:
- ❌ Hardcode API keys in your code
- ❌ Commit `.env` files to git
- ❌ Share API keys in chat, email, or screenshots
- ❌ Use the same API key across multiple projects
- ❌ Leave unused API keys active

## 🧪 Testing the Setup

After setting the config var on Heroku:

1. Deploy your app to Heroku
2. Open the app in your browser
3. Play some games (at least 5)
4. Click "View OpenAI Commentary"
5. You should see AI-generated commentary

If you see an error:
- Check that the config var is set correctly
- Verify your API key is valid on OpenAI platform
- Check Heroku logs: `heroku logs --tail -a your-app-name`

## 📊 Monitoring API Usage

Keep track of your OpenAI API costs:

1. Go to https://platform.openai.com/usage
2. Monitor daily/monthly usage
3. Set up billing alerts
4. Consider setting usage limits

## 🆘 Troubleshooting

### Error: "OpenAI API key not found"
**Solution**: Set the `OPENAI_API_KEY` config var on Heroku (see above)

### Error: "Invalid API key"
**Solution**: 
1. Check that your API key is correct
2. Verify it's active on OpenAI platform
3. Create a new API key if needed

### Error: "Rate limit exceeded"
**Solution**: 
1. Your API key has hit usage limits
2. Wait for the limit to reset
3. Upgrade your OpenAI plan if needed

### Commentary not loading
**Solution**:
1. Check Heroku logs: `heroku logs --tail`
2. Verify you have billing set up on OpenAI
3. Ensure you have available credits

## 📝 Code Reference

The API key is used in `app.py`:

```python
# Read from environment variable
api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    return jsonify({
        'error': 'OpenAI API key not found. Please set OPENAI_API_KEY environment variable.'
    }), 500

# Use the API key
client = OpenAI(api_key=api_key)
```

This is the **secure way** to handle API keys - never hardcode them!

## 🔄 Rotating API Keys

To rotate your API key:

1. Create a new key on OpenAI platform
2. Update Heroku config var:
   ```bash
   heroku config:set OPENAI_API_KEY=new_key_here -a your-app-name
   ```
3. Delete the old key on OpenAI platform

## 📚 Additional Resources

- [Heroku Config Vars Documentation](https://devcenter.heroku.com/articles/config-vars)
- [OpenAI API Keys Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [12-Factor App Configuration](https://12factor.net/config)

---

## ✅ Summary

Your app is **already secure**! You just need to:

1. Get your OpenAI API key from https://platform.openai.com/
2. Set it as a Heroku config var: `OPENAI_API_KEY`
3. Deploy your app
4. Enjoy AI-powered commentary! 🎉

**Never commit API keys to git - always use environment variables!** 🔐

