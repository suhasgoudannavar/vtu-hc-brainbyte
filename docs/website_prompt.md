# QRescue Website Prompt
# Adapted from websiteprompts.ai design framework for QRescue

Build a high-performance modern website for **QRescue** — an AI-powered disaster response simulation and quantum optimization platform. Near-black foundation, crisp white typography, animated quantum state vector / energy landscape visualizer, hazard amber accents, bold uppercase display typography. Minimal dark mission control / quantum laboratory aesthetic — serious engineering, zero noise, life-critical operational clarity.

## Tech Stack
React + Vite + TypeScript + Tailwind CSS + Framer Motion (`motion/react`) + shadcn/ui + lucide-react

## Design System
```css
:root {
  --background: 0 0% 5%;            /* #0d0d0d near-black terminal floor */
  --surface: 0 0% 8%;               /* #141414 surface panels */
  --surface-raised: 0 0% 11%;       /* #1c1c1c raised module cards */
  --border: 0 0% 15%;               /* #262626 subtle telemetry borders */
  --foreground: 0 0% 97%;           /* #f7f7f7 off-white high-contrast text */
  --muted: 0 0% 44%;                /* #707070 secondary telemetry & labels */
  --subtle: 0 0% 25%;               /* #404040 structural grid dividers */
  --primary: 0 0% 100%;             /* #ffffff pure white primary emphasis */
  --accent: 38 96% 56%;             /* #f5a623 emergency amber / quantum coherence highlight */
  --accent-cyan: 199 89% 48%;        /* #0ea5e9 quantum state secondary accent */
  --mono: 'JetBrains Mono', monospace;
}
```

## Typography
Import: `https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap`
- Display / H1–H2: Bebas Neue 400, letter-spacing 0.04em — all uppercase, massive impact
- Body / UI: DM Sans 300–600 — clean, readable operations interface
- Labels / Telemetry / Math / Qubits: JetBrains Mono 400–600

## Visual Effects

**Animated Quantum Probability Amplitude Equalizer** — bottom of hero, full-width, 80px tall bar visualizer:
```jsx
// 40 state-probability bars representing |00...0> to |11...1> state amplitudes
// Heights randomized or generated from QAOA cost Hamiltonian distribution (8px to 68px)
// Each bar: background white or amber accent (top 10%), opacity 0.12–0.65
// Framer Motion continuous quantum superposition oscillation:
// animate={{ scaleY: [1, random(0.2, 1.15), 1] }}
// transition={{ duration: random(0.9, 1.6), repeat: Infinity, ease: 'easeInOut', delay: index * 0.035 }}
// transform-origin: bottom
```
Wrap in `overflow: hidden`, full-width, `position: absolute; bottom: 0; left: 0; right: 0`.

**Hover Scenario Dispatch Preview** — disaster scenario cards reveal an interactive simulation launch button:
```
Simulation Trigger: white circle 48px, lucide icon `Play` or `Activity` filled, centered on card
transition: opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.2s ease
default: opacity 0, scale 0.92; hover: opacity 1, scale 1.0
Hover card also reveals real-time telemetry badge: "CASUALTY WINDOW: < 12 MIN"
```

**Stagger Fade-Up** — `initial={{ opacity: 0, y: 24 }}` → `animate={{ opacity: 1, y: 0 }}`, 0.45s ease-out per section/card.

**Operational Marquee** — live capabilities & algorithms scrolling strip: continuous, speed 22s, gap 64px, JetBrains Mono 10px with amber hazard dots.

---

## Sections

### 1. Navbar
- Fixed, `background: hsl(var(--background)/0.94)`, `backdrop-filter: blur(16px)`, `border-bottom: 1px solid hsl(var(--border))`.
- Left: "QRESCUE" Bebas Neue 24px white, letter-spacing 0.08em + small badge `v2.4-QAOA` in JetBrains Mono 9px amber.
- Center: Scenarios · Optimization Engines · Benchmarks · Architecture · Methodology.
- Right: "Launch Simulator →" — white filled button, dark text, DM Sans 600 13px, border-radius 4px, hover slight amber glow.

### 2. Hero Section
- Full viewport (`min-h-screen`), flex column, justify-content flex-end, padding `0 64px 100px`, relative, overflow hidden.
- Background layers: dark surface gradient + noise texture overlay (opacity 0.35, blend-mode overlay) + subtle radial glow in deep slate.
- Bottom: 80px tall animated Quantum Probability Amplitude Equalizer.
- Content (z-10):
  - Badge: JetBrains Mono 10px tracking-widest text amber: `● LIVE SIMULATION ENGINE · CLASSICAL & QUANTUM OPTIMIZATION`
  - H1 Bebas Neue, clamp(72px, 10vw, 160px), line-height 0.88, white, max-width 980px:
    ```
    WHEN SECONDS SAVE LIVES
    GREEDY DISPATCH FAILS
    ```
  - Sub: DM Sans 300 16px muted, max-width 560px, margin-top 22px:
    "End-to-end combinatorial disaster response optimization. Eliminating emergency fleet bottlenecks using Google OR-Tools CP-SAT and Qiskit QAOA quantum circuit simulation."
  - Action Row:
    - Primary CTA: "Launch Operations Dashboard" (white filled, dark text, DM Sans 600)
    - Secondary CTA: "Inspect QAOA Circuit" (ghost border, white text, lucide `Cpu` icon)
    - Telemetry Snippet: JetBrains Mono 11px muted: `100% Local & Offline · Zero Paid APIs · Qiskit 2.0+`
  - Floating Terminal/Console preview at right edge (mixing console metaphor adapted to quantum dispatch console with live objective loss curves).

### 3. Operational Telemetry Marquee
- Full-width strip, `background: hsl(var(--surface))`, border-top and border-bottom, 44px tall.
- Continuous scroll:
  `GOOGLE OR-TOOLS CP-SAT · QISKIT 2.0+ AER SIMULATOR · QAOA ISING HAMILTONIAN · MULTI-FACTOR TRIAGE · ROAD CURVATURE 1.35× · ZERO RESOURCE CONFLICTS · QUBO QUADRATIC PENALTIES · SUPERVISED RANDOM FOREST · HAVERSINE GEO-TRANSIT · COBYLA VARIATIONAL SOLVER ·`
  - Typography: JetBrains Mono 10px white 40%, items separated by amber pulse indicators `◆`.

### 4. Selected Scenarios & Disaster Benchmarks
- Padding: `96px 64px`.
- Heading: Bebas Neue clamp(52px, 6vw, 80px): "SIMULATED DISASTER SCENARIOS".
- Sub: DM Sans 14px muted: "Pre-configured multi-hazard crises testing resource exclusivity, transit congestion, and triage urgency."
- 3-column card grid (6 scenarios total):
  1. **Metro Flash Flood** — 38 Casualties, 6 Critical Zones · Urgent Swiftwater Rescue & Heavy Shoring.
  2. **Highland Ridge Landslide** — Trapped Vehicles, Severed Bridges · K9 Search, Heavy Excavation & Trauma Vans.
  3. **Industrial Chemical Fire & Vapor Cloud** — Multi-Alarm Fire, Structural Collapse · HazMat Containment & Foam Tankers.
  4. **Extreme Resource Shortage Stress-Test** — 14 Overlapping Incidents, 6 Available Units · Demonstrates total Greedy failure vs CP-SAT global optimum.
  5. **Seismic Mass-Casualty Incident** — Collapsed Infrastructure, Gridlock · Multi-Agency Air & Ground Medical Coordination.
  6. **Coastal Storm Surge & Blackout** — Island Cutoffs, Generator Failures · Amphibious Fleet & Mobile Triage Stations.
- Each Card:
  - Aspect ratio 16/10 visual graphic (minimalist dark topographic wireframe or radar vector with amber epicenter markers).
  - Hover trigger: play simulation button + real-time metrics preview.
  - Card Details: Scenario Name (DM Sans 600 16px), Category badge (JetBrains Mono 10px amber), Response Time Target (JetBrains Mono 10px muted).

### 5. Optimization Engines & Formulations
- Surface background, padding: `96px 64px`.
- Heading: Bebas Neue: "SOLVER ARCHITECTURE".
- 3-column modular card grid:
  - **Module 1: Google OR-Tools CP-SAT (Classical Mixed-Integer)**
    - "Exact combinatorial optimizer enforcing strict resource exclusivity, availability, and capability requirements. Guarantees global optimality with zero constraint violations."
    - Spec badge: JetBrains Mono 12px amber: `0.012s Solve Time · 100% Feasibility`
    - Action: "View Formulation →"
  - **Module 2: Qiskit QAOA Engine (Quantum Approximate Optimization)**
    - "Translates multi-resource allocation into QUBO & Ising spin Hamiltonians. Simulates parameterized $p$-layer quantum circuits with COBYLA variational feedback loop on Qiskit Aer."
    - Spec badge: JetBrains Mono 12px amber: `K=N×M Qubits · Parameterized Statevector`
    - Action: "Explore Circuit →"
  - **Module 3: Multi-Factor Triage & Travel Physics**
    - "Dynamic urgency scoring factoring casualty severity (1–5), access impediment, and time sensitivity. Computes road transit with 1.35× curvature factor and storm congestion multipliers."
    - Spec badge: JetBrains Mono 12px amber: `Haversine + Curvature · Scikit-Learn ML`
    - Action: "Inspect Model →"

### 6. Algorithmic Benchmark Audit (Side-by-Side Comparison)
- Padding: `96px 64px`.
- Heading: Bebas Neue: "BENCHMARK PERFORMANCE AUDIT".
- Sub: DM Sans 14px muted: "Comparative evaluation on identical disaster parameters."
- Horizontal telemetry table (each row `border-top: 1px solid hsl(var(--border))`, hover `background: hsl(var(--surface-raised))`, padding `18px 0`):
  - Row 1: **Resource Conflict Rate** · Greedy: 38% (High Double-Dispatch) · CP-SAT: 0.0% (Enforced) · QAOA: Audited via Penalty Matrix
  - Row 2: **High-Priority Incidents Unserved** · Greedy: 4 Incidents Abandoned · CP-SAT: 0 Unserved · QAOA: Minimizes Penalty Hamiltonian
  - Row 3: **Average Critical Response Time** · Greedy: 24.6 min · CP-SAT: 14.1 min (-42.6%) · QAOA: 15.3 min
  - Row 4: **Mathematical Guarantee** · Greedy: Local Heuristic · CP-SAT: Globally Optimal Branch & Bound · QAOA: Quantum State Superposition Sampling
  - Row 5: **Universal Constraint Verification** · Greedy: Fails Exclusivity · CP-SAT: 100% Verified · QAOA: Verified via Post-Sampling Filter
  - Row 6: **Computational Execution Time** · Greedy: 0.001s · CP-SAT: 0.015s · QAOA: 1.420s (Simulator)
- Entrance: Framer Motion stagger fade-in on scroll.

### 7. The Quantum Lab & Tech Matrix
- Two-column layout, padding: `96px 64px`.
- Left Column:
  - Heading Bebas Neue: "THE RESEARCH LAB".
  - DM Sans 15px muted body:
    "QRescue bridges real-world emergency operational logistics with frontier quantum computing. Built entirely on free, open-source scientific software running 100% locally and offline without external dependencies or cloud subscriptions."
  - System Tech Chips in JetBrains Mono 11px:
    `Python 3.12` · `Qiskit 2.0+` · `Qiskit Aer` · `Google OR-Tools` · `Streamlit` · `Scikit-Learn` · `Plotly` · `NumPy / SciPy` · `Pytest (25 Tests)`
  - Mathematical Equation Callout:
    $H(x) = H_{\text{cost}}(x) + P_{\text{excl}} H_{\text{excl}}(x) + P_{\text{mismatch}} H_{\text{mismatch}}(x)$
- Right Column:
  - Technical diagram or interactive visual card showcasing quantum circuit depth, Pauli-Z Ising terms, and energy convergence curve.

### 8. Call to Action (CTA)
- Near-black background, padding: `96px 64px`, centered.
- Heading Bebas Neue clamp(60px, 8vw, 110px) white: "EXPERIENCE QUANTUM-POWERED DISPATCH".
- Sub DM Sans 16px muted max-width 520px:
  "Run multi-hazard simulations, audit classical vs quantum solvers side-by-side, and inspect full optimization logs locally."
- Action Buttons:
  - "Launch Streamlit Dashboard →" (white filled, dark text, DM Sans 600)
  - "View Source on GitHub" (ghost border, lucide `Github` icon)
- Telemetry Footnote: JetBrains Mono 11px muted:
  "Designed for Emergency Operations Centers & Quantum Information Researchers · Fully Open-Source (MIT)"

### 9. Footer
- `background: hsl(0 0% 3%)`, padding `48px 64px 28px`, border-top: `1px solid hsl(var(--border))`.
- Left: "QRESCUE" Bebas Neue 20px white + "Disaster Response Decision-Support Platform" DM Sans 12px muted.
- Center: Quick navigation links (Scenarios, CP-SAT Solver, QAOA Circuit, Benchmarks, Methodology).
- Right: System badges (MIT License · Local Offline Mode · Qiskit 2.0+ Compliant · 25 Unit Tests Passing).
- Bottom: Copyright `© 2026 QRescue Project · Research & Educational Optimization Platform` in JetBrains Mono 10px muted.

---

## Responsive Specifications
- **Mobile (< 768px)**:
  - Navigation converts to slide-out sheet / mobile menu.
  - Hero H1: `clamp(52px, 14vw, 84px)`.
  - Quantum equalizer: 56px tall, 20 bars.
  - Disaster Scenarios grid: single column with full-bleed cards.
  - Benchmark audit table: responsive scroll or stacked card view.
  - Lab section: single column layout with architecture diagram stacked below description.

## Animation Matrix
| Component | Animation Trigger | Description |
| :--- | :--- | :--- |
| **Quantum Amplitudes** | Always active loop | Continuous scaleY superposition oscillation with randomized phase delays |
| **Telemetry Marquee** | Always active loop | Smooth seamless continuous horizontal scroll (22s loop) |
| **Hero Content** | Mount | Stagger fade-up (0.5s ease-out, staggered by 0.1s) |
| **Scenario Cards** | Scroll into view | Stagger fade-up with hover scale & amber halo glow |
| **Simulate Dispatch Button** | Card hover | Opacity 0 → 1, scale 0.92 → 1.0 with lucide `Activity` icon |
| **Benchmark Rows** | Scroll into view | Sequential line-by-line slide & fade-in with hover highlight |
