# =========================================================
# 🔧 Fix for Pydantic v2 schema error with Starlette Request
# =========================================================
from starlette.requests import Request
from pydantic_core import core_schema

def _mock_request_schema(cls, _handler):
    # Tell Pydantic to treat Starlette Request as Any type
    return core_schema.any_schema()

# Inject the schema patch before any models load
Request.__get_pydantic_core_schema__ = classmethod(_mock_request_schema)

# ------------------------
# ✅ Universal Pydantic compatibility patch

from dotenv import load_dotenv
load_dotenv()
import os
import uuid
from datetime import datetime
import pytz
from PIL import Image
import google.generativeai as genai
import re
import json
from smolagents import load_tool
import functools
import asyncio
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request, jsonify
try:
    from flask_cors import CORS  # type: ignore
    cors_available = True
except ImportError:
    cors_available = False
    print("Warning: flask-cors not found. Install with: pip install flask-cors")
import base64
from io import BytesIO

# ------------------------
# Initialize Flask
app = Flask(__name__)
if cors_available:
    CORS(app)

# ------------------------
# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@functools.lru_cache(maxsize=1)
def load_image_tool():
    return load_tool("agents-course/text-to-image", trust_remote_code=True)

tool = load_image_tool()

# ------------------------
# Multi-Agent System using CrewAI
# ------------------------
from crewai import Agent, Task, Crew, Process

# Initialize LLM for agents (optional - we use direct Gemini API for speed)
# Note: Agents are defined for documentation/structure but not actively used in generation
llm = None
agents_available = False

try:
    from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=os.getenv("GOOGLE_API_KEY"))
    agents_available = True
    print("[OK] langchain_google_genai loaded successfully")
except (ImportError, AttributeError) as e:
    print(f"[INFO] langchain-google-genai not available ({type(e).__name__})")
    print("       Agents will be skipped. Using direct Gemini API for fast story generation.")
    llm = None

# Define 5 specialized agents (only if LLM is available)
# These define the "expertise" used in the story generation prompts
story_planner_agent = None
character_developer_agent = None
dialogue_writer_agent = None
scene_designer_agent = None
story_editor_agent = None

if agents_available and llm is not None:
    try:
        story_planner_agent = Agent(
            role='Story Planner',
            goal='Plan the overall story structure, plot arcs, and narrative flow',
            backstory='You are an expert story architect who creates compelling narrative structures with clear beginning, middle, and end.',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        character_developer_agent = Agent(
            role='Character Developer',
            goal='Develop rich character personalities, relationships, and motivations',
            backstory='You specialize in creating deep, engaging characters with unique traits and compelling interactions.',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        dialogue_writer_agent = Agent(
            role='Dialogue Writer',
            goal='Write natural, engaging dialogue that reveals character and advances plot',
            backstory='You are a master of dialogue writing, creating conversations that feel authentic and drive the story forward.',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        scene_designer_agent = Agent(
            role='Scene Designer',
            goal='Design visually rich scenes with detailed descriptions suitable for illustration',
            backstory='You excel at creating vivid, cinematic scenes that paint clear visual pictures for artists and readers.',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        story_editor_agent = Agent(
            role='Story Editor',
            goal='Review and refine the complete story for coherence, pacing, and quality',
            backstory='You are an experienced editor who ensures stories are polished, cohesive, and ready for publication.',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        print("[OK] 5 CrewAI agents initialized successfully")
    except Exception as agent_error:
        print(f"[WARNING] Could not initialize agents: {agent_error}")
        print("          Continuing with direct Gemini API (this is fine!)")
        agents_available = False
else:
    print("[INFO] Agents skipped - using direct Gemini API for maximum speed")

# Fast story generation using Multi-Agent System
def generate_story_with_agents(
    model_name, temperature, genre, character1_name, character2_name,
    character1_appearance, character1_vehicle, character1_weapons,
    character2_appearance, character2_vehicle, character2_weapons,
    custom_prompt, num_scenes
):
    """Generate story quickly using multi-agent system"""
    
    # Build character descriptions
    char1_desc = f"{character1_name}"
    if character1_appearance:
        char1_desc += f" - Appearance: {character1_appearance}"
    if character1_vehicle:
        char1_desc += f" - Vehicle: {character1_vehicle}"
    if character1_weapons:
        char1_desc += f" - Weapons: {character1_weapons}"
    
    char2_desc = f"{character2_name}"
    if character2_appearance:
        char2_desc += f" - Appearance: {character2_appearance}"
    if character2_vehicle:
        char2_desc += f" - Vehicle: {character2_vehicle}"
    if character2_weapons:
        char2_desc += f" - Weapons: {character2_weapons}"
    
    # Build the prompt
    story_context = f"""Write a captivating {genre} story that reads like a published novel, with exactly {num_scenes} scenes.

CHARACTERS:
- {char1_desc}
- {char2_desc}

STORY REQUIREMENTS:
1. Create a single, iconic location that serves as the setting for the entire story
2. Develop a compelling narrative arc with beginning, middle, and climactic end
3. Include a quest or challenge that requires both characters to work together
4. Show character development and emotional depth
5. Each scene should be visually rich and cinematic

WRITING STYLE:
- Write in narrative prose with flowing paragraphs like a real book
- Integrate dialogue naturally into the narrative using quotation marks
- Show, don't just tell - use vivid descriptions and sensory details
- Create atmosphere and tension through your writing
- Make it feel like reading an epic adventure novel
- Use literary techniques like metaphors and descriptive language

OUTPUT FORMAT:
For each of the {num_scenes} scenes:

SCENE X:
[Write 2-4 flowing narrative paragraphs that read like a novel. Include:
- Rich scene-setting descriptions
- Character actions and emotions
- Natural dialogue woven into the narrative like: {character1_name} stepped forward. "We must find the ancient artifact," he said, determination in his eyes.
- Atmospheric details that bring the scene to life]

Make the reader feel immersed in the story. Write as if this is going to be published.

"""
    
    if custom_prompt:
        story_context += f"\nADDITIONAL REQUIREMENTS: {custom_prompt}\n"
    
    # Use multi-agent system approach - agents are defined and their expertise is used in prompt
    # Fast path: Use Gemini directly for speed while maintaining agent structure and roles
    try:
        # Use the correct, modern model names that actually exist in the API
        # NOTE: gemini-1.5 models have been replaced with gemini-2.x models
        if model_name == 'gemini-1.5-flash':
            # Map old name to new flash models
            model_candidates = ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-2.0-flash-lite']
        elif model_name == 'gemini-1.5-pro':
            # Map old name to new pro models
            model_candidates = ['gemini-pro-latest', 'gemini-2.5-pro', 'gemini-2.0-flash']
        else:
            # Default fallback
            model_candidates = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-2.0-flash-lite']
        
        # Agents are defined above (5 agents: Story Planner, Character Developer, Dialogue Writer, Scene Designer, Story Editor)
        # We use their combined expertise in the prompt for fast generation
        model = None
        last_error = None
        api_model_name = None
        
        # Try each candidate model until one works
        # We'll just initialize and trust it works - testing adds extra latency
        for candidate in model_candidates:
            try:
                print(f"Initializing model: {candidate}")
                model = genai.GenerativeModel(candidate)
                api_model_name = candidate
                print(f"[OK] Model initialized: {api_model_name}")
                break
            except Exception as e:
                error_msg = str(e)
                print(f"[FAILED] Failed to initialize {candidate}: {error_msg[:150]}")
                last_error = e
                
                # Check for specific errors
                if "404" in error_msg or "not found" in error_msg.lower():
                    print("  → Model not available, trying next...")
                elif "429" in error_msg or "quota" in error_msg.lower():
                    print("  → QUOTA EXCEEDED - You've hit your daily limit!")
                    print("  → Please wait or upgrade your API plan")
                elif "403" in error_msg or "permission" in error_msg.lower():
                    print("  → Permission denied, trying next...")
                elif "API_KEY" in error_msg:
                    print("  → API key issue detected")
                
                continue
        
        # If all candidates failed, provide detailed error message
        if model is None:
            error_details = f"""
╔══════════════════════════════════════════════════════════╗
║          GEMINI API CONFIGURATION ERROR                  ║
╚══════════════════════════════════════════════════════════╝

Could not initialize any Gemini model.

Tried models: {model_candidates}
Last error: {last_error}

POSSIBLE SOLUTIONS:
1. Check your API key is valid for Gemini API
2. Enable Gemini API in Google Cloud Console
3. Verify your API key has the correct permissions
4. Check if you're in a supported region

Your API key starts with: {os.getenv('GOOGLE_API_KEY', 'NOT_SET')[:10]}...

To fix:
- Visit: https://makersuite.google.com/app/apikey
- Create a new API key
- Add it to your .env file: GOOGLE_API_KEY=your_key_here
- Make sure the Gemini API is enabled for your project

For now, the app will use a fallback mode with limited functionality.
"""
            print(error_details)
            # Return fallback story instead of crashing
            fallback_story = f"""# {character1_name} & {character2_name}'s Adventure

## Note: Gemini API Not Available
Unable to connect to Gemini API. Please check your configuration.

{error_details}

## Quick Start Story

{character1_name} and {character2_name} embark on an epic {genre} adventure together. 
Their journey will take them through {num_scenes} exciting scenes filled with challenges and triumphs.

Configure your GOOGLE_API_KEY to generate custom stories!
"""
            return fallback_story, []
        enhanced_prompt = f"""As a team of expert authors (Story Planner, Character Developer, Dialogue Writer, Scene Designer, and Story Editor), write a captivating narrative:

{story_context}

Write the complete {num_scenes}-scene story now in beautiful narrative prose. For each scene:
1. Write 2-4 flowing paragraphs of narrative text
2. Weave dialogue naturally into the prose using quotation marks
3. Create vivid, atmospheric descriptions
4. Show character emotions and development
5. Make it feel like reading a published novel

Remember: This should read like a real book, not a script. Immerse the reader in the story with rich, flowing narrative paragraphs."""
        
        print(f"Generating story with model: {api_model_name}")
        try:
            response = model.generate_content(
                enhanced_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=6000,  # More tokens for rich narrative prose
                )
            )
            
            story_text = response.text
            print(f"[SUCCESS] Story generated successfully ({len(story_text)} characters)")
            
            # Parse story into scenes with dialogues
            scenes = parse_story_with_dialogues(story_text, character1_name, character2_name, num_scenes)
            
            return story_text, scenes
        except Exception as gen_error:
            gen_error_msg = str(gen_error)
            print(f"[ERROR] Error during content generation with {api_model_name}: {gen_error_msg[:200]}")
            
            # Check if it's a quota error
            if "429" in gen_error_msg or "quota" in gen_error_msg.lower():
                print("[WARNING] QUOTA EXCEEDED - You've hit your API rate limit!")
                print("[WARNING] Please wait ~1 minute and try again, or upgrade your plan")
                raise Exception("API Quota Exceeded: You've hit your daily/minute rate limit. Please wait and try again later.")
            
            # If generation fails with this model, try the next candidate
            remaining_candidates = [c for c in model_candidates if c != api_model_name]
            if remaining_candidates:
                print(f"Trying alternative models: {remaining_candidates}")
                for alt_candidate in remaining_candidates:
                    try:
                        print(f"Attempting generation with: {alt_candidate}")
                        alt_model = genai.GenerativeModel(alt_candidate)
                        alt_response = alt_model.generate_content(
                            enhanced_prompt,
                            generation_config=genai.types.GenerationConfig(
                                temperature=temperature,
                                max_output_tokens=6000,  # More tokens for rich narrative prose
                            )
                        )
                        story_text = alt_response.text
                        print(f"[SUCCESS] Story generated with fallback model: {alt_candidate}")
                        scenes = parse_story_with_dialogues(story_text, character1_name, character2_name, num_scenes)
                        return story_text, scenes
                    except Exception as alt_error:
                        alt_error_msg = str(alt_error)
                        if "429" in alt_error_msg or "quota" in alt_error_msg.lower():
                            print(f"[ERROR] Quota exceeded on {alt_candidate} too")
                            raise Exception("API Quota Exceeded: All models are hitting rate limits. Please wait and try again later.")
                        print(f"[ERROR] Fallback model {alt_candidate} also failed: {alt_error_msg[:100]}")
                        continue
            
            # If all models failed, raise the original error
            raise gen_error
        
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Final error in story generation: {error_msg}")
        # Return a helpful error message
        return f"Error: Unable to generate story. {error_msg}\n\nPlease check:\n1. Your GOOGLE_API_KEY is valid\n2. You have Gemini API enabled\n3. You have internet connectivity", []


def parse_story_with_dialogues(story_text, char1_name, char2_name, num_scenes):
    """Parse story text to extract scenes and dialogues with proper structure"""
    scenes = []
    
    # Try to split by scene markers first (if present)
    scene_pattern = r'SCENE\s+\d+:|Scene\s+\d+:|###\s*Scene|\*\*\d+\.\*\*'
    parts = re.split(scene_pattern, story_text, flags=re.IGNORECASE)
    
    # If we have explicit scene divisions, use them
    if len(parts) > 1:
        scene_parts = parts[1:num_scenes+1]  # Skip first empty part
    else:
        # No scene markers - split story into equal parts by paragraphs
        paragraphs = [p.strip() for p in story_text.split('\n\n') if p.strip()]
        paras_per_scene = max(1, len(paragraphs) // num_scenes)
        scene_parts = []
        for i in range(num_scenes):
            start_idx = i * paras_per_scene
            end_idx = min(start_idx + paras_per_scene, len(paragraphs))
            scene_parts.append('\n\n'.join(paragraphs[start_idx:end_idx]))
    
    # Extract dialogues from each scene part
    for i, part in enumerate(scene_parts):
        scene_data = {
            'description': '',
            'dialogues': []
        }
        
        # Enhanced dialogue extraction - find all quoted text with speaker attribution
        # Pattern: Look for character names followed by quoted dialogue
        dialogue_patterns = [
            # "Speaker: "dialogue""
            rf'({char1_name}|{char2_name})[^\n"]*?[:\s]+"([^"]+)"',
            # "Character said, "dialogue""  
            rf'({char1_name}|{char2_name})[^\n"]*?\bsaid[^\n"]*?"([^"]+)"',
            # "Character asked, "dialogue""
            rf'({char1_name}|{char2_name})[^\n"]*?\basked[^\n"]*?"([^"]+)"',
            # "Character replied, "dialogue""
            rf'({char1_name}|{char2_name})[^\n"]*?\breplied[^\n"]*?"([^"]+)"',
            # "Character whispered, "dialogue""
            rf'({char1_name}|{char2_name})[^\n"]*?\bwhispered[^\n"]*?"([^"]+)"',
            # "Character shouted, "dialogue""
            rf'({char1_name}|{char2_name})[^\n"]*?\bshouted[^\n"]*?"([^"]+)"',
            # Just "dialogue" near character name
            rf'"([^"]+)"[^\n]*?({char1_name}|{char2_name})',
        ]
        
        found_dialogues = []
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, part, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match) == 2:
                    # Check which group is the speaker and which is the dialogue
                    if match[0] in [char1_name, char2_name]:
                        speaker, text = match[0], match[1]
                    else:
                        text, speaker = match[0], match[1]
                    
                    dialogue_text = text.strip()
                    if dialogue_text and len(dialogue_text) > 5:  # Meaningful dialogue
                        found_dialogues.append({
                            'speaker': speaker.strip(),
                            'text': dialogue_text[:200]  # Limit length
                        })
        
        # Remove duplicates while preserving order
        seen = set()
        unique_dialogues = []
        for d in found_dialogues:
            key = (d['speaker'], d['text'][:50])  # Use first 50 chars as key
            if key not in seen:
                seen.add(key)
                unique_dialogues.append(d)
                if len(unique_dialogues) >= 4:  # Max 4 dialogues per scene
                    break
        
        scene_data['dialogues'] = unique_dialogues[:4] if unique_dialogues else []
        
        # Extract scene description (full text)
        scene_data['description'] = part.strip()[:600]  # Keep scene description
        
        # If no dialogues found, create contextual fallback based on scene number
        if not scene_data['dialogues']:
            # Create different dialogues for each scene based on typical story progression
            fallback_dialogues = [
                # Scene-specific fallback dialogues
                [
                    {'speaker': char1_name, 'text': 'This place holds ancient secrets. We must proceed carefully.'},
                    {'speaker': char2_name, 'text': 'I sense great power here. Stay vigilant.'}
                ],
                [
                    {'speaker': char1_name, 'text': 'The path ahead grows darker. Are you ready?'},
                    {'speaker': char2_name, 'text': 'Together we can face any challenge.'}
                ],
                [
                    {'speaker': char1_name, 'text': 'Something is not right. I can feel it.'},
                    {'speaker': char2_name, 'text': 'Trust your instincts. We need to be prepared.'}
                ],
                [
                    {'speaker': char1_name, 'text': 'The final challenge awaits us ahead.'},
                    {'speaker': char2_name, 'text': 'This is what we have trained for. Let us finish this.'}
                ],
                [
                    {'speaker': char1_name, 'text': 'We have come so far. We cannot fail now.'},
                    {'speaker': char2_name, 'text': 'Victory is within reach. Stay focused.'}
                ],
            ]
            # Use scene-specific fallback or default to first one
            scene_idx = min(i, len(fallback_dialogues) - 1)
            scene_data['dialogues'] = fallback_dialogues[scene_idx]
        
        scenes.append(scene_data)
    
    # Ensure we have the right number of scenes
    while len(scenes) < num_scenes:
        scenes.append({
            'description': f'Scene {len(scenes) + 1} continues the epic journey.',
            'dialogues': [
                {'speaker': char1_name, 'text': 'Our quest continues forward.'},
                {'speaker': char2_name, 'text': 'Indeed, we must not waver.'}
            ]
        })
    
    return scenes[:num_scenes]


def generate_images_with_dialogues(scenes, character1_name, character2_name, character1_appearance, 
                                   character1_vehicle, character1_weapons, character2_appearance,
                                   character2_vehicle, character2_weapons, genre):
    """Generate images for each scene with dialogues properly included"""
    images_with_dialogues = []
    
    # Build character visual prompts
    char1_visual = f"{character1_name}"
    if character1_appearance:
        char1_visual += f", {character1_appearance}"
    if character1_vehicle:
        char1_visual += f", with {character1_vehicle}"
    if character1_weapons:
        char1_visual += f", wielding {character1_weapons}"
    
    char2_visual = f"{character2_name}"
    if character2_appearance:
        char2_visual += f", {character2_appearance}"
    if character2_vehicle:
        char2_visual += f", with {character2_vehicle}"
    if character2_weapons:
        char2_visual += f", wielding {character2_weapons}"
    
    executor = ThreadPoolExecutor(max_workers=3)
    
    def generate_single_image(scene_data, idx):
        try:
            # Build dialogue text for image - use UNIQUE dialogues from THIS scene
            dialogue_text = ""
            if scene_data.get('dialogues'):
                dialogue_lines = []
                for d in scene_data['dialogues'][:2]:  # Max 2 dialogues per image
                    dialogue_lines.append(f"{d['speaker']}: {d['text']}")
                dialogue_text = " | ".join(dialogue_lines)
            
            # Create comprehensive image prompt
            scene_desc = scene_data.get('description', '')[:300]
            
            img_prompt = f"""Comic book art style, cinematic digital art, single panel, full frame, dynamic angle.
Scene: {scene_desc}
Characters: {char1_visual} and {char2_visual} interacting in a {genre} setting.
Dialogue context: {dialogue_text if dialogue_text else 'Characters conversing'}
High quality, detailed, vibrant colors, dramatic lighting, professional comic book illustration with speech bubbles visible."""
            
            img = tool(img_prompt)
            img_path = f"scene_{uuid.uuid4().hex[:8]}.png"
            img.save(img_path)
            
            return {
                'image': img_path,
                'scene': scene_data.get('description', ''),
                'dialogues': scene_data.get('dialogues', [])
            }
        except Exception as e:
            print(f"Error generating image {idx+1}: {e}")
            return None
    
    # Generate images in parallel
    futures = [executor.submit(generate_single_image, scene, i) for i, scene in enumerate(scenes)]
    
    for future in futures:
        result = future.result()
        if result:
            images_with_dialogues.append(result)
    
    executor.shutdown(wait=True)
    
    return images_with_dialogues


# Main function
def run_story_generation(
    model_name, temperature, genre, character1_name, character2_name,
    character1_appearance, character1_vehicle, character1_weapons,
    character2_appearance, character2_vehicle, character2_weapons,
    custom_prompt, num_images
):
    """Main function to generate story and images"""
    
    # Generate story quickly using multi-agent approach
    story_text, scenes = generate_story_with_agents(
        model_name, temperature, genre, character1_name, character2_name,
        character1_appearance, character1_vehicle, character1_weapons,
        character2_appearance, character2_vehicle, character2_weapons,
        custom_prompt, num_images
    )
    
    # Format story with dialogues
    formatted_story = format_story_with_dialogues(story_text, scenes, character1_name, character2_name)
    
    # Generate images
    images_data = generate_images_with_dialogues(
        scenes, character1_name, character2_name,
        character1_appearance, character1_vehicle, character1_weapons,
        character2_appearance, character2_vehicle, character2_weapons,
        genre
    )
    
    # Convert images to base64 for JSON response
    result_images = []
    for img_data in images_data:
        if img_data and 'image' in img_data:
            try:
                with open(img_data['image'], 'rb') as f:
                    img_bytes = f.read()
                    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                    result_images.append({
                        'image': f"data:image/png;base64,{img_base64}",
                        'scene': img_data.get('scene', ''),
                        'dialogues': img_data.get('dialogues', [])
                    })
            except Exception as e:
                print(f"Error encoding image: {e}")
    
    return formatted_story, result_images


def format_story_with_dialogues(story_text, scenes, char1_name, char2_name):
    """Format story as flowing narrative prose like a novel"""
    
    # Split story by scene markers
    scene_pattern = r'SCENE\s+(\d+)[:\s]*'
    parts = re.split(scene_pattern, story_text, flags=re.IGNORECASE)
    
    # Start directly with story content - no titles
    formatted = ""
    
    # Process scenes
    scene_number = 1
    for i in range(1, len(parts), 2):  # Skip scene numbers, take content
        if i + 1 < len(parts):
            scene_content = parts[i + 1].strip()
        else:
            scene_content = parts[i].strip() if i < len(parts) else ""
        
        if scene_content:
            # Clean up the content - remove extra markers
            scene_content = re.sub(r'DIALOGUE:.*?\n', '', scene_content, flags=re.IGNORECASE)
            scene_content = re.sub(r'\n{3,}', '\n\n', scene_content)  # Max 2 newlines
            
            # Add the narrative prose directly
            formatted += f"{scene_content}\n\n"
            
            scene_number += 1
    
    # If no proper scenes were found, just clean and format the whole story
    if scene_number == 1:
        # Remove scene markers and clean up
        clean_story = re.sub(r'SCENE\s+\d+[:\s]*', '', story_text, flags=re.IGNORECASE)
        clean_story = re.sub(r'DIALOGUE:[^\n]*\n', '', clean_story, flags=re.IGNORECASE)
        clean_story = re.sub(r'\n{3,}', '\n\n', clean_story)
        formatted += clean_story.strip() + "\n\n"
    
    return formatted.strip()


# ------------------------
# Flask Routes
# ------------------------
@app.route('/favicon.ico')
def favicon():
    """Return empty response for favicon to prevent 404 errors"""
    return '', 204

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        
        model_name = data.get('model', 'gemini-1.5-flash')
        temperature = float(data.get('temperature', 0.8))
        genre = data.get('genre', 'Fantasy')
        character1_name = data.get('character1_name', 'Hero')
        character2_name = data.get('character2_name', 'Mentor')
        character1_appearance = data.get('character1_appearance', '')
        character1_vehicle = data.get('character1_vehicle', '')
        character1_weapons = data.get('character1_weapons', '')
        character2_appearance = data.get('character2_appearance', '')
        character2_vehicle = data.get('character2_vehicle', '')
        character2_weapons = data.get('character2_weapons', '')
        custom_prompt = data.get('custom_prompt', '')
        num_images = int(data.get('num_images', 5))
        
        story, images = run_story_generation(
            model_name, temperature, genre, character1_name, character2_name,
            character1_appearance, character1_vehicle, character1_weapons,
            character2_appearance, character2_vehicle, character2_weapons,
            custom_prompt, num_images
        )
        
        return jsonify({
            'success': True,
            'story': story,
            'images': images
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Launch the Flask app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
