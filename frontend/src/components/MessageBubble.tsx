import type { Message } from "@/lib/api";

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 items-start ${isUser ? "flex-row-reverse" : ""}`}>
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${
          isUser ? "bg-gray-600" : "bg-blue-600"
        }`}
      >
        {isUser ? "You" : "AI"}
      </div>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap break-words ${
          isUser
            ? "bg-blue-600 text-white rounded-tr-sm"
            : "bg-gray-800 text-gray-100 rounded-tl-sm"
        }`}
      >
        {message.content}
      </div>
    </div>
  );
}
