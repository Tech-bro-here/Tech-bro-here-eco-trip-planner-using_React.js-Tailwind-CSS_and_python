from transformers import pipeline
from app import db
from app.models.models import Review, EmotionScore

class EmotionAnalyzer:
    def __init__(self):
        """Initialize the emotion analysis pipeline."""
        self.emotion_pipeline = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )

    def _analyze_text(self, text):
        """Analyze text and return emotion scores."""
        try:
            # Get emotion scores for the text
            results = self.emotion_pipeline(text)[0]
            
            # Convert to dictionary format
            emotion_scores = {
                score['label']: score['score']
                for score in results
            }
            
            return emotion_scores
        except Exception as e:
            print(f"Error analyzing text: {str(e)}")
            return None

    def analyze_reviews(self, batch_size=100):
        """Analyze all unprocessed reviews in the database."""
        # Get reviews that haven't been analyzed yet
        unprocessed_reviews = Review.query.outerjoin(
            EmotionScore,
            Review.id == EmotionScore.review_id
        ).filter(
            EmotionScore.id.is_(None)
        ).all()
        
        results = []
        
        # Process reviews in batches
        for i in range(0, len(unprocessed_reviews), batch_size):
            batch = unprocessed_reviews[i:i + batch_size]
            
            for review in batch:
                emotion_scores = self._analyze_text(review.text)
                
                if emotion_scores:
                    # Create EmotionScore objects for each emotion
                    for emotion, score in emotion_scores.items():
                        emotion_score = EmotionScore(
                            review_id=review.id,
                            emotion=emotion,
                            score=score
                        )
                        results.append(emotion_score)
            
            # Commit batch to database
            if results:
                db.session.bulk_save_objects(results)
                db.session.commit()
                results = []  # Clear results for next batch
        
        return len(unprocessed_reviews)

# Create analyzer instance
analyzer = EmotionAnalyzer()

def analyze_reviews():
    """Wrapper function to initiate review analysis."""
    return analyzer.analyze_reviews() 