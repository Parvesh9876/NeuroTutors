"use client";

import * as Progress from "@radix-ui/react-progress";
import { useLearningStore } from "@/store/useLearningStore";

export function ProgressPanel() {
  const dashboard = useLearningStore((state) => state.dashboard);
  const student = useLearningStore((state) => state.student);
  const profile = dashboard?.student.profile ?? student?.profile;
  const difficulty = dashboard?.difficulty_level ?? profile?.difficulty_level ?? 1;
  const bloom = dashboard?.student.current_bloom_level ?? student?.current_bloom_level ?? "Remember";

  return (
    <section className="grid gap-4 rounded-lg border border-border bg-white p-4 shadow-sm md:grid-cols-4">
      <Metric label="Bloom Level" value={bloom} />
      <Metric label="Difficulty" value={`${difficulty}/5`} />
      <Metric label="Learning Streak" value={`${dashboard?.learning_streak ?? 0}`} />
      <div>
        <div className="mb-2 text-sm font-medium">Skill Score</div>
        <Progress.Root className="h-2 overflow-hidden rounded-full bg-muted">
          <Progress.Indicator className="h-full bg-accent transition-all" style={{ width: `${Math.round((profile?.skill_score ?? 0.2) * 100)}%` }} />
        </Progress.Root>
        <p className="mt-2 text-xs text-slate-600">Weak: {(dashboard?.weak_topics ?? []).join(", ") || "None detected yet"}</p>
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-sm font-medium text-slate-600">{label}</div>
      <div className="mt-1 text-2xl font-bold">{value}</div>
    </div>
  );
}
