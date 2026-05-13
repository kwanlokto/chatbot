const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface DocGroup {
  filename: string;
  chunkCount: number;
}

export async function sendMessage(message: string, history: Message[]): Promise<string> {
  const res = await fetch(`${API_URL}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }

  const data = await res.json();
  return data.response as string;
}

export async function uploadPDF(
  file: File
): Promise<{ message: string; chunks: number; filename: string }> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_URL}/rag/doc`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Upload failed");
  }

  return res.json();
}

export async function fetchDocs(): Promise<DocGroup[]> {
  const res = await fetch(`${API_URL}/rag/docs`);
  if (!res.ok) throw new Error("Failed to fetch documents");

  const data = await res.json();
  const metadatas: Record<string, string>[] = data.metadatas ?? [];

  const grouped: Record<string, number> = {};
  for (const meta of metadatas) {
    const src = meta?.source ?? "Unknown";
    grouped[src] = (grouped[src] ?? 0) + 1;
  }

  return Object.entries(grouped).map(([filename, chunkCount]) => ({ filename, chunkCount }));
}

export async function deleteFile(filename: string): Promise<void> {
  const res = await fetch(`${API_URL}/rag/file/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete file");
}
