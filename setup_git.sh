#!/bin/bash
# Git setup script for GameStoryTeller

echo "🚀 Setting up Git repository for GameStoryTeller..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add remote (will fail if already exists, that's okay)
git remote add origin https://github.com/DARKxGHOST11/GameStoryTeller.git 2>/dev/null || git remote set-url origin https://github.com/DARKxGHOST11/GameStoryTeller.git

echo "✅ Remote repository configured"

# Add all files
git add .

echo "✅ Files staged"

# Commit
git commit -m "Initial commit: Epic Game Story Generator with Galaxy UI - Production ready for Vercel"

echo "✅ Changes committed"

echo ""
echo "📤 Ready to push! Run:"
echo "   git push -u origin main"
echo ""
echo "Or if your default branch is 'master':"
echo "   git push -u origin master"
echo ""

