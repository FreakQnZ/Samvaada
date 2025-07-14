import { useState, useRef, useEffect } from "react";
import { Send, Database, User, Bot, BarChart3, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";

interface Message {
  id: string;
  content: string;
  sender: "user" | "assistant";
  timestamp: Date;
  type?: "query" | "result" | "error";
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your database assistant. You can ask me questions about your data in natural language.",
      sender: "assistant",
      timestamp: new Date(),
      type: "query",
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    // Add user message to chat
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsTyping(true);

    try {
      const previousMessages = messages
        .filter((msg) => msg.sender === "user" || msg.sender === "assistant")
        .map((msg) => msg.content);

      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: inputValue,
          messages: previousMessages,
        }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        sender: "assistant",
        timestamp: new Date(),
        type: "result",
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        content: "Sorry, something went wrong while processing your request.",
        sender: "assistant",
        timestamp: new Date(),
        type: "error",
      };
      setMessages((prev) => [...prev, errorMessage]);
      console.error("Error:", error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleVisualize = () => {
    console.log("Visualize button clicked");
    // Add your visualization logic here
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearHistory = () => {
    setMessages([
      {
        id: "1",
        content:
          "Hello! I'm your database assistant. You can ask me questions about your data in natural language. For example, try asking 'Show me all customers from this month' or 'What are our top selling products?'",
        sender: "assistant",
        timestamp: new Date(),
        type: "query",
      },
    ]);
    setInputValue("");
    setIsTyping(false);
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden w-full max-w-7xl mx-auto h-[calc(100vh-1rem)]">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database className="w-6 h-6" />
            <div>
              <h2 className="font-semibold text-lg">Database Assistant</h2>
              <p className="text-blue-100 text-sm">
                Ask questions in natural language
              </p>
            </div>
          </div>
          <Button
            onClick={handleClearHistory}
            variant="ghost"
            size="sm"
            className="text-white hover:bg-white/20 hover:text-white"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Clear History
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="h-[calc(100vh-12rem)] overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your database..."
            className="flex-1"
          />
          <Button
            onClick={handleVisualize}
            variant="outline"
            className="border-purple-600 text-purple-600 hover:bg-purple-50"
          >
            <BarChart3 className="w-4 h-4" />
            Visualise
          </Button>
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim()}
            className="bg-blue-600 hover:bg-blue-700"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-xs text-gray-500 mt-2">Press Enter to send</p>
      </div>
    </div>
  );
};

export default ChatInterface;
