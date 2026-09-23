import os
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY غير موجود في متغيرات البيئة."
    )


client = OpenAI(
    api_key=api_key
)


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="Rafiq AI Server",
    version="3.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class DrawingRequest(BaseModel):

    image: str

    emotion: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "Rafiq AI server is running"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(value):

    return (
        str(value or "")
        .strip()
        .lower()
    )


# =========================================================
# PARSE AI RESULT
# =========================================================

def parse_ai_result(ai_text):

    text = str(
        ai_text or ""
    ).strip()


    # -----------------------------------------------------
    # DEFAULT VALUES
    # -----------------------------------------------------

    matches_target = False

    confidence = 0

    mouth = "غير واضح"

    emotion = "غير واضح"

    feedback = ""


    # =====================================================
    # MATCHES TARGET
    # =====================================================

    match = re.search(
        r"matches_target\s*[:=]\s*(true|false)",
        text,
        re.IGNORECASE
    )

    if match:

        matches_target = (
            match.group(1).lower()
            == "true"
        )


    # =====================================================
    # CONFIDENCE
    # =====================================================

    confidence_match = re.search(
        r"confidence\s*[:=]\s*(\d+(?:\.\d+)?)",
        text,
        re.IGNORECASE
    )

    if confidence_match:

        try:

            confidence = int(
                float(
                    confidence_match.group(1)
                )
            )

        except Exception:

            confidence = 0


    confidence = max(
        0,
        min(
            confidence,
            100
        )
    )


    # =====================================================
    # MOUTH
    # =====================================================

    mouth_match = re.search(
        r"mouth\s*[:=]\s*([^\n\r]+)",
        text,
        re.IGNORECASE
    )

    if mouth_match:

        mouth_value = (
            mouth_match.group(1)
            .strip()
        )


        if "غير مبتسم" in mouth_value:

            mouth = "غير مبتسم"


        elif "غير موجود" in mouth_value:

            mouth = "غير موجود"


        elif "غير واضح" in mouth_value:

            mouth = "غير واضح"


        elif (
            "مبتسم" in mouth_value
            or
            "مبتسمة" in mouth_value
        ):

            mouth = "مبتسم"


    # =====================================================
    # EMOTION
    # =====================================================

    emotion_match = re.search(
        r"emotion\s*[:=]\s*([^\n\r]+)",
        text,
        re.IGNORECASE
    )

    if emotion_match:

        emotion_value = (
            emotion_match.group(1)
            .strip()
        )


        normalized_emotion = normalize_text(
            emotion_value
        )


        if (
            "حزين" in normalized_emotion
            or
            "حزينة" in normalized_emotion
            or
            "حزن" in normalized_emotion
            or
            "sad" in normalized_emotion
        ):

            emotion = "حزين"


        elif (
            "غاضب" in normalized_emotion
            or
            "غاضبة" in normalized_emotion
            or
            "غضب" in normalized_emotion
            or
            "angry" in normalized_emotion
        ):

            emotion = "غاضب"


        elif (
            "محايد" in normalized_emotion
            or
            "محايدة" in normalized_emotion
            or
            "neutral" in normalized_emotion
        ):

            emotion = "محايد"


        elif (
            "سعيد" in normalized_emotion
            or
            "سعيدة" in normalized_emotion
            or
            "سعادة" in normalized_emotion
            or
            "happy" in normalized_emotion
        ):

            emotion = "سعيد"


    # =====================================================
    # FEEDBACK
    # =====================================================

    feedback_match = re.search(
        r"feedback\s*[:=]\s*([^\n\r]+)",
        text,
        re.IGNORECASE
    )

    if feedback_match:

        feedback = (
            feedback_match.group(1)
            .strip()
        )


    # =====================================================
    # IMPORTANT:
    # DETERMINE TARGET FROM MOUTH + CONFIDENCE
    # =====================================================

    if mouth == "مبتسم":

        if confidence >= 70:

            matches_target = True

        else:

            matches_target = False


    else:

        matches_target = False


    # =====================================================
    # IF EMOTION IS CLEARLY NOT HAPPY
    # =====================================================

    if emotion in [
        "حزين",
        "غاضب",
        "محايد"
    ]:

        matches_target = False


    # =====================================================
    # IF AI DID NOT RETURN EMOTION
    # TRY TO INFER IT FROM MOUTH
    # =====================================================

    if emotion == "غير واضح":

        if mouth == "مبتسم":

            if confidence >= 70:

                emotion = "سعيد"

        elif mouth == "غير مبتسم":

            emotion = "محايد"


    # =====================================================
    # RETURN STRUCTURED RESULT
    # =====================================================

    return {

        "matches_target":
            matches_target,

        "confidence":
            confidence,

        "mouth":
            mouth,

        "emotion":
            emotion,

        "feedback":
            feedback

    }


# =========================================================
# ANALYZE DRAWING
# =========================================================

@app.post("/analyze-drawing")
def analyze_drawing(
    data: DrawingRequest
):

    try:

        print("🎨 Received drawing")

        print(
            "Emotion:",
            data.emotion
        )

        print(
            "Image received:",
            bool(data.image)
        )


        # =================================================
        # CHECK IMAGE
        # =================================================

        if not data.image:

            raise HTTPException(
                status_code=400,
                detail="لم يتم إرسال الرسم."
            )


        if "," not in data.image:

            raise HTTPException(
                status_code=400,
                detail="صيغة الصورة غير صحيحة."
            )


        # =================================================
        # EMOTION REQUEST
        # =================================================

        requested_emotion = (
            data.emotion.strip()
        )


        # =================================================
        # AI PROMPT
        # =================================================

        prompt = f"""
أنت "رفيق"، مساعد تعليمي لطيف للأطفال.

الطفل طُلب منه رسم وجه يعبر عن:

{requested_emotion}

مهمتك تحليل الرسم بصريًا من الصورة المرفقة.

لا تقيم جودة الرسم الفنية.
لا تنتقد الطفل.
لا تقل إن الرسم سيئ.
لا تقارن الرسم برسومات أخرى.
لا تحاول معرفة هوية الطفل.
لا تستنتج أي معلومات شخصية.

==================================================
المطلوب
==================================================

حدد أولًا التعبير الظاهر على الوجه المرسوم.

اختر emotion واحدًا فقط من:

سعيد
حزين
غاضب
محايد
غير واضح

ثم افحص الفم بعناية.

==================================================
حالة الفم
==================================================

اختر mouth واحدًا فقط:

مبتسم
غير مبتسم
غير واضح
غير موجود

مهم جدًا:

"مبتسم":
يجب أن يكون هناك دليل بصري واضح على ابتسامة،
مثل قوس أو منحنى واضح يتجه إلى الأعلى.

"غير مبتسم":
يوجد فم واضح لكنه مستقيم أو متجه للأسفل،
ولا يعطي تعبير السعادة.

"غير واضح":
يوجد شيء يشبه الفم ولكن لا يمكن تحديد التعبير.

"غير موجود":
لا يوجد فم واضح.

==================================================
تمييز المشاعر
==================================================

إذا كان الفم منحنيًا بوضوح إلى الأعلى
وكان الوجه يعطي تعبير السعادة:

emotion: سعيد

إذا كان الفم أو تعبير الوجه يدل بوضوح على الحزن:

emotion: حزين

إذا كان التعبير يدل بوضوح على الغضب:

emotion: غاضب

إذا كان الوجه يحتوي على فم واضح ولكنه مستقيم
ولا توجد ابتسامة واضحة:

emotion: محايد

إذا لم تستطع تحديد التعبير:

emotion: غير واضح

==================================================
مهم جدًا بشأن الحزن
==================================================

إذا كان الوجه يبدو حزينًا،
لا تعتبره سعيدًا حتى لو كانت هناك ألوان جميلة
أو عيون أو دائرة للوجه.

إذا كان الفم متجهًا للأسفل أو يعطي تعبيرًا حزينًا:

emotion: حزين

mouth: غير مبتسم

matches_target: false

==================================================
مهم جدًا بشأن الابتسامة
==================================================

لا تعتبر الوجه سعيدًا فقط بسبب وجود:

دائرة للوجه
عينين
ألوان
أنف
زخارف
نجوم
قلوب
شعر

يجب أن تكون هناك ابتسامة واضحة.

==================================================
MATCHES_TARGET
==================================================

الهدف هو رسم وجه سعيد.

ضع:

matches_target: true

فقط إذا:

1. emotion = سعيد
2. mouth = مبتسم
3. الابتسامة واضحة بصريًا
4. confidence >= 70

في جميع الحالات الأخرى:

matches_target: false

لا تجامل الطفل.

==================================================
CONFIDENCE
==================================================

أعطِ رقمًا من 0 إلى 100.

إذا كانت الابتسامة واضحة جدًا:

85 إلى 100

إذا كانت موجودة ولكن الرسم غير واضح تمامًا:

50 إلى 84

إذا كان من الصعب تحديد التعبير:

0 إلى 49

==================================================
FEEDBACK
==================================================

اكتب جملة عربية قصيرة جدًا ومناسبة لطفل صغير.

إذا كان الوجه سعيدًا:

أحسنت! أرى ابتسامة جميلة في وجهك. 😊

إذا كان الوجه حزينًا:

هذا وجه حزين 😢 حاول أن تجعل الفم يبتسم إلى الأعلى ليصبح الوجه سعيدًا. 😊

إذا كان الوجه غاضبًا:

هذا وجه غاضب 😠 حاول أن ترسم فمًا مبتسمًا ليصبح الوجه سعيدًا. 😊

إذا كان الوجه محايدًا:

هذا الوجه ليس سعيدًا بعد 😐 حاول أن تجعل الفم منحنيًا إلى الأعلى. 😊

إذا كان الفم غير موجود:

رائع! حاول إضافة فم مبتسم إلى الوجه. 😊

إذا كان التعبير غير واضح:

محاولة جميلة! حاول رسم ابتسامة أوضح. 😊

لا تستخدم كلمات قاسية مثل:

خطأ
سيئ
فاشل
رسم غير جيد

==================================================
إخراج النتيجة
==================================================

يجب أن يكون الإخراج بهذا الشكل بالضبط:

matches_target: true أو false
confidence: رقم من 0 إلى 100
emotion: سعيد أو حزين أو غاضب أو محايد أو غير واضح
mouth: مبتسم أو غير مبتسم أو غير واضح أو غير موجود
feedback: جملة عربية قصيرة

لا تكتب أي شرح قبل هذه الأسطر.

لا تستخدم Markdown.

لا تستخدم JSON.

لا تضف أسطرًا أخرى.

لا تغير أسماء الحقول.

==================================================
الهدف
==================================================

الهدف تعليم الطفل تدريجيًا كيف يستخدم شكل الفم
للتعبير عن السعادة بطريقة لطيفة ومشجعة.
"""


        # =================================================
        # SEND TO OPENAI
        # =================================================

        response = client.responses.create(

            model="gpt-5.6",

            input=[

                {
                    "role": "user",

                    "content": [

                        {
                            "type": "input_text",

                            "text": prompt
                        },

                        {
                            "type": "input_image",

                            "image_url": data.image
                        }

                    ]

                }

            ]

        )


        # =================================================
        # GET AI TEXT
        # =================================================

        ai_result = (
            response.output_text or ""
        ).strip()


        print(
            "🤖 RAW AI RESULT:"
        )

        print(
            ai_result
        )


        # =================================================
        # PARSE RESULT
        # =================================================

        parsed = parse_ai_result(
            ai_result
        )


        # =================================================
        # FALLBACK
        # =================================================

        if not ai_result:

            parsed = {

                "matches_target":
                    False,

                "confidence":
                    0,

                "mouth":
                    "غير واضح",

                "emotion":
                    "غير واضح",

                "feedback":
                    "محاولة جميلة! حاول رسم ابتسامة أوضح."

            }


            ai_result = (
                "matches_target: false\n"
                "confidence: 0\n"
                "emotion: غير واضح\n"
                "mouth: غير واضح\n"
                "feedback: محاولة جميلة! حاول رسم ابتسامة أوضح."
            )


        # =================================================
        # NORMALIZED AI RESULT
        # =================================================

        normalized_ai_result = (
            "matches_target: "
            + str(
                parsed["matches_target"]
            ).lower()
            + "\n"
            + "confidence: "
            + str(
                parsed["confidence"]
            )
            + "\n"
            + "emotion: "
            + parsed["emotion"]
            + "\n"
            + "mouth: "
            + parsed["mouth"]
            + "\n"
            + "feedback: "
            + (
                parsed["feedback"]
                or
                "محاولة جميلة! حاول رسم ابتسامة أوضح."
            )
        )


        # =================================================
        # LOG
        # =================================================

        print(
            "🤖 NORMALIZED RESULT:"
        )

        print(
            normalized_ai_result
        )


        # =================================================
        # RETURN RESULT
        # =================================================

        return {

            "success":
                True,

            "ai_result":
                normalized_ai_result,

            "message":
                normalized_ai_result,

            "matches_target":
                parsed["matches_target"],

            "confidence":
                parsed["confidence"],

            "emotion":
                parsed["emotion"],

            "mouth":
                parsed["mouth"],

            "feedback":
                parsed["feedback"]

        }


    # =====================================================
    # HTTP ERROR
    # =====================================================

    except HTTPException:

        raise


    # =====================================================
    # OPENAI / SERVER ERROR
    # =====================================================

    except Exception as e:

        print(
            "❌ AI ERROR:",
            str(e)
        )

        return {

            "success":
                False,

            "ai_result":
                "",

            "message":
                "لم نتمكن من تحليل الرسم الآن. "
                "حاولي مرة أخرى."

        }