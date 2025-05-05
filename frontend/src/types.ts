export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Review {
  id: number;
  text: string;
  date: string;
  emotion_scores: {
    emotion: string;
    score: number;
  }[];
  hotspot_id: number;
}

export interface EmotionScore {
  emotion: string;
  score: number;
}

export interface Hotspot {
  id: string;
  name: string;
  location: {
    lat: number;
    lng: number;
  };
  emotion_scores: {
    [key: string]: number;
  };
}

export interface HeatmapPoint {
  lat: number;
  lng: number;
  weight: number;
}

export interface HeatmapFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: number[];
  };
  properties: {
    neighborhood: string;
    emotion: string;
    score: number;
    weight?: number;
    review_count: number;
  };
}

export interface HeatmapResponse {
  data?: HeatmapPoint[];
  type?: string;
  features?: HeatmapFeature[];
}

export interface AuthResponse {
  user: User;
  token: string;
} 