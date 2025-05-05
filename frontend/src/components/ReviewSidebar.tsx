import React from 'react';
import { Review } from '../types';

interface ReviewSidebarProps {
  reviews: Review[];
  isLoading: boolean;
  selectedEmotion: string;
  locationName?: string;
  onAddToItinerary?: () => void;
  hasAddButton?: boolean;
}

const ReviewSidebar: React.FC<ReviewSidebarProps> = ({
  reviews,
  isLoading,
  selectedEmotion,
  locationName,
  onAddToItinerary,
  hasAddButton = false
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getEmotionScore = (review: Review) => {
    const emotionScore = review.emotion_scores.find(
      (score) => score.emotion === selectedEmotion
    );
    return emotionScore ? (emotionScore.score * 100).toFixed(1) : '0';
  };

  if (isLoading) {
    return (
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-40 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="bg-white p-4 rounded-lg shadow text-center">
        <p className="text-gray-500">
          Click on a location to view traveler reviews
        </p>
      </div>
    );
  }

  // Filter the most positive reviews for the selected emotion
  const sortedReviews = [...reviews].sort((a, b) => {
    const scoreA = a.emotion_scores.find(s => s.emotion === selectedEmotion)?.score || 0;
    const scoreB = b.emotion_scores.find(s => s.emotion === selectedEmotion)?.score || 0;
    return scoreB - scoreA;
  });

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">
          {locationName ? `Reviews: ${locationName}` : 'Location Reviews'}
        </h3>
        {hasAddButton && onAddToItinerary && (
          <button
            onClick={onAddToItinerary}
            className="px-3 py-1 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
          >
            Add to Itinerary
          </button>
        )}
      </div>
      
      <div className="space-y-4">
        {sortedReviews.map(review => (
          <div key={review.id} className="border-b pb-3">
            <p className="text-sm mb-2">{review.text}</p>
            <div className="flex flex-wrap gap-2">
              {review.emotion_scores.map(score => (
                <span
                  key={score.emotion}
                  className={`px-2 py-1 text-xs rounded-full ${
                    score.emotion === selectedEmotion
                      ? 'bg-primary-100 text-primary-800 font-semibold'
                      : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {score.emotion}: {(score.score * 100).toFixed(0)}%
                </span>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">Posted on {formatDate(review.date)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReviewSidebar; 