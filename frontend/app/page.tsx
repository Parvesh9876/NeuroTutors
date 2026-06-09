"use client";

import { ChatTutor } from "@/components/Chat/ChatTutor";
import { CodeWorkspace } from "@/components/Editor/CodeWorkspace";
import { ProgressPanel } from "@/components/Dashboard/ProgressPanel";
import { OnboardingForm } from "@/components/Profile/OnboardingForm";
import { EmptyState } from "@/components/Loading/EmptyState";
import { useLearningStore } from "@/store/useLearningStore";

export default function Home() {
  const student = useLearningStore((state) => state.student);

  return (
    <main className="min-h-screen px-4 py-6 lg:px-8">
      <div className="mx-auto grid max-w-7xl gap-4">
        <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
          <aside className="space-y-4">
            <OnboardingForm />
            {student ? (
              <div className="rounded-lg border border-border bg-white p-4 text-sm shadow-sm">
                <div className="font-semibold">{student.name}</div>
                <div className="text-slate-600">{student.learning_level}</div>
                <div className="mt-2 text-slate-600">Goal: {student.profile?.goal}</div>
              </div>
            ) : (
              <EmptyState />
            )}
          </aside>
          <div className="grid gap-4 xl:grid-cols-2">
            <ChatTutor />
            <CodeWorkspace />
          </div>
        </div>
        <ProgressPanel />
      </div>
    </main>
  );
}
