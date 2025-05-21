from storyteller import generate_story, continue_story
from judge import judge_story

# This is a CLI app that generates bedtime stories. 
# This is the CLI controller and user interaction loop.

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

If I had two more hours, I'd probably focus on a few things to make the experience feel more complete. Here are some ideas:
- Add more complete story templates: I'd include a wider range of built-in templates for different vibes, or maybe try prompting the model 
to come up with custom templates based on what the user asks for.
- Track user feedback: I'd set up a db to track whether someone liked or disliked the story, and store that along with the original 
prompt and any edits they chose. That way, the system could start to learn what kinds of stories or suggestions people respond to most.
- Safety checks: I might add some content filters or run the story through another judge focused on safety, to make sure themes and language
are appropriate for the target age range.
- Build a simple frontend: I built this as a CLI app, but I'd add a lightweight frontend, maybe something with a night sky background, a 
typewriter / read aloud effect for the story, and thumbs up/down buttons, just to make it feel more like a bedtime story app and less like a script.
"""

def display_story_evaluation(evaluation):
    """Display the story evaluation in a user-friendly format."""
    print("\n📊 Story Evaluation:")
    print("-------------------")
    scores = evaluation["scores"]
    print(f"Age Appropriateness: {scores['age_appropriateness']}/10")
    print(f"Story Structure: {scores['story_structure']}/10")
    print(f"Character Development: {scores['character_development']}/10")
    print(f"Language & Vocabulary: {scores['language_vocabulary']}/10")
    print(f"Engagement: {scores['engagement']}/10")
    print(f"Educational Value: {scores['educational_value']}/10")
    print(f"\nOverall Score: {evaluation['average_score']}/10")
    
    print("\n✨ Strengths:")
    for strength in evaluation["strengths"]:
        print(f"• {strength.capitalize()}")
    
    print("\n🔧 Areas for Improvement:")
    for area in evaluation["areas_for_improvement"]:
        print(f"• {area.capitalize()}")

def main():
    print("🌙 Welcome to the Bedtime Story Generator!\n")
    print("I can help you create a magical story for children ages 5-10.")
    print("You can ask for any type of story - adventure, friendship, learning, fantasy, or mystery!")
    print("Try a story prompt like: 'A story about a girl named Alice and her best friend Bob, who happens to be a cat.'\n")
    
    user_input = input("What kind of story do you want to hear? ")

    while True:
        print(f"\n💭 The storyteller is thinking...")
        story = generate_story(user_input)
        print(f"\n📘 Here's your story:\n")
        print(story)

        while True:
            print("\nWhat would you like to do?")
            print("1. Get feedback and improve the story")
            print("2. Continue the story")
            print("3. Start a new story")
            print("4. Exit")
            
            choice = input("\nPick a number (1-4): ")
            
            if choice == "1":
                print(f"\n🧐 Let's see how we can improve it...")
                judge_response = judge_story(story)
                
                # Display the evaluation
                display_story_evaluation(judge_response["evaluation"])
                
                # Display improvement suggestions
                print("\n💡 Here are some ways we can make the story even better:")
                suggestions = judge_response["suggestions"]
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")
                print("4. Add my own idea")

                choice = input("\nPick a number (1-4): ")
                if choice == "4":
                    suggestion = input("Enter your own idea: ")
                else:
                    try:
                        suggestion = suggestions[int(choice) - 1]
                    except (ValueError, IndexError):
                        print("Invalid choice. Using the first suggestion.")
                        suggestion = suggestions[0]

                print("\n🔁 Regenerating the story with your feedback...\n")
                user_input = f"Here is the original story: {story}\n\nPlease revise the story to address the following: {suggestion}"
                break
                
            elif choice == "2":
                print("\n✨ Continuing the story...\n")
                continuation = continue_story(story)
                print(continuation)
                story = story + "\n\n" + continuation
                
            elif choice == "3":
                user_input = input("\nWhat kind of story do you want to hear? ")
                break
                
            elif choice == "4":
                print("\n🌟 Sweet dreams! I'm glad you enjoyed the story!")
                return
                
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()