import React, { useState } from 'react';
import { Activity, Menu, X, Terminal, ShieldAlert } from 'lucide-react';

interface NavbarProps {
  onOpenSimulator: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenSimulator }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: 'Scenarios', href: '#scenarios' },
    { name: 'Solvers', href: '#solvers' },
    { name: 'Benchmarks', href: '#benchmarks' },
    { name: 'Architecture', href: '#architecture' },
    { name: 'Lab', href: '#lab' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#0d0d0d]/90 backdrop-blur-xl border-b border-border transition-all">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 h-18 flex items-center justify-between">
        {/* Brand / Logo */}
        <a href="#" className="flex items-center gap-3 group">
          <div className="w-8 h-8 rounded border border-border bg-surface flex items-center justify-center text-accent group-hover:border-accent transition-colors">
            <ShieldAlert className="w-4 h-4" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="font-display text-2xl tracking-[0.08em] text-white">QRESCUE</span>
            <span className="font-mono text-[9px] uppercase tracking-wider text-accent bg-accent/10 px-1.5 py-0.5 rounded border border-accent/20">
              v2.4 · QAOA
            </span>
          </div>
        </a>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className="text-sm font-sans font-medium text-muted hover:text-white transition-colors relative py-1 after:absolute after:bottom-0 after:left-0 after:w-0 after:h-[1px] after:bg-accent hover:after:w-full after:transition-all"
            >
              {link.name}
            </a>
          ))}
        </nav>

        {/* Right Action Button */}
        <div className="hidden sm:flex items-center gap-3">
          <a
            href="#lab"
            className="flex items-center gap-2 text-xs font-mono text-muted hover:text-white px-3 py-2 rounded border border-border hover:border-subtle transition-colors"
          >
            <Terminal className="w-3.5 h-3.5 text-accent" />
            <span>Local Offline</span>
          </a>

          <button
            onClick={onOpenSimulator}
            className="flex items-center gap-2 bg-white hover:bg-neutral-200 text-black font-sans font-semibold text-[13px] px-4 py-2 rounded transition-all shadow-[0_0_20px_rgba(255,255,255,0.15)] hover:shadow-[0_0_25px_rgba(245,166,35,0.35)] cursor-pointer active:scale-95"
          >
            <Activity className="w-4 h-4 text-black" />
            <span>Simulate Dispatch</span>
          </button>
        </div>

        {/* Mobile Hamburger Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-muted hover:text-white border border-border rounded"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-surface border-b border-border px-6 py-6 space-y-4">
          <nav className="flex flex-col space-y-3">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="text-base font-sans font-medium text-muted hover:text-white py-1"
              >
                {link.name}
              </a>
            ))}
          </nav>
          <div className="pt-4 border-t border-border flex flex-col gap-3">
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenSimulator();
              }}
              className="w-full flex items-center justify-center gap-2 bg-white text-black font-semibold text-sm py-2.5 rounded shadow cursor-pointer"
            >
              <Activity className="w-4 h-4" />
              <span>Simulate Dispatch</span>
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
