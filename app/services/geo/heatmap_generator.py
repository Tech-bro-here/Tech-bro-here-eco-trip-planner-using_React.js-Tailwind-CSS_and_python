import json
import math
from sqlalchemy import func
from app import db
from app.models.models import Venue, Review, EmotionScore, Neighborhood, EmotionalHotspot

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

class HeatmapGenerator:
    def __init__(self):
        pass

    def _calculate_neighborhood_scores(self, emotion):
        """Calculate average emotion scores for each neighborhood."""
        try:
            # Get all neighborhoods
            neighborhoods = Neighborhood.query.all()
            
            # For each neighborhood, calculate average emotion score
            results = []
            
            for neighborhood in neighborhoods:
                # Extract neighborhood coordinates from GeoJSON
                try:
                    boundary = json.loads(neighborhood.boundary)
                    neighborhood_lat = boundary["coordinates"][1]
                    neighborhood_lng = boundary["coordinates"][0]
                except (json.JSONDecodeError, KeyError, IndexError):
                    # Skip neighborhoods with invalid boundaries
                    continue
                
                # Find nearby venues using distance calculation
                nearby_venues = []
                for venue in Venue.query.all():
                    distance = haversine_distance(
                        neighborhood_lat, neighborhood_lng,
                        venue.latitude, venue.longitude
                    )
                    
                    # Consider venues within 2km as "nearby"
                    if distance <= 2.0:
                        nearby_venues.append(venue.id)
                
                if not nearby_venues:
                    continue
                
                # Get emotion scores for reviews of nearby venues
                emotion_scores = db.session.query(
                    EmotionScore.score
                ).join(
                    Review, Review.id == EmotionScore.review_id
                ).filter(
                    EmotionScore.emotion == emotion,
                    Review.venue_id.in_(nearby_venues)
                ).all()
                
                # Calculate average score
                scores = [score[0] for score in emotion_scores]
                if scores:
                    avg_score = sum(scores) / len(scores)
                    results.append((neighborhood, avg_score, len(scores)))
            
            return results
        
        except Exception as e:
            print(f"Error calculating neighborhood scores: {str(e)}")
            return []

    def _update_hotspots(self, emotion, neighborhood_scores):
        """Update or create emotional hotspots in the database."""
        for neighborhood, avg_score, review_count in neighborhood_scores:
            hotspot = EmotionalHotspot.query.filter_by(
                neighborhood_id=neighborhood.id,
                emotion=emotion
            ).first()
            
            if hotspot:
                hotspot.average_score = avg_score
                hotspot.review_count = review_count
            else:
                hotspot = EmotionalHotspot(
                    neighborhood_id=neighborhood.id,
                    emotion=emotion,
                    average_score=avg_score,
                    review_count=review_count
                )
                db.session.add(hotspot)
        
        db.session.commit()

    def _create_geojson(self, emotion, neighborhood_scores):
        """Create GeoJSON representation of emotional hotspots."""
        features = []
        
        for neighborhood, avg_score, review_count in neighborhood_scores:
            # Parse the neighborhood boundary GeoJSON
            try:
                boundary = json.loads(neighborhood.boundary)
            except json.JSONDecodeError:
                continue
            
            # Create feature properties
            properties = {
                'neighborhood': neighborhood.name,
                'emotion': emotion,
                'score': float(avg_score),
                'weight': float(avg_score * 10),  # Scale for heatmap
                'review_count': review_count
            }
            
            # Create GeoJSON feature
            feature = {
                'type': 'Feature',
                'geometry': boundary,
                'properties': properties
            }
            
            features.append(feature)
        
        # Create final GeoJSON object
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        return geojson

    def generate(self, emotion):
        """Generate emotional heatmap for specified emotion."""
        try:
            # Calculate scores for each neighborhood
            neighborhood_scores = self._calculate_neighborhood_scores(emotion)
            
            # If no scores (likely due to no data), return fallback data
            if not neighborhood_scores:
                return self._generate_fallback_data(emotion)
            
            # Update hotspots in database
            self._update_hotspots(emotion, neighborhood_scores)
            
            # Generate GeoJSON
            return self._create_geojson(emotion, neighborhood_scores)
        except Exception as e:
            print(f"Error generating heatmap: {str(e)}")
            return self._generate_fallback_data(emotion)
    
    def _generate_fallback_data(self, emotion):
        """Generate fallback data when no real data is available."""
        # London landmarks for demo
        demo_locations = [
            {"name": "Central London", "lat": 51.5074, "lng": -0.1278, "score": 0.85},
            {"name": "Westminster", "lat": 51.5012, "lng": -0.1426, "score": 0.75},
            {"name": "Shoreditch", "lat": 51.5177, "lng": -0.0753, "score": 0.92},
            {"name": "Camden", "lat": 51.5390, "lng": -0.1427, "score": 0.88},
            {"name": "South Bank", "lat": 51.5050, "lng": -0.1167, "score": 0.79},
        ]
        
        features = []
        for location in demo_locations:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [location["lng"], location["lat"]]
                },
                "properties": {
                    "neighborhood": location["name"],
                    "emotion": emotion,
                    "score": location["score"],
                    "weight": location["score"] * 10,
                    "review_count": int(location["score"] * 50)  # Fake review count
                }
            }
            features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }

# Create generator instance
generator = HeatmapGenerator()

def generate(emotion):
    """Wrapper function to generate heatmap."""
    return generator.generate(emotion) 