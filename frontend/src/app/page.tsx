"use client";

import { useCallback, useState } from "react";

import ChatWindow from "@/components/ChatWindow";
import Sidebar from "@/components/Sidebar";
import { sendMessage, type Message } from "@/lib/api";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = useCallback(
    async (text: string) => {
      const userMsg: Message = { role: "user", content: text };
      const nextHistory = [...messages, userMsg];
      setMessages(nextHistory);
      setIsLoading(true);
      setError(null);

      try {
        const response = await sendMessage(text, messages);
        setMessages([...nextHistory, { role: "assistant", content: response }]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Something went wrong");
      } finally {
        setIsLoading(false);
      }
    },
    [messages]
  );

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        error={error}
        onSend={handleSend}
      />
    </div>
  );
}
