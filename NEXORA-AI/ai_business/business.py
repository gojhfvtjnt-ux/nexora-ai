
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

router = APIRouter(
    prefix="/api/business",
    tags=["AI Business"]
)


class BusinessRequest(BaseModel):
    text: str
    task: str


@router.post("/process")
def process_business(request: BusinessRequest):
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
                        "Ты профессиональный бизнес-консультант "
                        "платформы NEXORA AI. "
                        "Отвечай на русском языке. "
                        "Создавай подробные, понятные и практичные "
                        "бизнес-планы и стратегии. "
                        "Финансовые расчёты обозначай как примерные "
                        "оценки, а не гарантии. "
                        "Не выдумывай реальные данные о конкурентах, "
                        "ценах и рынках. Если данных недостаточно, "
                        "честно указывай на это."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Задача: {request.task}\n"
                        f"Информация о бизнесе: {request.text}"
                    )
                }
            ],
            temperature=0.5,
            max_completion_tokens=2500
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
