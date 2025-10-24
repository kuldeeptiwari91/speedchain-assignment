from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import conversation, appointments
import uvicorn

app = FastAPI(title="AI Receptionist - SmileCare Dental")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversation.router, prefix="/api/conversation", tags=["conversation"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["appointments"])

@app.get("/")
async def root():
    return {
        "message": "AI Receptionist API - SmileCare Dental",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)