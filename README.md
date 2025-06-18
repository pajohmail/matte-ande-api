# Matte-Ande API 🧮✨

En magisk API som hjälper barn att lära sig matematik genom en interaktiv matte-ande. Byggd med AWS Lambda och OpenAI's GPT-3.5.

## 🎯 Syfte

Matte-Ande API är designad för att göra matematiklärande roligt och engagerande för barn i åldrarna 7-10 år. Genom att kombinera pedagogik med en fantasifull matte-ande som heter Numerio, skapar vi en unik och underhållande lärupplevelse.

## ✨ Funktioner

- 🤖 Interaktiv matte-ande (Numerio) som förklarar matematik på ett roligt sätt
- 📚 Anpassad svårighetsgrad baserad på användarens förmåga
- 🔄 Stöd för alla grundläggande räknesätt (addition, subtraktion, multiplikation, division)
- 📊 Loggning av användarinteraktioner för att spåra framsteg
- 🎯 Personliga övningsproblem efter varje förklaring
- 🌐 RESTful API med CORS-stöd

## 🛠️ Teknisk Stack

- **Backend**: AWS Lambda
- **AI**: OpenAI GPT-3.5-turbo
- **Databas**: Supabase (för användarhistorik)
- **API**: RESTful med JSON

## 🚀 Installation

1. **Förutsättningar**
   ```bash
   - Python 3.8+
   - AWS CLI konfigurerad
   - OpenAI API-nyckel
   - Supabase konto och projekt
   ```

2. **Konfiguration**
   ```bash
   # Klona repositoryt
   git clone https://github.com/ditt-användarnamn/matte-ande-api.git
   cd matte-ande-api

   # Installera dependencies
   pip install -r requirements.txt
   ```

3. **Miljövariabler**
   Skapa en `.env` fil med följande:
   ```
   OPENAI_API_KEY=din_openai_api_nyckel
   SUPABASE_URL=din_supabase_url
   SUPABASE_KEY=din_supabase_nyckel
   ```

## 📝 Användning

### API Endpoints

#### POST /lambda
Genererar ett svar från matte-anden.

**Request Body:**
```json
{
    "prompt": "Vad är 7 + 5?",
    "operation": "addition",
    "difficulty": "easy",
    "history": [
        {"question": "Vad är 3 + 2?", "answer": "5"}
    ]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Hej unga trollkarl! Låt oss räkna ut 7 + 5 tillsammans..."
}
```

## 🔧 Utveckling

### Projektstruktur
```
matte-ande-api/
├── lambda_function.py    # Huvudfunktion för AWS Lambda
├── prompt_template.py    # Prompt-mall för matte-anden
├── requirements.txt      # Python dependencies
└── README.md            # Denna fil
```

### Lokal utveckling
```bash
# Testa lokalt med AWS SAM
sam local invoke MatteAndeFunction --event events/event.json
```

## 🤝 Bidra

1. Forka projektet
2. Skapa en feature branch (`git checkout -b feature/AmazingFeature`)
3. Committa dina ändringar (`git commit -m 'Add some AmazingFeature'`)
4. Pusha till branchen (`git push origin feature/AmazingFeature`)
5. Öppna en Pull Request

## 📄 Licens

Detta projekt är licensierat under MIT-licensen - se [LICENSE](LICENSE) filen för detaljer.

## 👥 Författare

- **Ditt Namn** - *Initialt arbete* - [DinGitHub](https://github.com/din-github)

## 🙏 Tack

- OpenAI för GPT-3.5
- AWS för Lambda
- Supabase för databashantering
- Alla som bidrar till projektet

## 📞 Kontakt


Projekt Link: [https://github.com/ditt-användarnamn/matte-ande-api](https://github.com/pajohmail
