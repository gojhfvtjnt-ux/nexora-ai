
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

router = APIRouter(
    prefix="/api/writer",
    tags=["AI Writer"]
)


class WriterRequest(BaseModel):
    text: str
    task: str


@router.post("/process")
def process_text(request: WriterRequest):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Не найден API-ключ Groq"
        )

    try:
        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты профессиональный AI Writer платформы "
                        "NEXORA AI. Отвечай на русском языке. "
                        "Создавай качественные, грамотные "
                        "и полезные тексты."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Задача: {request.task}\n"
                        f"Исходный текст: {request.text}"
                    )
                }
            ],
            temperature=0.7,
            max_completion_tokens=1200
        )

        result = completion.choices[0].message.content

        return {
            "success": True,
            "task": request.task,
            "result": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Ошибка AI-сервиса: {str(error)}"
        )
