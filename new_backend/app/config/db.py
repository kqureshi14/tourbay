from datetime import datetime, timedelta
from functools import lru_cache
import logging
import os
import certifi 
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import asyncio
from typing import Optional
from contextvars import ContextVar



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://kaleemq968:MBdlv0GEePlm1XIs@bookingsystem.tvphx.mongodb.net/tour_booking_system?retryWrites=true&w=majority")

# # Create a single client instance
# client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
# db = client['tour_booking_system']

# def get_db_client():
#     try:
#         # Ensure event loop exists
#         try:
#             loop = asyncio.get_event_loop()
#             if loop.is_closed():
#                 loop = asyncio.new_event_loop()
#                 asyncio.set_event_loop(loop)
#         except RuntimeError:
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
            
#         # Create client with the current event loop
#         client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where(), io_loop=loop)
#         return client
#     except Exception as e:
#         logger.error(f"Failed to create database client: {str(e)}")
#         raise

# client = get_db_client()
# db = client['tour_booking_system']

# # Add basic error handling
# async def get_collection(collection_name):
#     try:
#         return db[collection_name]
#     except Exception as e:
#         print(f"Database error: {str(e)}")
#         raise e




# Context variable to store client per request
client_context: ContextVar[Optional[AsyncIOMotorClient]] = ContextVar('client', default=None)

async def get_client():
    client = client_context.get()
    if client is None:
        client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
        client_context.set(client)
    return client

async def get_db():
    client = await get_client()
    return client['tour_booking_system']

async def get_collection(collection_name):
    try:
        db = await get_db()
        return db[collection_name]
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
