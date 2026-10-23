import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, ArrowRight, ShieldCheck, Zap, Layers, HeartPulse } from 'lucide-react';
import { WaveformEqualizer } from './WaveformEqualizer';

interface HeroProps {
  onOpenSimulator: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onOpenSimulator }) => {
  return (
    <section className="relative min-h-screen flex flex-col justify-end pt-32 pb-28 md:pb-36 px-6 sm:px-12 md:px-16 overflow-hidden bg-background circuit-grid noise-overlay">
      {/* Background Ambient Glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 w-[480px] h-[480px] bg-accent-cyan/5 rounded-full blur-3xl pointer-events-none" />

      {/* Hero Content Container */}
      <div className="relative z-20 max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-end mb-14">
        {/* Left Column: Headlines & CTAs */}
        <div className="lg:col-span-7 flex flex-col items-start">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-surface border border-border text-[11px] font-mono tracking-wider mb-6 text-foreground/90"
          >
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            <span className="text-accent uppercase font-medium">SAVING LIVES WITH SMART COMPUTING</span>
            <span className="text-muted">·</span>
            <span className="text-muted hidden sm:inline">FREE & WORKS 100% OFFLINE</span>
          </motion.div>

          {/* Main Display Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="font-display uppercase text-white tracking-[0.04em] text-[68px] sm:text-[96px] md:text-[124px] lg:text-[144px] leading-[0.88] max-w-[940px] drop-shadow-sm select-none"
          >
            WHEN SECONDS SAVE LIVES<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-white/90 to-white/60">
              GUESSWORK FAILS
            </span>
          </motion.h1>

          {/* Subtitle with Simple Words */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="font-sans font-normal text-base sm:text-lg text-muted max-w-[540px] mt-6 leading-relaxed"
          >
            During floods, earthquakes, and fires, sending whatever ambulance is closest usually leaves the most critical victims stranded. 
            <strong className="text-white font-medium block mt-1">
              QRescue finds the single smartest rescue plan in seconds so help arrives up to 42% faster.
            </strong>
          </motion.p>

          {/* CTA Row */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mt-8 flex flex-wrap items-center gap-4"
          >
            <button
              onClick={onOpenSimulator}
              className="flex items-center gap-3 bg-white hover:bg-neutral-200 text-black font-sans font-semibold text-sm px-6 py-3.5 rounded transition-all duration-200 shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:shadow-[0_0_35px_rgba(245,166,35,0.4)] cursor-pointer active:scale-95"
            >
              <span>See It In Action</span>
              <ArrowRight className="w-4 h-4 text-black" />
            </button>

            <a
              href="#solvers"
              className="flex items-center gap-2.5 bg-surface hover:bg-surface-raised border border-border hover:border-subtle text-foreground text-sm font-sans font-medium px-5 py-3.5 rounded transition-all"
            >
              <Cpu className="w-4 h-4 text-accent" />
              <span>How It Works</span>
            </a>
          </motion.div>

          {/* Telemetry Chips in Simple Words */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.45 }}
            className="mt-8 flex flex-wrap items-center gap-6 text-[11px] font-mono text-muted/80"
          >
            <div className="flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-accent" />
              <span>Zero Double-Bookings</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Zap className="w-3.5 h-3.5 text-white" />
              <span>No Internet Needed (Runs Offline)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <HeartPulse className="w-3.5 h-3.5 text-accent-cyan" />
              <span>Right Equipment to Every Victim</span>
            </div>
          </motion.div>
        </div>

        {/* Right Column: High-Tech Mission Control Telemetry Card */}
        <motion.div
          initial={{ opacity: 0, x: 25 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.25 }}
          className="lg:col-span-5 bg-surface/95 border border-border rounded-lg p-6 backdrop-blur-xl relative shadow-2xl amber-glow"
        >
          {/* Card Header */}
          <div className="flex items-center justify-between border-b border-border/80 pb-3 mb-4">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-accent animate-ping" />
              <span className="font-mono text-xs font-semibold uppercase text-white tracking-wider">
                LIVE RESCUE COMPARISON
              </span>
            </div>
            <span className="font-mono text-[10px] text-muted">Guesswork vs Smart Math</span>
          </div>

          {/* Quick Metrics Grid */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="bg-surface-raised p-3 rounded border border-border/50">
              <span className="text-[10px] font-mono text-muted uppercase block">Time Saved</span>
              <span className="font-display text-3xl text-accent font-normal tracking-wide">42% Faster</span>
              <span className="text-[10px] font-mono text-muted/80 block mt-0.5">Saves ~10 vital minutes</span>
            </div>
            <div className="bg-surface-raised p-3 rounded border border-border/50">
              <span className="text-[10px] font-mono text-muted uppercase block">Dispatch Mistakes</span>
              <span className="font-display text-3xl text-white font-normal tracking-wide">0 Errors</span>
              <span className="text-[10px] font-mono text-accent block mt-0.5">100% Verified Safe</span>
            </div>
          </div>

          {/* Live Progress Bar Visual */}
          <div className="bg-background/80 p-3.5 rounded border border-border/70 mb-4 font-mono text-xs">
            <div className="flex items-center justify-between text-[10px] text-muted mb-2">
              <span>RESCUE FLEET OPTIMIZATION</span>
              <span className="text-accent">Solved in 0.015s</span>
            </div>
            <div className="h-10 flex items-end gap-1 px-1">
              {[85, 78, 64, 52, 45, 38, 31, 25, 20, 18, 15, 14, 12, 11].map((val, idx) => (
                <div
                  key={idx}
                  className="flex-1 bg-white/20 hover:bg-accent transition-colors rounded-t-sm"
                  style={{ height: `${val}%` }}
                />
              ))}
            </div>
            <div className="flex justify-between text-[9px] text-muted/60 mt-1.5">
              <span>Step 1: Traffic & Roads</span>
              <span>Step 2: Optimal Plan Found</span>
            </div>
          </div>

          {/* Incident Feed Preview */}
          <div className="space-y-1.5 text-xs font-mono">
            <div className="flex items-center justify-between py-1 px-2 rounded bg-surface-raised/60 text-muted">
              <span className="text-foreground/90">Flood Emergency (#104)</span>
              <span className="text-accent text-[11px]">→ Rescue Boat Sent (6 min)</span>
            </div>
            <div className="flex items-center justify-between py-1 px-2 rounded bg-surface-raised/60 text-muted">
              <span className="text-foreground/90">Factory Fire (#107)</span>
              <span className="text-white text-[11px]">→ Foam Tanker Sent (4 min)</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Bottom Waveform Equalizer */}
      <WaveformEqualizer />
    </section>
  );
};
