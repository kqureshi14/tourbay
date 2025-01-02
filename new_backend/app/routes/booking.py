from fastapi import APIRouter, HTTPException,Query
from typing import List
from app.models.booking import Booking
# from app.config.db import conn,db  

# from app.config.db import DatabaseManager, conn,db,booking_collection,collection  # MongoDB connection

# from app.config import booking_collection,collection
from bson import ObjectId
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

# from ..config.db import get_database
from ..config.db import get_collection
# booking = APIRouter()

# @booking.post("/bookings", response_model=Booking)
# async def create_booking(booking: Booking):
#     # Your logic to create a booking
#     pass






booking = APIRouter()
booking_collection_name = 'bookings'
tour_collection_name = 'tours'



# Global variable to store the database client (MongoDB connection)
# client = None




# booking_collection = db["bookings"]
# collection = db["tours"]


@booking.post("/bookings", response_model=Booking)
async def create_booking(booking: Booking):
    print("Here", booking)
    # async with get_database() as db:  
    
        # database = DatabaseManager.get_db()
        # async with DatabaseManager.get_db_context() as database:
        #     booking_collection = database.bookings 
        #     collection = database.tours # Debugging: Print received payload
        
        # Verify if `tour_id` is a valid ObjectId
    try:
        tour_id = ObjectId(booking.tour_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid tour_id")
    
    booking_collection  = await get_collection(booking_collection_name)
    tours_collection = await get_collection(tour_collection_name)
    # Check if the referenced tour exists
    tour = await tours_collection.find_one({"_id": tour_id})
    
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    

    # Calculate total price based on the number of adults and children
    total_price = (tour["charge_price"] * booking.adults) + (tour["charge_price"] * 0.5 * booking.children)
    
    # Prepare the booking document
    booking_dict = booking.dict()
    booking_dict["total_price"] = total_price
    booking_dict["tour_details"] = tour
    
    # Convert tour_id to string to make it JSON serializable
    booking_dict["tour_id"] = str(booking_dict["tour_id"])
    
    # Insert the booking into the bookings collection
    result = await booking_collection.insert_one(booking_dict)
    
    # Fetch the new booking and prepare for response
    new_booking = await booking_collection.find_one({"_id": result.inserted_id})
    

    # Convert ObjectId to string for JSON serialization
    if new_booking:
        new_booking["_id"] = str(new_booking["_id"])
        if "tour_details" in new_booking and "_id" in new_booking["tour_details"]:
            new_booking["tour_details"]["_id"] = str(new_booking["tour_details"]["_id"])
    
        # Return as Pydantic model
        return Booking(**new_booking)
    


@booking.get("/bookings/", response_model=List[Booking])
async def get_all_bookings():
    # async with get_database() as db:
    # database = DatabaseManager.get_db()
    # async with DatabaseManager.get_db_context() as database:
    # booking_collection = db[bookings

    booking_collection  = await get_collection(booking_collection_name)
    bookings = await booking_collection.find().to_list(100)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    
    # Convert MongoDB _id to string format and assign to id field
    for bookingData in bookings:
        bookingData['id'] = str(bookingData.pop('_id'))
    
    return [Booking(**bookingData) for bookingData in bookings]


#    # Convert the ObjectId to a string for each booking and return as Pydantic models
#     # return [Booking(id=str(booking["_id"]), **booking) for booking in bookings]
# # Return bookings with `id` properly mapped from `_id` field
#     # return [Booking(id=str(booking["_id"]), **{key: value for key, value in booking.items() if key != "_id"}) for booking in bookings]
    

@booking.get("/")
async def read_root():
    return {"message": "Hello, World!"}



# @booking.get("/bookings/search", response_model=List[Booking])
# async def get_bookings_by_email(email: str = Query(..., description="Email to filter bookings")):

#     # database = DatabaseManager.get_db()
#     # async with DatabaseManager.get_db_context() as database:
#     #     booking_collection = database.bookings
#     #     collection = database.tours 

#     booking_collection  = await get_collection(booking_collection_name)
#     tour_collection  = await get_collection(tour_collection_name)
#     try:

#         if booking_collection is None or tour_collection is None:
#             raise HTTPException(status_code=500, detail="Database collections not initialized")
#         # if booking_collection is None or collection is None:
#         #     raise HTTPException(status_code=500, detail="Database collections not initialized")
#         # Case-insensitive email search
#         query = {"email": {"$regex": f"^{email}$", "$options": "i"}}
        
#         # Retrieve all bookings for the user
#         bookings_cursor = booking_collection.find(query)  # Replace with correct collection
#         bookings = await bookings_cursor.to_list(length=None)
        
#         if not bookings:
#             raise HTTPException(status_code=404, detail="No bookings found for the given email")
        
#         # Extract tour IDs and convert them to ObjectId for MongoDB query
#         tour_ids = []
#         for bookingData in bookings:
#             try:
#                 # Convert string tour_id to ObjectId for MongoDB query
#                 tour_ids.append(ObjectId(bookingData["tour_id"]))
#             except:
#                 print(f"Invalid tour_id format: {bookingData['tour_id']}")
#                 continue
        
#         # Fetch tour details for all tour IDs in a single query
#         tours_cursor = tour_collection.find({"_id": {"$in": tour_ids}})  # Replace with correct collection
#         tours = await tours_cursor.to_list(length=None)
        
#         # Create a dictionary mapping tour IDs (as strings) to tour details
#         tour_dict = {str(tour["_id"]): tour for tour in tours}
        
#         # Attach tour details to each booking
#         for bookingData in bookings:
#             booking_tour_id = str(bookingData["tour_id"])
#             if booking_tour_id in tour_dict:
#                 tour_data = tour_dict[booking_tour_id]
#                 # Convert ObjectId to string in tour data
#                 tour_data["_id"] = str(tour_data["_id"])
#                 bookingData["tour_details"] = tour_data
#             else:
#                 bookingData["tour_details"] = None
        
#         # Return the bookings with tour details (FastAPI handles serialization)
#         return bookings
        
#     except Exception as e:
#         print(f"Error processing booking search: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")
    




@booking.get("/bookings/search", response_model=List[Booking])
async def get_bookings_by_email(email: str = Query(..., description="Email to filter bookings")):
    booking_collection = await get_collection(booking_collection_name)
    tour_collection = await get_collection(tour_collection_name)
    try:
        if booking_collection is None or tour_collection is None:
            raise HTTPException(status_code=500, detail="Database collections not initialized")

        # Case-insensitive email search
        query = {"email": {"$regex": f"^{email}$", "$options": "i"}}
        
        # Retrieve all bookings for the user
        bookings_cursor = booking_collection.find(query)
        bookings = await bookings_cursor.to_list(length=None)

        if not bookings:
            # Stop further processing if no bookings are found
            raise HTTPException(status_code=404, detail="No bookings found for the given email")

        # Extract tour IDs and convert them to ObjectId for MongoDB query
        tour_ids = []
        for bookingData in bookings:
            try:
                tour_ids.append(ObjectId(bookingData["tour_id"]))
            except Exception:
                print(f"Invalid tour_id format: {bookingData['tour_id']}")
                continue

        if not tour_ids:
            # If there are no valid tour IDs, return the bookings without tour details
            return bookings

        # Fetch tour details for all tour IDs in a single query
        tours_cursor = tour_collection.find({"_id": {"$in": tour_ids}})
        tours = await tours_cursor.to_list(length=None)

        # Create a dictionary mapping tour IDs to tour details
        tour_dict = {str(tour["_id"]): tour for tour in tours}

        # Attach tour details to each booking
        for bookingData in bookings:
            booking_tour_id = str(bookingData["tour_id"])
            bookingData["tour_details"] = tour_dict.get(booking_tour_id, None)

        # Return the bookings with tour details
        return bookings

    except HTTPException:
        # Re-raise HTTPExceptions to FastAPI
        raise
    except Exception as e:
        print(f"Error processing booking search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# @booking.get("/bookings/search", response_model=List[Booking])
# async def get_bookings_by_email(email: str = Query(..., description="Email to filter bookings")):
    
#     database = DatabaseManager.get_db()
#     booking_collection = database.bookings
#     collection = database.tours

#     try:
#         # Case-insensitive email search
#         query = {"email": {"$regex": f"^{email}$", "$options": "i"}}
        
#         # Retrieve all bookings for the user
#         bookings_cursor = booking_collection.find(query)
#         bookings = await bookings_cursor.to_list(length=None)
        
#         if not bookings:
#             raise HTTPException(status_code=404, detail="No bookings found for the given email")
        
#         # Extract tour IDs and convert them to ObjectId for MongoDB query
#         tour_ids = []
#         for booking in bookings:
#             try:
#                 tour_ids.append(ObjectId(booking["tour_id"]))
#             except Exception as e:
#                 print(f"Invalid tour_id format: {booking['tour_id']}")
#                 continue
        
#         # Fetch tour details for all tour IDs in a single query
#         tours_cursor = collection.find({"_id": {"$in": tour_ids}})
#         tours = await tours_cursor.to_list(length=None)
        
#         # Create a dictionary mapping tour IDs (as strings) to tour details
#         tour_dict = {str(tour["_id"]): tour for tour in tours}
        
#         # Process bookings and attach tour details
#         processed_bookings = []
#         for booking in bookings:
#             # Convert booking _id to string
#             booking['id'] = str(booking.pop('_id'))
            
#             # Process tour details
#             booking_tour_id = str(booking["tour_id"])
#             if booking_tour_id in tour_dict:
#                 tour_data = tour_dict[booking_tour_id].copy()  # Create a copy to avoid modifying original
#                 # Convert tour ObjectId to string
#                 tour_data['id'] = str(tour_data.pop('_id'))
#                 booking["tour_details"] = tour_data
#             else:
#                 booking["tour_details"] = None
            
#             processed_bookings.append(booking)
        
#         return processed_bookings
    
#     except Exception as e:
#         print(f"Error processing booking search: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal server error")


@booking.delete("/bookings/{booking_id}", response_model=dict)
async def delete_booking(booking_id: str):
    # async with DatabaseManager.get_db_context() as database:
    # # database = DatabaseManager.get_db()
    #     booking_collection = database.bookings
    booking_collection  = await get_collection(booking_collection_name)
    bookingData = booking_collection.find_one({"_id": ObjectId(booking_id)})
    if not bookingData:
        raise HTTPException(status_code=404, detail="Booking not found")

    await booking_collection.delete_one({"_id": ObjectId(booking_id)})
    return {"message": f"Booking with id {booking_id} has been deleted successfully"}

@booking.put("/bookings/{booking_id}", response_model=Booking)
async def update_booking(booking_id: str, updated_booking: Booking):
    
    # database = DatabaseManager.get_db()
    # async with DatabaseManager.get_db_context() as database:
    #     booking_collection = database.bookings
    booking_collection  = await get_collection(booking_collection_name)
    # Fetch the existing booking
    bookingData = await booking_collection.find_one({"_id": ObjectId(booking_id)})

    if not bookingData:
        raise HTTPException(status_code=404, detail="Booking not found")

        # Prepare the data to be updated, excluding None values
    updated_data = {key: value for key, value in updated_booking.dict().items() if value is not None}

        # Perform the update operation
    await booking_collection.update_one({"_id": ObjectId(booking_id)}, {"$set": updated_data})

        # Fetch the updated booking from the database
    updated_booking_data = await booking_collection.find_one({"_id": ObjectId(booking_id)})

        # Convert the updated booking data to a dictionary (Pydantic model automatically handles it)
    return Booking(**updated_booking_data)