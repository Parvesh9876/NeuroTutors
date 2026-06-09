import axios from "axios";
import type { Dashboard, OnboardingRequest, Student, TutorResponse } from "@/types/neurotutor";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api",
  timeout: 30000
});

export async function onboard(payload: OnboardingRequest) {
  const { data } = await api.post<{ student: Student; onboarding_summary: string }>("/onboarding", payload);
  return data;
}

export async function sendTutorMessage(studentId: number, question: string, topic: string) {
  const { data } = await api.post<TutorResponse>("/chat", { student_id: studentId, question, topic });
  return data;
}

export async function analyzeCode(studentId: number, code: string, language: "python" | "java", topic: string) {
  const { data } = await api.post("/analyze", { student_id: studentId, code, language, topic });
  return data as { guidance: string; findings: string[]; misconception_detected: boolean };
}

export async function fetchDashboard(studentId: number) {
  const { data } = await api.get<Dashboard>(`/dashboard/${studentId}`);
  return data;
}
