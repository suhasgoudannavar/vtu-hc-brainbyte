import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { Marquee } from './components/Marquee';
import { ScenariosSection } from './components/ScenariosSection';
import { SolversSection } from './components/SolversSection';
import { BenchmarksSection } from './components/BenchmarksSection';
import { ArchitectureSection } from './components/ArchitectureSection';
import { QuantumLabSection } from './components/QuantumLabSection';
import { CTASection } from './components/CTASection';
import { Footer } from './components/Footer';
import { DispatchSimulatorModal } from './components/DispatchSimulatorModal';
import type { ScenarioData } from './data/mockData';

export function App() {
  const [isSimulatorOpen, setIsSimulatorOpen] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState<ScenarioData | null>(null);

  const handleOpenSimulator = (scenario?: ScenarioData) => {
    if (scenario) {
      setSelectedScenario(scenario);
    }
    setIsSimulatorOpen(true);
  };

  const handleCloseSimulator = () => {
    setIsSimulatorOpen(false);
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans selection:bg-accent selection:text-black">
      {/* Fixed Navigation Bar */}
      <Navbar onOpenSimulator={() => handleOpenSimulator()} />

      {/* Hero Section with Quantum Waveform Equalizer */}
      <main className="flex-grow">
        <Hero onOpenSimulator={() => handleOpenSimulator()} />

        {/* Operational Telemetry Marquee */}
        <Marquee />

        {/* Simulated Disaster Scenarios Grid */}
        <ScenariosSection onSelectScenario={handleOpenSimulator} />

        {/* Optimization Engines & Solvers */}
        <SolversSection />

        {/* Comparative Benchmark Performance Audit */}
        <BenchmarksSection />

        {/* End-to-End System Architecture */}
        <ArchitectureSection />

        {/* The Quantum Lab & Tech Matrix */}
        <QuantumLabSection />

        {/* Call To Action */}
        <CTASection onOpenSimulator={() => handleOpenSimulator()} />
      </main>

      {/* Footer */}
      <Footer />

      {/* Interactive Live Benchmark Simulation Modal */}
      <DispatchSimulatorModal
        isOpen={isSimulatorOpen}
        onClose={handleCloseSimulator}
        initialScenario={selectedScenario}
      />
    </div>
  );
}

export default App;
