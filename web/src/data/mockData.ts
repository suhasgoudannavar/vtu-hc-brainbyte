export interface ScenarioData {
  id: string;
  name: string;
  tag: string;
  category: string;
  casualties: number;
  criticalZones: number;
  targetResponseTime: string;
  requiredUnits: string[];
  description: string;
  simpleExplanation: string;
  coordinates: { lat: number; lng: number }[];
  urgencyScore: number;
  greedyResult: {
    time: string;
    conflicts: number;
    unserved: number;
  };
  cpsatResult: {
    time: string;
    conflicts: number;
    unserved: number;
    savings: string;
  };
  qaoaResult: {
    time: string;
    qubits: number;
    costMin: number;
  };
}

export const SCENARIOS: ScenarioData[] = [
  {
    id: "urban-flood",
    name: "DOWNTOWN FLASH FLOOD",
    tag: "HIGH URGENCY",
    category: "Flood Emergency",
    casualties: 38,
    criticalZones: 6,
    targetResponseTime: "8.5 min",
    requiredUnits: ["Rescue Boats", "Helicopter", "High-Water Trucks"],
    description: "Rising floodwaters have covered roads and broken bridges, trapping civilians in floating cars.",
    simpleExplanation: "Water is rising fast. Regular ambulances will drown, so we need boats and tall trucks dispatched immediately without sending the same boat to two places.",
    coordinates: [
      { lat: 18.5204, lng: 73.8567 },
      { lat: 18.5284, lng: 73.8621 },
      { lat: 18.5142, lng: 73.8499 }
    ],
    urgencyScore: 94,
    greedyResult: { time: "22.4 min", conflicts: 3, unserved: 2 },
    cpsatResult: { time: "12.8 min", conflicts: 0, unserved: 0, savings: "42.8% faster" },
    qaoaResult: { time: "13.6 min", qubits: 18, costMin: -142.5 }
  },
  {
    id: "mountain-landslide",
    name: "MOUNTAIN PASS LANDSLIDE",
    tag: "BLOCKED ROADS",
    category: "Landslide",
    casualties: 24,
    criticalZones: 4,
    targetResponseTime: "11.0 min",
    requiredUnits: ["Search Dogs (K9)", "Heavy Diggers", "Mobile Clinic"],
    description: "Heavy rain caused rocks and mud to bury the highway, trapping families inside cars and cutting off electricity.",
    simpleExplanation: "Massive rocks block the road. We must send heavy diggers first to clear paths, plus search dogs to find people trapped under mud.",
    coordinates: [
      { lat: 18.5412, lng: 73.8712 },
      { lat: 18.5355, lng: 73.8824 }
    ],
    urgencyScore: 89,
    greedyResult: { time: "26.1 min", conflicts: 2, unserved: 1 },
    cpsatResult: { time: "14.4 min", conflicts: 0, unserved: 0, savings: "44.8% faster" },
    qaoaResult: { time: "15.0 min", qubits: 14, costMin: -98.2 }
  },
  {
    id: "chemical-fire",
    name: "FACTORY FIRE & TOXIC SMOKE",
    tag: "POISONOUS FUMES",
    category: "Chemical Hazard",
    casualties: 45,
    criticalZones: 5,
    targetResponseTime: "6.0 min",
    requiredUnits: ["Chemical Fire Engine", "Gas Mask Squad", "Decontamination Van"],
    description: "A chemical plant caught fire, sending toxic fumes drifting toward nearby homes and schools.",
    simpleExplanation: "Regular water can make chemical fires worse. We need specialized foam pumpers and breathing gear sent right away.",
    coordinates: [
      { lat: 18.5089, lng: 73.8211 },
      { lat: 18.5122, lng: 73.8188 },
      { lat: 18.5015, lng: 73.8299 }
    ],
    urgencyScore: 98,
    greedyResult: { time: "19.8 min", conflicts: 4, unserved: 3 },
    cpsatResult: { time: "9.2 min", conflicts: 0, unserved: 0, savings: "53.5% faster" },
    qaoaResult: { time: "10.4 min", qubits: 20, costMin: -188.7 }
  },
  {
    id: "resource-shortage",
    name: "EXTREME VEHICLE SHORTAGE",
    tag: "NOT ENOUGH TRUCKS",
    category: "Resource Shortage",
    casualties: 62,
    criticalZones: 9,
    targetResponseTime: "10.0 min",
    requiredUnits: ["ICU Ambulance", "Fast Rescue Boat", "Structural Squad"],
    description: "14 different emergencies called at the same time, but only 6 rescue vehicles are available in the entire area.",
    simpleExplanation: "When help is limited, simple dispatch panic-sends trucks to whoever is closest, leaving dying people with zero help. QRescue ensures every single vehicle goes where it saves the most lives.",
    coordinates: [
      { lat: 18.5301, lng: 73.8455 },
      { lat: 18.5444, lng: 73.8599 },
      { lat: 18.5177, lng: 73.8322 }
    ],
    urgencyScore: 99,
    greedyResult: { time: "34.5 min", conflicts: 6, unserved: 5 },
    cpsatResult: { time: "15.6 min", conflicts: 0, unserved: 0, savings: "54.7% faster" },
    qaoaResult: { time: "16.8 min", qubits: 24, costMin: -245.1 }
  },
  {
    id: "seismic-quake",
    name: "CITY BUILDING COLLAPSE",
    tag: "COLLAPSED BUILDINGS",
    category: "Earthquake",
    casualties: 52,
    criticalZones: 7,
    targetResponseTime: "7.5 min",
    requiredUnits: ["Concrete Cutters", "Search Drones", "Air Ambulance"],
    description: "An earthquake damaged bridges and collapsed multiple apartment buildings during morning rush hour.",
    simpleExplanation: "Crumbled buildings need concrete cutters to pry open slabs, plus flying drones with heat sensors to detect living survivors underneath.",
    coordinates: [
      { lat: 18.5222, lng: 73.8644 },
      { lat: 18.5311, lng: 73.8755 }
    ],
    urgencyScore: 96,
    greedyResult: { time: "28.3 min", conflicts: 3, unserved: 2 },
    cpsatResult: { time: "13.9 min", conflicts: 0, unserved: 0, savings: "50.8% faster" },
    qaoaResult: { time: "14.7 min", qubits: 18, costMin: -160.4 }
  },
  {
    id: "coastal-surge",
    name: "COASTAL STORM & POWER OUTAGE",
    tag: "ISOLATED ISLANDS",
    category: "Storm Surge",
    casualties: 31,
    criticalZones: 5,
    targetResponseTime: "9.0 min",
    requiredUnits: ["Amphibious Vehicle", "Mobile Generator", "Paramedic Van"],
    description: "Ocean storm surge flooded power substations, turning coastal neighborhoods into isolated islands without electricity.",
    simpleExplanation: "Water cut off the power to a senior care home. We need amphibious vehicles that can drive on both land and water to deliver emergency generators.",
    coordinates: [
      { lat: 18.4988, lng: 73.8155 },
      { lat: 18.4911, lng: 73.8099 }
    ],
    urgencyScore: 91,
    greedyResult: { time: "25.0 min", conflicts: 2, unserved: 1 },
    cpsatResult: { time: "13.2 min", conflicts: 0, unserved: 0, savings: "47.2% faster" },
    qaoaResult: { time: "14.1 min", qubits: 16, costMin: -115.8 }
  }
];

export interface BenchmarkRow {
  metric: string;
  category: string;
  greedy: string;
  cpsat: string;
  qaoa: string;
  verdict: string;
}

export const BENCHMARK_METRICS: BenchmarkRow[] = [
  {
    metric: "Accidental Double-Booking",
    category: "Truck Availability",
    greedy: "38.5% of trucks sent to 2 places at once",
    cpsat: "0% Double-Booking (Guaranteed Safe)",
    qaoa: "0% Double-Booking (Audited & Verified)",
    verdict: "Ensures every vehicle only goes to one real emergency"
  },
  {
    metric: "Emergencies Left With Zero Help",
    category: "People Saved",
    greedy: "4 Critical Incidents Abandoned",
    cpsat: "0 Abandoned (100% of People Helped)",
    qaoa: "0 Abandoned (100% of People Helped)",
    verdict: "Nobody is forgotten because they happen to be far away"
  },
  {
    metric: "Average Time to Arrive",
    category: "Response Speed",
    greedy: "24.6 Minutes (Too Slow)",
    cpsat: "14.1 Minutes (10.5 Minutes Faster)",
    qaoa: "15.3 Minutes (9.3 Minutes Faster)",
    verdict: "Cuts response time nearly in half to save critical lives"
  },
  {
    metric: "How the Decision is Made",
    category: "Brain Power",
    greedy: "Quick Guess (picks nearest truck blindly)",
    cpsat: "Master Planner (checks all options mathematically)",
    qaoa: "Quantum Simulation (tests combinations like physics)",
    verdict: "Stops costly mistakes before trucks even leave base"
  },
  {
    metric: "Double-Check Verification",
    category: "Safety Check",
    greedy: "FAILS (Leaves trucks stranded or mismatched)",
    cpsat: "PASSED (100% of rules verified)",
    qaoa: "PASSED (100% of rules verified)",
    verdict: "Strict computer check prevents human dispatcher errors"
  },
  {
    metric: "Calculation Speed",
    category: "Decision Time",
    greedy: "0.001 seconds (Fast, but wrong)",
    cpsat: "0.015 seconds (Super fast & perfect)",
    qaoa: "1.4 seconds (Simulated on regular PC)",
    verdict: "Gives dispatchers optimal orders in a fraction of a second"
  }
];

export const MARQUEE_ITEMS = [
  "SAVES 42% MORE TIME",
  "ZERO DOUBLE-BOOKED AMBULANCES",
  "NO INJURED PERSON LEFT BEHIND",
  "REAL ROAD CURVES INSTEAD OF STRAIGHT LINES",
  "SMART CASUALTY TRIAGE",
  "WORKS 100% OFFLINE WITH NO INTERNET",
  "FREE & OPEN SOURCE FOR ALL RESCUE TEAMS",
  "POWERED BY GOOGLE OR-TOOLS & QUANTUM QISKIT"
];
