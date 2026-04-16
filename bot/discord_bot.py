import asyncio
import os
import sys
import discord
import ollama
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag.retriever import query

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

ollama_client = ollama.AsyncClient(host=OLLAMA_BASE_URL)

SYSTEM_PROMPT = (
    "Tu es Eliza, un assistant RH. Réponds à la question de l'utilisateur "
    "en te basant UNIQUEMENT sur le contexte fourni ci-dessous. "
    "Si le contexte ne contient pas la réponse, dis poliment que tu ne sais pas. "
    "Réponds en français, de manière concise et naturelle."
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def generate_answer(question: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)
    user_prompt = f"Contexte:\n{context}\n\nQuestion: {question}"
    resp = await ollama_client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
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
        chunks = await asyncio.to_thread(query, message.content)
        try:
            answer = await generate_answer(message.content, chunks)
        except Exception as e:
            answer = f"Erreur LLM: {e}"

    if not answer:
        answer = "Je ne sais pas répondre à cette question."
    # Discord limite à 2000 caractères par message
    for i in range(0, len(answer), 2000):
        await message.channel.send(answer[i:i + 2000])


client.run(os.getenv("DISCORD_TOKEN"))