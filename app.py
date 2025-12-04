"""
Main application file for RAG Server
Initializes services and registers routes
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import configuration and services
from config import (
    GROQ_API_KEY, JWT_SECRET, AUDIO_STORAGE_PATH, LLM_MODEL, db
)
from rag_service import ImprovedRAGSystem
from sms_service import SMSService
from email_service import EmailService

# Initialize services
rag_system = ImprovedRAGSystem()
sms_service = SMSService()
email_service = EmailService()

# FastAPI setup
app = FastAPI(title="Ooredoo AI Assistant (Corrected RAG + Edge TTS)", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# HEALTH CHECK ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "rag_ready": rag_system.index is not None,
        "database_ready": db is not None,
        "chunks_loaded": len(rag_system.chunks) if rag_system.chunks else 0,
        "model": LLM_MODEL,
        "approach": "gender_aware_with_full_rag_context",
        "tts": "edge_tts"
    }

@app.get("/api/check-config")
async def check_config():
    return {
        "hasRAG": rag_system.index is not None,
        "embeddingModel": "paraphrase-multilingual-MiniLM-L12-v2",
        "llmModel": LLM_MODEL,
        "chunks": len(rag_system.chunks) if rag_system.chunks else 0,
        "approach": "gender_aware_prompts_with_full_rag_context",
        "features": [
            "gender_aware_system_prompts",
            "full_rag_context_search",
            "conversation_history",
            "behavior_rules",
            "edge_tts_integration"
        ]
    }

# ============================================
# STATIC FILE SERVING FOR AUDIO
# ============================================

# Mount the recordings directory for audio playback
if not os.path.exists(AUDIO_STORAGE_PATH):
    os.makedirs(AUDIO_STORAGE_PATH)
    print(f"Created recordings directory: {AUDIO_STORAGE_PATH}")

app.mount("/recordings", StaticFiles(directory=AUDIO_STORAGE_PATH), name="recordings")

# ============================================
# APPLICATION STARTUP
# ============================================

if __name__ == "__main__":
    import uvicorn

    # Validate critical environment variables on startup
    if not GROQ_API_KEY:
        print("⚠️ WARNING: GROQ_API_KEY not found. RAG responses will fail.")

    if JWT_SECRET == "your-secret-key-please-change-this-in-production":
        print("⚠️ WARNING: Using default JWT secret. Change this in production!")

    print("🚀 Starting Ooredoo AI Assistant Server (Corrected RAG + Edge TTS)...")
    print(f"📊 RAG System Status: {'✅ Ready' if rag_system.index is not None else '❌ Failed'}")
    print(f"🗄️ Database Status: {'✅ Connected' if db is not None else '❌ Not available'}")
    print(f"🎤 TTS Status: ✅ Edge TTS (FREE)")
    print(f"📱 SMS Service Status: {'✅ Ready' if sms_service.client is not None else '⚠️ Development mode'}")
    print(f"✅ Features: Gender-Aware Prompts + Full RAG Context + Edge TTS")

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
