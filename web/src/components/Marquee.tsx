import React from 'react';
import { MARQUEE_ITEMS } from '../data/mockData';

export const Marquee: React.FC = () => {
  return (
    <div className="w-full h-11 bg-surface border-y border-border overflow-hidden flex items-center relative select-none">
      {/* Side Fade Gradients */}
      <div className="absolute left-0 top-0 bottom-0 w-16 bg-gradient-to-r from-background to-transparent z-10 pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-16 bg-gradient-to-l from-background to-transparent z-10 pointer-events-none" />

      {/* Scrolling Track */}
      <div className="flex whitespace-nowrap animate-marquee">
        {/* First repetition */}
        <div className="flex items-center gap-12 pr-12">
          {MARQUEE_ITEMS.map((item, idx) => (
            <span key={idx} className="flex items-center gap-4 font-mono text-[11px] text-white/40 uppercase tracking-widest hover:text-white transition-colors">
              <span>{item}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-accent inline-block" />
            </span>
          ))}
        </div>

        {/* Second repetition for infinite seamless scroll */}
        <div className="flex items-center gap-12 pr-12">
          {MARQUEE_ITEMS.map((item, idx) => (
            <span key={`repeat-${idx}`} className="flex items-center gap-4 font-mono text-[11px] text-white/40 uppercase tracking-widest hover:text-white transition-colors">
              <span>{item}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-accent inline-block" />
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};
