import numpy as np
from typing import Dict, List, Tuple
import pandas as pd

class DataProcessor:
    def __init__(self):
        self.significance_threshold = 0.05  # 5% difference threshold

    async def analyze_champion(self, champion_name: str) -> Dict:
        """Analyze a champion's winrate data across regions."""
        # This is a placeholder - in production, you'd want to use real data
        mock_data = self._get_mock_analysis_data(champion_name)
        return self._process_analysis(mock_data)

    def _process_analysis(self, data: Dict) -> Dict:
        """Process and analyze the champion data."""
        winrates = data["regions"]
        
        # Calculate basic statistics
        stats = {
            "mean_winrate": np.mean(list(winrates.values())),
            "std_winrate": np.std(list(winrates.values())),
            "max_winrate": max(winrates.values()),
            "min_winrate": min(winrates.values()),
            "max_region": max(winrates.items(), key=lambda x: x[1])[0],
            "min_region": min(winrates.items(), key=lambda x: x[1])[0],
        }

        # Identify significant divergences
        divergences = self._find_significant_divergences(winrates, stats["mean_winrate"])
        
        # Generate insights
        insights = self._generate_insights(stats, divergences)

        return {
            "statistics": stats,
            "divergences": divergences,
            "insights": insights
        }

    def _find_significant_divergences(self, winrates: Dict[str, float], mean_winrate: float) -> List[Dict]:
        """Find regions where winrate significantly differs from the mean."""
        divergences = []
        for region, winrate in winrates.items():
            difference = abs(winrate - mean_winrate)
            if difference > self.significance_threshold:
                divergences.append({
                    "region": region,
                    "winrate": winrate,
                    "difference": difference,
                    "type": "above" if winrate > mean_winrate else "below"
                })
        return sorted(divergences, key=lambda x: x["difference"], reverse=True)

    def _generate_insights(self, stats: Dict, divergences: List[Dict]) -> List[str]:
        """Generate insights based on the analysis."""
        insights = []
        
        # Overall performance insight
        if stats["std_winrate"] > 0.03:
            insights.append(f"High variance in winrate across regions (std: {stats['std_winrate']:.2f})")
        else:
            insights.append("Relatively consistent winrate across regions")

        # Regional differences
        if divergences:
            top_divergence = divergences[0]
            insights.append(
                f"Strongest divergence in {top_divergence['region']} "
                f"({top_divergence['type']} average by {top_divergence['difference']:.2f})"
            )

        # Meta analysis
        if stats["max_winrate"] > 0.55:
            insights.append("Potentially overpowered in some regions")
        elif stats["min_winrate"] < 0.45:
            insights.append("Potentially underpowered in some regions")

        return insights

    def _get_mock_analysis_data(self, champion_name: str) -> Dict:
        """Generate mock analysis data for testing."""
        return {
            "name": champion_name,
            "regions": {
                "NA": 0.52,
                "EUW": 0.51,
                "EUNE": 0.50,
                "KR": 0.54,
                "CN": 0.53,
                "JP": 0.49,
                "BR": 0.48,
                "RU": 0.51,
                "OCE": 0.50,
                "TR": 0.49,
                "LAN": 0.48,
                "LAS": 0.47
            }
        } 