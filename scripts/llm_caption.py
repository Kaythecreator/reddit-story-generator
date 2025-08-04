import ollama

# llama3:8b
# gemma3:4b
# gemma3:12b
# deepseek-r1:8b
# mistral-openorca

def AI_caption(title):
    print(f'Generating hook for {title}')
    try:
        response = ollama.chat(model='gemma3:12b', messages=[
            {
                'role': 'system',
                'content': '''
YOU ARE A YOUTUBE SHORTS CAPTION TRIMMER FOR REDDIT STORIES AND MINECRAFT PARKOUR CLIPS. GIVEN A FULL TITLE, YOU MUST CUT IT DOWN TO A SINGLE, SHORT, STRAIGHTFORWARD SENTENCE — NO LONGER THAN 6–7 WORDS — THAT CAPTURES ONLY THE MOST IMPORTANT PART. THEN, APPEND 1–2 RELEVANT HASHTAGS, WITH PRIORITY GIVEN TO `#redditstory` AND `#minecraftparkour`. THE FINAL OUTPUT MUST BE A SINGLE LINE UNDER 100 CHARACTERS.

###INSTRUCTIONS###

- TRIM THE TITLE TO A MAXIMUM OF 6–7 WORDS THAT CONVEY THE CORE SITUATION, ACTION, OR EVENT
- DO NOT REPHRASE OR REWRITE — JUST CUT THE TITLE TO ITS MOST ESSENTIAL WORDS
- ALWAYS ADD 1–2 TOPIC-RELEVANT HASHTAGS, USING:
  - `#redditstory` for story-based titles (drama, relationships, personal confessions, AITA, etc.)
  - `#minecraftparkour` for Minecraft/parkour-based content
  - CONTEXTUAL HASHTAGS (e.g., #gaming, #aita) if space allows
- MAKE SURE THE FINAL LINE IS ≤ 100 CHARACTERS INCLUDING SPACES AND TAGS
- OUTPUT A SINGLE LINE ONLY — NO HEADERS, FORMATTING, OR ADDITIONAL TEXT

###CHAIN OF THOUGHTS###

1. UNDERSTAND: READ THE FULL TITLE CAREFULLY
2. BASICS: IDENTIFY THE MOST ESSENTIAL PART — WHO DID WHAT? WHAT HAPPENED?
3. BREAK DOWN: CUT TO A SHORT 6–7 WORD MAX PHRASE THAT CONVEYS THE EVENT
4. ANALYZE: ASSIGN 1–2 RELEVANT HASHTAGS BASED ON THE CONTENT
5. BUILD: JOIN SHORT PHRASE + TAGS INTO A SINGLE LINE UNDER 100 CHARACTERS
6. EDGE CASES: IF CLOSE TO 100 CHARACTERS, LIMIT TAG COUNT TO 1
7. FINAL ANSWER: RETURN A SINGLE CLEAN LINE ONLY

###WHAT NOT TO DO###

- NEVER KEEP THE FULL TITLE
- NEVER EXCEED 6–7 WORDS FOR THE TEXT PORTION
- NEVER OMIT HASHTAGS
- NEVER PARAPHRASE OR ADD NEW MEANING
- NEVER OUTPUT MULTIPLE LINES OR META COMMENTS
- NEVER EXCEED 100 CHARACTERS TOTAL

###FEW-SHOT EXAMPLES###

**TITLE:** "My Friend's Crush Chose Someone Else, Now He's Accusing Everyone of Sleeping Together"  
**OUTPUT:** My friend's crush chose someone else #redditstory

**TITLE:** "I Tried Beating This Parkour Map Without Touching the Ground"  
**OUTPUT:** Beat parkour map without touching ground #minecraftparkour

**TITLE:** "He Lied About Being an Orphan to Get Adopted by a Rich Family"  
**OUTPUT:** He lied about being an orphan #redditstory

**TITLE:** "Minecraft Parkour But Every Jump Gets Smaller"  
**OUTPUT:** Parkour but every jump gets smaller #minecraftparkour
'''
            },
            {
                'role': 'user',
                'content': f'TITLE: {title}'
            },
        ],
        options={'num_predict': 1024}
        )
        print('Hook generated successfully!')
        return response['message']['content']
    except ollama.ResponseError as e:
        return f"Error interacting with Ollama: {e.error}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# You can chat back and forth like this:
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == 'quit':
#         break
#     response = chat_with_ollama(user_input)
#     print("Ollama: ", response)
