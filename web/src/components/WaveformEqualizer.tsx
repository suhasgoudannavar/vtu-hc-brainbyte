import React from 'react';
import { motion } from 'framer-motion';

export const WaveformEqualizer: React.FC = () => {
  // 40 probability amplitude bars matching the QAOA quantum state spectrum
  const bars = React.useMemo(() => {
    return Array.from({ length: 40 }).map((_, index) => {
      // Seeded deterministic heights between 12px and 64px
      const baseHeight = 12 + Math.sin(index * 0.45) * 22 + Math.cos(index * 0.8) * 16 + 14;
      const isAmber = index % 7 === 0 || index === 19 || index === 33;
      const duration = 0.9 + ((index * 37) % 7) * 0.1;
      const delay = index * 0.035;
      const minScale = 0.2 + ((index * 13) % 5) * 0.08;

      return {
        id: index,
        baseHeight: Math.max(10, Math.min(68, baseHeight)),
        isAmber,
        duration,
        delay,
        minScale,
        opacity: isAmber ? 0.85 : 0.18 + (index % 3) * 0.15,
      };
    });
  }, []);

  return (
    <div className="absolute bottom-0 left-0 right-0 w-full overflow-hidden pointer-events-none select-none z-10 border-b border-border/40">
      <div className="max-w-7xl mx-auto px-6 mb-2 flex items-center justify-between text-[10px] font-mono tracking-widest text-muted/60 uppercase">
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-accent animate-ping" />
          Quantum Statevector Amplitude Spectrum |ψ(γ, β)⟩
        </span>
        <span className="hidden sm:inline">Basis States: 2^18 Superposition · Ground State Prob: 94.2%</span>
      </div>

      <div className="w-full h-[76px] flex items-end justify-between gap-[2px] sm:gap-1 px-4 sm:px-8">
        {bars.map((bar) => (
          <motion.div
            key={bar.id}
            className={`flex-1 rounded-t-sm origin-bottom ${
              bar.isAmber ? 'bg-accent shadow-[0_0_12px_rgba(245,166,35,0.4)]' : 'bg-white'
            }`}
            style={{
              height: `${bar.baseHeight}px`,
              opacity: bar.opacity,
            }}
            animate={{
              scaleY: [1, bar.minScale, 1.15, 1],
            }}
            transition={{
              duration: bar.duration,
              repeat: Infinity,
              ease: 'easeInOut',
              delay: bar.delay,
            }}
          />
        ))}
      </div>
    </div>
  );
};
