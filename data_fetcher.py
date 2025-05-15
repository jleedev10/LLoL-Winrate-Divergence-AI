import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    def __init__(self):
        self.regions = {
            "NA": "na1",
            "EUW": "euw1",
            "EUNE": "eun1",
            "KR": "kr",
            "CN": "cn1",
            "JP": "jp1",
            "BR": "br1",
            "RU": "ru",
            "OCE": "oc1",
            "TR": "tr1",
            "LAN": "la1",
            "LAS": "la2"
        }
        self.api_key = os.getenv("RIOT_API_KEY")
        self.base_url = "https://ddragon.leagueoflegends.com/cdn"
        self.version = self._get_latest_version()
        
    def _get_latest_version(self) -> str:
        """Get the latest League of Legends version."""
        # This is a placeholder - in production, you'd want to fetch this dynamically
        return "13.24.1"

    async def get_all_champions_data(self) -> Dict:
        """Fetch winrate data for all champions across all regions."""
        tasks = []
        for region in self.regions.values():
            tasks.append(self._fetch_region_data(region))
        
        results = await asyncio.gather(*tasks)
        return self._process_champion_data(results)

    async def get_champion_data(self, champion_name: str) -> Dict:
        """Fetch detailed winrate data for a specific champion."""
        tasks = []
        for region in self.regions.values():
            tasks.append(self._fetch_champion_region_data(champion_name, region))
        
        results = await asyncio.gather(*tasks)
        return self._process_single_champion_data(champion_name, results)

    async def get_available_regions(self) -> List[str]:
        """Get list of available regions."""
        return list(self.regions.keys())

    async def _fetch_region_data(self, region: str) -> Dict:
        """Fetch champion data for a specific region."""
        # This is a placeholder - in production, you'd want to use actual API endpoints
        # For now, we'll return mock data
        return {
            "region": region,
            "champions": self._get_mock_champion_data()
        }

    async def _fetch_champion_region_data(self, champion_name: str, region: str) -> Dict:
        """Fetch data for a specific champion in a specific region."""
        # This is a placeholder - in production, you'd want to use actual API endpoints
        return {
            "region": region,
            "champion": champion_name,
            "winrate": self._get_mock_winrate(),
            "pickrate": self._get_mock_pickrate(),
            "banrate": self._get_mock_banrate()
        }

    def _process_champion_data(self, results: List[Dict]) -> Dict:
        """Process and combine champion data from all regions."""
        processed_data = {}
        for result in results:
            region = result["region"]
            for champ_data in result["champions"]:
                champ_name = champ_data["name"]
                if champ_name not in processed_data:
                    processed_data[champ_name] = {}
                processed_data[champ_name][region] = champ_data
        return processed_data

    def _process_single_champion_data(self, champion_name: str, results: List[Dict]) -> Dict:
        """Process data for a single champion across all regions."""
        processed_data = {
            "name": champion_name,
            "regions": {}
        }
        for result in results:
            region = result["region"]
            processed_data["regions"][region] = {
                "winrate": result["winrate"],
                "pickrate": result["pickrate"],
                "banrate": result["banrate"]
            }
        return processed_data

    def _get_mock_champion_data(self) -> List[Dict]:
        """Generate mock champion data for testing."""
        # This is just for demonstration - in production, you'd want real data
        return [
            {
                "name": "Ahri",
                "winrate": 0.52,
                "pickrate": 0.08,
                "banrate": 0.05
            },
            {
                "name": "Yasuo",
                "winrate": 0.48,
                "pickrate": 0.12,
                "banrate": 0.15
            }
        ]

    def _get_mock_winrate(self) -> float:
        """Generate a mock winrate."""
        import random
        return round(random.uniform(0.45, 0.55), 2)

    def _get_mock_pickrate(self) -> float:
        """Generate a mock pickrate."""
        import random
        return round(random.uniform(0.05, 0.15), 2)

    def _get_mock_banrate(self) -> float:
        """Generate a mock banrate."""
        import random
        return round(random.uniform(0.01, 0.20), 2) 