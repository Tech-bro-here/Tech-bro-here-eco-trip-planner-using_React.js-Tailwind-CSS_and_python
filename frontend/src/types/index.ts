export interface User {
  id: string;
  username: string;
  email: string;
}

export interface Review {
  id: string;
  text: string;
  date: string;
  emotion_scores: {
    [key: string]: number;
  };
  hotspot_id?: string;
}

export interface EmotionScore {
  emotion: string;
  score: number;
}

export interface Hotspot {
  id: string;
  name: string;
  lat: number;
  lng: number;
  emotion_scores: {
    [key: string]: number;
  };
}

export interface HeatmapPoint {
  lat: number;
  lng: number;
  weight: number;
}

export interface HeatmapResponse {
  data: HeatmapPoint[];
}

export interface AuthResponse {
  user: User;
  token?: string;
} 