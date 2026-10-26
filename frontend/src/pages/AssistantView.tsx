import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, Sparkles, Bot, User, ShieldCheck, HelpCircle } from 'lucide-react';
import { api } from '../services/api';
import { StudentProfile } from '../types';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  isFallback?: boolean;
  sources?: string[];
  timestamp: string;
}

interface AssistantViewProps {
  student: StudentProfile | null;
  selectedRoleSlug?: string;
  initialQuery?: string;
}

export const AssistantView: React.FC<AssistantViewProps> = ({
  student,
  selectedRoleSlug,
  initialQuery
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content:
        `Hello ${student?.name || 'Student'}! I am your Intelligent Career Path Planning Assistant. ` +
        `I am grounded in our career knowledge base and verified AI/Data Science curricula. ` +
        `Ask me anything about role skills, projects, study roadmaps, or viva interview preparation!`,
      isFallback: false,
      sources: ['Knowledge Base Engine', 'Curriculum Standards'],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
    }
  }, [initialQuery]);

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || input;
    if (!text.trim() || isLoading) return;

    const userMsg: Message = {
      role: 'user',
      content: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await api.chatWithAssistant(
        text.trim(),
        student?.id,
        selectedRoleSlug
      );

      const assistantMsg: Message = {
        role: 'assistant',
        content: res.content,
        isFallback: res.is_fallback,
        sources: res.sources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: Message = {
        role: 'assistant',
        content: `I encountered a communication issue: ${err.message}. Please try again or check the deterministic knowledge base.`,
        isFallback: true,
        sources: ['Offline Error Handler'],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const samplePrompts = [
    'What portfolio projects should I build for an AI Engineer?',
    'What is the difference between Data Science and MLOps?',
    'What are the core skills I should learn first?',
    'How should I explain my agentic career project in my viva?'
  ];

  return (
    <div className="rubick-card flex flex-col h-[750px] overflow-hidden shadow-rubick-md">
      {/* Assistant Header */}
      <div className="p-5 border-b border-slate-200 bg-white flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-[#1b3bbb]">
            <Bot className="w-5 h-5 text-[#1b3bbb]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-slate-900">Career Intelligence Assistant</h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700">
                Active Grounding
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              Verified curriculum data • 100% deterministic offline fallback enabled
            </p>
          </div>
        </div>
      </div>

      {/* Suggested Prompt Chips */}
      <div className="p-3 bg-slate-50 border-b border-slate-200 flex items-center gap-2 overflow-x-auto">
        <span className="text-[10px] uppercase font-bold text-slate-500 shrink-0 px-2">
          Suggested:
        </span>
        {samplePrompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSend(prompt)}
            className="text-xs px-3 py-1 rounded-lg bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 shrink-0 transition-all font-medium shadow-sm"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-50/40">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${
              msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-xs shrink-0 shadow-sm ${
                msg.role === 'user'
                  ? 'bg-[#1b3bbb] text-white font-bold'
                  : 'bg-white border border-slate-200 text-[#1b3bbb]'
              }`}
            >
              {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div
              className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed shadow-sm ${
                msg.role === 'user'
                  ? 'bg-[#1b3bbb] text-white rounded-tr-none'
                  : 'bg-white border border-slate-200 text-slate-800 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>

              {msg.role === 'assistant' && (
                <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400">
                  <div className="flex items-center gap-1.5 font-medium">
                    <ShieldCheck className="w-3.5 h-3.5 text-[#1b3bbb]" />
                    <span>
                      {msg.isFallback
                        ? 'Deterministic Knowledge Base Engine'
                        : 'Google Gemini 1.5 Flash Grounded'}
                    </span>
                  </div>
                  <span>{msg.timestamp}</span>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-white border border-slate-200 text-[#1b3bbb] flex items-center justify-center shadow-sm">
              <Bot className="w-4 h-4 animate-spin-slow" />
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl p-4 text-xs text-slate-500 rounded-tl-none flex items-center gap-2 shadow-sm">
              <Sparkles className="w-3.5 h-3.5 text-[#1b3bbb] animate-pulse" />
              <span>Analyzing curriculum knowledge base...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Box Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-4 bg-white border-t border-slate-200 flex items-center gap-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about careers, skills, projects, or viva preparation..."
          className="flex-1 bg-slate-50 border border-slate-300 rounded-xl px-5 py-3 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-[#1b3bbb] focus:bg-white transition-all shadow-inner"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="rubick-btn w-11 h-11 rounded-xl flex items-center justify-center disabled:opacity-40 shrink-0"
        >
          <Send className="w-4 h-4 text-white" />
        </button>
      </form>
    </div>
  );
};
