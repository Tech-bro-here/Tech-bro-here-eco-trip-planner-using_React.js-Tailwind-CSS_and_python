import React from 'react';
import { Hotspot } from '../types';

interface ItineraryBuilderProps {
  selectedHotspots: Hotspot[];
  onRemoveHotspot: (id: string) => void;
  onReorderHotspots: (hotspots: Hotspot[]) => void;
  onSaveItinerary: () => void;
}

const ItineraryBuilder: React.FC<ItineraryBuilderProps> = ({
  selectedHotspots,
  onRemoveHotspot,
  onReorderHotspots,
  onSaveItinerary,
}) => {
  const handleDragStart = (e: React.DragEvent<HTMLDivElement>, index: number) => {
    e.dataTransfer.setData('text/plain', index.toString());
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>, dropIndex: number) => {
    e.preventDefault();
    const dragIndex = parseInt(e.dataTransfer.getData('text/plain'), 10);
    if (dragIndex === dropIndex) return;

    const newHotspots = [...selectedHotspots];
    const [removed] = newHotspots.splice(dragIndex, 1);
    newHotspots.splice(dropIndex, 0, removed);
    onReorderHotspots(newHotspots);
  };

  if (selectedHotspots.length === 0) {
    return (
      <div className="bg-white p-4 rounded-lg shadow text-center">
        <p className="text-gray-500">
          Click on hotspots to add them to your itinerary
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Your Itinerary</h3>
        <button
          onClick={onSaveItinerary}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          Save Itinerary
        </button>
      </div>

      <div className="space-y-2">
        {selectedHotspots.map((hotspot, index) => (
          <div
            key={hotspot.id}
            draggable
            onDragStart={(e) => handleDragStart(e, index)}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, index)}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-md cursor-move hover:bg-gray-100"
          >
            <div>
              <div className="font-medium">{hotspot.name}</div>
              <div className="text-sm text-gray-500">
                {Object.entries(hotspot.emotion_scores)
                  .map(([emotion, score]) => `${emotion}: ${(score * 100).toFixed(0)}%`)
                  .join(' • ')}
              </div>
            </div>
            <button
              onClick={() => onRemoveHotspot(hotspot.id)}
              className="p-1 text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ItineraryBuilder; 