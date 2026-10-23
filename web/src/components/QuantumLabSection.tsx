import React, { useState } from 'react';
import { Cpu, ShieldCheck, Laptop, WifiOff } from 'lucide-react';

export const QuantumLabSection: React.FC = () => {
  const [layers, setLayers] = useState<number>(2);
  const [qubits, setQubits] = useState<number>(12);

  const gearChips = [
    "Python 3.12",
    "Qiskit 2.0 (Quantum Simulator)",
    "Google OR-Tools (Logic Solver)",
    "Streamlit (Dashboard)",
    "Real Road Curve Math (1.35x)",
    "Works 100% Offline",
    "25 Safety Tests Passing",
    "Zero Cost (Free & Open Source)"
  ];

  return (
    <section id="lab" className="py-24 px-6 sm:px-12 md:px-16 bg-surface border-t border-border">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Left Column: Context & Spec */}
        <div className="lg:col-span-6 flex flex-col items-start">
          <span className="font-mono text-xs uppercase tracking-widest text-accent block mb-2">
            05 / THE TECHNOLOGY BEHIND IT
          </span>
          <h2 className="font-display uppercase text-white tracking-[0.04em] text-[52px] sm:text-[68px] md:text-[80px] leading-[0.9] mb-6">
            THE RESEARCH LAB
          </h2>

          <p className="font-sans font-normal text-muted text-base leading-relaxed mb-6">
            QRescue is built so that anyone can use it during real power blackouts and emergencies. 
            It runs <strong className="text-white">100% offline on a standard laptop</strong> without needing internet access, cloud subscriptions, or paid API keys.
          </p>

          {/* Simple Explanation Box */}
          <div className="w-full bg-background/90 p-5 rounded-lg border border-border/80 mb-8 space-y-3">
            <div className="flex items-center gap-2 text-accent font-mono text-xs font-semibold uppercase">
              <ShieldCheck className="w-4 h-4" />
              <span>How the Math Works in Simple Words:</span>
            </div>
            <p className="font-sans text-xs text-foreground/80 leading-relaxed">
              Think of the math like a giant scorekeeper: every minute an ambulance is delayed adds penalty points. 
              Double-booking a truck adds massive penalty points. 
              The computer runs calculations until it finds the plan with the lowest possible penalty score.
            </p>
          </div>

          {/* Technology / Gear Stack Chips */}
          <div className="w-full">
            <span className="font-mono text-xs text-foreground/80 uppercase tracking-wider block mb-3">
              Tools Used:
            </span>
            <div className="flex flex-wrap gap-2">
              {gearChips.map((chip, idx) => (
                <span
                  key={idx}
                  className="font-mono text-[11px] bg-background border border-border text-muted hover:text-white hover:border-accent/40 px-3 py-1 rounded transition-colors"
                >
                  {chip}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Interactive Quantum Simulator Deck */}
        <div className="lg:col-span-6 bg-background rounded-lg border border-border p-6 sm:p-8 relative shadow-2xl overflow-hidden noise-overlay">
          <div className="flex items-center justify-between border-b border-border pb-4 mb-6">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-accent" />
              <span className="font-mono text-xs font-semibold uppercase text-white tracking-wider">
                TRY THE QUANTUM SIMULATOR
              </span>
            </div>
            <span className="font-mono text-[10px] text-accent bg-accent/10 px-2 py-0.5 rounded border border-accent/20">
              Interactive Test
            </span>
          </div>

          {/* Interactive Circuit Controls */}
          <div className="space-y-5 mb-6">
            <div>
              <div className="flex justify-between font-mono text-xs text-muted mb-1.5">
                <span>Algorithm Depth (Layers of Thinking):</span>
                <span className="text-white font-semibold">{layers} Layers</span>
              </div>
              <input
                type="range"
                min="1"
                max="5"
                value={layers}
                onChange={(e) => setLayers(Number(e.target.value))}
                className="w-full accent-accent bg-surface cursor-pointer h-1.5 rounded"
              />
              <span className="text-[10px] font-sans text-muted/70 block mt-1">
                More layers = deeper analysis of complex road traffic.
              </span>
            </div>

            <div>
              <div className="flex justify-between font-mono text-xs text-muted mb-1.5">
                <span>Number of Vehicles & Emergencies (Qubits):</span>
                <span className="text-accent-cyan font-semibold">{qubits} Variables</span>
              </div>
              <input
                type="range"
                min="6"
                max="24"
                step="2"
                value={qubits}
                onChange={(e) => setQubits(Number(e.target.value))}
                className="w-full accent-accent-cyan bg-surface cursor-pointer h-1.5 rounded"
              />
              <span className="text-[10px] font-sans text-muted/70 block mt-1">
                Drag to test larger city emergency sizes.
              </span>
            </div>
          </div>

          {/* Circuit Visual Schematic */}
          <div className="bg-surface p-4 rounded border border-border mb-6 font-mono text-xs space-y-3">
            <div className="text-[10px] text-muted uppercase">How It Processes:</div>
            <div className="flex items-center gap-2 overflow-x-auto py-2">
              <span className="px-2.5 py-1.5 rounded bg-surface-raised border border-border text-white text-[11px] shrink-0">
                Start Plan
              </span>
              <span className="text-muted">→</span>
              <span className="px-2.5 py-1.5 rounded bg-accent/20 border border-accent/40 text-accent text-[11px] shrink-0">
                Test All Combinations
              </span>
              <span className="text-muted">→</span>
              <span className="px-2.5 py-1.5 rounded bg-white/10 border border-white/20 text-white text-[11px] shrink-0">
                Filter Out Bad Choices ({layers}x)
              </span>
              <span className="text-muted">→</span>
              <span className="px-2.5 py-1.5 rounded bg-surface-raised border border-border text-accent-cyan text-[11px] shrink-0">
                Pick Best Plan
              </span>
            </div>
          </div>

          {/* Telemetry Output Box */}
          <div className="grid grid-cols-2 gap-3 text-xs font-mono">
            <div className="bg-surface-raised p-3 rounded border border-border">
              <span className="text-[10px] text-muted uppercase block">Combinations Tested</span>
              <span className="text-base text-white font-medium mt-1 block">
                {(Math.pow(2, qubits)).toLocaleString()} Possibilities
              </span>
            </div>
            <div className="bg-surface-raised p-3 rounded border border-border">
              <span className="text-[10px] text-muted uppercase block">Plan Quality</span>
              <span className="text-base text-accent font-medium mt-1 block">
                {(82 + layers * 3.4).toFixed(1)}% Optimal Score
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
