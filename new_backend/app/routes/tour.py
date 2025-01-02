import logging
from fastapi import APIRouter, HTTPException,Query
from typing import List
from app.models.tour import Tour
# from app.config.db import booking_collection,collection
# from app.config.db import DatabaseManager, conn,db  # MongoDB connection
from bson import ObjectId
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# from ..config.db import get_database

import certifi
from ..config.db import get_collection
# booking = APIRouter()

# @booking.post("/bookings", response_model=Booking)
# async def create_booking(booking: Booking):
#     # Your logic to create a booking
#     pass






tourApi = APIRouter()
tour_collection_name = 'tours'

# client = AsyncIOMotorClient("mongodb+srv://kaleemq968:MBdlv0GEePlm1XIs@bookingsystem.tvphx.mongodb.net/tour_booking_system?retryWrites=true&w=majority",tlsCAFile=certifi.where())

# db = client['tour_booking_system']
# booking_collection = db['bookings']
# tour_collection = db['tours']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# booking_collection = db["bookings"]
# collection = db["tours"]



@tourApi.get("/tours", response_model=List[Tour])
async def get_all_tours(
    city: str = Query(None, description="City to filter tours by"),
    price: str = Query(None, description="Price to filter tours by"),
    start_date: str = Query(None, description="Start Date to filter tours by (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End Date to filter tours by (YYYY-MM-DD)")
):
    query = {}
    # async with get_collection("tours") as tour_collection:
    # async with get_collection("tours") as collection:
    tour_collection  = await get_collection(tour_collection_name)
    logger.info(f"Query parameters: city={city}, price={price}, start_date={start_date}, end_date={end_date}")

    # Add filters to query
    if city:
        query["city"] = city

    if price:
        query["price"] = price  

    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            query["start_date"] = {"$gte": start_date_obj}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            query["end_date"] = {"$lte": end_date_obj}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

    logger.info(f"Constructed query: {query}")

    # Query the database
    try:
        tours_cursor = await tour_collection.find(query).to_list(100)
        
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tours.")

    if not tours_cursor:
        raise HTTPException(status_code=404, detail="No tours found for the specified filters.")

    # Convert the ObjectId to string before creating the Tour model
    return [Tour(id=str(tour["_id"]), **tour) for tour in tours_cursor]


@tourApi.put("/tours/{tour_id}", response_model=Tour)
async def update_tour(tour_id: str, updated_tour: Tour):

        # Find the tour by ID
    tour_collection  = await get_collection(tour_collection_name)
    tour = await tour_collection.find_one({"_id": ObjectId(tour_id)})
    
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    
    # Prepare the data to be updated, excluding None values
    updated_data = {key: value for key, value in updated_tour.dict().items() if value is not None}
    
    # Perform the update operation
    await tour_collection.update_one({"_id": ObjectId(tour_id)}, {"$set": updated_data})

    # Fetch the updated tour from the database
    updated_tour_data = await tour_collection.find_one({"_id": ObjectId(tour_id)})
    
    # Return the updated tour directly as a Pydantic model (FastAPI will handle serialization)
    return Tour(**updated_tour_data)


# Delete tour API
@tourApi.delete("/tours/{tour_id}", response_model=dict)
async def delete_tour(tour_id: str):
    

        # database = DatabaseManager.get_db()
        # async with DatabaseManager.get_db_context() as database:
        #     collection = database.tours  # Use 
    tour_collection  = await get_collection(tour_collection_name)
    # Find the tour by ID
    tour = await tour_collection.find_one({"_id": ObjectId(tour_id)})
    
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    
    # Delete the tour from the collection
    await tour_collection.delete_one({"_id": ObjectId(tour_id)})

    # Return a success message
    return {"message": f"Tour with id {tour_id} has been deleted successfully"}


@tourApi.get("/tours/{tour_id}", response_model=Tour)
async def get_tour(tour_id: str):
    # async with get_database() as db:
            # database = DatabaseManager.get_db()
            # async with DatabaseManager.get_db_context() as database:
            #     collection = database.tours 
    # async with get_collection("tours") as tour_collection:
    tour_collection  = await get_collection(tour_collection_name)
    # Fetch the tour from the MongoDB collection
    tour = await tour_collection.find_one({"_id": ObjectId(tour_id)})
    
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")

    # Return the tour directly as a Pydantic model (FastAPI will handle serialization)
    # Convert ObjectId to string if needed (FastAPI will handle the serialization of ObjectId automatically if orm_mode=True is set)
    tour["_id"] = str(tour["_id"])  # Ensure ObjectId is converted to string for JSON compatibility
    
    return Tour(**tour)
        # return JSONResponse(content=tour, headers={"Access-Control-Allow-Origin": "*"})


# @tourApi.post("/tours/", response_model=Tour)
# async def create_tour(tour: Tour):
#     # Convert the Pydantic model to a dictionary
#     tour_dict = tour.dict()

#     # Insert the new tour into the MongoDB collection
#     result = await collection.insert_one(tour_dict)

#     # Fetch the newly inserted tour from the database
#     new_tour = await collection.find_one({"_id": result.inserted_id})
    
#     if not new_tour:
#         raise HTTPException(status_code=500, detail="Failed to create tour")

#     # Convert ObjectId to string if necessary
#     new_tour["_id"] = str(new_tour["_id"])

#     # Return the new tour directly as a Pydantic model
#     return Tour(**new_tour)