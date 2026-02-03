from fastapi import FastAPI, Header, HTTPException, Request
import requests
import base64

app = FastAPI(
    title="Voice Detection API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

API_KEY = "testkey123"
SUPPORTED_LANGS = {"ta", "en", "hi", "ml", "te"}

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/api/v1/detect-voice")
async def detect_voice(
    request: Request,
    x_api_key: str = Header(None),
    authorization: str = Header(None)
):
    # ---- AUTH ----
    key = x_api_key
    if authorization and authorization.lower().startswith("bearer"):
        key = authorization.split(" ")[1]

    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ---- READ BODY SAFELY ----
    try:
        body = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    language = body.get("language")
    if language not in SUPPORTED_LANGS:
        raise HTTPException(status_code=400, detail="Invalid input")

    # ---- HANDLE AUDIO URL SAFELY ----
    if "audio_url" in body:
        try:
            r = requests.get(body["audio_url"], timeout=10)
            if r.status_code != 200 or len(r.content) == 0:
                raise Exception("Audio download failed")
        except:
            raise HTTPException(status_code=400, detail="Invalid audio_url")

    # ---- HANDLE BASE64 SAFELY ----
    elif "audio_base64" in body:
        try:
            base64.b64decode(body["audio_base64"])
        except:
            raise HTTPException(status_code=400, detail="Invalid audio_base64")

    else:
        raise HTTPException(status_code=400, detail="Invalid input")

    # ---- SAFE DUMMY RESPONSE ----
    return {
        "classification": "AI_GENERATED",
        "confidence": 0.75
    }