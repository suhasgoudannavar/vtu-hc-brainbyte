# QRescue: Mathematical Methodology & Optimization Formulation

## 1. Problem Formulation
During large-scale emergency response, coordinators face a multi-criteria resource allocation problem under severe capacity constraints.

Let:
- $\mathcal{I} = \{1, \dots, N\}$ be the set of active incidents.
- $\mathcal{R} = \{1, \dots, M\}$ be the set of emergency response resources.
- $\mathcal{T}$ be the set of resource types: $\{\text{Ambulance}, \text{Rescue Team}, \text{Fire Team}, \text{Medical Supply}\}$.
- $R_t \subseteq \mathcal{R}$ be the subset of resources of type $t \in \mathcal{T}$.
- $\mathcal{T}_i \subseteq \mathcal{T}$ be the set of resource types required to fully mitigate incident $i$.
- $c_{i, r} \ge 0$ be the estimated transit time (minutes) from resource $r$'s current location to incident $i$.
- $P_i \ge 0$ be the unserved penalty proportional to incident $i$'s simulated priority score: $P_i = 15 \times \text{UrgencyScore}_i$.
- $\text{Cost}_{i, r}$ be the operational dispatch cost of resource $r$.

---

## 2. Classical Mixed-Integer Formulation

### Binary Decision Variables
- $x_{i, r} \in \{0, 1\}$: $1$ if resource $r$ is assigned to incident $i$, $0$ otherwise.
- $y_i \in \{0, 1\}$: $1$ if incident $i$ is fully served across all required resource types, $0$ otherwise.

### Objective Function
$$\min \quad w_{\text{resp}} \sum_{i \in \mathcal{I}} \sum_{r \in \mathcal{R}} \left( \frac{\text{UrgencyScore}_i}{100} \right) c_{i, r} x_{i, r} + w_{\text{unserved}} \sum_{i \in \mathcal{I}} P_i (1 - y_i) + w_{\text{cost}} \sum_{i \in \mathcal{I}} \sum_{r \in \mathcal{R}} \text{Cost}_{i, r} x_{i, r}$$

### Constraints
1. **Resource Exclusivity:**
   $$\sum_{i \in \mathcal{I}} x_{i, r} \le 1, \quad \forall r \in \mathcal{R}_{\text{available}}$$
2. **Resource Availability:**
   $$\sum_{i \in \mathcal{I}} x_{i, r} = 0, \quad \forall r \notin \mathcal{R}_{\text{available}}$$
3. **Type Compatibility:**
   $$x_{i, r} = 0, \quad \forall (i, r) \text{ such that } \text{Type}(r) \notin \mathcal{T}_i$$
4. **Type Coverage (Fulfillment):**
   $$\sum_{r \in R_t} x_{i, r} \ge y_i, \quad \forall i \in \mathcal{I}, \quad \forall t \in \mathcal{T}_i$$
5. **Total Capability Count Link:**
   $$\sum_{r \in \mathcal{R}} x_{i, r} \ge |\mathcal{T}_i| \cdot y_i, \quad \forall i \in \mathcal{I}$$

---

## 3. QUBO (Quadratic Unconstrained Binary Optimization) Formulation
To convert this constrained optimization into a form solvable by quantum algorithms or Ising solvers, constraints are cast into quadratic penalties:

$$H(x) = H_{\text{cost}}(x) + H_{\text{penalties}}(x)$$

### 1. Cost & Urgency Terms:
$$H_{\text{cost}}(x) = \sum_{i, r} \left( w_{\text{transit}} c_{i, r} - w_{\text{urgency}} \frac{\text{UrgencyScore}_i}{100} \right) x_{i, r}$$

### 2. Penalty Terms:
- **Exclusivity Penalty:**
  $$H_{\text{excl}}(x) = P_{\text{excl}} \sum_{r \in \mathcal{R}} \sum_{i < i'} 2 x_{i, r} x_{i', r}$$
- **Type Incompatibility Penalty:**
  $$H_{\text{mismatch}}(x) = P_{\text{mismatch}} \sum_{\substack{i, r \\ \text{Type}(r) \notin \mathcal{T}_i}} x_{i, r}$$
- **Unavailability Penalty:**
  $$H_{\text{unavail}}(x) = P_{\text{unavail}} \sum_{\substack{i, r \\ r \notin \mathcal{R}_{\text{avail}}}} x_{i, r}$$

In matrix form:
$$H(x) = x^T Q x + \text{offset}$$
where $Q \in \mathbb{R}^{K \times K}$ is an upper-triangular matrix, and $K = N \times M$ is the number of binary decision variables (qubits).

---

## 4. Mapping to Ising Spin Hamiltonian
Using the standard transformation from binary variables $x_k \in \{0, 1\}$ to Pauli-$Z$ eigenvalues $s_k \in \{+1, -1\}$:
$$x_k = \frac{I - Z_k}{2}$$

Substituting into $x^T Q x$:
- Linear term: $Q_{kk} x_k = \frac{Q_{kk}}{2} I - \frac{Q_{kk}}{2} Z_k$
- Quadratic term: $Q_{jk} x_j x_k = \frac{Q_{jk}}{4} (I - Z_j - Z_k + Z_j Z_k)$

Summing all terms produces the Ising Hamiltonian:
$$H_{\text{Ising}} = \sum_{k=1}^K h_k Z_k + \sum_{j < k} J_{jk} Z_j Z_k + \text{const}$$

---

## 5. QAOA (Quantum Approximate Optimization Algorithm) Circuit
The QAOA ansatz creates a parameterized state $|\psi(\vec{\gamma}, \vec{\beta})\rangle$ over $p$ layers:
1. **Initial State:** Uniform superposition over all $K$ qubits:
   $$|\psi_0\rangle = H^{\otimes K} |0\rangle^{\otimes K} = |+\rangle^{\otimes K}$$
2. **Cost Layer:** $U(C, \gamma_l) = \exp(-i \gamma_l H_C)$
   - Implemented via single-qubit $R_Z(2 \gamma_l h_k)$ and two-qubit $CX \to R_Z(2 \gamma_l J_{jk}) \to CX$.
3. **Mixer Layer:** $U(M, \beta_l) = \exp(-i \beta_l H_M)$ where $H_M = \sum_{k=1}^K X_k$
   - Implemented via single-qubit $R_X(2 \beta_l)$ on every qubit.
4. **Classical Optimization:**
   The expectation value $\langle \psi(\vec{\gamma}, \vec{\beta}) | H_C | \psi(\vec{\gamma}, \vec{\beta}) \rangle$ is minimized using the classical `COBYLA` optimizer over parameters $(\vec{\gamma}, \vec{\beta})$.
5. **Measurement:**
   The circuit is measured across $N_{\text{shots}}$ on Qiskit Aer, yielding bitstring samples. The candidate with minimum QUBO energy is decoded and checked by the universal constraint validator.

---

## 6. Scientific Limitations & Disclosure
1. **Classical Simulation Overhead:** Qiskit Aer simulates quantum states classically using matrix representations. Statevector simulation scales exponentially ($O(2^K)$) in memory and CPU time.
2. **No Quantum Advantage Claim:** This project does not claim quantum advantage over classical integer programming. Current noisy intermediate-scale quantum (NISQ) devices and simulators are used to demonstrate algorithmic formulations and comparative feasibility.
3. **Synthetic Coordinates:** All road networks, transit calculations, and disaster coordinates are synthetic approximations.
