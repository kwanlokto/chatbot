"use client";

import { useEffect, useRef } from "react";

import type { Message } from "@/lib/api";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";

interface Props {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  onSend: (text: string) => void;
}

export default function ChatWindow({ messages, isLoading, error, onSend }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex flex-col flex-1 h-full overflow-hidden">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full text-gray-500 select-none">
            <svg
              className="w-16 h-16 mb-4 opacity-20"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
            <p className="text-lg font-medium text-gray-400">Start a conversation</p>
            <p className="text-sm mt-1 text-gray-600">Upload a PDF, then ask questions about it</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {isLoading && (
          <div className="flex gap-3 items-start">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0 text-xs font-bold">
              AI
            </div>
            <div className="bg-gray-800 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1 items-center h-4">
                {[0, 150, 300].map((delay) => (
                  <span
                    key={delay}
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: `${delay}ms` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-900/30 border border-red-800 rounded-lg px-4 py-3 text-red-300 text-sm">
            {error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={onSend} disabled={isLoading} />
    </div>
  );
}
