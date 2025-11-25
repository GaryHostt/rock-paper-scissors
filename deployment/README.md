# Deployment Configuration

This directory contains files needed for deploying the Rock Paper Scissors game to production environments.

## Files

### `Procfile`
Heroku process file that tells Heroku how to run the application:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### `HEROKU_DEPLOYMENT.md`
Complete guide for deploying to Heroku, including:
- Prerequisites and setup
- Step-by-step deployment instructions
- Environment variable configuration
- Troubleshooting tips
- Monitoring and maintenance

## Usage

### Deploy to Heroku
See `HEROKU_DEPLOYMENT.md` for detailed instructions.

Quick start:
```bash
# From project root
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
git push heroku main
```

### Other Platforms

The configuration in this directory is Heroku-specific, but the concepts apply to other platforms:
- **AWS Elastic Beanstalk**: Can use the Procfile
- **Google App Engine**: Needs `app.yaml` instead
- **Docker**: See suggested Dockerfile in `docs/BEST_PRACTICES.md`
- **Railway/Render**: Can use the Procfile directly

## Requirements

All deployment platforms need:
- Python 3.13+
- Dependencies from `requirements.txt` (in project root)
- Gunicorn web server (included in requirements)
- Environment variables (especially `OPENAI_API_KEY` for commentary feature)

## Related Documentation

- `../docs/BEST_PRACTICES.md` - Docker and deployment best practices
- `../README.md` - Main project documentation
- `../config/env.example` - Environment variable template

