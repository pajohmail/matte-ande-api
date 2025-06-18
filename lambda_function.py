"""
Matte-Ande API - AWS Lambda Function
===================================

Detta är en AWS Lambda-funktion som hanterar interaktioner med OpenAI's GPT-3.5
för att skapa en interaktiv matte-ande som hjälper barn att lära sig matematik.

Funktionalitet:
-------------
- Tar emot mattefrågor och användarhistorik
- Genererar pedagogiska svar med GPT-3.5
- Anpassar svårighetsgrad och operationstyp
- Hanterar CORS och felhantering

Konfiguration:
------------
- Kräver OPENAI_API_KEY som miljövariabel
- Använder GPT-3.5-turbo modellen
- Max 300 tokens per svar
- Temperature: 0.7 för balanserad kreativitet

Användning:
---------
POST /lambda
{
    "prompt": "Vad är 7 + 5?",
    "operation": "addition",
    "difficulty": "easy",
    "history": [
        {"question": "Vad är 3 + 2?", "answer": "5"}
    ]
}

Svar:
----
{
    "status": "success",
    "message": "Ande-svar med förklaring..."
}

Författare: [Ditt namn]
Version: 1.0.0
"""

import json
import os
import openai
from prompt_template import MATTE_ANDE_PROMPT

def lambda_handler(event, context):
    """
    AWS Lambda handler för att framkalla matte-anden.
    
    Args:
        event (dict): AWS Lambda event med HTTP request data
            - httpMethod: HTTP-metod (POST/OPTIONS)
            - body: JSON-sträng med request data
                - prompt: Mattefrågan
                - operation: Typ av operation (addition/subtraction/multiplication/division)
                - difficulty: Svårighetsgrad (easy/medium/hard)
                - history: Lista med tidigare frågor och svar
        
        context (LambdaContext): AWS Lambda context objekt
    
    Returns:
        dict: API Gateway response med:
            - statusCode: HTTP status kod
            - headers: Response headers
            - body: JSON-sträng med response data
                - status: "success" eller "error"
                - message: Ande-svar eller felmeddelande
    
    Raises:
        Exception: Loggas och returneras som 500-fel
    """
    # Hantera CORS preflight (OPTIONS) först
    # Detta behövs för att webbläsaren ska kunna göra cross-origin requests
    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        # Säkerhetskontroll: Verifiera att OpenAI API-nyckel finns
        # API-nyckeln måste sättas som miljövariabel i Lambda-konfigurationen
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

        # Extrahera och validera input från request body
        # Alla fält är valfria utom prompt som måste finnas
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

        # Hämta valfria parametrar med standardvärden
        operation = body.get('operation', 'addition')  # Standard: addition
        difficulty = body.get('difficulty', 'easy')    # Standard: lätt
        history = body.get('history', [])              # Standard: tom historik

        # Formatera användarhistorik för att ge kontext till AI:n
        # Visar max 3 senaste frågorna för att hålla prompten kort
        history_text = ""
        if history and isinstance(history, list) and len(history) > 0:
            history_text = "\nTidigare frågor och svar:\n"
            for i, entry in enumerate(history[:3], 1):
                if isinstance(entry, dict):
                    q = str(entry.get("question", "")).strip()
                    a = str(entry.get("answer", "")).strip()
                    if q and a:
                        history_text += f"{i}. Fråga: {q}\n   Svar: {a}\n"

        # Definiera operation-specifika instruktioner
        # Varje operation har sin egen pedagogiska förklaring
        operation_prompts = {
            'addition': "Förklara hur man adderar talen och visar stegen tydligt.",
            'subtraction': "Förklara hur man subtraherar talen och visar stegen tydligt.",
            'multiplication': "Förklara hur man multiplicerar talen och visar stegen tydligt.",
            'division': "Förklara hur man dividerar talen och visar stegen tydligt."
        }

        # Definiera svårighetsgrad-specifika instruktioner
        # Varje nivå anpassar komplexiteten i förklaringen
        difficulty_context = {
            'easy': "Använd enkla tal och grundläggande koncept för en nybörjare-trollkarl.",
            'medium': "Använd lite svårare tal och koncept för en trollkarl under utbildning.",
            'hard': "Använd utmanande tal och koncept för en nästan fullärd trollkarl."
        }

        # Bygg den slutliga prompten genom att kombinera:
        # 1. Grundläggande ande-personlighet (från prompt_template.py)
        # 2. Användarhistorik
        # 3. Nuvarande fråga
        # 4. Operation-specifika instruktioner
        # 5. Svårighetsgrad-specifika instruktioner
        full_prompt = (
            f"{MATTE_ANDE_PROMPT}\n"
            f"{history_text}\n"
            f"Matteproblemet är: {user_prompt}\n\n"
            f"{operation_prompts.get(operation, '')}\n"
            f"{difficulty_context.get(difficulty, '')}"
        )

        # Anropa OpenAI API med GPT-3.5-turbo
        # Använder chat completion format med system och user messages
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,      # Begränsa svarslängden
            temperature=0.7      # Balansera mellan kreativitet och konsistens
        )
        
        # Extrahera ande-svaret från API-svaret
        ande_response = response["choices"][0]["message"]["content"]

        # Returnera framgångsrikt svar
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
        # Logga och hantera alla oväntade fel
        # Detta fångar både API-fel och andra runtime-fel
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