# Eco-Mood Travel Planner 🌍✨

An emotion-driven itinerary website that helps travelers discover "positive-vibe" zones in any city by analyzing sentiment from traveler reviews and creating interactive mood-based heatmaps.

## Features

- 🔍 Automated scraping of TripAdvisor and Reddit reviews
- 💭 Advanced sentiment and emotion analysis of locations
- 🗺️ Interactive heatmaps showing emotional hotspots
- 📅 Smart itinerary builder with emotion-based recommendations
- 🎨 Beautiful, responsive UI with intuitive filtering

## Tech Stack

- Backend: Python 3.10+, Flask
- NLP: Hugging Face Transformers
- Data Processing: pandas, NumPy, GeoPandas
- Mapping: Folium (Leaflet.js)
- Frontend: React.js + Tailwind CSS
- Database: SQLite

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
5. Run the development server:
   ```bash
   flask run
   ```

## Project Structure

```
eco-trip-planner/
├── app/
│   ├── api/            # API routes
│   ├── models/         # Database models
│   ├── services/       # Business logic
│   │   ├── scraper/    # Web scraping modules
│   │   ├── sentiment/  # Emotion analysis
│   │   └── geo/        # Geospatial processing
│   ├── static/         # Static files
│   └── templates/      # HTML templates
├── frontend/          # React frontend
├── tests/            # Test suite
├── .env.example      # Environment variables template
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for any purpose. 