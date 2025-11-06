# Vercel Deployment Notes

## Issue Fixed

**Error:** `RangeError [ERR_OUT_OF_RANGE]: The value of "size" is out of range. Received 4_311_905_200`

**Cause:** Deployment package was too large due to heavy ML dependencies (torch, diffusers, etc.)

**Solution Applied:**
1. ✅ Removed heavy ML dependencies from `requirements.txt`:
   - Removed: `torch`, `diffusers`, `accelerate`, `safetensors`, `huggingface_hub`, `moviepy`, `openai`
   - Kept only essential packages for Flask + Gemini + smolagents

2. ✅ Added `.vercelignore` to exclude large files from deployment

3. ✅ Updated `vercel.json` with function timeout settings

## Current Requirements (Optimized)

```
flask>=2.3.0
flask-cors>=4.0.0
crewai>=0.28.0
smolagents>=0.1.0
langchain>=0.1.0
langchain-community>=0.0.10
langchain-google-genai>=0.0.6
python-dotenv>=1.0.0
requests>=2.31.0
google-generativeai>=0.3.0
pillow>=10.0.0
```

## Next Steps

1. **Redeploy on Vercel** - The optimized requirements should now deploy successfully
2. **Monitor Build Logs** - Check if smolagents downloads models at runtime (this is expected)
3. **Test Image Generation** - Verify images generate correctly after deployment

## Potential Issues

### If Deployment Still Fails:

1. **smolagents Model Downloads**: smolagents may download models at runtime (not build time), which should be fine
2. **Vercel Limits**: Free tier has 100GB bandwidth/month - image generation uses bandwidth
3. **Function Timeout**: Set to 60s max - image generation might need more time

### If Image Generation Fails:

smolagents uses HuggingFace models which download at runtime. This should work, but:
- First request may be slow (model download)
- Subsequent requests will be faster
- Vercel free tier: 10s timeout (might need Pro for longer)

## Alternative Solutions (If Needed)

If deployment still fails due to size:

1. **Use External Image API**: Replace smolagents with an external API (e.g., Replicate, Stability AI)
2. **Vercel Pro Plan**: Allows larger deployments and longer timeouts
3. **Separate Image Service**: Deploy image generation as separate service

## Current Status

✅ Requirements optimized
✅ Large files excluded
✅ Configuration updated
✅ Pushed to GitHub

**Ready for Vercel redeployment!**

