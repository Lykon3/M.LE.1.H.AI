# RAWE Swarm Intelligence System

This system includes:
- ✅ AgentEvolver for real-time personality mutation and breeding
- ✅ MetaLearner and AdversarialMetaLearner for regime detection and stress-testing
- ✅ Weighted voting consensus engine
- ✅ Collective execution with Redis-backed messaging

Run:
```
python scripts/run_collective_rawe.py
```

Make sure your Redis server is live and .env contains your Alpaca API keys.


# RAWE Collective with Consensus Layer

This version includes:

✅ Redis-backed inter-agent communication  
✅ Signal voting + consensus detection  
✅ `ConsensusEngine` that evaluates agreement and triggers actions

---

### Run Instructions

1. Ensure Redis is installed and running.
2. Use `run_collective_rawe.py` to simulate multiple RAWE agents.
3. Plug the consensus engine into your Redis loop using `consensus.py`.

More advanced integrations can include signal scoring, trust weighting, and capital pooling across agent profiles.

# RAWE – Reality Arbitrage Wealth Engine
Integrated into the RicFlairProtocol

## 🔮 Overview
RAWE transforms belief volatility into capital gains. It arbitrages the delay between narrative shifts and financial market reactions using:

- 🧠 **Narrative Entanglement** (Spectral Gap)
- 📉 **Institutional Decay Geometry** (Ricci Curvature)
- 📊 **Liquidity Flow Gradients** (Categorical Gradient Flow)
- 💥 **Position Sizing via Bottleneck Scaling**

## 📦 Modules
- `collapse_topology.py` – Detects entropy and Ricci-based collapse zones
- `narrative_flux.py` – Measures memetic impact via spectral entanglement
- `math_utils.py` – Core mathematical logic for categorical liquidity optimization
- `unified_arbitrage_system.py` – Orchestrates all trades, signal detection, and execution
- `run_rawe.py` – Your launch script

## 🚀 Usage
```bash
python scripts/run_rawe.py
```

## 🔗 Deployment Goals
- Live data integration
- Alpaca/ccxt trade execution
- Streamlit or Terminal control panel

RAWE is real. Capitalize on narrative collapse.

# RAWE-PRIME

Reality Arbitrage Wealth Engine (RAWE) - Core system modules

## Components
- collapse_topology.py: Collapse detection using entropy gradients
- narrative_flux.py: Tracks belief spread and virality
- liquidity_probe.py: Detects synthetic volatility corridors
- execution_core.py: Real-time trade deployment
- reflexive_arbiter.py: Learns and adjusts for narrative reversals
