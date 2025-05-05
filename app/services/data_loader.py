import json
import random
from datetime import datetime, timedelta
from app import db
from app.models.models import Venue, Review, EmotionScore, Neighborhood, EmotionalHotspot

def load_sample_data():
    """Populate the database with sample data for testing."""
    try:
        # Only load data if the database is empty
        if Venue.query.count() == 0:
            # Create sample neighborhoods
            neighborhoods = [
                Neighborhood(
                    name="Central London",
                    city="London",
                    boundary=json.dumps({
                        "type": "Point",
                        "coordinates": [-0.1278, 51.5074]
                    })
                ),
                Neighborhood(
                    name="Westminster",
                    city="London",
                    boundary=json.dumps({
                        "type": "Point",
                        "coordinates": [-0.1426, 51.5012]
                    })
                ),
                Neighborhood(
                    name="Shoreditch",
                    city="London",
                    boundary=json.dumps({
                        "type": "Point",
                        "coordinates": [-0.0753, 51.5177]
                    })
                ),
                Neighborhood(
                    name="Camden",
                    city="London",
                    boundary=json.dumps({
                        "type": "Point",
                        "coordinates": [-0.1427, 51.5390]
                    })
                ),
                Neighborhood(
                    name="South Bank",
                    city="London",
                    boundary=json.dumps({
                        "type": "Point",
                        "coordinates": [-0.1167, 51.5050]
                    })
                )
            ]
            
            db.session.add_all(neighborhoods)
            db.session.commit()
            
            # Create venues in each neighborhood
            venues = []
            venue_data = [
                {
                    "name": "The British Museum",
                    "address": "Great Russell St, London WC1B 3DG",
                    "lat": 51.5194, 
                    "lng": -0.1270,
                    "category": "attractions"
                },
                {
                    "name": "Tower of London",
                    "address": "Tower Hill, London EC3N 4AB",
                    "lat": 51.5081,
                    "lng": -0.0759,
                    "category": "attractions"
                },
                {
                    "name": "The Shard",
                    "address": "32 London Bridge St, London SE1 9SG",
                    "lat": 51.5045,
                    "lng": -0.0865,
                    "category": "attractions"
                },
                {
                    "name": "Camden Market",
                    "address": "Camden Lock Place, London NW1 8AF",
                    "lat": 51.5415,
                    "lng": -0.1466,
                    "category": "attractions"
                },
                {
                    "name": "Dishoom Shoreditch",
                    "address": "7 Boundary St, London E2 7JE",
                    "lat": 51.5266,
                    "lng": -0.0784,
                    "category": "restaurants"
                }
            ]
            
            for venue_info in venue_data:
                venue = Venue(
                    name=venue_info["name"],
                    address=venue_info["address"],
                    latitude=venue_info["lat"],
                    longitude=venue_info["lng"],
                    category=venue_info["category"]
                )
                venues.append(venue)
                
            db.session.add_all(venues)
            db.session.commit()
            
            # Create reviews for each venue
            reviews = []
            sample_texts = [
                "I absolutely loved this place! The atmosphere was electric and everyone was so friendly.",
                "Great spot, but it does get crowded on weekends. Still worth it for the amazing sights!",
                "A peaceful oasis in the city. Highly recommend visiting in the morning.",
                "The experience exceeded my expectations, truly a must-visit!",
                "Fantastic place to spend an afternoon. The staff were incredibly helpful.",
                "A bit overrated in my opinion, but still enjoyed my time there.",
                "Such a charming location with lots of character.",
                "I felt so relaxed here, perfect escape from the busy city.",
                "The energy of this place is incredible! So much to see and do.",
                "A bit pricey but the experience is worth every penny."
            ]
            
            for venue in venues:
                # Create 3-5 reviews per venue
                for _ in range(random.randint(3, 5)):
                    review_text = random.choice(sample_texts)
                    days_ago = random.randint(1, 90)
                    review_date = datetime.now() - timedelta(days=days_ago)
                    
                    review = Review(
                        venue_id=venue.id,
                        source="sample",
                        text=review_text,
                        reviewer_location="Sample City",
                        review_date=review_date
                    )
                    reviews.append(review)
            
            db.session.add_all(reviews)
            db.session.commit()
            
            # Create emotion scores for each review
            emotion_scores = []
            emotions = ["joy", "excitement", "calm", "trust", "anticipation"]
            
            for review in reviews:
                # Create scores for each emotion
                for emotion in emotions:
                    # Generate realistic scores based on review text
                    base_score = 0.5
                    
                    # Simple keyword-based scoring
                    positive_keywords = ["loved", "great", "peaceful", "amazing", "fantastic", "charming"]
                    negative_keywords = ["overrated", "crowded", "pricey"]
                    
                    for keyword in positive_keywords:
                        if keyword in review.text.lower():
                            base_score += 0.1
                    
                    for keyword in negative_keywords:
                        if keyword in review.text.lower():
                            base_score -= 0.05
                    
                    # Add some randomness
                    score = min(max(base_score + random.uniform(-0.1, 0.1), 0.1), 0.95)
                    
                    emotion_score = EmotionScore(
                        review_id=review.id,
                        emotion=emotion,
                        score=score
                    )
                    emotion_scores.append(emotion_score)
            
            db.session.add_all(emotion_scores)
            db.session.commit()
            
            # Generate emotional hotspots
            for neighborhood in neighborhoods:
                for emotion in emotions:
                    # Calculate average score for this neighborhood and emotion
                    emotion_scores_query = db.session.query(
                        EmotionScore.score
                    ).join(
                        Review, Review.id == EmotionScore.review_id
                    ).join(
                        Venue, Venue.id == Review.venue_id
                    ).filter(
                        EmotionScore.emotion == emotion,
                        # Simplified proximity check - normally we'd use spatial functions
                        ((Venue.latitude - float(json.loads(neighborhood.boundary)["coordinates"][1]))**2 + 
                         (Venue.longitude - float(json.loads(neighborhood.boundary)["coordinates"][0]))**2) < 0.01
                    )
                    
                    scores = [score[0] for score in emotion_scores_query]
                    if scores:
                        avg_score = sum(scores) / len(scores)
                        review_count = len(scores)
                    else:
                        avg_score = random.uniform(0.5, 0.9)  # Fallback to random
                        review_count = random.randint(5, 20)
                    
                    hotspot = EmotionalHotspot(
                        neighborhood_id=neighborhood.id,
                        emotion=emotion,
                        average_score=avg_score,
                        review_count=review_count
                    )
                    db.session.add(hotspot)
            
            db.session.commit()
            
            return {
                "neighborhoods": len(neighborhoods),
                "venues": len(venues),
                "reviews": len(reviews),
                "emotion_scores": len(emotion_scores)
            }
        return {"message": "Database already contains data"}
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error loading sample data: {str(e)}")

# Convenience function to get sample data status
def get_sample_data_status():
    return {
        "neighborhoods": Neighborhood.query.count(),
        "venues": Venue.query.count(),
        "reviews": Review.query.count(),
        "emotion_scores": EmotionScore.query.count(),
        "hotspots": EmotionalHotspot.query.count()
    } 