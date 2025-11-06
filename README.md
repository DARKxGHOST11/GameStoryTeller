# Epic Game Story Generator

A powerful 3D UI application for generating AI-powered game stories with custom characters, dialogues, and stunning visuals.

## Features

- 🎮 **Multi-Agent Story Generation**: 5 specialized AI agents work together
  - Story Planner - Structures narrative arcs
  - Character Developer - Creates rich personalities  
  - Dialogue Writer - Crafts authentic conversations
  - Scene Designer - Designs vivid, cinematic scenes
  - Story Editor - Refines and polishes the story

- 🎨 **3D Interactive UI**: Modern, Vercel-inspired design with parallax effects
- 🖼️ **Image Generation**: Automatic scene visualization with speech bubbles
- ⚡ **Fast Generation**: Stories created in seconds
- 📝 **Customizable**: Full control over characters, genre, and story elements

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Get your Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Make sure Gemini API is enabled for your project
4. Copy the key to your `.env` file

### 3. Run the Application

```bash
python main.py
```

The app will be available at `http://localhost:7860`

## Usage

1. **Choose Model**: Select your preferred Gemini model (Flash for speed, Pro for quality)
2. **Set Genre**: Enter any genre (Fantasy, Sci-Fi, Horror, etc.)
3. **Define Characters**: Add names, appearance, vehicles, and weapons for both characters
4. **Custom Prompt (Optional)**: Add specific story requirements or themes
5. **Generate**: Click the button and watch your story come to life!

## Project Structure

```
├── main.py              # Backend Flask app with AI agents
├── templates/
│   └── index.html       # HTML structure
├── static/
│   ├── style.css        # Modern 3D UI styles
│   └── script.js        # Interactive JavaScript
├── requirements.txt     # Python dependencies
└── .env                 # API keys (create this)
```

## Troubleshooting

### Gemini API Errors

If you see "404 models/gemini-xxx not found":

1. **Check API Key**: Make sure your `GOOGLE_API_KEY` is valid
2. **Enable API**: Visit [Google Cloud Console](https://console.cloud.google.com/) and enable the Generative Language API
3. **Check Permissions**: Ensure your API key has access to Gemini models
4. **Region**: Some regions may not have access to all models

### Model Not Working

The app tries multiple model names automatically:
- `gemini-1.5-flash` 
- `gemini-1.5-flash-latest`
- `gemini-pro`
- `gemini-1.0-pro`

If none work, check your API configuration.

### Image Generation Slow

Images are generated in parallel with 3 workers. For faster generation:
- Reduce the number of scenes
- Use `gemini-1.5-flash` instead of Pro
- Ensure good internet connection

## Technologies

- **Backend**: Flask, Python 3.10+
- **AI**: Google Gemini API, CrewAI agents
- **Image Generation**: Smolagents text-to-image
- **Frontend**: Vanilla JavaScript, Modern CSS
- **Styling**: Custom 3D CSS with parallax effects

## Features in Detail

### Multi-Agent System

The app uses 5 specialized AI agents that collaborate:

1. **Story Planner**: Creates the overall narrative structure
2. **Character Developer**: Develops personalities and relationships
3. **Dialogue Writer**: Writes natural, engaging dialogue
4. **Scene Designer**: Designs visually rich scenes
5. **Story Editor**: Ensures coherence and quality

### 3D UI

- Parallax background that moves with cursor
- 3D particle system with WebGL
- Glass-morphism design elements
- Smooth animations and transitions
- Mobile-responsive layout

### Smart Dialogue Parsing

The system automatically:
- Extracts dialogue from story text
- Matches speakers to characters
- Formats conversations properly
- Includes dialogues in generated images

## Contributing

Feel free to fork and improve! Key areas for contribution:
- Additional AI agents
- More story genres
- Enhanced image generation
- UI improvements

## Deployment

### Deploy to Vercel

This project is configured for easy deployment on Vercel:

1. **Push to GitHub**: 
   ```bash
   git push origin main
   ```

2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Add environment variable: `GOOGLE_API_KEY=your_key_here`
   - Click Deploy

3. **See DEPLOYMENT.md** for detailed instructions

### Production Checklist

- ✅ `vercel.json` configured
- ✅ Environment variables set
- ✅ Static files properly routed
- ✅ Production-ready Flask configuration

## License

MIT License - feel free to use for personal or commercial projects

## Credits

Built with:
- Google Gemini API
- CrewAI
- Flask
- Smolagents

---

Made with ⚡ by AI-powered creativity

