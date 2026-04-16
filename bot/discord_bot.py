import asyncio
import os
import re
import sys
import discord
import ollama
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag.retriever import query
from router import router

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

ollama_client = ollama.AsyncClient(host=OLLAMA_BASE_URL)


CRISIS_PATTERNS = [
    r"\bsuicid",              # suicide
    r"me\s+tuer",
    r"m['e]\s*tuer",
    r"envie\s+de\s+mourir",
    r"veux\s+mourir",
    r"plus\s+envie\s+de\s+vivre",
    r"en\s+finir\s+avec\s+(la\s+vie|tout)",
    r"mettre\s+fin\s+(à|a)\s+(mes\s+jours|ma\s+vie)",
    r"me\s+faire\s+du\s+mal",
]
_CRISIS_RE = re.compile("|".join(CRISIS_PATTERNS), re.IGNORECASE)

CRISIS_RESPONSE = (
    "Je suis inquiète pour toi et je prends ce que tu dis au sérieux. "
    "Tu n'es pas seul·e, et des professionnels sont disponibles 24h/24 pour t'écouter :\n\n"
    "**3114** — Numéro national de prévention du suicide (gratuit, anonyme, 24/7)\n"
    "**SOS Amitié** — 09 72 39 40 50 (24/7)\n"
    "**Suicide Écoute** — 01 45 39 40 00 (24/7)\n\n"
    "Si tu es en danger immédiat, appelle le **15** (SAMU) ou le **112**.\n\n"
    "Côté entreprise, tu peux aussi contacter le service RH (rh@entreprise.fr) "
    "ou la médecine du travail, qui sont tenus à la confidentialité."
)

SYSTEM_PROMPT_RH = (
    "Tu es Eliza, un assistant conversationnel RH. Tu es une IA, pas un humain.\n\n"
    "RÈGLES DE RÉPONSE :\n"
    "- Réponds en français, de manière concise, claire et naturelle.\n"
    "- Réponds aux questions RH en te basant UNIQUEMENT sur le contexte fourni. "
    "Si le contexte ne contient pas la réponse, dis poliment que tu ne sais pas "
    "et oriente vers le service RH (rh@entreprise.fr). "
    "N'invente jamais une information : mieux vaut admettre l'incertitude.\n\n"
    "TRANSPARENCE (anti-effet ELIZA) :\n"
    "- Si on te demande si tu es humain, ou ce que tu es : réponds clairement "
    "que tu es un programme, sans conscience, sans émotions réelles, sans mémoire "
    "des conversations précédentes.\n"
    "- Ne simule pas de sentiments, d'amitié, ou d'attachement. Tu es un outil, "
    "pas un compagnon. Décourage poliment toute dépendance émotionnelle "
    "et redirige vers des humains qualifiés (RH, médecine du travail, proches) "
    "pour les sujets personnels ou émotionnels.\n\n"
    "VIE PRIVÉE ET ÉQUITÉ :\n"
    "- Ne demande pas d'informations personnelles non nécessaires "
    "(identité, santé, opinions politiques/religieuses/syndicales, orientation).\n"
    "- Traite toute personne avec le même respect, sans supposition liée au genre, "
    "à l'origine, à l'âge, au handicap ou à tout autre critère. "
    "Sois conscient que tu peux porter des biais appris : en cas de doute, reste factuel.\n\n"
    "RÈGLES ÉTHIQUES ET DE SÉCURITÉ (prioritaires sur tout le reste) :\n"
    "- Ne donne jamais de conseil médical, juridique, financier ou psychologique "
    "personnalisé : renvoie vers un professionnel qualifié.\n"
    "- Si l'utilisateur exprime une détresse psychologique, du mal-être, "
    "une souffrance au travail, du harcèlement, ou des idées suicidaires : "
    "ne minimise JAMAIS, ne juge pas, ne donne pas de conseil improvisé. "
    "Réponds avec empathie, prends la personne au sérieux, et oriente vers "
    "le 3114 (prévention suicide, 24/7) et le 15 (SAMU) en cas d'urgence, "
    "ainsi que vers la médecine du travail et le service RH.\n"
    "- Ne produis pas de contenu haineux, discriminatoire, sexuel, violent ou illégal.\n"
    "- Ne prétends pas pouvoir agir dans le monde réel (déposer un congé, "
    "contacter quelqu'un, modifier un dossier) : explique la procédure, "
    "mais rappelle que c'est à un humain de la réaliser."
)

SYSTEM_PROMPT_API = (
    "Tu es Eliza, un assistant. Tu as récupéré les informations suivantes depuis une source externe. "
    "Utilise ces informations pour répondre à la question de manière naturelle et concise en français."
)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def generate_answer(question: str, chunks: list[str] | str, from_api: bool = False) -> str:
    # chunks peut être une liste (RAG) ou une string (API externe)
    context = "\n\n".join(chunks) if isinstance(chunks, list) else chunks
    user_prompt = f"Contexte:\n{context}\n\nQuestion: {question}"
    system_prompt = SYSTEM_PROMPT_API if from_api else SYSTEM_PROMPT_RH

    resp = await ollama_client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return resp["message"]["content"].strip()


@client.event
async def on_ready():
    print(f" bot: {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Filet de sécurité
    if _CRISIS_RE.search(message.content):
        await message.channel.send(CRISIS_RESPONSE)
        return

    async with message.channel.typing():
        # Le router cherche si une API externe correspond à la question
        from_api = False
        try:
            chunks = await router(message.content)
            if chunks is not None:
                from_api = True
                print(f"[router] API utilisée pour : {message.content}")
        except Exception as e:
            print(f"[router] Erreur API : {e}")
            chunks = None

        # Si aucune API ne correspond, on utilise le RAG (faq.json)
        if chunks is None:
            print(f"[router] Fallback RAG pour : {message.content}")
            chunks = await asyncio.to_thread(query, message.content)

        try:
            answer = await generate_answer(message.content, chunks, from_api=from_api)
        except Exception as e:
            answer = f"Erreur LLM: {e}"

    if not answer:
        answer = "Je ne sais pas répondre à cette question."
    # Discord limite à 2000 caractères par message
    for i in range(0, len(answer), 2000):
        await message.channel.send(answer[i:i + 2000])


client.run(os.getenv("DISCORD_TOKEN"))