from utils import call_model
import json
from typing import Dict

# This is the judge, which evaluates the story and provides improvement suggestions.
# It is used to improve the story after it is generated.

def evaluate_story_quality(story: str):
    """Evaluate the story's quality across multiple dimensions.
        Return a JSON with the following:
        - scores: a dictionary of scores for each dimension
        - average_score: the average score of the story
        - strengths: a list of strengths of the story
        - areas_for_improvement: a list of areas for improvement of the story
    """
    evaluation_prompt = f"""
    As a children's literature expert, evaluate this story across these dimensions:
    1. Age Appropriateness (1-10)
    2. Story Structure (1-10)
    3. Character Development (1-10)
    4. Language & Vocabulary (1-10)
    5. Engagement & Entertainment (1-10)
    6. Educational Value (1-10)
    
    Story:
    {story}
    
    Return in this JSON format:
    {{
        "scores": {{
            "age_appropriateness": score,
            "story_structure": score,
            "character_development": score,
            "language_vocabulary": score,
            "engagement": score,
            "educational_value": score
        }},
        "average_score": average,
        "strengths": ["strength1", "strength2"],
        "areas_for_improvement": ["area1", "area2"]
    }}
    """
    try:
        model_response = call_model(evaluation_prompt, temperature=0.1)
        evaluation = json.loads(model_response)
        return evaluation
    except:
        return {
            "scores": {
                "age_appropriateness": 7,
                "story_structure": 7,
                "character_development": 7,
                "language_vocabulary": 7,
                "engagement": 7,
                "educational_value": 7
            },
            "average_score": 7,
            "strengths": ["Good basic structure", "Age-appropriate language"],
            "areas_for_improvement": ["Could use more character development", "Could be more engaging"]
        }

def generate_improvement_suggestions(story: str, evaluation: Dict):
    """Generate specific improvement suggestions based on the evaluation.
        Based on the evaluation, the suggestions will focus on dimensions that have low scores or areas for improvement.
        If nothing is low, the suggestions will focus on making the story better without a focus on specific areas.
    """
    # Identify the areas that need most improvement (scores below 8)
    low_scores = {k: v for k, v in evaluation["scores"].items() if v < 8}
    improvement_areas = evaluation["areas_for_improvement"]
    
    # If all scores are high (8 or above), focus on making the story even more magical
    if not low_scores and not improvement_areas:
        suggestions_prompt = f"""
        You are a friendly story wizard who helps make stories even more magical and fun for kids ages 5-10.
        
        This is already a great story:
        {story}
        
        The story has high scores in all areas! Let's make it even more magical and exciting.
        Generate 3 fun, kid-friendly suggestions to add extra magic and wonder to the story.
        Each suggestion should:
        - Be written in a playful, magical way that kids would love
        - Add an extra layer of magic or fun to the story
        - Be something that would make a kid say "Wow!" or "That's cool!"
        - Be short and sweet - just the magical idea itself
        
        For example:
        "What if the story had a magical surprise at the end that no one expected?"
        
        Return in this JSON format:
        {{
            "suggestions": [
                "fun, magical suggestion"
            ]
        }}
        """
    else:
        suggestions_prompt = f"""
        You are a friendly story wizard who helps make stories more magical and fun for kids ages 5-10.
        
        Based on this story:
        {story}
        
        The story needs most improvement in these areas:
        {json.dumps(low_scores, indent=2)}
        
        Specific areas to improve:
        {json.dumps(improvement_areas, indent=2)}
        
        Generate 3 fun, kid-friendly suggestions that would help improve these specific areas.
        Each suggestion should:
        - Be written in a playful, magical way that kids would love
        - Directly address one of the areas that needs improvement
        - Be something that would make a kid say "Wow!" or "That's cool!"
        - Be short and sweet - just the magical idea itself
        
        For example, if "character development" needs improvement, instead of saying that directly, say something like:
        "What if Bob the cat had a special magical power that only appears when he's helping others?"
        
        Return in this JSON format:
        {{
            "suggestions": [
                "fun, magical suggestion"
            ]
        }}
        """
    
    try:
        model_response = call_model(suggestions_prompt, temperature=0.7)
        suggestions = json.loads(model_response) # Convert the JSON string to a Python dictionary
        return suggestions["suggestions"]
    except:
        # Fallback suggestions so we can still continue the story if the model fails
        return [
            "What if the story had a magical surprise at the end that no one expected?",
            "Maybe they could discover a secret magical door that leads to even more adventures!",
            "What if they found a magical object that makes their friendship even stronger?"
        ]

def judge_story(story: str):
    """Main function to evaluate a story and provide improvement suggestions."""
    # First, evaluate the story quality
    evaluation = evaluate_story_quality(story)
    
    # Then, generate specific improvement suggestions based on the evaluation
    suggestions = generate_improvement_suggestions(story, evaluation)
    
    return {
        "evaluation": evaluation,
        "suggestions": suggestions
    }