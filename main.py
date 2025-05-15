from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path
import json
from data_fetcher import DataFetcher
from data_processor import DataProcessor

app = FastAPI(title="LoL Winrate Divergence Analysis")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize data fetcher and processor
data_fetcher = DataFetcher()
data_processor = DataProcessor()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with champion winrate data."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/api/champions")
async def get_champions():
    """Get list of all champions with their winrates across regions."""
    champions_data = await data_fetcher.get_all_champions_data()
    return champions_data

@app.get("/api/champion/{champion_name}")
async def get_champion_data(champion_name: str):
    """Get detailed winrate data for a specific champion."""
    champion_data = await data_fetcher.get_champion_data(champion_name)
    return champion_data

@app.get("/api/regions")
async def get_regions():
    """Get list of available regions and their data."""
    regions = await data_fetcher.get_available_regions()
    return regions

@app.get("/api/analysis/{champion_name}")
async def get_champion_analysis(champion_name: str):
    """Get detailed analysis of a champion's winrate divergence."""
    analysis = await data_processor.analyze_champion(champion_name)
    return analysis

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 