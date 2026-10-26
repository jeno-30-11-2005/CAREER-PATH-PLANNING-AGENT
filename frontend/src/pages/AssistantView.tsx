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
    <div className="bg-[#14141D] border border-white/5 rounded-3xl flex flex-col h-[750px] overflow-hidden shadow-2xl">
      {/* Assistant Header */}
      <div className="p-5 border-b border-white/5 bg-[#12121A] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#9D4EDD] to-[#C77DFF] flex items-center justify-center shadow-glow-violet">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-white">Career Intelligence Assistant</h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-950/40 border border-emerald-500/30 text-emerald-400">
                Online
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Grounded in verified curriculum data • Deterministic offline fallback enabled
            </p>
          </div>
        </div>
      </div>

      {/* Suggested Prompt Chips */}
      <div className="p-3 bg-[#0B0B0E] border-b border-white/5 flex items-center gap-2 overflow-x-auto">
        <span className="text-[10px] uppercase font-bold text-slate-400 shrink-0 px-2">
          Suggested:
        </span>
        {samplePrompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSend(prompt)}
            className="text-xs px-3 py-1 rounded-full bg-[#181824] hover:bg-white/10 text-slate-300 hover:text-white border border-white/5 shrink-0 transition-all"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${
              msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-xs shrink-0 ${
                msg.role === 'user'
                  ? 'bg-gradient-to-tr from-[#9D4EDD] to-[#E0AAFF] text-white font-bold'
                  : 'bg-[#1C1C28] border border-purple-500/30 text-[#C77DFF]'
              }`}
            >
              {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div
              className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-purple-900/40 border border-purple-500/30 text-white rounded-tr-none'
                  : 'bg-[#161622] border border-white/5 text-slate-200 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>

              {msg.role === 'assistant' && (
                <div className="mt-3 pt-2.5 border-t border-white/5 flex items-center justify-between text-[10px] text-slate-400">
                  <div className="flex items-center gap-1.5">
                    <ShieldCheck className="w-3 h-3 text-[#C77DFF]" />
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
            <div className="w-8 h-8 rounded-full bg-[#1C1C28] border border-purple-500/30 text-[#C77DFF] flex items-center justify-center">
              <Bot className="w-4 h-4 animate-spin-slow" />
            </div>
            <div className="bg-[#161622] border border-white/5 rounded-2xl p-4 text-xs text-slate-400 rounded-tl-none flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-[#C77DFF] animate-pulse" />
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
        className="p-4 bg-[#12121A] border-t border-white/5 flex items-center gap-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about careers, skills, projects, or viva preparation..."
          className="flex-1 bg-[#1A1A26] border border-white/10 rounded-2xl px-5 py-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="neon-btn w-11 h-11 rounded-2xl flex items-center justify-center disabled:opacity-40"
        >
          <Send className="w-4 h-4 text-white" />
        </button>
      </form>
    </div>
  );
};
