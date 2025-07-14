
import { User, Bot, Database, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  content: string;
  sender: "user" | "assistant";
  timestamp: Date;
  type?: "query" | "result" | "error";
}

interface ChatMessageProps {
  message: Message;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.sender === "user";
  
  const getIcon = () => {
    if (isUser) return <User className="w-5 h-5" />;
    if (message.type === "error") return <AlertCircle className="w-5 h-5 text-red-500" />;
    return <Bot className="w-5 h-5 text-blue-500" />;
  };

  const getMessageStyle = () => {
    if (isUser) {
      return "bg-blue-600 text-white ml-12";
    }
    if (message.type === "error") {
      return "bg-red-50 text-red-800 border border-red-200 mr-12";
    }
    return "bg-white border border-gray-200 mr-12";
  };

  return (
    <div className={cn("flex gap-3 animate-fade-in", isUser ? "flex-row-reverse" : "flex-row")}>
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
        isUser ? "bg-blue-600 text-white" : "bg-gray-100"
      )}>
        {getIcon()}
      </div>
      
      <div className={cn("max-w-[80%] rounded-2xl px-4 py-3 shadow-sm", getMessageStyle())}>
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </p>
        <p className={cn(
          "text-xs mt-2 opacity-70",
          isUser ? "text-blue-100" : "text-gray-500"
        )}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
};

export default ChatMessage;
