import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { X, Play, RefreshCw, CheckCircle2, Zap, Activity } from 'lucide-react';
import { SCENARIOS, type ScenarioData } from '../data/mockData';

interface DispatchSimulatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialScenario?: ScenarioData | null;
}

export const DispatchSimulatorModal: React.FC<DispatchSimulatorModalProps> = ({
  isOpen,
  onClose,
  initialScenario
}) => {
  const [selectedScenario, setSelectedScenario] = useState<ScenarioData>(
    initialScenario || SCENARIOS[0]
  );
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [simStep, setSimStep] = useState<number>(0);

  useEffect(() => {
    if (initialScenario) {
      setSelectedScenario(initialScenario);
    }
  }, [initialScenario]);

  const runSimulation = () => {
    setIsSimulating(true);
    setSimStep(1);

    setTimeout(() => setSimStep(2), 600);
    setTimeout(() => setSimStep(3), 1300);
    setTimeout(() => {
      setSimStep(4);
      setIsSimulating(false);
    }, 1900);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-md">
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 15 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 15 }}
        className="w-full max-w-4xl bg-surface border border-border rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]"
      >
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-border flex items-center justify-between bg-surface-raised">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-accent/10 border border-accent/20 flex items-center justify-center text-accent">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-display text-xl text-white tracking-wide">
                TEST RESCUE DISPATCH IN REAL TIME
              </h3>
              <span className="font-mono text-[10px] text-muted">
                Compare Simple Guesswork vs QRescue's Smart Math
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded text-muted hover:text-white hover:bg-surface border border-transparent hover:border-border transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Scenario Selector Tabs */}
          <div>
            <label className="font-mono text-xs uppercase text-muted tracking-wider block mb-2.5">
              Select an Emergency to Test:
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {SCENARIOS.map((sc) => (
                <button
                  key={sc.id}
                  onClick={() => {
                    setSelectedScenario(sc);
                    setSimStep(0);
                  }}
                  className={`text-left p-3 rounded border text-xs transition-all cursor-pointer ${
                    selectedScenario.id === sc.id
                      ? 'bg-surface-raised border-accent text-white shadow-sm'
                      : 'bg-background border-border text-muted hover:text-white hover:border-subtle'
                  }`}
                >
                  <span className="font-mono text-[9px] uppercase tracking-wider text-accent block mb-1">
                    {sc.tag}
                  </span>
                  <span className="font-sans font-medium line-clamp-1 block">
                    {sc.name}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Simple Explanation of the Crisis */}
          <div className="bg-background/90 p-4 rounded-lg border border-border">
            <span className="font-mono text-[10px] text-accent uppercase tracking-wider block mb-1">
              What Is Happening:
            </span>
            <p className="font-sans text-xs text-foreground/90 leading-relaxed">
              {selectedScenario.simpleExplanation}
            </p>
          </div>

          {/* Scenario Overview Box */}
          <div className="bg-background p-4 rounded-lg border border-border grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <span className="font-mono text-[10px] text-muted uppercase block">People in Danger</span>
              <span className="font-display text-2xl text-white">{selectedScenario.casualties} Trapped</span>
            </div>
            <div>
              <span className="font-mono text-[10px] text-muted uppercase block">Emergency Locations</span>
              <span className="font-display text-2xl text-accent">{selectedScenario.criticalZones} Hotspots</span>
            </div>
            <div>
              <span className="font-mono text-[10px] text-muted uppercase block">Goal Arrival Time</span>
              <span className="font-display text-2xl text-accent-cyan">&lt; {selectedScenario.targetResponseTime}</span>
            </div>
          </div>

          {/* Solver Comparison Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Greedy Card */}
            <div className="bg-surface-raised p-4 rounded border border-border flex flex-col justify-between">
              <div>
                <span className="font-mono text-[10px] text-red-400 uppercase tracking-wider block mb-1">
                  1. Blind Guesswork (Old Way)
                </span>
                <h4 className="font-sans font-semibold text-white text-sm">
                  Send Whatever Is Nearest
                </h4>
                <div className="mt-3 space-y-2 text-xs font-mono">
                  <div className="flex justify-between text-muted">
                    <span>Average Wait:</span>
                    <span className="text-white">{selectedScenario.greedyResult.time}</span>
                  </div>
                  <div className="flex justify-between text-muted">
                    <span>Double-Bookings:</span>
                    <span className="text-red-400 font-semibold">{selectedScenario.greedyResult.conflicts} Trucks Conflicted</span>
                  </div>
                  <div className="flex justify-between text-muted">
                    <span>People Left With Zero Help:</span>
                    <span className="text-red-400 font-semibold">{selectedScenario.greedyResult.unserved} Forgotten</span>
                  </div>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 text-[10px] font-mono text-red-400/80">
                ⚠️ Causes traffic jams & leaves victims stranded
              </div>
            </div>

            {/* CP-SAT Card */}
            <div className="bg-surface-raised p-4 rounded border border-accent/40 flex flex-col justify-between relative shadow-lg">
              <div className="absolute -top-2 right-3 font-mono text-[9px] uppercase tracking-wider bg-accent text-black font-bold px-2 py-0.5 rounded">
                Recommended
              </div>
              <div>
                <span className="font-mono text-[10px] text-accent uppercase tracking-wider block mb-1">
                  2. QRescue Master Planner
                </span>
                <h4 className="font-sans font-semibold text-white text-sm">
                  Google OR-Tools CP-SAT
                </h4>
                <div className="mt-3 space-y-2 text-xs font-mono">
                  <div className="flex justify-between text-muted">
                    <span>Average Wait:</span>
                    <span className="text-accent font-semibold">{selectedScenario.cpsatResult.time}</span>
                  </div>
                  <div className="flex justify-between text-muted">
                    <span>Time Saved:</span>
                    <span className="text-white font-semibold">{selectedScenario.cpsatResult.savings}</span>
                  </div>
                  <div className="flex justify-between text-muted">
                    <span>Double-Bookings:</span>
                    <span className="text-accent font-semibold">0 (Zero Conflicts)</span>
                  </div>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 text-[10px] font-mono text-accent flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>100% of Victims Receive Help</span>
              </div>
            </div>

            {/* QAOA Quantum Card */}
            <div className="bg-surface-raised p-4 rounded border border-border flex flex-col justify-between">
              <div>
                <span className="font-mono text-[10px] text-accent-cyan uppercase tracking-wider block mb-1">
                  3. Quantum Simulation
                </span>
                <h4 className="font-sans font-semibold text-white text-sm">
                  Qiskit Quantum Solver
                </h4>
                <div className="mt-3 space-y-2 text-xs font-mono">
                  <div className="flex justify-between text-muted">
                    <span>Average Wait:</span>
                    <span className="text-accent-cyan font-semibold">{selectedScenario.qaoaResult.time}</span>
                  </div>
                  <div className="flex justify-between text-muted">
                    <span>Variables Handled:</span>
                    <span className="text-white">{selectedScenario.qaoaResult.qubits} Variables</span>
                  </div>
                  <div className="flex justify-between text-muted">
                    <span>Double-Bookings:</span>
                    <span className="text-white">0 Conflicts</span>
                  </div>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 text-[10px] font-mono text-accent-cyan flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5" />
                <span>Future-Proof Quantum Math</span>
              </div>
            </div>
          </div>

          {/* Simple Step-by-Step Execution Stream */}
          <div className="bg-black/90 p-4 rounded border border-border font-mono text-xs text-muted space-y-1.5">
            <div className="flex items-center justify-between text-[10px] text-muted/60 mb-1 border-b border-border/60 pb-1">
              <span>LIVE COMPUTER THINKING LOG</span>
              <span>STATUS: {isSimulating ? 'SOLVING...' : simStep === 4 ? 'DISPATCH ORDERS READY!' : 'READY TO RUN'}</span>
            </div>
            <div className={simStep >= 1 ? 'text-white' : 'text-muted/40'}>
              [Step 1] Checking real road turns and storm traffic for all {selectedScenario.requiredUnits.length} vehicle types...
            </div>
            <div className={simStep >= 2 ? 'text-white' : 'text-muted/40'}>
              [Step 2] Ranking which emergencies are in the most immediate danger...
            </div>
            <div className={simStep >= 3 ? 'text-accent' : 'text-muted/40'}>
              [Step 3] Testing thousands of vehicle combinations to find the fastest plan...
            </div>
            <div className={simStep >= 4 ? 'text-accent font-semibold' : 'text-muted/40'}>
              [Step 4] Verified! All victims covered with 0 double-bookings. Rescuers are en route!
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-border bg-surface-raised flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="font-mono text-xs text-muted">
            Run on your laptop anytime: <code className="text-white">streamlit run app.py</code>
          </span>

          <div className="flex items-center gap-3 w-full sm:w-auto">
            <button
              onClick={runSimulation}
              disabled={isSimulating}
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-white hover:bg-neutral-200 text-black font-sans font-semibold text-xs px-5 py-2.5 rounded transition-all cursor-pointer disabled:opacity-50"
            >
              {isSimulating ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Calculating Best Plan...</span>
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5 fill-black" />
                  <span>Click to Test Rescue Plan</span>
                </>
              )}
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
