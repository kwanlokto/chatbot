"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { deleteFile, fetchDocs, uploadPDF, type DocGroup } from "@/lib/api";

export default function Sidebar() {
  const [docs, setDocs] = useState<DocGroup[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadDocs = useCallback(async () => {
    try {
      setDocs(await fetchDocs());
    } catch {
      // silently ignore — backend may not be ready yet
    }
  }, []);

  useEffect(() => {
    loadDocs();
  }, [loadDocs]);

  const handleUpload = useCallback(
    async (file: File) => {
      setUploading(true);
      setUploadError(null);
      try {
        await uploadPDF(file);
        await loadDocs();
      } catch (err) {
        setUploadError(err instanceof Error ? err.message : "Upload failed");
      } finally {
        setUploading(false);
      }
    },
    [loadDocs]
  );

  const handleDelete = useCallback(
    async (filename: string) => {
      try {
        await deleteFile(filename);
        await loadDocs();
      } catch {
        // silently ignore
      }
    },
    [loadDocs]
  );

  return (
    <aside className="w-64 flex flex-col bg-gray-900 border-r border-gray-800 h-full flex-shrink-0">
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-base font-semibold text-white">PDF Chatbot</h1>
        <p className="text-xs text-gray-500 mt-0.5">RAG · Open Source</p>
      </div>

      {/* Doc list */}
      <div className="flex-1 overflow-y-auto p-4">
        <p className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
          Documents
        </p>

        {docs.length === 0 ? (
          <p className="text-sm text-gray-600 italic">No documents yet</p>
        ) : (
          <ul className="space-y-2">
            {docs.map((doc) => (
              <li
                key={doc.filename}
                className="flex items-start gap-2 bg-gray-800 rounded-lg p-2.5"
              >
                <svg
                  className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zm-1 1.5L18.5 9H13V3.5zM6 20V4h5v7h7v9H6z" />
                </svg>
                <div className="min-w-0 flex-1">
                  <p className="text-sm text-gray-200 truncate" title={doc.filename}>
                    {doc.filename}
                  </p>
                  <p className="text-xs text-gray-500">{doc.chunkCount} chunks</p>
                </div>
                <button
                  onClick={() => handleDelete(doc.filename)}
                  className="text-gray-600 hover:text-red-400 transition-colors flex-shrink-0"
                  aria-label={`Delete ${doc.filename}`}
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Upload section */}
      <div className="p-4 border-t border-gray-800">
        {uploadError && (
          <p className="text-xs text-red-400 mb-2 break-words">{uploadError}</p>
        )}
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="w-full py-2.5 px-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {uploading ? (
            <>
              <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              Uploading…
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                />
              </svg>
              Upload PDF
            </>
          )}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleUpload(file);
            e.target.value = "";
          }}
        />
      </div>
    </aside>
  );
}
