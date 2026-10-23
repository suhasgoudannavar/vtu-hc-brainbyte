import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Cpu, Terminal, Compass, ArrowRight, CheckCircle2, Code2 } from 'lucide-react';

export const SolversSection: React.FC = () => {
  const [activeCodeTab, setActiveCodeTab] = useState<number | null>(null);

  const solvers = [
    {
      id: 1,
      icon: Terminal,
      name: "GOOGLE OR-TOOLS CP-SAT",
      role: "The Master Planner (Classical Computer)",
      simpleSummary: "Checks every single vehicle and emergency to guarantee no vehicle is sent to two places at once, and every victim gets the exact equipment they need.",
      metric: "Solves in 0.012 seconds · 100% Guaranteed Safe",
      features: [
        "Zero Double-Booking: An ambulance is never sent to two places at once",
        "Right Equipment: A fire call gets a fire engine, not a basic van",
        "Mathematically Proven: Guaranteed to find the best possible plan"
      ],
      codeSnippet: `# Classical Constraint Formulation
# Rule 1: No double booking (each truck serves at most 1 emergency)
for truck in available_trucks:
    model.Add(sum(assigned[incident, truck] for incident in emergencies) <= 1)

# Rule 2: Send the closest valid truck to save critical time
model.Minimize(
    sum(travel_minutes[incident, truck] * assigned[incident, truck])
)`
    },
    {
      id: 2,
      icon: Cpu,
      name: "QISKIT QAOA SIMULATOR",
      role: "The Quantum Supercomputer (Next-Gen Tech)",
      simpleSummary: "Uses quantum physics principles to explore millions of possible rescue combinations at the same time, finding solutions to giant city-wide traffic gridlocks.",
      metric: "Tests 16+ Qubits · Simulated on Any Standard PC",
      features: [
        "Explores all routes simultaneously using quantum states",
        "Penalizes any bad choices like sending the wrong truck",
        "Prepares disaster response for real quantum hardware"
      ],
      codeSnippet: `# Quantum Circuit Simulation
# Converts rules into an energy landscape (bad choices cost extra energy)
hamiltonian, offset = disaster_qubo_to_ising(penalty_matrix)

# Uses quantum wave pulses to settle into the lowest-energy (best) plan
ansatz = QAOAAnsatz(cost_operator=hamiltonian, reps=2)
result = minimize_energy(ansatz)`
    },
    {
      id: 3,
      icon: Compass,
      name: "REAL-WORLD TRAVEL & TRIAGE",
      role: "The Smart GPS & Medical Priority Engine",
      simpleSummary: "Calculates realistic travel times by measuring real curved roads and storm traffic delays (not fake straight lines) and ranks who needs help first.",
      metric: "1.35× Road Curvature · Storm Traffic Multipliers",
      features: [
        "Real Road Curves: Adds 35% for actual street turns and hills",
        "Storm Slowdown: Accounts for flooded roads and bridge closures",
        "Life-First Ranking: Ranks emergencies by danger to save the most lives"
      ],
      codeSnippet: `# Real-World Road Transit Calculation
straight_line_km = distance(station.lat, incident.lat)
real_road_km = straight_line_km * 1.35  # Account for road bends

# Factor in weather traffic (rain & debris slow trucks down)
actual_travel_minutes = (real_road_km / truck_speed) * weather_traffic_delay`
    }
  ];

  return (
    <section id="solvers" className="py-24 px-6 sm:px-12 md:px-16 bg-surface border-y border-border">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
          <div>
            <span className="font-mono text-xs uppercase tracking-widest text-accent block mb-2">
              02 / HOW IT WORKS
            </span>
            <h2 className="font-display uppercase text-white tracking-[0.04em] text-[52px] sm:text-[68px] md:text-[80px] leading-[0.9]">
              THE 3 SMART ENGINES
            </h2>
          </div>
          <p className="font-sans font-normal text-muted text-sm sm:text-base max-w-md">
            Three powerful systems working together to replace human panic and guesswork with fast, reliable computer planning.
          </p>
        </div>

        {/* 3-Column Card Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {solvers.map((solver, idx) => {
            const Icon = solver.icon;
            const isCodeOpen = activeCodeTab === solver.id;

            return (
              <motion.div
                key={solver.id}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="bg-background border border-border hover:border-subtle rounded-lg p-7 flex flex-col justify-between transition-all group relative"
              >
                <div>
                  {/* Icon & Role */}
                  <div className="flex items-center justify-between mb-6">
                    <div className="w-12 h-12 rounded bg-surface border border-border flex items-center justify-center text-accent group-hover:border-accent/40 transition-colors">
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="font-mono text-[10px] text-muted uppercase tracking-wider">
                      Engine 0{solver.id}
                    </span>
                  </div>

                  {/* Title & Description */}
                  <h3 className="font-sans font-semibold text-white text-xl tracking-tight">
                    {solver.name}
                  </h3>
                  <span className="font-mono text-xs text-accent/90 block mt-1">
                    {solver.role}
                  </span>
                  <p className="font-sans text-sm text-muted mt-4 leading-relaxed">
                    {solver.simpleSummary}
                  </p>

                  {/* Core Features */}
                  <ul className="mt-6 space-y-2.5">
                    {solver.features.map((feat, fIdx) => (
                      <li key={fIdx} className="flex items-start gap-2.5 text-xs font-sans text-foreground/80">
                        <CheckCircle2 className="w-4 h-4 text-accent shrink-0 mt-0.5" />
                        <span>{feat}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mt-8 pt-6 border-t border-border">
                  {/* Performance Spec Badge */}
                  <div className="font-mono text-xs text-accent font-medium mb-4 flex items-center justify-between">
                    <span>{solver.metric}</span>
                  </div>

                  {/* Code Snippet Toggle */}
                  <button
                    onClick={() => setActiveCodeTab(isCodeOpen ? null : solver.id)}
                    className="w-full flex items-center justify-between font-mono text-xs text-white hover:text-accent border border-border/80 hover:border-accent/40 px-3 py-2 rounded bg-surface transition-colors cursor-pointer"
                  >
                    <span className="flex items-center gap-2">
                      <Code2 className="w-3.5 h-3.5 text-accent" />
                      {isCodeOpen ? "Hide Python Code" : "Show Python Code"}
                    </span>
                    <ArrowRight className={`w-3.5 h-3.5 transition-transform ${isCodeOpen ? 'rotate-90' : ''}`} />
                  </button>

                  {/* Code Snippet Drawer */}
                  {isCodeOpen && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-4 p-3 bg-surface-raised rounded border border-border font-mono text-[10.5px] text-muted overflow-x-auto leading-relaxed"
                    >
                      <pre className="text-foreground/90 whitespace-pre">
                        <code>{solver.codeSnippet}</code>
                      </pre>
                    </motion.div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
