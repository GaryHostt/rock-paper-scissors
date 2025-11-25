# Heroku Deployment Guide

This guide explains how to deploy the Rock Paper Scissors game to Heroku.

---

## 🚀 Quick Deploy

### Prerequisites
- Heroku account ([signup](https://signup.heroku.com/))
- Heroku CLI installed ([install](https://devcenter.heroku.com/articles/heroku-cli))
- Git repository initialized

---

## 📝 Required Files (Already Configured)

The following files have been created for Heroku deployment (located in `deployment/` directory):

### 1. **Procfile**
Tells Heroku how to run your app:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### 2. **.python-version**
Specifies Python version:
```
3.13
```

### 3. **requirements.txt** (Updated)
Added `gunicorn` web server:
```
Flask==3.0.0
Flask-CORS==4.0.0
openai>=1.0.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
```

---

## 🛠️ Deployment Steps

### Step 1: Login to Heroku
```bash
heroku login
```

### Step 2: Create Heroku App
```bash
heroku create rock-paper-scissors-app
# Or let Heroku generate a random name:
heroku create
```

### Step 3: Set Environment Variables (Optional)
If using OpenAI commentary feature:
```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: Commit Changes
```bash
git add deployment/Procfile .python-version requirements.txt
git commit -m "Add Heroku deployment configuration"
```

### Step 5: Deploy to Heroku
```bash
git push heroku main
```

Or if your main branch is named `master`:
```bash
git push heroku master
```

### Step 6: Open Your App
```bash
heroku open
```

---

## 🔍 Troubleshooting

### Check Logs
```bash
heroku logs --tail
```

### View Build Logs
```bash
heroku logs --source app
```

### Restart App
```bash
heroku restart
```

### Check App Status
```bash
heroku ps
```

---

## ⚙️ Configuration

### Scale Dynos (Free Tier)
```bash
heroku ps:scale web=1
```

### View App Info
```bash
heroku info
```

### View Config Variables
```bash
heroku config
```

---

## 📊 What Was Fixed

The original deployment failed because:

❌ **Problem 1**: No `Procfile`
- Heroku didn't know how to start the app

✅ **Solution**: Created `deployment/Procfile` with gunicorn command

❌ **Problem 2**: No Python version specified
- Warning about relying on default version

✅ **Solution**: Created `.python-version` file with `3.13`

❌ **Problem 3**: Missing `gunicorn`
- Development server (Flask's built-in) not suitable for production

✅ **Solution**: Added `gunicorn>=21.2.0` to requirements.txt

---

## 🌐 Environment Variables

### Required (if using features)
- `OPENAI_API_KEY` - For OpenAI commentary feature (optional)

### Automatically Set by Heroku
- `PORT` - Port number for the app to listen on

---

## 📱 Post-Deployment

After successful deployment:

1. ✅ Test the app in browser
2. ✅ Verify all features work
3. ✅ Check that static files load correctly
4. ✅ Test API endpoints
5. ✅ Monitor logs for any errors

---

## 🔒 Security Notes

- Never commit `.env` file (it's in `.gitignore`)
- Set sensitive keys using `heroku config:set`
- Use Heroku's environment variables for secrets

---

## 💡 Tips

### Custom Domain
```bash
heroku domains:add www.yourdomain.com
```

### Enable HTTPS (Automatic on Heroku)
Heroku automatically provides HTTPS for all apps.

### View Recent Deploys
```bash
heroku releases
```

### Rollback to Previous Version
```bash
heroku rollback v2
```

---

## 📈 Monitoring

### View App Metrics
```bash
heroku addons:create newrelic:wayne
```

### View Database (if added)
```bash
heroku pg:info
```

---

## 🎯 Common Issues & Solutions

### Issue: "Application Error"
**Solution**: Check logs with `heroku logs --tail`

### Issue: Static files not loading
**Solution**: Verify static files are committed to git

### Issue: App crashes on startup
**Solution**: Check Procfile syntax and ensure gunicorn is installed

### Issue: Environment variables not working
**Solution**: Use `heroku config:set KEY=value` instead of .env file

---

## 🔄 Continuous Deployment

### Option 1: GitHub Integration
1. Go to Heroku Dashboard
2. Select your app
3. Click "Deploy" tab
4. Connect to GitHub repository
5. Enable automatic deploys

### Option 2: Heroku Git (Manual)
```bash
git push heroku main
```

---

## 📚 Additional Resources

- [Heroku Python Documentation](https://devcenter.heroku.com/categories/python-support)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/3.0.x/deploying/)

---

## ✅ Deployment Checklist

- [x] Create `deployment/Procfile`
- [x] Create `.python-version`
- [x] Add `gunicorn` to requirements.txt
- [x] Test locally with gunicorn: `gunicorn app:app`
- [ ] Commit all changes
- [ ] Create Heroku app
- [ ] Set environment variables (if needed)
- [ ] Deploy to Heroku
- [ ] Test deployed app
- [ ] Monitor logs

---

**Your app is now ready for Heroku deployment!** 🚀

Follow the steps above to deploy your Rock Paper Scissors game to the cloud.


