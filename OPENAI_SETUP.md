# OpenAI Commentary Setup Guide

This guide explains how to set up OpenAI-powered commentary for your Rock Paper Scissors game.

## 📋 Prerequisites

1. An OpenAI API account
2. An OpenAI API key

## 🔑 Getting Your API Key

1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys** in your account settings
4. Click **"Create new secret key"**
5. Copy the key (it starts with `sk-...`)
6. **Important:** Save it somewhere safe - you won't be able to see it again!

## 💻 Setting Up the API Key

### Option 1: Set Environment Variable (Recommended)

#### On macOS/Linux:

**Temporary (current terminal session only):**
```bash
export OPENAI_API_KEY='sk-your-api-key-here'
```

**Permanent (add to your shell profile):**
```bash
# For Bash (add to ~/.bashrc or ~/.bash_profile)
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# For Zsh (add to ~/.zshrc)
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### On Windows:

**Temporary (current command prompt):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

**Permanent (System Environment Variables):**
1. Press `Win + X` and select **System**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Under **User variables**, click **New**
5. Variable name: `OPENAI_API_KEY`
6. Variable value: `sk-your-api-key-here`
7. Click **OK** on all windows

### Option 2: Create a .env File (Alternative)

1. Create a file named `.env` in your project root:
```bash
cd /path/to/cursor-11242025
touch .env
```

2. Add your API key to the file:
```
OPENAI_API_KEY=sk-your-api-key-here
```

3. Install python-dotenv:
```bash
pip3 install python-dotenv
```

4. Update `app.py` to load from .env:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top of your app.py
```

## 📦 Install OpenAI Library

```bash
# If using virtual environment (recommended):
cd /path/to/cursor-11242025
source venv/bin/activate

# Install openai
pip3 install openai
```

Or add to your `requirements.txt`:
```
Flask==3.0.0
Flask-CORS==4.0.0
openai>=1.0.0
```

Then run:
```bash
pip3 install -r requirements.txt
```

## ✅ Verifying the Setup

1. Start your Flask server:
```bash
cd /path/to/cursor-11242025
source venv/bin/activate  # if using venv
python3 app.py
```

2. Open your game in the browser: `http://localhost:5000`

3. Play at least 5 games

4. Click the menu (☰) and select **"🤖 View OpenAI Commentary"**

5. If everything is set up correctly, you'll see AI-generated commentary analyzing your gameplay!

## 🔍 Troubleshooting

### "OpenAI library is not installed"
**Solution:** Run `pip3 install openai`

### "OpenAI API key not found"
**Solution:** Make sure you've set the `OPENAI_API_KEY` environment variable correctly. Try restarting your terminal and server.

### "Need at least 5 games for meaningful commentary"
**Solution:** Play more rounds! The AI needs data to analyze.

### API Key Not Working
- Make sure you copied the entire key (starts with `sk-`)
- Check that there are no extra spaces or quotes
- Verify your API key is active on [platform.openai.com](https://platform.openai.com/)

### "Error generating commentary"
- Check your internet connection
- Verify you have API credits on your OpenAI account
- Check the browser console (Cmd+Option+I) for detailed error messages

## 💰 Cost Information

- The app uses the `gpt-4o-mini` model by default (very affordable)
- Cost per commentary request: ~$0.001-0.002 (less than a penny!)
- You can change the model in `app.py` (line ~385) to `gpt-4` for better quality but higher cost

## 🔒 Security Best Practices

1. **Never commit your API key to Git!**
   - Add `.env` to your `.gitignore` file
   - Never hardcode the key in your code

2. **Use environment variables** instead of storing in code

3. **Rotate your keys regularly** on the OpenAI platform

4. **Set usage limits** on your OpenAI account to prevent unexpected charges

## 📝 How It Works

When you click "View OpenAI Commentary":

1. The frontend sends your last 50 games to the backend
2. The backend formats the data and sends it to OpenAI's API
3. OpenAI's GPT model analyzes your gameplay patterns
4. The commentary is displayed in a sidebar

The commentary includes:
- Overall performance assessment
- Pattern detection in your play style
- Strengths and weaknesses
- Strategic recommendations
- Notable trends

## 🎮 Enjoy AI-Powered Insights!

Now you can get professional-level analysis of your Rock Paper Scissors strategy! 🚀

