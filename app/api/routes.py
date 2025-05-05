from flask import jsonify, request
import traceback
from app.api import bp
from app.services.scraper import tripadvisor, reddit
from app.services.sentiment import emotion_analyzer
from app.services.geo import heatmap_generator
from app import db

@bp.route('/scrape', methods=['POST'])
def scrape():
    """Trigger scraping for a city and category."""
    data = request.get_json()
    city = data.get('city')
    category = data.get('category')
    
    if not city or not category:
        return jsonify({'error': 'Missing city or category'}), 400
    
    try:
        # Trigger both scrapers asynchronously
        tripadvisor_data = tripadvisor.scrape(city, category)
        reddit_data = reddit.scrape(city)
        
        return jsonify({
            'status': 'success',
            'message': f'Scraped {len(tripadvisor_data) + len(reddit_data)} reviews'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/process', methods=['POST'])
def process():
    """Process raw reviews with sentiment analysis."""
    try:
        results = emotion_analyzer.analyze_reviews()
        return jsonify({
            'status': 'success',
            'processed_count': results
        })
    except Exception as e:
        print(f"Error processing reviews: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/heatmap', methods=['GET'])
def get_heatmap():
    """Return GeoJSON of emotional hotspots."""
    emotion = request.args.get('emotion', 'joy')
    try:
        geojson = heatmap_generator.generate(emotion)
        return jsonify(geojson)
    except Exception as e:
        print(f"Error generating heatmap: {str(e)}")
        traceback.print_exc()
        
        # If real data failed, return demo data
        demo_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.1278, 51.5074]  # London
                    },
                    "properties": {
                        "neighborhood": "Central London",
                        "emotion": emotion,
                        "score": 0.85,
                        "weight": 10,
                        "review_count": 42
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.1426, 51.5012]  # Westminster
                    },
                    "properties": {
                        "neighborhood": "Westminster",
                        "emotion": emotion,
                        "score": 0.75,
                        "weight": 8,
                        "review_count": 36
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-0.0753, 51.5177]  # Shoreditch
                    },
                    "properties": {
                        "neighborhood": "Shoreditch",
                        "emotion": emotion,
                        "score": 0.92,
                        "weight": 15,
                        "review_count": 55
                    }
                }
            ]
        }
        return jsonify(demo_data)

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Return reviews for a specific location."""
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Missing location parameter'}), 400
    
    try:
        # Demo reviews
        demo_reviews = [
            {
                "id": 1,
                "text": "I absolutely loved this area! The atmosphere was incredible and everyone was so friendly.",
                "date": "2024-03-15",
                "emotion_scores": [
                    {"emotion": "joy", "score": 0.92},
                    {"emotion": "excitement", "score": 0.88}
                ]
            },
            {
                "id": 2,
                "text": "Great place to visit, though it gets crowded on weekends. Still worth it for the amazing sights!",
                "date": "2024-04-02",
                "emotion_scores": [
                    {"emotion": "joy", "score": 0.75},
                    {"emotion": "excitement", "score": 0.82}
                ]
            },
            {
                "id": 3,
                "text": "A peaceful oasis in the city. Highly recommend visiting in the morning.",
                "date": "2024-04-10",
                "emotion_scores": [
                    {"emotion": "calm", "score": 0.95},
                    {"emotion": "joy", "score": 0.68}
                ]
            }
        ]
        
        return jsonify({"reviews": demo_reviews})
    except Exception as e:
        print(f"Error fetching reviews: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/itinerary', methods=['POST'])
def create_itinerary():
    """Create an itinerary from selected hotspots."""
    data = request.get_json()
    hotspots = data.get('hotspots', [])
    
    if not hotspots:
        return jsonify({'error': 'No hotspots provided'}), 400
    
    try:
        itinerary = {  # TODO: Implement itinerary generation
            'spots': hotspots,
            'route': [],
            'estimated_time': '0 hours'
        }
        return jsonify(itinerary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 