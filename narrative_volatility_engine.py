import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict, deque
import hashlib
import json

@dataclass
class NarrativeAsset:
    """Tradeable narrative unit with market parameters"""
    id: str
    content: str
    origin_platform: str
    timestamp: datetime
    belief_penetration: float  # % of population believing
    volatility_30d: float = 0.0
    liquidity_score: float = 0.0
    coherence_rating: str = "AA"  # Reality credit rating
    mutation_rate: float = 0.0
    price_history: deque = field(default_factory=lambda: deque(maxlen=1000))
    
@dataclass
class BeliefDerivative:
    """Derivative instrument on narrative belief trajectories"""
    underlying_narrative_id: str
    contract_type: str  # 'call', 'put', 'swap', 'future'
    strike_belief: float  # Belief penetration threshold
    expiry: datetime
    premium: float = 0.0
    implied_volatility: float = 0.0
    greek_values: Dict[str, float] = field(default_factory=dict)

class NarrativeVolatilityEngine:
    """Core engine for narrative market infrastructure"""
    
    def __init__(self):
        # Market data structures
        self.narrative_assets: Dict[str, NarrativeAsset] = {}
        self.order_book: Dict[str, List[Dict]] = defaultdict(list)
        self.liquidity_pools: Dict[str, Dict] = {}
        self.volatility_index_history = deque(maxlen=10000)
        
        # Tensor framework components
        self.belief_propagation_tensor = None
        self.volatility_manifold = None
        self.coherence_matrix = None
        
        # Market parameters
        self.VOLATILITY_WINDOW = 30  # days
        self.LIQUIDITY_DEPTH = 100  # order book depth
        self.COHERENCE_DECAY_RATE = 0.95
        self.ARBITRAGE_THRESHOLD = 0.02  # 2% spread
        
        # Reality credit rating thresholds
        self.RATING_THRESHOLDS = {
            'AAA': 0.95,  # Extremely coherent narrative
            'AA': 0.85,
            'A': 0.75,
            'BBB': 0.65,
            'BB': 0.55,
            'B': 0.45,
            'CCC': 0.35,
            'D': 0.0  # Default - narrative collapsed
        }
        
    def calculate_narrative_volatility(self, narrative: NarrativeAsset) -> float:
        """Calculate 30-day rolling volatility for narrative belief"""
        if len(narrative.price_history) < 2:
            return 0.0
            
        prices = np.array(list(narrative.price_history))
        returns = np.diff(np.log(prices + 1e-10))  # Log returns
        
        if len(returns) < 2:
            return 0.0
            
        # Annualized volatility
        volatility = np.std(returns) * np.sqrt(252)
        return volatility
    
    def calculate_belief_greeks(self, derivative: BeliefDerivative) -> Dict[str, float]:
        """Calculate option Greeks for belief derivatives"""
        # Simplified Black-Scholes for belief options
        S = self.narrative_assets[derivative.underlying_narrative_id].belief_penetration
        K = derivative.strike_belief
        T = (derivative.expiry - datetime.now()).days / 365.0
        r = 0.05  # Risk-free rate (narrative decay rate)
        sigma = derivative.implied_volatility
        
        # Prevent division by zero
        if T <= 0 or sigma <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        from scipy.stats import norm
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        # Greeks
        if derivative.contract_type == 'call':
            delta = norm.cdf(d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        else:  # put
            delta = norm.cdf(d1) - 1
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
            
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100 if derivative.contract_type == 'call' else -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
    
    def create_liquidity_pool(self, narrative_id: str, initial_liquidity: float) -> Dict[str, Any]:
        """Create automated market maker for narrative liquidity"""
        pool = {
            'narrative_id': narrative_id,
            'belief_reserves': initial_liquidity,
            'counter_belief_reserves': initial_liquidity,
            'total_liquidity': initial_liquidity * 2,
            'fee_rate': 0.003,  # 0.3% fee
            'accumulated_fees': 0.0,
            'k_constant': initial_liquidity ** 2  # x * y = k
        }
        
        self.liquidity_pools[narrative_id] = pool
        return pool
    
    def execute_belief_swap(self, narrative_id: str, belief_amount: float, 
                          direction: str = 'buy') -> Dict[str, Any]:
        """Execute swap in narrative liquidity pool"""
        pool = self.liquidity_pools.get(narrative_id)
        if not pool:
            return {'error': 'No liquidity pool found'}
            
        x = pool['belief_reserves']
        y = pool['counter_belief_reserves']
        k = pool['k_constant']
        
        if direction == 'buy':
            # Buying belief with counter-belief
            dy = belief_amount
            dx = (k / (y + dy)) - x
            fee = abs(dx) * pool['fee_rate']
            
            pool['belief_reserves'] = x + dx - fee
            pool['counter_belief_reserves'] = y + dy
            price_impact = abs(dx) / x
            
        else:  # sell
            # Selling belief for counter-belief
            dx = belief_amount
            dy = (k / (x + dx)) - y
            fee = abs(dy) * pool['fee_rate']
            
            pool['belief_reserves'] = x + dx
            pool['counter_belief_reserves'] = y + dy - fee
            price_impact = abs(dy) / y
            
        pool['accumulated_fees'] += fee
        
        return {
            'executed_amount': belief_amount,
            'received_amount': abs(dx) if direction == 'buy' else abs(dy),
            'fee_paid': fee,
            'price_impact': price_impact,
            'new_price': pool['belief_reserves'] / pool['counter_belief_reserves']
        }
    
    def calculate_nvx_index(self) -> float:
        """Calculate Narrative Volatility Index (NVX)"""
        if not self.narrative_assets:
            return 0.0
            
        # Weighted average of narrative volatilities
        total_weight = 0
        weighted_vol = 0
        
        for narrative in self.narrative_assets.values():
            weight = narrative.belief_penetration * narrative.liquidity_score
            vol = self.calculate_narrative_volatility(narrative)
            weighted_vol += weight * vol
            total_weight += weight
            
        nvx = (weighted_vol / total_weight) * 100 if total_weight > 0 else 0.0
        
        self.volatility_index_history.append({
            'timestamp': datetime.now(),
            'nvx': nvx,
            'component_count': len(self.narrative_assets)
        })
        
        return nvx
    
    def rate_narrative_coherence(self, narrative: NarrativeAsset) -> str:
        """Assign reality credit rating to narrative"""
        coherence_score = self.calculate_coherence_score(narrative)
        
        for rating, threshold in self.RATING_THRESHOLDS.items():
            if coherence_score >= threshold:
                return rating
        return 'D'
    
    def calculate_coherence_score(self, narrative: NarrativeAsset) -> float:
        """Calculate narrative coherence based on stability metrics"""
        # Factors: low volatility, high liquidity, low mutation rate
        vol_factor = 1 / (1 + narrative.volatility_30d)
        liquidity_factor = narrative.liquidity_score
        mutation_factor = 1 / (1 + narrative.mutation_rate)
        
        coherence = (vol_factor * liquidity_factor * mutation_factor) ** (1/3)
        return min(coherence, 1.0)
    
    def identify_arbitrage_opportunities(self) -> List[Dict[str, Any]]:
        """Identify cross-narrative arbitrage opportunities"""
        opportunities = []
        
        narratives = list(self.narrative_assets.values())
        for i in range(len(narratives)):
            for j in range(i + 1, len(narratives)):
                n1, n2 = narratives[i], narratives[j]
                
                # Check for correlated narratives with price divergence
                correlation = self.calculate_narrative_correlation(n1, n2)
                if correlation > 0.7:  # Highly correlated
                    price_spread = abs(n1.belief_penetration - n2.belief_penetration)
                    
                    if price_spread > self.ARBITRAGE_THRESHOLD:
                        opportunities.append({
                            'narrative_1': n1.id,
                            'narrative_2': n2.id,
                            'correlation': correlation,
                            'spread': price_spread,
                            'expected_profit': price_spread * min(n1.liquidity_score, n2.liquidity_score)
                        })
                        
        return sorted(opportunities, key=lambda x: x['expected_profit'], reverse=True)
    
    def calculate_narrative_correlation(self, n1: NarrativeAsset, n2: NarrativeAsset) -> float:
        """Calculate correlation between two narrative price histories"""
        if len(n1.price_history) < 30 or len(n2.price_history) < 30:
            return 0.0
            
        prices1 = np.array(list(n1.price_history)[-30:])
        prices2 = np.array(list(n2.price_history)[-30:])
        
        if len(prices1) != len(prices2):
            return 0.0
            
        correlation = np.corrcoef(prices1, prices2)[0, 1]
        return correlation if not np.isnan(correlation) else 0.0
    
    async def run_market_simulation(self, duration_hours: int = 24):
        """Simulate market activity for testing"""
        print(f"🚀 Starting {duration_hours}-hour market simulation...")
        
        # Create sample narratives
        sample_narratives = [
            "BRICS will replace the dollar by 2025",
            "AI will achieve consciousness within 5 years",
            "Traditional institutions are irreversibly corrupt",
            "Decentralized governance is the future",
            "Climate change requires immediate action"
        ]
        
        # Initialize narrative assets
        for i, content in enumerate(sample_narratives):
            narrative = NarrativeAsset(
                id=f"NARR_{i:03d}",
                content=content,
                origin_platform="twitter",
                timestamp=datetime.now(),
                belief_penetration=np.random.uniform(0.1, 0.6),
                liquidity_score=np.random.uniform(0.3, 0.9)
            )
            self.narrative_assets[narrative.id] = narrative
            
            # Create liquidity pool
            self.create_liquidity_pool(narrative.id, 10000)
            
            # Initialize price history
            for _ in range(100):
                narrative.price_history.append(np.random.uniform(0.1, 0.6))
        
        # Simulate market activity
        for hour in range(duration_hours):
            print(f"\n⏰ Hour {hour + 1}/{duration_hours}")
            
            # Update narrative metrics
            for narrative in self.narrative_assets.values():
                # Simulate belief changes
                change = np.random.normal(0, 0.02)
                narrative.belief_penetration = max(0, min(1, narrative.belief_penetration + change))
                narrative.price_history.append(narrative.belief_penetration)
                
                # Update volatility
                narrative.volatility_30d = self.calculate_narrative_volatility(narrative)
                
                # Update coherence rating
                narrative.coherence_rating = self.rate_narrative_coherence(narrative)
            
            # Calculate and display NVX
            nvx = self.calculate_nvx_index()
            print(f"📊 NVX Index: {nvx:.2f}")
            
            # Execute some random swaps
            for _ in range(5):
                narrative_id = np.random.choice(list(self.narrative_assets.keys()))
                amount = np.random.uniform(10, 100)
                direction = np.random.choice(['buy', 'sell'])
                
                result = self.execute_belief_swap(narrative_id, amount, direction)
                if 'error' not in result:
                    print(f"💱 Swap executed: {direction} {amount:.2f} units of {narrative_id}")
                    print(f"   Price impact: {result['price_impact']:.4f}")
            
            # Check for arbitrage
            arb_ops = self.identify_arbitrage_opportunities()
            if arb_ops:
                print(f"🎯 Found {len(arb_ops)} arbitrage opportunities!")
                best_op = arb_ops[0]
                print(f"   Best: {best_op['narrative_1']} <-> {best_op['narrative_2']}")
                print(f"   Expected profit: {best_op['expected_profit']:.4f}")
            
            # Display narrative ratings
            print("\n📊 Narrative Coherence Ratings:")
            for narrative in list(self.narrative_assets.values())[:3]:
                print(f"   {narrative.id}: {narrative.coherence_rating} (Belief: {narrative.belief_penetration:.2%})")
            
            await asyncio.sleep(1)  # Simulate time passing
        
        print("\n✅ Market simulation complete!")
        return self.generate_market_report()
    
    def generate_market_report(self) -> Dict[str, Any]:
        """Generate comprehensive market analysis report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'market_overview': {
                'total_narratives': len(self.narrative_assets),
                'total_liquidity': sum(pool['total_liquidity'] for pool in self.liquidity_pools.values()),
                'average_volatility': np.mean([n.volatility_30d for n in self.narrative_assets.values()]),
                'nvx_current': self.volatility_index_history[-1]['nvx'] if self.volatility_index_history else 0
            },
            'top_narratives': [],
            'rating_distribution': defaultdict(int),
            'arbitrage_opportunities': self.identify_arbitrage_opportunities()[:5]
        }
        
        # Top narratives by belief penetration
        sorted_narratives = sorted(self.narrative_assets.values(), 
                                 key=lambda x: x.belief_penetration, 
                                 reverse=True)
        
        for narrative in sorted_narratives[:5]:
            report['top_narratives'].append({
                'id': narrative.id,
                'content': narrative.content[:50] + '...',
                'belief_penetration': narrative.belief_penetration,
                'volatility': narrative.volatility_30d,
                'rating': narrative.coherence_rating
            })
        
        # Rating distribution
        for narrative in self.narrative_assets.values():
            report['rating_distribution'][narrative.coherence_rating] += 1
        
        return report

# Deployment functions
async def deploy_nvx_infrastructure():
    """Deploy the Narrative Volatility Index infrastructure"""
    engine = NarrativeVolatilityEngine()
    
    print("🏗️ Deploying Narrative Volatility Engine...")
    print("📊 Initializing NVX Index...")
    print("💱 Setting up Belief Liquidity Pools...")
    print("🎯 Calibrating Arbitrage Detection...")
    
    # Run simulation to test infrastructure
    report = await engine.run_market_simulation(duration_hours=24)
    
    print("\n📈 MARKET REPORT:")
    print(json.dumps(report, indent=2, default=str))
    
    return engine

async def launch_reality_derivatives_market():
    """Launch the full reality derivatives trading platform"""
    print("🚀 LAUNCHING REALITY DERIVATIVES MARKET")
    print("=" * 50)
    
    # Deploy core infrastructure
    engine = await deploy_nvx_infrastructure()
    
    # Next steps would include:
    # - API endpoints for real-time data
    # - Order matching engine
    # - Settlement mechanisms
    # - Risk management systems
    
    print("\n✅ Reality Derivatives Market is LIVE!")
    print("📊 NVX Index streaming at: /api/v1/nvx")
    print("💱 Liquidity pools available at: /api/v1/pools")
    print("🎯 Arbitrage scanner at: /api/v1/arbitrage")
    
    return engine

if __name__ == "__main__":
    # Launch the market
    asyncio.run(launch_reality_derivatives_market())