import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Users, Clock, AlertTriangle, ArrowUpRight } from 'lucide-react';
import { SCENARIOS, type ScenarioData } from '../data/mockData';

interface ScenariosSectionProps {
  onSelectScenario: (scenario: ScenarioData) => void;
}

export const ScenariosSection: React.FC<ScenariosSectionProps> = ({ onSelectScenario }) => {
  return (
    <section id="scenarios" className="py-24 px-6 sm:px-12 md:px-16 max-w-7xl mx-auto">
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-14 gap-6">
        <div>
          <span className="font-mono text-xs uppercase tracking-widest text-accent block mb-2">
            01 / REAL-WORLD CRISIS TESTS
          </span>
          <h2 className="font-display uppercase text-white tracking-[0.04em] text-[52px] sm:text-[68px] md:text-[80px] leading-[0.9]">
            DISASTER SCENARIOS
          </h2>
        </div>
        <p className="font-sans font-normal text-muted text-sm sm:text-base max-w-md">
          Six real disaster simulations testing what happens when multiple emergencies call for help at the same time.
        </p>
      </div>

      {/* 3-Column Card Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {SCENARIOS.map((scenario, index) => (
          <motion.div
            key={scenario.id}
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-50px' }}
            transition={{ duration: 0.5, delay: index * 0.08 }}
            className="group bg-surface hover:bg-surface-raised border border-border hover:border-accent/40 rounded-lg overflow-hidden transition-all duration-300 flex flex-col justify-between"
          >
            {/* Top Interactive Radar Area with Hover Trigger */}
            <div
              onClick={() => onSelectScenario(scenario)}
              className="relative aspect-video sm:aspect-square bg-gradient-to-b from-surface-raised to-background p-6 flex flex-col justify-between overflow-hidden cursor-pointer select-none border-b border-border/80"
            >
              {/* Radar Grid Graphic */}
              <div className="absolute inset-0 circuit-grid opacity-30 group-hover:opacity-50 transition-opacity" />

              {/* Top Bar inside Card */}
              <div className="relative z-10 flex items-center justify-between">
                <span className="font-mono text-[10px] text-accent bg-accent/10 border border-accent/20 px-2 py-0.5 rounded uppercase">
                  {scenario.tag}
                </span>
                <span className="font-mono text-[11px] text-muted flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3 text-accent" />
                  Danger Level: {scenario.urgencyScore}%
                </span>
              </div>

              {/* Animated Radar Center Graphic */}
              <div className="relative z-10 my-auto flex items-center justify-center">
                <div className="relative w-32 h-32 flex items-center justify-center">
                  <div className="absolute inset-0 rounded-full border border-border/60 group-hover:border-accent/30 transition-colors" />
                  <div className="absolute inset-4 rounded-full border border-border/40" />
                  <div className="absolute inset-10 rounded-full border border-border/20" />
                  <div className="w-3 h-3 rounded-full bg-accent animate-ping" />
                  <div className="w-2.5 h-2.5 rounded-full bg-accent" />

                  {/* Satellite Points */}
                  <div className="absolute top-4 left-6 w-1.5 h-1.5 rounded-full bg-white/70" />
                  <div className="absolute bottom-6 right-8 w-1.5 h-1.5 rounded-full bg-accent-cyan" />
                </div>
              </div>

              {/* Bottom Quick Stats inside Radar Card */}
              <div className="relative z-10 flex items-center justify-between text-[11px] font-mono text-muted">
                <span className="flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-white/60" />
                  {scenario.casualties} People In Danger
                </span>
                <span className="flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-accent" />
                  Goal: &lt; {scenario.targetResponseTime}
                </span>
              </div>

              {/* Hover Center Play Trigger */}
              <div className="absolute inset-0 bg-black/60 backdrop-blur-[2px] opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex flex-col items-center justify-center gap-3 z-20">
                <div className="w-14 h-14 rounded-full bg-white text-black flex items-center justify-center shadow-[0_0_25px_rgba(255,255,255,0.4)] group-hover:scale-105 transition-transform">
                  <Activity className="w-6 h-6 text-black" />
                </div>
                <span className="font-mono text-xs uppercase tracking-wider text-white font-medium">
                  Test Rescue Plan →
                </span>
              </div>
            </div>

            {/* Bottom Metadata & Simple Explanation */}
            <div className="p-5 flex flex-col justify-between flex-grow">
              <div>
                <h3 className="font-sans font-semibold text-white text-base group-hover:text-accent transition-colors">
                  {scenario.name}
                </h3>
                <p className="font-sans text-xs text-muted mt-2 leading-relaxed">
                  {scenario.simpleExplanation}
                </p>
              </div>

              {/* Required Help Vehicles */}
              <div className="mt-4 pt-4 border-t border-border/60">
                <span className="text-[10px] font-mono text-muted/70 uppercase block mb-1.5">Vehicles Needed:</span>
                <div className="flex flex-wrap gap-1.5">
                  {scenario.requiredUnits.map((unit, uIdx) => (
                    <span
                      key={uIdx}
                      className="font-mono text-[9px] bg-background text-foreground/90 px-2 py-0.5 rounded border border-border/80"
                    >
                      {unit}
                    </span>
                  ))}
                </div>
              </div>

              {/* Action Link */}
              <button
                onClick={() => onSelectScenario(scenario)}
                className="mt-4 flex items-center justify-between text-xs font-mono text-foreground hover:text-accent transition-colors pt-1 cursor-pointer"
              >
                <span>Compare Simple vs Smart Dispatch</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};
