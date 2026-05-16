"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";

const API_URL = "http://localhost:8001";

const TEMPLATES = [
  "Build a sales agent for a SaaS company with RAG over product docs, guardrails, and a web chat interface",
  "Build a customer support agent for an e-commerce store with FAQ knowledge base and audit logging",
  "Build a research agent that retrieves information from documents and answers questions with citations"
];

export default function Home() {
  const [description, setDescription] = useState("");
  const [auth, setAuth] = useState(true);
  const [audit, setAudit] = useState(true);
  const [frontend, setFrontend] = useState("webchat");
  const [llm, setLlm] = useState("gemini");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  const generate = async () => {
    if (!description.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description, auth, audit, frontend, llm })
      });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
        setSelectedFile(data.filenames[0]);
      }
    } catch (e) {
      setError("Failed to connect to AgentForge backend");
    } finally {
      setLoading(false);
    }
  };

  const download = async () => {
    const res = await fetch(`${API_URL}/generate/download`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, auth, audit, frontend, llm })
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "agentforge-project.zip";
    a.click();
  };

  return (
    <div className="min-h-screen">
      <div className="border-b border-white/10 bg-background/60 backdrop-blur-md px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[#0f172a] flex items-center justify-center text-white font-bold text-sm">A</div>
          <span className="font-bold text-lg">AgentForge</span>
          <Badge variant="secondary" className="text-xs">Powered by IBM Bob</Badge>
        </div>
      </div>

      <div className="max-w-6xl mx-auto p-8 flex flex-col gap-8">
        {!result ? (
          <>
            <div className="text-center flex flex-col gap-3">
              <h1 className="text-4xl font-bold">Turn any AI agent idea into working code</h1>
              <p className="text-muted-foreground text-lg">Describe your agent system in plain English. IBM Bob generates the complete codebase.</p>
            </div>

            <div className="flex flex-col gap-2">
              <p className="text-sm font-medium text-muted-foreground">Quick start templates:</p>
              <div className="flex flex-col gap-2">
                  {TEMPLATES.map((t, i) => (
                  <button key={i} onClick={() => setDescription(t)}
                    className="text-left text-sm border rounded-xl px-4 py-3 bg-white/10 hover:bg-white/20 transition-colors">
                    {t}
                  </button>
                ))}
              </div>
            </div>

            <Card>
              <CardHeader><CardTitle>Describe your agent system</CardTitle></CardHeader>
              <CardContent className="flex flex-col gap-4">
                <Textarea
                  placeholder="e.g. Build a sales agent for a SaaS company with RAG over product docs..."
                  value={description}
                  onChange={e => setDescription(e.target.value)}
                  className="min-h-[120px]"
                />
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center justify-between border rounded-lg px-4 py-3 bg-muted/30">
                    <span className="text-sm">JWT Authentication</span>
                    <Switch checked={auth} onCheckedChange={setAuth} />
                  </div>
                  <div className="flex items-center justify-between border rounded-lg px-4 py-3 bg-muted/30">
                    <span className="text-sm">Audit Logging</span>
                    <Switch checked={audit} onCheckedChange={setAudit} />
                  </div>
                  <div className="flex items-center justify-between border rounded-lg px-4 py-3 bg-muted/30">
                    <span className="text-sm">Web Chat UI</span>
                    <Switch checked={frontend === "webchat"} onCheckedChange={v => setFrontend(v ? "webchat" : "api")} />
                  </div>
                  <div className="flex items-center justify-between border rounded-lg px-4 py-3 bg-muted/30">
                    <span className="text-sm">LLM: {llm === "gemini" ? "Gemini" : "Featherless"}</span>
                    <Switch checked={llm === "gemini"} onCheckedChange={v => setLlm(v ? "gemini" : "featherless")} />
                  </div>
                </div>
                <Button onClick={generate} disabled={loading || !description.trim()} size="lg">
                  {loading ? "Bob is generating your project... (~6 min)" : "Generate with IBM Bob"}
                </Button>
                {error && <p className="text-destructive text-sm">{error}</p>}
              </CardContent>
            </Card>
          </>
        ) : (
          <>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Your project is ready!</h2>
                <p className="text-muted-foreground">{result.file_count} files generated by IBM Bob</p>
              </div>
              <div className="flex gap-3">
                <Button variant="secondary" onClick={() => setResult(null)}>Generate another</Button>
                <Button onClick={download}>Download ZIP</Button>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-4 h-[600px]">
              <div className="border rounded-xl overflow-auto bg-white/5">
                {result.filenames.map((f: string) => (
                  <button key={f} onClick={() => setSelectedFile(f)}
                    className={"w-full text-left px-3 py-2 text-xs font-mono hover:bg-white/10 transition-colors border-b border-white/10 " + (selectedFile === f ? "bg-white/15 font-bold" : "")}>
                    {f}
                  </button>
                ))}
              </div>
              <div className="col-span-3 border rounded-xl overflow-auto bg-white/10 p-4">
                <pre className="text-xs font-mono whitespace-pre-wrap">
                  {selectedFile && result.files[selectedFile]}
                </pre>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
