
import { Bot } from "lucide-react";

const TypingIndicator = () => {
  return (
    <div className="flex gap-3 animate-fade-in">
      <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
        <Bot className="w-5 h-5 text-blue-500" />
      </div>
      
      <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm mr-12">
        <div className="flex items-center gap-1">
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <span className="text-sm text-gray-500 ml-2">Assistant is thinking...</span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
