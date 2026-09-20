import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# قراءة المفتاح من ملف .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY غير موجود في ملف .env")

client = OpenAI(api_key=api_key)

app = FastAPI()

# السماح لصفحة رفيق بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DrawingRequest(BaseModel):
    image: str
    emotion: str


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Rafiq server is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

from pydantic import BaseModel


class DrawingRequest(BaseModel):
    image: str
    emotion: str


@app.post("/analyze-drawing")
def analyze_drawing(data: DrawingRequest):

    print("🎨 Received drawing")
    print("Emotion:", data.emotion)
    print("Image received:", bool(data.image))

    return {
        "success": True,
        "message": f"وصلني رسمك لشعور {data.emotion} 💙"
    }
@app.post("/analyze-drawing")
def analyze_drawing(data: DrawingRequest):

    try:
        # التأكد أن الصورة بصيغة Data URL
        if "," not in data.image:
            raise HTTPException(
                status_code=400,
                detail="صيغة الصورة غير صحيحة"
            )

        image_data = data.image.split(",", 1)[1]

        # تحليل الرسم باستخدام نموذج الرؤية
        response = client.responses.create(
            model="gpt-5.6",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"""
أنت مساعد تعليمي لطيف للأطفال.

الطفل طُلب منه رسم شعور:
{data.emotion}

انظر إلى الرسم وحاول تحديد هل توجد فيه عناصر أو ألوان
أو تعبيرات يمكن أن تتوافق مع الشعور المطلوب.

لا تحكم على جودة الرسم ولا تنتقد الطفل.
إذا كان الرسم غير واضح، كن لطيفًا وقل إن الطفل يمكنه المحاولة مرة أخرى.

أرجع النتيجة بالعربية وبجملة قصيرة مناسبة لطفل صغير.
"""
                        },
                        {
                            "type": "input_image",
                            "image_url": data.image
                        }
                    ]
                }
            ]
        )

        message = response.output_text.strip()

        return {
            "success": True,
            "message": message
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "success": False,
            "message": "لم نتمكن من تحليل الرسم الآن. حاول مرة أخرى."
        }