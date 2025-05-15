# League of Legends Winrate Divergence Analysis

This project analyzes and visualizes champion winrates across different League of Legends servers, helping to identify regional differences in champion performance.

## Features

- Real-time winrate data from multiple League of Legends servers
- Interactive visualizations of winrate differences
- Champion-specific analysis across regions
- Historical data tracking
- Easy-to-use web interface

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Riot Games API key (if needed)
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

- `main.py`: FastAPI application entry point
- `data_fetcher.py`: Handles data collection from different servers
- `data_processor.py`: Processes and analyzes the winrate data
- `static/`: Frontend assets
- `templates/`: HTML templates
- `utils/`: Utility functions

## Data Sources

The project uses data from:
- Riot Games API
- Community statistics websites
- Official League of Legends statistics

## Contributing

Feel free to submit issues and enhancement requests!
