"use client";

import { useState } from "react";
import { onboard } from "@/services/api";
import { useLearningStore } from "@/store/useLearningStore";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function OnboardingForm() {
  const setStudent = useLearningStore((state) => state.setStudent);
  const addMessage = useLearningStore((state) => state.addMessage);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(formData: FormData) {
    setLoading(true);
    setError("");
    try {
      const response = await onboard({
        name: String(formData.get("name")),
        email: String(formData.get("email")),
        experience_level: String(formData.get("experience")),
        programming_knowledge: String(formData.get("knowledge")),
        problem_solving_confidence: Number(formData.get("confidence")),
        goal: String(formData.get("goal")),
        preferred_language: String(formData.get("language")),
        preferred_learning_style: String(formData.get("style"))
      });
      setStudent(response.student);
      addMessage({ role: "tutor", content: response.onboarding_summary });
    } catch {
      setError("Could not create profile. Check that the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form action={submit} className="grid gap-3 rounded-lg border border-border bg-white p-4 shadow-sm">
      <div>
        <h2 className="text-lg font-semibold">Learner Profile</h2>
        <p className="text-sm text-slate-600">Start with a short assessment so the tutor can adapt.</p>
      </div>
      <Input name="name" placeholder="Student name" required />
      <Input name="email" type="email" placeholder="Email" required />
      <Input name="experience" placeholder="Experience level" defaultValue="beginner" required />
      <Input name="knowledge" placeholder="Programming knowledge" defaultValue="basic Python" required />
      <label className="text-sm text-slate-700">
        Confidence
        <input name="confidence" type="range" min="1" max="5" defaultValue="3" className="mt-2 w-full" />
      </label>
      <Input name="goal" placeholder="Goal" defaultValue="placement preparation" required />
      <select name="language" className="rounded-md border border-border bg-white px-3 py-2 text-sm" defaultValue="Python">
        <option>Python</option>
        <option>Java</option>
      </select>
      <Input name="style" placeholder="Learning style" defaultValue="guided examples" />
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <Button disabled={loading}>{loading ? "Creating..." : "Create Profile"}</Button>
    </form>
  );
}
