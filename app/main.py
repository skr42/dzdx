from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="Profanity and Abuse Filtering API",
    description="API for detecting toxic content",
    version="1.0.0",
    docs_url="/docs",

)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Profanity and Abuse Filtering API", "status": "active"}


