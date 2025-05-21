from utils import call_model
import json

# This is the storyteller, which generates the story based on the user's prompt.

def analyze_story_request(user_prompt: str):
    """Analyze the story request to determine its type and key elements."""
    analysis_prompt = f"""
    Analyze this story request and return a JSON with the following:
    - story_type: one of [adventure, friendship, learning, fantasy, mystery]
    - key_elements: list of main characters, setting, and plot elements
    - target_age: specific age range within 5-10
    - emotional_tone: one of [happy, exciting, calming, mysterious, educational]
    
    Story request: {user_prompt}
    
    Return in this JSON format:
    {{
        "story_type": "type",
        "key_elements": ["element1", "element2"],
        "target_age": "age_range",
        "emotional_tone": "tone"
    }}
    """
    try:
        model_response = call_model(analysis_prompt, temperature=0.1)
        analysis = json.loads(model_response)
        return analysis
    except:
        # Fallback to default values if analysis fails
        return {
            "story_type": "adventure",
            "key_elements": ["main character", "magical element"],
            "target_age": "7-8",
            "emotional_tone": "happy"
        }

def get_story_template(story_type: str):
    """Get a story template based on the story type."""
    templates = {
        "adventure": """
        Story Arc:
        1. Introduction: Introduce the main character and their normal world
        2. Call to Adventure: Something changes or a problem arises
        3. Journey: The character faces challenges and meets helpers
        4. Climax: The biggest challenge or most exciting moment
        5. Resolution: How the character solves the problem and what they learn
        """,
        "friendship": """
        Story Arc:
        1. Introduction: Show the character's life before meeting their friend
        2. Meeting: How the characters meet and become friends
        3. Challenge: A problem that tests their friendship
        4. Solution: How they work together to solve it
        5. Lesson: What they learn about friendship
        """,
        "learning": """
        Story Arc:
        1. Introduction: The character's initial understanding
        2. Discovery: What they learn or discover
        3. Challenge: How they apply their new knowledge
        4. Success: How they succeed using what they learned
        5. Reflection: What they learned and how it helps them
        """,
        "fantasy": """
        Story Arc:
        1. Introduction: The magical world and its rules
        2. Discovery: The character finds something magical
        3. Adventure: How they use or explore the magic
        4. Challenge: A magical problem they must solve
        5. Resolution: How they use magic to help others
        """,
        "mystery": """
        Story Arc:
        1. Introduction: The mysterious situation
        2. Investigation: Clues the character finds
        3. Discovery: What they learn about the mystery
        4. Solution: How they solve the mystery
        5. Revelation: The truth and what they learned
        """
    }
    return templates.get(story_type, templates["adventure"])

def generate_story(user_prompt: str):
    """Generate a story based on the user's prompt with enhanced structure and age-appropriate content."""
    # First, analyze the story request
    analysis = analyze_story_request(user_prompt)
    
    # Get the appropriate story template
    template = get_story_template(analysis["story_type"])
    
    # Construct the enhanced prompt
    prompt = f"""
    You are a master children's storyteller writing a bedtime story for ages {analysis['target_age']}.
    Your story should have a {analysis['emotional_tone']} tone and be a {analysis['story_type']} story.
    
    Story Elements to Include:
    {', '.join(analysis['key_elements'])}
    
    {template}
    
    Writing Guidelines:
    - Use age-appropriate vocabulary and sentence structure
    - Include sensory details (sights, sounds, smells) to make the story come alive
    - Add dialogue to make characters more engaging
    - Include repetition and rhythm for younger readers
    - Keep the story between 250-300 words
    - End with a clear moral or lesson that's relevant to the story
    
    Original Request: {user_prompt}
    
    Now, write the story following these guidelines and structure.
    """
    
    return call_model(prompt, temperature=0.7)

def continue_story(story: str):
    """Generate a continuation of the story."""
    continuation_prompt = f"""
    You are a master children's storyteller continuing a bedtime story for ages 5-10.
    
    Here is the story so far:
    {story}
    
    Continue the story in a way that:
    - Maintains the same characters and setting
    - Keeps the same magical and playful tone
    - Adds a new exciting element or adventure
    - Keeps the story age-appropriate
    - Ends with a satisfying conclusion
    
    Write 2-3 paragraphs that continue the story naturally.
    """
    return call_model(continuation_prompt, temperature=0.7)


