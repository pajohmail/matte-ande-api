import json
import os
import openai
from prompt_template import MATTE_ANDE_PROMPT

def lambda_handler(event, context):
    """
    AWS Lambda handler för att framkalla matte-anden
    """
    # Hantera CORS preflight (OPTIONS)
    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        # Kontrollera att API-nyckel finns
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "status": "error",
                    "message": "OpenAI API-nyckel saknas!"
                })
            }
        openai.api_key = api_key

        # Extrahera data från event
        body = json.loads(event.get('body', '{}'))
        user_prompt = body.get('prompt', '').strip()
        if not user_prompt:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "status": "error",
                    "message": "Ingen prompt angiven!"
                })
            }
        operation = body.get('operation', 'addition')
        difficulty = body.get('difficulty', 'easy')
        history = body.get('history', [])

        # Formatera historiken om den finns
        history_text = ""
        if history and isinstance(history, list) and len(history) > 0:
            history_text = "\nTidigare frågor och svar:\n"
            for i, entry in enumerate(history[:3], 1):
                if isinstance(entry, dict):
                    q = str(entry.get("question", "")).strip()
                    a = str(entry.get("answer", "")).strip()
                    if q and a:
                        history_text += f"{i}. Fråga: {q}\n   Svar: {a}\n"

        operation_prompts = {
            'addition': "Förklara hur man adderar talen och visar stegen tydligt.",
            'subtraction': "Förklara hur man subtraherar talen och visar stegen tydligt.",
            'multiplication': "Förklara hur man multiplicerar talen och visar stegen tydligt.",
            'division': "Förklara hur man dividerar talen och visar stegen tydligt."
        }
        difficulty_context = {
            'easy': "Använd enkla tal och grundläggande koncept för en nybörjare-trollkarl.",
            'medium': "Använd lite svårare tal och koncept för en trollkarl under utbildning.",
            'hard': "Använd utmanande tal och koncept för en nästan fullärd trollkarl."
        }
        full_prompt = (
            f"{MATTE_ANDE_PROMPT}\n"
            f"{history_text}\n"
            f"Matteproblemet är: {user_prompt}\n\n"
            f"{operation_prompts.get(operation, '')}\n"
            f"{difficulty_context.get(difficulty, '')}"
        )

        # OpenAI klassisk syntax (v0.28.1)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        ande_response = response["choices"][0]["message"]["content"]
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "success",
                "message": ande_response
            })
        }
    except Exception as e:
        print(f"Lambda-fel: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "error",
                "message": f"Magisk olycka: {str(e)}"
            })
        } 