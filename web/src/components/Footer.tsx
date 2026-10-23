import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-[#080808] border-t border-border pt-16 pb-10 px-6 sm:px-12 md:px-16 text-muted">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 pb-12 border-b border-border/80">
          {/* Brand Info */}
          <div>
            <div className="flex items-center gap-2.5 mb-2">
              <div className="w-6 h-6 rounded bg-surface border border-border flex items-center justify-center text-accent">
                <ShieldAlert className="w-3.5 h-3.5" />
              </div>
              <span className="font-display text-2xl text-white tracking-wider">QRESCUE</span>
            </div>
            <p className="font-sans text-xs text-muted max-w-sm">
              AI-Powered Disaster Response Optimization using Google OR-Tools CP-SAT and Qiskit QAOA.
            </p>
          </div>

          {/* Quick Nav & Links */}
          <div className="flex flex-wrap items-center gap-8 font-sans text-xs">
            <a href="#scenarios" className="hover:text-white transition-colors">Scenarios</a>
            <a href="#solvers" className="hover:text-white transition-colors">Solvers</a>
            <a href="#benchmarks" className="hover:text-white transition-colors">Benchmarks</a>
            <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
            <a href="#lab" className="hover:text-white transition-colors">Research Lab</a>
          </div>

          {/* Status Badges */}
          <div className="flex items-center gap-3 font-mono text-[11px]">
            <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-surface border border-border text-foreground">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              25 Tests Passing
            </span>
            <span className="px-2.5 py-1 rounded bg-surface border border-border text-accent">
              MIT License
            </span>
          </div>
        </div>

        {/* Bottom Credits & Legal */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-[10px] text-muted/70">
          <span>
            © {new Date().getFullYear()} QRescue Project · Scientific Simulation & Operational Research Platform.
          </span>
          <span className="flex items-center gap-4">
            <span>100% Free & Open Source</span>
            <span>·</span>
            <span>Zero Paid APIs</span>
            <span>·</span>
            <span>Deterministic Auditing</span>
          </span>
        </div>
      </div>
    </footer>
  );
};
