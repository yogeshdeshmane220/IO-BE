from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.products import router as products_router
from app.api.upload import router as upload_router
from app.api.webhooks import router as webhooks_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers ONLY after CORS
app.include_router(upload_router)
app.include_router(products_router)
app.include_router(webhooks_router)
