"use client";

import { FormEvent, useState } from "react";
import { Send } from "lucide-react";
import { sendTutorMessage, fetchDashboard } from "@/services/api";
import { useLearningStore } from "@/store/useLearningStore";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function ChatTutor() {
  const { student, messages, topic, addMessage, setDashboard, setTopic } = useLearningStore();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!student || !question.trim()) return;
    const nextQuestion = question.trim();
    setQuestion("");
    addMessage({ role: "student", content: nextQuestion });
    setLoading(true);
    try {
      const response = await sendTutorMessage(student.id, nextQuestion, topic);
      addMessage({
        role: "tutor",
        content: `${response.response}\n\nGuiding questions:\n- ${response.guiding_questions.join("\n- ")}\n\nModel: ${response.model_used}`
      });
      setDashboard(await fetchDashboard(student.id));
    } catch {
      addMessage({ role: "tutor", content: "I could not reach the tutor engine. Please check the backend and try again." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="flex min-h-[520px] flex-col rounded-lg border border-border bg-white shadow-sm">
      <div className="border-b border-border p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-bold">NeuroTutor</h1>
            <p className="text-sm text-slate-600">{student ? `${student.name} · ${student.learning_level}` : "Create a learner profile to begin"}</p>
          </div>
          <Input value={topic} onChange={(event) => setTopic(event.target.value)} className="max-w-48" />
        </div>
      </div>
      <div className="flex-1 space-y-3 overflow-auto p-4">
        {messages.map((message, index) => (
          <div key={`${message.role}-${index}`} className={message.role === "student" ? "ml-auto max-w-[85%] rounded-lg bg-primary p-3 text-sm text-white" : "max-w-[90%] whitespace-pre-wrap rounded-lg bg-muted p-3 text-sm"}>
            {message.content}
          </div>
        ))}
      </div>
      <form onSubmit={submit} className="flex gap-2 border-t border-border p-3">
        <Input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask for guidance, not final answers" disabled={!student || loading} />
        <Button disabled={!student || loading} aria-label="Send message" className="px-3">
          <Send size={18} />
        </Button>
      </form>
    </section>
  );
}
