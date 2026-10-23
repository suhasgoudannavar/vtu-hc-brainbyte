import React from 'react';
import { motion } from 'framer-motion';
import { Database, GitFork, CheckCheck, FileText, ArrowRight } from 'lucide-react';

export const ArchitectureSection: React.FC = () => {
  const steps = [
    {
      num: "01",
      icon: Database,
      title: "1. Gather Emergency Calls",
      subtitle: "Who Needs Help & Where",
      desc: "Collects 911 disaster calls, maps where people are trapped, and scores who is in the greatest immediate danger.",
      badge: "Real-Time Mapping"
    },
    {
      num: "02",
      icon: GitFork,
      title: "2. Smart Computer Thinking",
      subtitle: "Calculates Best Routes",
      desc: "Our algorithms test millions of truck assignments in a fraction of a second to find the fastest combination.",
      badge: "Classical & Quantum"
    },
    {
      num: "03",
      icon: CheckCheck,
      title: "3. Safety Double-Check",
      subtitle: "Eliminates Human Errors",
      desc: "Automatically verifies that no ambulance is double-booked and every truck has the exact tools needed.",
      badge: "Zero Mistakes"
    },
    {
      num: "04",
      icon: FileText,
      title: "4. Clear Orders to Rescuers",
      subtitle: "Real-Time Map & Routes",
      desc: "Gives rescue drivers exact turn-by-turn routes with estimated arrival times, cutting wait times by up to 42%.",
      badge: "Faster Arrival"
    }
  ];

  return (
    <section id="architecture" className="py-24 px-6 sm:px-12 md:px-16 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
        <div>
          <span className="font-mono text-xs uppercase tracking-widest text-accent block mb-2">
            04 / SIMPLE 4-STEP PROCESS
          </span>
          <h2 className="font-display uppercase text-white tracking-[0.04em] text-[52px] sm:text-[68px] md:text-[80px] leading-[0.9]">
            HOW QRESCUE WORKS
          </h2>
        </div>
        <p className="font-sans font-normal text-muted text-sm sm:text-base max-w-md">
          From the moment disaster strikes to the second rescue vehicles arrive on the scene.
        </p>
      </div>

      {/* 4-Step Pipeline Flow */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.45, delay: idx * 0.1 }}
              className="bg-surface border border-border hover:border-subtle rounded-lg p-6 flex flex-col justify-between relative group"
            >
              <div>
                {/* Step Number & Badge */}
                <div className="flex items-center justify-between mb-6">
                  <span className="font-mono text-2xl text-white/30 group-hover:text-accent transition-colors font-bold">
                    {step.num}
                  </span>
                  <span className="font-mono text-[9px] uppercase tracking-wider text-accent bg-accent/10 px-2 py-0.5 rounded border border-accent/20">
                    {step.badge}
                  </span>
                </div>

                {/* Icon & Title */}
                <div className="w-10 h-10 rounded bg-surface-raised border border-border flex items-center justify-center text-white mb-4 group-hover:border-accent/40 transition-colors">
                  <Icon className="w-5 h-5 text-accent" />
                </div>

                <h3 className="font-sans font-semibold text-white text-lg">
                  {step.title}
                </h3>
                <span className="font-mono text-xs text-muted block mt-0.5 mb-3">
                  {step.subtitle}
                </span>

                <p className="font-sans text-xs text-muted leading-relaxed">
                  {step.desc}
                </p>
              </div>

              {/* Step indicator arrow for desktop */}
              {idx < steps.length - 1 && (
                <div className="hidden lg:block absolute -right-3 top-1/2 -translate-y-1/2 z-20 text-border group-hover:text-accent transition-colors">
                  <ArrowRight className="w-5 h-5" />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </section>
  );
};
