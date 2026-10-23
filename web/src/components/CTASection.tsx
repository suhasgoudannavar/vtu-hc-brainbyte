import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Terminal, Github, ShieldCheck } from 'lucide-react';

interface CTASectionProps {
  onOpenSimulator: () => void;
}

export const CTASection: React.FC<CTASectionProps> = ({ onOpenSimulator }) => {
  return (
    <section className="py-28 px-6 sm:px-12 md:px-16 bg-background relative overflow-hidden text-center circuit-grid border-t border-border">
      {/* Ambient Radial Highlights */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] bg-accent/5 rounded-full blur-3xl pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
        className="relative z-10 max-w-4xl mx-auto flex flex-col items-center"
      >
        <span className="font-mono text-xs uppercase tracking-widest text-accent mb-3 block">
          05 / REAL-TIME DEPLOYMENT
        </span>

        <h2 className="font-display uppercase text-white tracking-[0.04em] text-[60px] sm:text-[84px] md:text-[112px] leading-[0.88] max-w-3xl">
          EXPERIENCE QUANTUM-POWERED DISPATCH
        </h2>

        <p className="font-sans font-light text-muted text-base sm:text-lg max-w-xl mt-6 leading-relaxed">
          Test real-time combinatorial optimization with your own incident coordinates, road congestion multipliers, and fleet constraints. 100% free and open-source.
        </p>

        {/* Action Buttons */}
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <button
            onClick={onOpenSimulator}
            className="flex items-center gap-3 bg-white hover:bg-neutral-200 text-black font-sans font-semibold text-sm px-7 py-4 rounded transition-all shadow-[0_0_30px_rgba(255,255,255,0.25)] hover:shadow-[0_0_35px_rgba(245,166,35,0.45)] cursor-pointer active:scale-95"
          >
            <span>Launch Interactive Simulator</span>
            <ArrowRight className="w-4 h-4 text-black" />
          </button>

          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-2.5 bg-surface hover:bg-surface-raised border border-border hover:border-subtle text-foreground text-sm font-sans font-medium px-6 py-4 rounded transition-all"
          >
            <Github className="w-4 h-4" />
            <span>GitHub Repository</span>
          </a>
        </div>

        {/* Local Command Runner Box */}
        <div className="mt-10 inline-flex items-center gap-3 px-4 py-2.5 rounded-lg bg-surface border border-border font-mono text-xs text-muted">
          <Terminal className="w-4 h-4 text-accent shrink-0" />
          <span>Local launch:</span>
          <code className="text-white bg-black/60 px-2 py-0.5 rounded border border-border/80">
            streamlit run app.py
          </code>
        </div>

        {/* Footnote */}
        <div className="mt-8 font-mono text-[11px] text-muted flex items-center gap-2">
          <ShieldCheck className="w-3.5 h-3.5 text-accent" />
          <span>Designed for Emergency Operations Centers & Quantum Researchers · Open-Source (MIT)</span>
        </div>
      </motion.div>
    </section>
  );
};
