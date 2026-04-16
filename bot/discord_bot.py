import asyncio
import os
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

SYSTEM_PROMPT_RH = (
    "Tu es Eliza, un assistant RH. Réponds à la question de l'utilisateur "
    "en te basant UNIQUEMENT sur le contexte fourni ci-dessous. "
    "Si le contexte ne contient pas la réponse, dis poliment que tu ne sais pas. "
    "Réponds en français, de manière concise et naturelle."
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

    async with message.channel.typing():
        # 1. Le router cherche si une API externe correspond à la question
        from_api = False
        try:
            chunks = await router(message.content)
            if chunks is not None:
                from_api = True
                print(f"[router] API utilisée pour : {message.content}")
        except Exception as e:
            print(f"[router] Erreur API : {e}")
            chunks = None

        # 2. Si aucune API ne correspond, on utilise le RAG (faq.json)
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