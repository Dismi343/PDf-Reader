# local_llma_openrouter.py
import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

#add your api key here
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "YOUR_OPENROUTER_API_KEY_HERE"

if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY_HERE":
    raise ValueError(
        "OPENROUTER_API_KEY is not set. "
        "Set it in environment or edit this file with your key (for local testing only)."
    )

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


MODEL_ID = "openai/gpt-4.1-mini"  # replace with your OpenRouter model

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

def build_context_prompt(contexts: List[Dict]) -> str:
    if not contexts:
        return "No context found."
    context_texts = []
    for c in contexts:
        meta = c.get("metadata", {})
        context_texts.append(
            f"[Source: {meta.get('source', 'unknown')} | Page: {meta.get('page_num', '?')}]\n{c['text']}"
        )
    return "\n\n---\n\n".join(context_texts)

def answer_query_with_openrouter(query: str, contexts: List[Dict]) -> str:
    context_block = build_context_prompt(contexts)

    system_prompt = (
        "You are a helpful assistant that answers questions strictly based on the "
        "provided PDF context. If the answer is not in the context, say you don't know."
    )

    user_prompt = (
        f"Context:\n{context_block}\n\n"
        f"User question:\n{query}\n\n"
        "Answer based only on the context above."
    )

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 512,
        "temperature": 0.2,
        "top_p": 0.9,
    }

    try:
        resp = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=60)
    except Exception as e:
        return f"Error calling OpenRouter: {e}"

    if not resp.ok:
        return f"OpenRouter API error {resp.status_code}: {resp.text}"

    data = resp.json()
    try:
        choices = data.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            content = msg.get("content", "")
            if content:
                return content.strip()
    except Exception:
        pass

    # fallback
    return str(data)
