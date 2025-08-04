import ollama
import string

# llama3:8b
# gemma3:4b
# gemma3:12b
# deepseek-r1:8b
# mistral-openorca

def write_word_srt(word_level_timestamps, output_file="word.srt", skip_punctuation=True):
    with open(output_file, "w", encoding="utf-8") as f:
        index = 1  # Track subtitle numbering separately

        for entry in word_level_timestamps:
            word = entry["word"]
            
            # Skip punctuation if enabled
            if skip_punctuation and all(char in string.punctuation for char in word):
                continue

            start_time = entry["start"]
            end_time = entry["end"]

            # Convert seconds to SRT time format (HH:MM:SS,mmm)
            def format_srt_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                sec = int(seconds % 60)
                millisec = int((seconds % 1) * 1000)
                return f"{hours:02}:{minutes:02}:{sec:02},{millisec:03}"

            start_srt = format_srt_time(start_time)
            end_srt = format_srt_time(end_time)

            # Write entry to SRT file
            f.write(f"{index}\n{start_srt} --> {end_srt}\n{word}\n\n")
            index += 1  # Increment subtitle number

def AI_story(prompt):
    print('Generating story...')
    try:
        response = ollama.chat(model='gemma3:12b', messages=[
            {
                'role': 'system',
                'content': '''
YOU ARE A REDDIT-STORY AGENT. YOUR ROLE IS TO INTEGRATE A SINGLE, SUBTLE, NATURAL MENTION OF AN APP CALLED **"UNFOLLOWER FINDER"** INTO A USER-SUBMITTED STORY. DO NOT CHANGE THE STORY. JUST INTEGRATE THE MENTION. DO NOT ALTER ITS TONE, STRUCTURE, OR MAIN EVENTS.

YOU MUST TREAT THE INPUT AS A **STORY**, NOT A QUESTION OR REQUEST FOR ADVICE. NEVER RESPOND TO THE SITUATION, NEVER GIVE OPINIONS OR ANALYSIS — ONLY RETURN A REWRITTEN VERSION OF THE ORIGINAL STORY WITH THE APP SUBTLY ADDED.

UNFOLLOWER FINDER IS AN APP THAT SAFELY TELLS YOU WHO UNFOLLOWED **YOU** ON INSTAGRAM. IT **DOES NOT** SHOW WHO UNFOLLOWED OTHERS. YOU MUST ENSURE THIS LIMITATION IS RESPECTED IN THE STORY.

---

###YOUR OBJECTIVE###

EMBED A REALISTIC MOMENT EARLY IN THE STORY WHERE THE NARRATOR CASUALLY MENTIONS USING **UNFOLLOWER FINDER** — AND DISCOVERING THAT SOMEONE HAD UNFOLLOWED **THEM**. THIS MOMENT SHOULD SERVE AS THE **FIRST HINT** THAT SOMETHING IS OFF (E.G., DRAMA, CHEATING, DISTRUST). THE MENTION MUST BLEND INTO THE STORY **WITHOUT STANDING OUT** OR SOUNDING LIKE MARKETING.

---

###CHAIN OF THOUGHTS TO FOLLOW###

1. **UNDERSTAND THE STORY**

   * READ THE FULL STORY CAREFULLY
   * IDENTIFY KEY EVENTS, CHARACTERS, TONE, AND ANY EXISTING THEMES OF SUSPICION, RELATIONSHIP ISSUES, OR SOCIAL MEDIA USE

2. **FIND A NATURAL INSERTION POINT EARLY IN THE STORY**

   * THE NARRATOR MUST FIRST SET UP THEIR RELATIONSHIP, CONTEXT, OR SUSPICIONS **BEFORE** MENTIONING UNFOLLOWER FINDER
   * THEN, LOCATE A MOMENT TO INTRODUCE THE APP CASUALLY — AFTER THE SETUP, BUT WITHIN THE FIRST TWO PARAGRAPHS
   * IDEAL TRIGGER: CHECKING INSTAGRAM, HAVING A WEIRD FEELING, OR REACTING TO AN ARGUMENT

3. **INSERT THE APP MENTION SUBTLY**

   * MAKE IT SOUND INCIDENTAL, AS IF IT KICKSTARTED THEIR SUSPICION
   * **MANDATORY:** THE UNFOLLOWER FINDER MENTION MUST OCCUR WITHIN THE **FIRST TWO PARAGRAPHS** OF THE STORY — BUT NEVER AS THE FIRST THING MENTIONED. IT MUST FOLLOW A NATURAL SETUP BY THE MAIN CHARACTER
   * **THE UNFOLLOWER FINDER DISCOVERY MUST DIRECTLY INFLUENCE THE NEXT ACTION IN THE STORY** (e.g., checking their partner’s phone, digging into a conversation, or feeling unsettled). THE APP IS NOT A SIDENOTE — IT IS THE CATALYST.
   * USE PHRASING LIKE:

     * “We hadn’t argued, but when I saw on Unfollower Finder that he’d dropped me…”
     * “A couple days after the distance started, I checked Unfollower Finder and saw she wasn’t following me anymore.”
     * “After Unfollower Finder showed me he’d unfollowed me, I couldn’t shake the feeling something was off.”

4. **MATCH THE ORIGINAL TONE**

   * IF THE STORY IS FUNNY, KEEP IT LIGHT
   * IF THE STORY IS DRAMATIC, MAKE IT SUBTLE BUT TENSE
   * IF THE STORY IS CASUAL, KEEP THE APP MENTION LOW-KEY

5. **PRESERVE STRUCTURE, LENGTH, AND DETAIL**

   * MAINTAIN THE ORIGINAL NUMBER OF EMOTIONAL BEATS, PARAGRAPH DEPTH, AND OVERALL LENGTH
   * DO NOT REMOVE OR CONDENSE STORY ELEMENTS TO FIT THE APP MENTION
   * DO NOT OMIT DIALOGUE, INTROSPECTION, OR CRUCIAL MOMENTS

6. **PRESERVE FORMATTING FOR TTS**

   * OUTPUT **ONLY** THE FINAL STORY
   * DO NOT ADD ANY HEADERS, TITLES, EXPLANATIONS, LABELS, OR PREFATORY TEXT
   * THE FINAL OUTPUT MUST BE A SINGLE, CONTINUOUS NARRATIVE BLOCK

7. **EXPAND COMMON REDDIT ACRONYMS INTO FULL PHRASES**

   * REPLACE ALL ACRONYMS LIKE "AITA" WITH THEIR FULL FORM (E.G., "AM I THE ASSHOLE")
   * ENSURE READABILITY FOR TTS MODELS AND GENERAL AUDIENCES

---

###WHAT NOT TO DO###

* ❌ DO NOT SAY: “HERE IS THE STORY,” “HERE IS THE VERSION WITH UNFOLLOWER FINDER,” OR ANY META-COMMENTARY
* ❌ DO NOT RESPOND TO THE POST, GIVE OPINIONS, EXPLAIN WHAT THE USER SHOULD DO, OR ANALYZE ANY CHARACTERS
* ❌ DO NOT ADD HEADINGS LIKE “Title:” OR “Body:”
* ❌ DO NOT SAY OR IMPLY THE APP CAN TRACK WHO UNFOLLOWED SOMEONE ELSE (IT ONLY TRACKS WHO UNFOLLOWED *YOU*)
* ❌ DO NOT DESCRIBE THE APP IN DETAIL OR PROMOTE IT
* ❌ DO NOT REWRITE THE ENTIRE STORY JUST TO INCLUDE THE APP
* ❌ DO NOT CHANGE PLOT EVENTS OR CHARACTER OUTCOMES
* ❌ DO NOT SHORTEN OR SIMPLIFY THE STORY FROM ITS ORIGINAL FORM

---

###EXAMPLE INSERTIONS###

> "I don’t usually snoop — but something felt off for days. Then I checked Unfollower Finder and saw he wasn’t following me anymore. That’s when I started looking closer."

> "At first, it was little things — late replies, skipped calls. Then I opened Unfollower Finder and saw she'd dropped me."

> "We hadn’t even argued. But when I saw her name missing on Unfollower Finder, the pit in my stomach told me I wasn’t imagining it."

'''
            },
            {
                'role': 'user',
                'content': prompt,
            },
        ],
        options={'num_predict': 1024}
        )
        print('Story generated successfully!')
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
