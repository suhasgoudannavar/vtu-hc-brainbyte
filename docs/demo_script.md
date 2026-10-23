# QRescue: 3-Minute Hackathon Demo Script & Judge Q&A Guide

## ⏱️ 3-Minute Presentation Timeline

### 0:00 – 0:30 | The Emergency Dilemma (Problem Statement)
**Speaker:**
> "During natural disasters like flash floods, landslides, or industrial fires, emergency dispatchers face an agonizing challenge: multiple critical incidents competing for a limited fleet of ambulances, heavy rescue squads, and fire engines.
> A naive nearest-neighbor approach often creates disastrous bottlenecks—sending a specialized rescue squad to a minor fender bender while a collapsed building with trapped families waits unserved.
> Today, we present **QRescue**: an AI-assisted disaster response platform that combines transparent incident triage with mathematical and quantum optimization."

---

### 0:30 – 1:00 | Scenario Generation & Fleet Overview (Live Dashboard)
**Speaker:**
*(Screen: Dashboard View)*
> "Here on the QRescue operational dashboard, we are looking at **Scenario A: An Urban Flood Crisis**.
> On the left, our transparent triage engine has scored each incident from 0 to 100 based on severity, casualties, time sensitivity, and terrain access. Notice this Metro Station Inundation: 85 people affected, severity 5/5, requiring both a rescue team and an ambulance.
> On our spatial simulation map, we see 5 emergencies and 5 fleet assets. Notice that Flood Unit 2 is currently marked offline for maintenance. A robust optimizer must respect that hard constraint."

---

### 1:00 – 1:40 | Classical Constraint Optimization (OR-Tools)
**Speaker:**
*(Action: Click 'Quick Solve (Classical OR-Tools)')*
> "When we run our classical constraint optimizer powered by Google OR-Tools CP-SAT, it solves the problem globally in under 55 milliseconds.
> Look at the dispatch routes rendered on the map in cyan. The optimizer intelligently assigned Paramedic Alpha to the senior living evacuation, matched the swiftwater squad to the highest-priority flooded metro station, and left the lower-severity basement flooding flagged as unserved because fleet capacity was exhausted.
> Crucially, our universal constraint checker verifies zero conflicts, zero capability mismatches, and no illegal assignments to unavailable vehicles."

---

### 1:40 – 2:20 | The Quantum Optimization Experiment (QUBO & QAOA)
**Speaker:**
*(Action: Navigate to 'Optimization Lab', select 'Quantum (QAOA - Qiskit Aer)', click 'Execute Optimization Solver')*
> "Now, how does quantum computing fit into disaster logistics?
> We formulated this allocation challenge into a Quadratic Unconstrained Binary Optimization (QUBO) problem and mapped it to an Ising spin Hamiltonian.
> Using Qiskit and Qiskit Aer, we simulate the Quantum Approximate Optimization Algorithm (QAOA).
> Here you can see the parameterized quantum circuit: alternating Cost and Mixer operators. After variational optimization with COBYLA, we sample the quantum state across 512 shots.
> The bitstring probability distribution highlights the top candidate solutions explored by the quantum state."

---

### 2:20 – 2:45 | Fair Benchmark & Scientific Honesty
**Speaker:**
*(Action: Navigate to 'Algorithm Comparison')*
> "On our Algorithm Comparison page, we benchmark all three methods side-by-side on identical inputs.
> We pride ourselves on scientific honesty:
> 1. We do NOT claim quantum advantage. Classical integer programming is currently faster and achieves zero violations on these problem sizes.
> 2. Classical CPU simulation of quantum circuits involves exponential matrix overhead.
> 3. Our platform provides a research sandbox to test how disaster dispatch can transition to future fault-tolerant quantum processors."

---

### 2:45 – 3:00 | Impact, Export, & Conclusion
**Speaker:**
*(Action: Click 'Download Full JSON Audit' or 'Download Markdown Report')*
> "With one click, coordinators can export a complete, reproducible audit report in JSON, CSV, or Markdown.
> QRescue is 100% open-source, runs completely offline on standard hardware, and bridges AI triage with quantum algorithms to build more resilient disaster management.
> Thank you, and we welcome your questions!"

---

## 💡 Judge Q&A Preparation: Anticipated Questions & Answers

### Q1: Why is quantum optimization relevant to disaster response?
**Answer:**
Disaster logistics is an NP-hard combinatorial problem. As the number of incidents, specialized resources, and dynamic time windows grows during regional catastrophes, the solution space explodes exponentially. Quantum approaches like QAOA and quantum annealers explore combinatorial solution spaces via quantum superposition and tunneling. Investigating QUBO formulations today prepares disaster logistics frameworks for future quantum processors.

### Q2: Why not just use classical optimization?
**Answer:**
For current problem sizes (5–50 incidents), classical solvers like Google OR-Tools CP-SAT are exceptionally fast, reliable, and optimal. We explicitly demonstrate this in our benchmark. However, classical solvers can encounter combinatorial bottlenecks in massive, multi-period dynamic routing with non-linear constraints. Researching quantum formulations provides valuable insights into how hybrid classical-quantum solvers will operate in the future.

### Q3: What is QUBO?
**Answer:**
QUBO stands for Quadratic Unconstrained Binary Optimization. It represents an optimization problem using binary decision variables $x_i \in \{0, 1\}$ with linear weights and pairwise quadratic interactions: $\min x^T Q x$. Constraints (such as exclusivity and vehicle availability) are converted into quadratic penalty terms via Lagrange multipliers. Because QUBO variables map directly to quantum spin-$1/2$ Pauli-$Z$ operators ($x_k = \frac{I - Z_k}{2}$), it serves as the universal language connecting classical combinatorial problems to quantum hardware.

### Q4: How does the AI/ML component work?
**Answer:**
We provide two distinct modes. Mode A is a transparent, configurable multi-factor baseline that scores urgency using severity, casualty count, time sensitivity, and terrain access. Mode B is an optional machine learning experiment where we train a Random Forest classifier on synthetic historical dispatch records to predict triage categories, reporting precision, recall, and feature importances. We emphasize that neither mode is a clinical triage diagnostic—both are simulation priority scores.

### Q5: How do you measure solution quality?
**Answer:**
We evaluate:
1. **Constraint Feasibility:** Zero violations of exclusivity, availability, and capability requirements.
2. **High-Priority Fulfillment:** Number of Critical and High-severity incidents served.
3. **Total Weighted Response Time:** Sum of transit times weighted by incident priority.
4. **Objective Value:** Balanced combination of transit delay, unserved penalties, and operational costs.
5. **Runtime:** Solver execution time.

### Q6: What happens when resources are insufficient?
**Answer:**
In disaster response, resource scarcity is inevitable. When fleet capacity is exceeded, our optimizer explicitly leaves lower-priority or unreachable incidents unserved, logging them in an unserved manifest and applying a proportional penalty in the objective function. It never makes false promises or violates vehicle exclusivity.

### Q7: What are the limitations of your simulation?
**Answer:**
1. Coordinates and street topologies are synthetic (using a 1.35x road curvature factor).
2. Straight-line Euclidean/Haversine calculations are approximations of real-world road networks.
3. The quantum solver is simulated on a classical CPU via Qiskit Aer, which incurs classical simulation overhead.
4. The tool is an educational research prototype, not certified for real-world life-or-death dispatch.

### Q8: Does the project use real quantum hardware?
**Answer:**
No. We run a genuine quantum circuit simulation using Qiskit and Qiskit Aer on classical CPU hardware. We deliberately avoid claiming physical quantum hardware execution or artificial quantum speedup.

### Q9: What evidence supports the reported improvements?
**Answer:**
All improvements are computed dynamically using identical scenario inputs. The improvement percentage is calculated strictly using:
$$\text{Improvement} = \frac{\text{Baseline Cost} - \text{Optimized Cost}}{\text{Baseline Cost}} \times 100$$
We only calculate this when the baseline cost is strictly positive, ensuring no false division-by-zero statistics.
