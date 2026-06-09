"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import { analyzeCode } from "@/services/api";
import { useDebouncedEffect } from "@/hooks/useDebouncedEffect";
import { useLearningStore } from "@/store/useLearningStore";

const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export function CodeWorkspace() {
  const { student, code, language, topic, setCode, setLanguage, addMessage } = useLearningStore();
  const [analysis, setAnalysis] = useState("Code analysis will appear after you start editing.");
  const [busy, setBusy] = useState(false);

  useDebouncedEffect(() => {
    if (!student || code.trim().length < 8) return;
    setBusy(true);
    analyzeCode(student.id, code, language, topic)
      .then((result) => {
        setAnalysis(`${result.guidance}\n\nFindings:\n- ${result.findings.join("\n- ")}`);
        addMessage({ role: "tutor", content: `Workspace feedback: ${result.guidance}` });
      })
      .catch(() => setAnalysis("Analyzer is offline. Keep coding; the backend may need to be started."))
      .finally(() => setBusy(false));
  }, [code, language, student?.id, topic], 2000);

  return (
    <section className="overflow-hidden rounded-lg border border-border bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-border p-3">
        <h2 className="font-semibold">Live Coding Workspace</h2>
        <select value={language} onChange={(event) => setLanguage(event.target.value as "python" | "java")} className="rounded-md border border-border bg-white px-2 py-1 text-sm">
          <option value="python">Python</option>
          <option value="java">Java</option>
        </select>
      </div>
      <div className="h-[360px]">
        <Editor
          height="100%"
          language={language}
          value={code}
          theme="vs-light"
          options={{ minimap: { enabled: false }, fontSize: 14, scrollBeyondLastLine: false }}
          onChange={(value) => setCode(value ?? "")}
        />
      </div>
      <div className="min-h-28 border-t border-border bg-slate-50 p-3 text-sm text-slate-700">
        <div className="mb-1 font-medium">{busy ? "Analyzing..." : "Tutor Analysis"}</div>
        <p className="whitespace-pre-wrap">{analysis}</p>
      </div>
    </section>
  );
}
