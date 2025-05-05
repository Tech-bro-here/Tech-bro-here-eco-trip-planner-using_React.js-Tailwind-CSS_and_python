import os
import praw
import re
from datetime import datetime
from app import db
from app.models.models import Venue, Review
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'eco-mood-travel:v0.1 (by /u/your_username)')

def init_reddit_client():
    """Initialize the Reddit API client with credentials."""
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("Warning: Reddit API credentials not set in environment variables.")
        print("Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")
        print("Returning sample data instead.")
        return None
    
    try:
        return praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    except Exception as e:
        print(f"Error initializing Reddit client: {e}")
        return None

def extract_location_from_text(text, city):
    """Extract potential location names from text."""
    # Simple regex to find location-like patterns
    location_pattern = re.compile(r'\b([A-Z][a-z]+ (?:Park|Square|Market|Bridge|Museum|Tower|Palace|Garden|Street|St\.|Road|Rd\.|Avenue|Ave\.))\b')
    locations = location_pattern.findall(text)
    
    # If no specific locations found, use the city as a general location
    if not locations:
        return city + " General"
    
    return locations[0]

def scrape(city, limit=25):
    """Scrape Reddit for posts about a city."""
    reddit = init_reddit_client()
    reviews = []
    
    if not reddit:
        # Return empty list if Reddit client initialization failed
        return reviews
    
    try:
        # Subreddits to search
        subreddits = [f"r/{city.lower()}", "r/travel", "r/TravelTips"]
        
        for sub_name in subreddits:
            try:
                subreddit = reddit.subreddit(sub_name.replace("r/", ""))
                
                # Search posts containing the city name
                search_query = f"{city} experience OR visit OR review"
                search_results = subreddit.search(search_query, limit=limit)
                
                for post in search_results:
                    # Skip if post doesn't have text content
                    if not post.selftext:
                        continue
                    
                    # Extract location from post title/text
                    location_name = extract_location_from_text(post.title + " " + post.selftext, city)
                    
                    # Check if venue exists, otherwise create it
                    venue = Venue.query.filter_by(name=location_name).first()
                    if not venue:
                        # Create a generic venue with approximate coordinates
                        venue = Venue(
                            name=location_name,
                            address=f"{location_name}, {city}",
                            latitude=0.0,  # These would need to be geocoded in a real app
                            longitude=0.0,
                            category="general"
                        )
                        db.session.add(venue)
                        db.session.commit()
                    
                    # Create a review from the post
                    review = Review(
                        venue_id=venue.id,
                        source="reddit",
                        text=post.selftext[:1000],  # Limit text length
                        reviewer_location="Unknown",
                        review_date=datetime.fromtimestamp(post.created_utc)
                    )
                    
                    db.session.add(review)
                    reviews.append(review)
            
            except Exception as e:
                print(f"Error scraping {sub_name}: {str(e)}")
                continue
        
        # Commit all reviews to the database
        if reviews:
            db.session.commit()
        
        return reviews
    
    except Exception as e:
        # Roll back any changes if an error occurs
        db.session.rollback()
        print(f"Error during Reddit scraping: {str(e)}")
        return [] 