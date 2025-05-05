from datetime import datetime
from app import db

class Venue(db.Model):
    """Represents a location or venue."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='venue', lazy=True)

class Review(db.Model):
    """Represents a raw review from TripAdvisor or Reddit."""
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    source = db.Column(db.String(50), nullable=False)  # 'tripadvisor' or 'reddit'
    text = db.Column(db.Text, nullable=False)
    reviewer_location = db.Column(db.String(200))
    review_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmotionScore(db.Model):
    """Represents the emotional analysis of a review."""
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    emotion = db.Column(db.String(50), nullable=False)  # joy, excitement, calm, etc.
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    review = db.relationship('Review', backref='emotion_scores', lazy=True)

class Neighborhood(db.Model):
    """Represents a city neighborhood or area."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    boundary = db.Column(db.Text)  # GeoJSON polygon of the neighborhood boundary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmotionalHotspot(db.Model):
    """Represents an aggregated emotional hotspot."""
    id = db.Column(db.Integer, primary_key=True)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'), nullable=False)
    emotion = db.Column(db.String(50), nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    review_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    neighborhood = db.relationship('Neighborhood', backref='hotspots', lazy=True) 