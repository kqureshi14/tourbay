import os
import asyncio

import certifi
# from app.config.db import client
# from app.config.db import init_db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
# from app.config.db import lifespan
from app.routes import booking, tour
# from app.config.db import booking_collection,collection,client
# from .config.db import db_connection
# from app.config.db import get_database
import logging

# from app.config.db import DatabaseConnection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Environment configuration
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ALLOWED_ORIGINS = {
    'development': ["http://localhost:5173"],
    'production': ["https://bookingsys-new-front.vercel.app",
                   "https://new-backend-rm5ejzt7l-kqureshi14s-projects.vercel.app"]

}

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS.get(ENVIRONMENT.lower(), ["*"]),
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Loaded")

# Include routers
app.include_router(booking.booking)
app.include_router(tour.tourApi, tags=["tours"])
