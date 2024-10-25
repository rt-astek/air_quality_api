import os
from fastapi import APIRouter, HTTPException
from app.models import AirQualityData
from app.schemas import AirQualityEntry
import pandas as pd
from fastapi import HTTPException
import xarray as xr
import logging
import rasterio
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()


def load_geotiff(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Leer la primera banda
        profile = src.profile
        return data, profile


@api_router.get("/data/csv")
async def convert_to_csv():
    try:
        # Load the NetCDF dataset with chunk sizes
        dataset = xr.open_dataset('./app/data/air_quality_data.nc', chunks={'lat': 100, 'lon': 100})

        # Log dimensions and variables
        logger.info(f"Dataset dimensions: {dataset.dims}")
        logger.info(f"Dataset variables: {dataset.variables}")

        # Select subset of of rows
        pm25_data = dataset['GWRPM25'].isel(lat=slice(0, 100), lon=slice(0, 100))  # Adjust slices as needed
        pm25_data_filled = pm25_data.where(~pm25_data.isnull(), np.random.uniform(0, 10, pm25_data.shape))
        
        # Convert to DataFrame
        df = pm25_data_filled.to_dataframe().reset_index()
        df['year'] = 2020

        # Save as CSV
        csv_file_path = './app/data/air_quality_data.csv'
        df.to_csv(csv_file_path, index=False)

        return {"message": f"CSV saved at: {csv_file_path}"}
    except Exception as e:
        logger.error(f"Error converting to CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


data_model = AirQualityData(pd.read_csv('./app/data/air_quality_data.csv'))

@api_router.get("/data")
async def get_data():
    try:
        return data_model.get_all_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/data/filter")
async def filter_data(year: int = None, lat: float = None, long: float = None):
    results = data_model.filter_data(year, lat, long)
    return results

@api_router.get("/data/stats")
async def get_statistics():
    stats = data_model.get_statistics()
    return stats


@api_router.get("/data/{id}")
async def get_data_by_id(id: int):
    entry = data_model.get_data_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Data entry not found")
    return entry

@api_router.post("/data", response_model=AirQualityEntry)
async def add_data_entry(entry: AirQualityEntry):
    data_model.add_data_entry(entry.dict())
    return entry

@api_router.put("/data/{id}", response_model=AirQualityEntry)
async def update_data_entry(id: int, entry: AirQualityEntry):
    existing_entry = data_model.get_data_by_id(id)
    if existing_entry is None:
        raise HTTPException(status_code=404, detail="Data entry not found")
    data_model.update_data_entry(id, entry.dict())
    return entry

@api_router.delete("/data/{id}")
async def delete_data_entry(id: int):
    existing_entry = data_model.get_data_by_id(id)
    if existing_entry is None:
        raise HTTPException(status_code=404, detail="Data entry not found")
    data_model.delete_data_entry(id)
    return {"detail": "Data entry deleted"}
