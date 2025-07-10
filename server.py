from fastapi import FastAPI, Depends, HTTPException, Request
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sqlite3
import uuid
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    
    # CONNECT DB
    global db
    db = sqlite3.connect("/tmp/hospitals.db", check_same_thread=False)
    db.row_factory = sqlite3.Row

    # CREATE TABLE
    db.execute("""
        CREATE TABLE IF NOT EXISTS hospitals (
            id TEXT NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT CHECK(phone IS NULL OR phone GLOB '[0-9]*'),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (name, address)
        )
    """)
    db.commit()

    yield
    print("Shutting down...")
    db.close()

app = FastAPI(lifespan=lifespan)

# Pydantic model for input validation: Hospital Input
class HospitalIn(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None

# Pydantic model for output validation: Hospital Output
class HospitalOut(HospitalIn):
    # all the fields from HospitalIn along with the following fields
    id: str
    created_at: str


@app.post("/")
def add_hospital(hospital: HospitalIn):
    logging.info(f"POST Request Received: {hospital}")
    try:
        id = str(uuid.uuid4())
        
        db.execute("""
            INSERT INTO hospitals (id, name, address, phone)
            VALUES (?, ?, ?, ?)
        """, (id, hospital.name, hospital.address, hospital.phone))
        
        db.commit()
        return {"message": "Hospital added", "id": id}
    
    except Exception as e:
        logging.error("Failed to add hospital", exc_info=True)
        return {"error": f"Failed to add hospital"}


@app.get("/", response_model=list[HospitalOut])
def get_hospitals():
    logging.info(f"GET Request Received")
    try:
        rows = db.execute("SELECT id, name, address, phone, created_at FROM hospitals").fetchall()
        hospitals = []

        for row in rows:
            hospitals.append(HospitalOut(id=row[0], name=row[1], address=row[2], phone=row[3], created_at=row[4]))

        if hospitals:
            return hospitals
    
    except Exception as e:
        logging.error("Failed to get any hospital", exc_info=True)
        return {"error": f"Failed to get any hospital"}
            
@app.get("/{id}", response_model=HospitalOut)
def get_hospital(id: str):
    logging.info(f"GET Request Received with id = {id}")
    try:
        row = db.execute("SELECT id, name, address, phone, created_at FROM hospitals WHERE id = ?", (id,)).fetchone()
        if row:
            return HospitalOut(id=row[0], name=row[1], address=row[2], phone=row[3], created_at=row[4])
        
    except Exception as e:
        logging.error(f"Failed to get hospital with id = {id}", exc_info=True)
        return {"error": f"Failed to get hospital with id = {id}"}

@app.put("/{id}")
def update_hospital(id:str, hospital: HospitalIn):
    logging.info(f"PUT Request Received with id = {id}, new data: {hospital}")

    try:
        # First check if the hospital with the specified id exists
        if not db.execute("SELECT id FROM hospitals WHERE id = ?", (id,)).fetchone():
            return {"error": f"Hospital with id = {id} does not exist"}
    
        # Then update
        db.execute("""
                UPDATE hospitals
                SET name = ?, address = ?, phone = ?
                WHERE id = ?
            """, (hospital.name, hospital.address, hospital.phone, id))
        
        db.commit()
        return {"message": "Hospital updated successfully"}

    except:
        logging.info(f"Failed to update hospital with id = {id}", exc_info=True)
        return {"error": f"Failed to update hospital with id = {id}"}

@app.delete("/{id}")
def delete_hospital(id: str):
    logging.info(f"DELETE Request Received with id = {id}")
    try:
        # First check if the hospital with the specified id exists
        if not db.execute("SELECT id FROM hospitals WHERE id = ?", (id,)).fetchone():
            return {"error": f"Hospital with id = {id} does not exist"}
        
        # Then delete
        db.execute("DELETE FROM hospitals WHERE id = ?", (id,))
        db.commit()
        return {"message": "Hospital deleted successfully"}

    except:
        logging.error(f"Failed to delete hospital with id = {id}", exc_info=True)
        return {"error": f"Failed to delete hospital with id = {id}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8191))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True, log_level="error", access_log=False)
