import * as React from 'react';
import type { HeatmapResponse } from '../types';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet.heat';

interface MapProps {
  emotion: string;
  heatmapData: HeatmapResponse;
  onNeighborhoodClick: (lat: number, lng: number, name: string) => void;
}

const Map: React.FC<MapProps> = ({ emotion, heatmapData, onNeighborhoodClick }) => {
  const mapRef = React.useRef<L.Map | null>(null);
  const heatmapLayerRef = React.useRef<any>(null);
  const markersLayerRef = React.useRef<L.LayerGroup | null>(null);

  React.useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map('map').setView([51.505, -0.09], 13); // London by default

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapRef.current);

      markersLayerRef.current = L.layerGroup().addTo(mapRef.current);
    }

    // Clear previous markers
    if (markersLayerRef.current) {
      markersLayerRef.current.clearLayers();
    }

    // Clear previous heatmap
    if (heatmapLayerRef.current && mapRef.current) {
      mapRef.current.removeLayer(heatmapLayerRef.current);
    }

    if (heatmapData && heatmapData.features) {
      // Handle GeoJSON data
      const points: [number, number, number][] = [];
      const latLngs: L.LatLng[] = [];

      heatmapData.features.forEach(feature => {
        if (feature.geometry.type === "Point") {
          const coords = feature.geometry.coordinates;
          const lng = coords[0];
          const lat = coords[1];
          const weight = feature.properties.weight || feature.properties.score || 1;
          
          points.push([lat, lng, weight]);
          latLngs.push(L.latLng(lat, lng));
          
          // Add marker with popup
          const marker = L.marker([lat, lng])
            .bindPopup(`
              <strong>${feature.properties.neighborhood}</strong><br>
              ${emotion} score: ${feature.properties.score.toFixed(2)}<br>
              Reviews: ${feature.properties.review_count}
            `)
            .on('click', () => {
              onNeighborhoodClick(lat, lng, feature.properties.neighborhood);
            });
          
          markersLayerRef.current?.addLayer(marker);
        }
      });

      // Add heatmap layer
      if (points.length > 0) {
        // @ts-ignore
        heatmapLayerRef.current = L.heatLayer(points, {
          radius: 25,
          blur: 15,
          maxZoom: 10,
          gradient: {
            0.4: 'blue',
            0.6: 'lime',
            0.8: 'yellow',
            1.0: 'red'
          }
        }).addTo(mapRef.current!);

        // Fit map to all points
        if (latLngs.length > 0) {
          const bounds = L.latLngBounds(latLngs);
          mapRef.current?.fitBounds(bounds);
        }
      }
    } else if (heatmapData && heatmapData.data) {
      // Handle old format (array of points in data property)
      const points = heatmapData.data.map(point => 
        [point.lat, point.lng, point.weight] as [number, number, number]
      );

      if (points.length > 0) {
        // @ts-ignore
        heatmapLayerRef.current = L.heatLayer(points, {
          radius: 25,
          blur: 15,
          maxZoom: 10,
          gradient: {
            0.4: 'blue',
            0.6: 'lime',
            0.8: 'yellow',
            1.0: 'red'
          }
        }).addTo(mapRef.current!);

        const latLngs = points.map(p => L.latLng(p[0], p[1]));
        const bounds = L.latLngBounds(latLngs);
        mapRef.current?.fitBounds(bounds);
      }
    }
  }, [heatmapData, onNeighborhoodClick, emotion]);

  return <div id="map" style={{ height: '500px', width: '100%' }} />;
};

export default Map; 