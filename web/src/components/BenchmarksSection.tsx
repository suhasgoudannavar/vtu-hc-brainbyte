import React from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, AlertOctagon, CheckCircle2 } from 'lucide-react';
import { BENCHMARK_METRICS } from '../data/mockData';

export const BenchmarksSection: React.FC = () => {
  return (
    <section id="benchmarks" className="py-24 px-6 sm:px-12 md:px-16 max-w-7xl mx-auto">
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
        <div>
          <span className="font-mono text-xs uppercase tracking-widest text-accent block mb-2">
            03 / THE PROOF IN NUMBERS
          </span>
          <h2 className="font-display uppercase text-white tracking-[0.04em] text-[52px] sm:text-[68px] md:text-[80px] leading-[0.9]">
            HEAD-TO-HEAD COMPARISON
          </h2>
        </div>
        <p className="font-sans font-normal text-muted text-sm sm:text-base max-w-md">
          See what happens when you compare normal guesswork (sending whatever is nearest) vs. QRescue's smart planning on the exact same disaster.
        </p>
      </div>

      {/* Audit Table Header */}
      <div className="hidden lg:grid grid-cols-12 gap-4 pb-3 border-b border-border/80 text-[11px] font-mono uppercase text-muted tracking-wider">
        <div className="col-span-3">Performance Test</div>
        <div className="col-span-3 text-red-400">Regular Guesswork (Greedy)</div>
        <div className="col-span-3 text-accent">QRescue Exact (CP-SAT)</div>
        <div className="col-span-3 text-accent-cyan">QRescue Quantum (QAOA)</div>
      </div>

      {/* Horizontal Table Rows */}
      <div className="divide-y divide-border">
        {BENCHMARK_METRICS.map((row, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: idx * 0.07 }}
            className="group py-5 px-3 rounded hover:bg-surface-raised transition-colors flex flex-col lg:grid lg:grid-cols-12 gap-3 lg:gap-4 items-start lg:items-center"
          >
            {/* Metric Name */}
            <div className="lg:col-span-3">
              <span className="font-sans font-semibold text-white text-base block group-hover:text-accent transition-colors">
                {row.metric}
              </span>
              <span className="font-mono text-[10px] text-muted uppercase">
                {row.category}
              </span>
            </div>

            {/* Greedy Baseline Result */}
            <div className="lg:col-span-3 flex items-center gap-2 font-mono text-xs text-red-300">
              <AlertOctagon className="w-3.5 h-3.5 text-red-400 shrink-0 lg:hidden" />
              <span>{row.greedy}</span>
            </div>

            {/* CP-SAT Result */}
            <div className="lg:col-span-3 flex items-center gap-2 font-mono text-xs text-foreground font-medium">
              <CheckCircle2 className="w-3.5 h-3.5 text-accent shrink-0 lg:hidden" />
              <span className="text-white group-hover:text-accent transition-colors">{row.cpsat}</span>
            </div>

            {/* QAOA Result */}
            <div className="lg:col-span-3 flex items-center gap-2 font-mono text-xs text-accent-cyan/90">
              <ShieldCheck className="w-3.5 h-3.5 text-accent-cyan shrink-0 lg:hidden" />
              <span>{row.qaoa}</span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Audit Footnote */}
      <div className="mt-8 p-4 rounded bg-surface border border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 font-mono text-xs text-muted">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-accent" />
          <span>Every result is tested and verified by 25 automated safety checks.</span>
        </div>
        <div className="text-accent text-[11px]">
          100% Reliable Every Single Run
        </div>
      </div>
    </section>
  );
};
