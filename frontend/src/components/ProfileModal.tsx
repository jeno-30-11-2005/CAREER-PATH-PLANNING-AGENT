import React, { useState, useEffect } from 'react';
import { X, Save, Sparkles, BookOpen, Clock, Target } from 'lucide-react';
import { StudentProfile } from '../types';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: StudentProfile | null;
  onSave: (saved: StudentProfile) => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({ isOpen, onClose, profile, onSave }) => {
  const [formData, setFormData] = useState<StudentProfile>({
    name: 'Nadia Rachel',
    education_level: 'Undergraduate',
    degree_specialization: 'BE Artificial Intelligence & Data Science',
    current_year_sem: '3rd Year, Semester 6',
    interests: ['Machine Learning', 'Deep Learning', 'Generative AI'],
    technical_skills: ['Python', 'SQL', 'Pandas', 'Scikit-Learn'],
    soft_skills: ['Problem Solving', 'Critical Thinking', 'Communication'],
    programming_experience: 'Intermediate',
    preferred_career_fields: ['Artificial Intelligence & Data Science'],
    weekly_learning_hours: 12,
    career_goals: 'Aspiring to become an AI Engineer building scalable intelligent agents.'
  });

  const [techInput, setTechInput] = useState('');
  const [interestInput, setInterestInput] = useState('');

  useEffect(() => {
    if (profile) {
      setFormData(profile);
      setTechInput(profile.technical_skills?.join(', ') || '');
      setInterestInput(profile.interests?.join(', ') || '');
    } else {
      setTechInput(formData.technical_skills.join(', '));
      setInterestInput(formData.interests.join(', '));
    }
  }, [profile]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const updated: StudentProfile = {
      ...formData,
      technical_skills: techInput.split(',').map((s) => s.trim()).filter(Boolean),
      interests: interestInput.split(',').map((s) => s.trim()).filter(Boolean),
      weekly_learning_hours: Number(formData.weekly_learning_hours) || 10
    };
    onSave(updated);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="bg-[#12121A] border border-white/10 rounded-3xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl p-6 sm:p-8">
        <div className="flex items-center justify-between pb-4 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#9D4EDD] to-[#C77DFF] flex items-center justify-center shadow-glow-violet">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Student Academic Profile</h2>
              <p className="text-xs text-slate-400">Configure your skills, interests & weekly availability</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-slate-400 hover:text-white transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Full Name</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Degree & Specialization</label>
              <input
                type="text"
                required
                value={formData.degree_specialization}
                onChange={(e) => setFormData({ ...formData, degree_specialization: e.target.value })}
                className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Current Year & Semester</label>
              <input
                type="text"
                required
                value={formData.current_year_sem}
                onChange={(e) => setFormData({ ...formData, current_year_sem: e.target.value })}
                className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Programming Experience</label>
              <select
                value={formData.programming_experience}
                onChange={(e) => setFormData({ ...formData, programming_experience: e.target.value })}
                className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
              >
                <option value="Beginner">Beginner (1st/2nd Year)</option>
                <option value="Intermediate">Intermediate (Hands-on)</option>
                <option value="Advanced">Advanced (Projects Built)</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Weekly Study Hours</label>
              <div className="relative">
                <Clock className="w-3.5 h-3.5 text-slate-500 absolute left-3.5 top-3" />
                <input
                  type="number"
                  min="1"
                  max="60"
                  required
                  value={formData.weekly_learning_hours}
                  onChange={(e) => setFormData({ ...formData, weekly_learning_hours: parseInt(e.target.value) || 10 })}
                  className="w-full bg-[#1A1A24] border border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">
              Technical Skills <span className="text-slate-500 font-normal">(comma-separated)</span>
            </label>
            <input
              type="text"
              value={techInput}
              onChange={(e) => setTechInput(e.target.value)}
              placeholder="Python, SQL, Pandas, Scikit-Learn, Git"
              className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">
              Areas of Interest <span className="text-slate-500 font-normal">(comma-separated)</span>
            </label>
            <input
              type="text"
              value={interestInput}
              onChange={(e) => setInterestInput(e.target.value)}
              placeholder="Machine Learning, Computer Vision, Cloud Infrastructure, APIs"
              className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:border-purple-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Career Aspirations & Goals</label>
            <textarea
              rows={2}
              value={formData.career_goals || ''}
              onChange={(e) => setFormData({ ...formData, career_goals: e.target.value })}
              placeholder="What are your goals after graduation?"
              className="w-full bg-[#1A1A24] border border-white/10 rounded-xl px-4 py-2 text-xs text-white focus:border-purple-500 focus:outline-none resize-none"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-white/5">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2.5 rounded-full text-xs font-semibold text-slate-400 hover:text-white hover:bg-white/5 transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="neon-btn px-6 py-2.5 rounded-full text-xs font-semibold flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              <span>Save & Update Profile</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
