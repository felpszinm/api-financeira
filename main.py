from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

app = FastAPI()


DATABASE_URL=os.getenv("DATABASE_URL")
@app.get("/")
def read_root():
    return {"message": "API running with sucessfull"}

