import os
import json
import requests
from fastapi import HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from langchain import OpenAI
from typing import List, Dict

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HealthData(Base):
    __tablename__ = "health_data"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    data_type = Column(String, index=True)
    value = Column(Float)

Base.metadata.create_all(bind=engine)

async def fetch_health_data(source_url: str) -> Dict:
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from {source_url}: {str(e)}")

async def aggregate_health_data(sources: List[str]) -> List[Dict]:
    aggregated_data = []
    for source in sources:
        data = await fetch_health_data(source)
        aggregated_data.extend(data.get("results", []))
    return aggregated_data

async def save_health_data(data: List[Dict]):
    db = SessionLocal()
    try:
        for item in data:
            health_data = HealthData(source=item.get("source"), data_type=item.get("data_type"), value=item.get("value"))
            db.add(health_data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
    finally:
        db.close()

async def run_data_aggregation(sources: List[str]):
    aggregated_data = await aggregate_health_data(sources)
    await save_health_data(aggregated_data)