"use client";

import { create } from "zustand";
import type { ChatMessage, Dashboard, Student } from "@/types/neurotutor";

type LearningState = {
  student: Student | null;
  dashboard: Dashboard | null;
  messages: ChatMessage[];
  topic: string;
  language: "python" | "java";
  code: string;
  setStudent: (student: Student) => void;
  setDashboard: (dashboard: Dashboard) => void;
  addMessage: (message: ChatMessage) => void;
  setTopic: (topic: string) => void;
  setLanguage: (language: "python" | "java") => void;
  setCode: (code: string) => void;
};

export const useLearningStore = create<LearningState>((set) => ({
  student: null,
  dashboard: null,
  messages: [
    {
      role: "tutor",
      content: "Welcome to NeuroTutor. Ask a question or write code, and I will guide your thinking instead of jumping to the answer."
    }
  ],
  topic: "Binary Search",
  language: "python",
  code: "def binary_search(nums, target):\n    left, right = 0, len(nums) - 1\n    # write your next step here\n",
  setStudent: (student) => set({ student }),
  setDashboard: (dashboard) => set({ dashboard }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setTopic: (topic) => set({ topic }),
  setLanguage: (language) => set({ language }),
  setCode: (code) => set({ code })
}));
