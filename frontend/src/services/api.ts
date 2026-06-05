import axios from "axios";

export const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 20000,
});

export interface Stats {
  articles: number;
  top_stories: number;
  newsletters: number;
}

export interface Story {
  id: number;
  title: string;
  source: string;
  score: number;
  summary: string;
  url?: string;
}

export interface Newsletter {
  id: number;
  title: string;
  content: string;
  created_at?: string;
  published_at?: string;
}

export const getStats = async (): Promise<Stats> => {
  const { data } = await api.get<Stats>("/news/stats");
  return data;
};

export const getTopStories = async (): Promise<Story[]> => {
  const { data } = await api.get<Story[]>("/news/top-stories");
  return data;
};

export const getLatestNewsletter = async (): Promise<Newsletter> => {
  const { data } = await api.get<Newsletter>("/news/latest-newsletter");
  return data;
};

export const generateNewsletter = async (): Promise<Newsletter> => {
  const { data } = await api.post<Newsletter>("/news/generate-newsletter");
  return data;
};

export const subscribeUser = async (email: string) => {
  const { data } = await api.post("/subscribers", { email });
  return data;
};
