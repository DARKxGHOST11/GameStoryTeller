# 🚀 Deployment Guide for Vercel

## Prerequisites

1. GitHub account with repository: https://github.com/DARKxGHOST11/GameStoryTeller.git
2. Vercel account (free tier works)
3. Google Gemini API key

## Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/DARKxGHOST11/GameStoryTeller.git

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Epic Game Story Generator with Galaxy UI"

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your GitHub repository: `DARKxGHOST11/GameStoryTeller`
4. Vercel will auto-detect Python/Flask
5. Configure environment variables (see below)
6. Click **"Deploy"**

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? GameStoryTeller
# - Directory? ./
# - Override settings? No
```

## Step 3: Environment Variables

In Vercel Dashboard → Your Project → Settings → Environment Variables, add:

```
GOOGLE_API_KEY=your_google_api_key_here
FLASK_DEBUG=False
```

**Important:** 
- Never commit `.env` file to GitHub
- Add environment variables in Vercel dashboard
- Redeploy after adding environment variables

## Step 4: Verify Deployment

1. Visit your Vercel deployment URL (e.g., `https://gamestoryteller.vercel.app`)
2. Test story generation
3. Check logs in Vercel Dashboard if issues occur

## Troubleshooting

### Build Errors

- **Python version**: Ensure `runtime.txt` specifies `python-3.10`
- **Dependencies**: Check `requirements.txt` is complete
- **Static files**: Verify `static/` and `templates/` folders exist

### Runtime Errors

- **API Key**: Verify `GOOGLE_API_KEY` is set in Vercel
- **Port**: App automatically uses Vercel's PORT (no manual config needed)
- **Memory**: Vercel free tier has 1GB RAM limit

### Common Issues

1. **Module not found**: Add missing package to `requirements.txt`
2. **Import errors**: Check all imports are available
3. **Static files 404**: Verify `vercel.json` routes are correct

## Production Checklist

- ✅ `vercel.json` configured
- ✅ `requirements.txt` complete
- ✅ `.gitignore` excludes sensitive files
- ✅ Environment variables set in Vercel
- ✅ Static files properly routed
- ✅ Flask app uses PORT from environment
- ✅ Debug mode disabled in production

## File Structure

```
.
├── main.py              # Flask application
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version
├── .gitignore          # Git ignore rules
├── static/             # CSS, JS files
│   ├── style.css
│   └── script.js
└── templates/          # HTML templates
    └── index.html
```

## Notes

- Vercel free tier: 100GB bandwidth/month
- Serverless functions: 10s timeout (free tier)
- Image generation may be slow on free tier
- Consider upgrading for production use

## Support

If deployment fails:
1. Check Vercel build logs
2. Verify all environment variables
3. Test locally first: `python main.py`
4. Check GitHub repository is public/accessible

