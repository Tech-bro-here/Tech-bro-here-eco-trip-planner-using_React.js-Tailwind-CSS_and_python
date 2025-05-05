import React, { useState, useEffect } from 'react';
import Map from './Map';
import ReviewSidebar from './ReviewSidebar';
import ItineraryBuilder from './ItineraryBuilder';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Hotspot, Review, HeatmapResponse } from '../types';

const EMOTIONS = ['joy', 'excitement', 'calm', 'trust', 'anticipation'];

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [city, setCity] = useState('');
  const [category, setCategory] = useState('restaurants');
  const [selectedEmotion, setSelectedEmotion] = useState<string>('joy');
  const [isLoading, setIsLoading] = useState(false);
  const [heatmapData, setHeatmapData] = useState<HeatmapResponse | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [selectedHotspots, setSelectedHotspots] = useState<Hotspot[]>([]);
  const [currentLocation, setCurrentLocation] = useState<{ lat: number, lng: number, name: string } | null>(null);

  useEffect(() => {
    const fetchHeatmap = async () => {
      try {
        const data = await api.getHeatmap(selectedEmotion);
        setHeatmapData(data);
      } catch (error) {
        console.error('Failed to fetch heatmap:', error);
      }
    };

    fetchHeatmap();
  }, [selectedEmotion]);

  const handleSearch = async () => {
    if (!city) return;

    setIsLoading(true);
    try {
      await api.scrape({ city, category });
      await api.processReviews();
      const heatmap = await api.getHeatmap(selectedEmotion);
      setHeatmapData(heatmap);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNeighborhoodClick = async (lat: number, lng: number, name: string) => {
    try {
      setIsLoading(true);
      setCurrentLocation({ lat, lng, name });
      const { reviews: apiReviews } = await api.getReviews(`${lat},${lng}`);
      setReviews(apiReviews);
    } catch (error) {
      console.error('Failed to fetch reviews:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEmotionChange = async (emotion: string) => {
    setSelectedEmotion(emotion);
    try {
      const heatmap = await api.getHeatmap(emotion);
      setHeatmapData(heatmap);
    } catch (error) {
      console.error('Error updating heatmap:', error);
    }
  };

  const handleAddToItinerary = () => {
    if (!currentLocation) return;
    
    // Check if this location is already in the itinerary
    const existingHotspot = selectedHotspots.find(
      h => h.location.lat === currentLocation.lat && h.location.lng === currentLocation.lng
    );
    
    if (existingHotspot) {
      alert('This location is already in your itinerary');
      return;
    }
    
    // Create a new hotspot object
    const newHotspot: Hotspot = {
      id: `hotspot-${Date.now()}`,
      name: currentLocation.name,
      location: {
        lat: currentLocation.lat,
        lng: currentLocation.lng
      },
      emotion_scores: {
        [selectedEmotion]: reviews.length > 0 ? 
          reviews.reduce((sum, review) => {
            const emotionScore = review.emotion_scores.find(es => es.emotion === selectedEmotion);
            return emotionScore ? sum + emotionScore.score : sum;
          }, 0) / reviews.length : 0.8
      }
    };
    
    setSelectedHotspots([...selectedHotspots, newHotspot]);
  };

  const handleSaveItinerary = async () => {
    if (selectedHotspots.length === 0) {
      alert('Please add at least one location to your itinerary');
      return;
    }
    
    try {
      setIsLoading(true);
      const hotspotIds = selectedHotspots.map(h => h.id);
      await api.itineraries.create(hotspotIds);
      alert('Itinerary saved successfully!');
      // Optionally clear the current itinerary
      // setSelectedHotspots([]);
    } catch (error) {
      console.error('Failed to save itinerary:', error);
      alert('Failed to save itinerary. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      {/* Welcome Message */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900">
          Welcome back, {user?.username}!
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Start exploring emotional hotspots in your desired destination.
        </p>
      </div>

      {/* Search Section */}
      <div className="mb-6 flex gap-4">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="restaurants">Restaurants</option>
          <option value="attractions">Attractions</option>
          <option value="hotels">Hotels</option>
        </select>
        <button
          onClick={handleSearch}
          disabled={isLoading || !city}
          className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-400"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {/* Emotion Filter */}
      <div className="mb-6 flex gap-2">
        {EMOTIONS.map(emotion => (
          <button
            key={emotion}
            onClick={() => handleEmotionChange(emotion)}
            className={`px-4 py-2 rounded-md ${
              selectedEmotion === emotion
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            {emotion.charAt(0).toUpperCase() + emotion.slice(1)}
          </button>
        ))}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map */}
        <div className="lg:col-span-2">
          {heatmapData && (
            <Map
              emotion={selectedEmotion}
              heatmapData={heatmapData}
              onNeighborhoodClick={handleNeighborhoodClick}
            />
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <ReviewSidebar
            reviews={reviews}
            isLoading={isLoading}
            selectedEmotion={selectedEmotion}
            locationName={currentLocation?.name}
            onAddToItinerary={handleAddToItinerary}
            hasAddButton={!!currentLocation && reviews.length > 0}
          />
          <ItineraryBuilder
            selectedHotspots={selectedHotspots}
            onRemoveHotspot={(id: string) => setSelectedHotspots(spots => spots.filter(s => s.id !== id))}
            onReorderHotspots={setSelectedHotspots}
            onSaveItinerary={handleSaveItinerary}
          />
        </div>
      </div>
    </main>
  );
};

export default Dashboard; 