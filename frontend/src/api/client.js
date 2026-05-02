import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const fetchDashboardStats = async () => (await client.get("/dashboard/stats")).data;
export const fetchTeacherScores = async () => (await client.get("/teachers/fairness-score")).data;
export const fetchEvaluations = async (params) => (await client.get("/evaluations", { params })).data;
export const exportEvaluationsCsv = async (params) =>
  (await client.get("/evaluations/export.csv", { params, responseType: "blob" })).data;

export default client;
