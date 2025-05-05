import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from app import db
from app.models.models import Venue, Review

class TripAdvisorScraper:
    def __init__(self):
        self.base_url = "https://www.tripadvisor.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _build_search_url(self, city, category):
        """Build the search URL for a city and category."""
        city_encoded = city.replace(' ', '+')
        category_encoded = category.replace(' ', '+')
        return f"{self.base_url}/Search?q={city_encoded}+{category_encoded}"

    def _extract_coordinates(self, script_text):
        """Extract latitude and longitude from script content."""
        lat_match = re.search(r'"latitude":\s*"([^"]+)"', script_text)
        lng_match = re.search(r'"longitude":\s*"([^"]+)"', script_text)
        
        if lat_match and lng_match:
            return float(lat_match.group(1)), float(lng_match.group(1))
        return None, None

    def _parse_review_date(self, date_text):
        """Parse review date from TripAdvisor format."""
        try:
            return datetime.strptime(date_text, '%B %Y')
        except ValueError:
            return None

    def _scrape_venue(self, venue_url):
        """Scrape details and reviews for a specific venue."""
        response = requests.get(self.base_url + venue_url, headers=self.headers)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract venue details
        name = soup.find('h1', {'class': 'title'}).text.strip() if soup.find('h1', {'class': 'title'}) else ''
        address = soup.find('address').text.strip() if soup.find('address') else ''
        
        # Extract coordinates from script tags
        scripts = soup.find_all('script')
        lat, lng = None, None
        for script in scripts:
            if script.string and 'latitude' in script.string:
                lat, lng = self._extract_coordinates(script.string)
                break
        
        if not all([name, address, lat, lng]):
            return None
            
        # Create or update venue
        venue = Venue.query.filter_by(name=name, address=address).first()
        if not venue:
            venue = Venue(
                name=name,
                address=address,
                latitude=lat,
                longitude=lng
            )
            db.session.add(venue)
            db.session.commit()
        
        # Extract reviews
        reviews = []
        review_containers = soup.find_all('div', {'class': 'review-container'})
        
        for container in review_containers:
            review_text = container.find('p', {'class': 'review-text'}).text.strip() if container.find('p', {'class': 'review-text'}) else ''
            reviewer_location = container.find('span', {'class': 'reviewer-location'}).text.strip() if container.find('span', {'class': 'reviewer-location'}) else ''
            date_text = container.find('span', {'class': 'review-date'}).text.strip() if container.find('span', {'class': 'review-date'}) else ''
            
            if review_text:
                review = Review(
                    venue_id=venue.id,
                    source='tripadvisor',
                    text=review_text,
                    reviewer_location=reviewer_location,
                    review_date=self._parse_review_date(date_text)
                )
                reviews.append(review)
        
        return reviews

    def scrape(self, city, category):
        """Main scraping function for TripAdvisor."""
        search_url = self._build_search_url(city, category)
        response = requests.get(search_url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to access TripAdvisor search: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        venue_links = soup.find_all('a', {'class': 'result-title'})
        
        all_reviews = []
        for link in venue_links[:10]:  # Limit to first 10 venues for demo
            venue_url = link.get('href')
            if venue_url:
                reviews = self._scrape_venue(venue_url)
                if reviews:
                    all_reviews.extend(reviews)
        
        # Bulk save reviews
        if all_reviews:
            db.session.bulk_save_objects(all_reviews)
            db.session.commit()
        
        return all_reviews

# Create scraper instance
scraper = TripAdvisorScraper()

def scrape(city, category):
    """Wrapper function to initiate scraping."""
    return scraper.scrape(city, category) 