import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

# Import your modules
from collapse_topology import detect_topological_stress
from narrative_flux import map_narrative_velocity
from liquidity_probe import probe_liquidity_channels
from reflexive_arbiter import evaluate_reflexive_pattern
from execution_core import execute_trade

# Import the main engine
from numpy_funnyword_eh import NarrativeVolatilityEngine, NarrativeAsset

@dataclass
class ArbitrageSignal:
    """Unified arbitrage signal combining narrative and financial data"""
    timestamp: datetime
    narrative_id: str
    financial_asset: str
    signal_type: str  # 'narrative_leads', 'capital_leads', 'divergence'
    strength: float
    expected_profit: float
    risk_score: float
    metadata: Dict[str, Any]

class UnifiedArbitrageSystem:
    """Master system orchestrating narrative-capital arbitrage"""
    
    def __init__(self, narrative_engine: NarrativeVolatilityEngine):
        self.narrative_engine = narrative_engine
        self.active_positions = {}
        self.signal_history = []
        self.pnl_tracker = {
            'realized': 0.0,
            'unrealized': 0.0,
            'positions': []
        }
        
    async def scan_arbitrage_universe(self) -> List[ArbitrageSignal]:
        """Scan for arbitrage opportunities across narrative and capital markets"""
        signals = []
        
        # 1. Get narrative market state
        nvx = self.narrative_engine.calculate_nvx_index()
        narrative_arbs = self.narrative_engine.identify_arbitrage_opportunities()
        
        # 2. Analyze each narrative for capital market divergence
        for narrative in self.narrative_engine.narrative_assets.values():
            # Get narrative metrics
            narrative_data = {
                'id': narrative.id,
                'belief': narrative.belief_penetration,
                'volatility': narrative.volatility_30d,
                'coherence': narrative.coherence_rating
            }
            
            # Run signal generation modules
            topology_signal = detect_topological_stress(narrative_data)
            flux_signal = map_narrative_velocity({'narrative': narrative.content})
            
            # Map to financial assets
            financial_mapping = self.map_narrative_to_financial(narrative)
            
            for asset, correlation in financial_mapping.items():
                # Check for liquidity
                liquidity_signal = probe_liquidity_channels({
                    'asset': asset,
                    'narrative_correlation': correlation
                })
                
                # Generate unified signal
                if self.is_tradeable_divergence(narrative_data, liquidity_signal):
                    signal = ArbitrageSignal(
                        timestamp=datetime.now(),
                        narrative_id=narrative.id,
                        financial_asset=asset,
                        signal_type=self.classify_signal_type(topology_signal, flux_signal),
                        strength=topology_signal['signal_strength'] * flux_signal['memetic_impact'],
                        expected_profit=self.calculate_expected_profit(narrative_data, liquidity_signal),
                        risk_score=topology_signal['entropy'],
                        metadata={
                            'nvx': nvx,
                            'topology': topology_signal,
                            'flux': flux_signal,
                            'liquidity': liquidity_signal
                        }
                    )
                    signals.append(signal)
        
        return sorted(signals, key=lambda x: x.expected_profit, reverse=True)
    
    def map_narrative_to_financial(self, narrative: NarrativeAsset) -> Dict[str, float]:
        """Map narratives to correlated financial assets"""
        mapping = {}
        
        # Example mappings (would be ML-driven in production)
        if "BRICS" in narrative.content or "dollar" in narrative.content:
            mapping['DXY'] = -0.8  # Dollar index negative correlation
            mapping['GLD'] = 0.7   # Gold positive correlation
            mapping['CNY'] = 0.6   # Yuan correlation
            
        if "AI" in narrative.content or "consciousness" in narrative.content:
            mapping['NVDA'] = 0.9  # AI stocks
            mapping['MSFT'] = 0.7
            mapping['GOOGL'] = 0.6
            
        if "collapse" in narrative.content or "corrupt" in narrative.content:
            mapping['VIX'] = 0.8   # Volatility index
            mapping['TLT'] = 0.5   # Bonds (flight to safety)
            mapping['BTC'] = 0.4   # Crypto (alternative system)
            
        return mapping
    
    def is_tradeable_divergence(self, narrative_data: Dict, liquidity_signal: Dict) -> bool:
        """Determine if divergence is large enough to trade"""
        # High narrative volatility + stable liquidity = opportunity
        if narrative_data['volatility'] > 0.3 and liquidity_signal.get('volatility_spike'):
            return True
            
        # Narrative acceleration without price movement = opportunity
        # (Would check actual price data in production)
        return False
    
    def classify_signal_type(self, topology: Dict, flux: Dict) -> str:
        """Classify the type of arbitrage signal"""
        if topology['entropy'] > 0.7 and flux['velocity_index'] > 1.0:
            return 'narrative_leads'  # Narrative change preceding capital
        elif topology['entropy'] < 0.3 and flux['velocity_index'] < 0.5:
            return 'capital_leads'    # Capital movement preceding narrative
        else:
            return 'divergence'       # Complex divergence pattern
    
    def calculate_expected_profit(self, narrative_data: Dict, liquidity_signal: Dict) -> float:
        """Calculate expected profit from arbitrage"""
        base_profit = narrative_data['volatility'] * 1000  # Base on volatility
        
        # Adjust for liquidity
        if liquidity_signal.get('target_zone'):
            base_profit *= 1.5
            
        # Adjust for coherence rating
        rating_multipliers = {'AAA': 0.5, 'AA': 0.7, 'A': 1.0, 'BBB': 1.2, 'BB': 1.5}
        base_profit *= rating_multipliers.get(narrative_data['coherence'], 1.0)
        
        return base_profit
    
    async def execute_arbitrage_strategy(self, signals: List[ArbitrageSignal]):
        """Execute trades based on signals"""
        
        for signal in signals[:5]:  # Top 5 signals
            # Use reflexive arbiter to determine strategy
            strategy = evaluate_reflexive_pattern({
                'signal': signal,
                'market_state': {
                    'nvx': signal.metadata['nvx'],
                    'narrative_positions': len(self.active_positions)
                }
            })
            
            if strategy['confidence'] > 0.7:
                # Build trade package
                trade_package = {
                    'timestamp': datetime.now(),
                    'narrative_id': signal.narrative_id,
                    'financial_asset': signal.financial_asset,
                    'direction': 'long' if signal.signal_type == 'narrative_leads' else 'short',
                    'size': self.calculate_position_size(signal, strategy),
                    'strategy': strategy['strategy'],
                    'metadata': signal.metadata
                }
                
                # Execute trade
                execution_result = execute_trade(trade_package)
                
                if execution_result['status'] == 'executed':
                    self.active_positions[f"{signal.narrative_id}_{signal.financial_asset}"] = {
                        'trade': trade_package,
                        'execution': execution_result,
                        'entry_time': datetime.now()
                    }
                    
                    print(f"✅ Executed: {strategy['strategy']} on {signal.financial_asset}")
                    print(f"   Narrative: {signal.narrative_id}")
                    print(f"   Expected profit: ${signal.expected_profit:.2f}")
    
    def calculate_position_size(self, signal: ArbitrageSignal, strategy: Dict) -> float:
        """Kelly Criterion-based position sizing"""
        # Simplified Kelly: f = (p*b - q) / b
        # where p = win probability, b = win/loss ratio, q = loss probability
        
        win_prob = strategy['confidence']
        loss_prob = 1 - win_prob
        win_loss_ratio = 2.0  # Assume 2:1 reward/risk
        
        kelly_fraction = (win_prob * win_loss_ratio - loss_prob) / win_loss_ratio
        
        # Cap at 25% of capital per position
        position_fraction = min(kelly_fraction, 0.25)
        
        # Adjust for risk score
        position_fraction *= (1 - signal.risk_score)
        
        return position_fraction * 10000  # $10k base capital
    
    async def monitor_and_rebalance(self):
        """Monitor positions and rebalance based on narrative shifts"""
        while True:
            for position_id, position in list(self.active_positions.items()):
                # Check narrative state
                narrative_id = position['trade']['narrative_id']
                narrative = self.narrative_engine.narrative_assets.get(narrative_id)
                
                if narrative:
                    # Check for narrative collapse
                    if narrative.coherence_rating == 'D':
                        print(f"⚠️ Narrative collapsed: {narrative_id}")
                        # Emergency exit
                        self.close_position(position_id, reason='narrative_collapse')
                    
                    # Check for profit target
                    elif self.calculate_position_pnl(position) > position['trade']['size'] * 0.2:
                        print(f"💰 Profit target reached: {position_id}")
                        self.close_position(position_id, reason='profit_target')
            
            await asyncio.sleep(60)  # Check every minute
    
    def calculate_position_pnl(self, position: Dict) -> float:
        """Calculate P&L for a position"""
        # Simplified - would use real price feeds
        time_held = (datetime.now() - position['entry_time']).seconds / 3600
        
        # Simulate P&L based on narrative volatility
        narrative_id = position['trade']['narrative_id']
        narrative = self.narrative_engine.narrative_assets.get(narrative_id)
        
        if narrative:
            pnl = position['trade']['size'] * narrative.volatility_30d * time_held * np.random.normal(0.1, 0.5)
            return pnl
        return 0.0
    
    def close_position(self, position_id: str, reason: str):
        """Close a position and record P&L"""
        position = self.active_positions.pop(position_id)
        pnl = self.calculate_position_pnl(position)
        
        self.pnl_tracker['realized'] += pnl
        self.pnl_tracker['positions'].append({
            'position_id': position_id,
            'pnl': pnl,
            'reason': reason,
            'closed_at': datetime.now()
        })
        
        print(f"📊 Closed {position_id}: ${pnl:.2f} ({reason})")
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'pnl': {
                'realized': self.pnl_tracker['realized'],
                'unrealized': sum(self.calculate_position_pnl(p) for p in self.active_positions.values()),
                'total': self.pnl_tracker['realized'] + sum(self.calculate_position_pnl(p) for p in self.active_positions.values())
            },
            'positions': {
                'active': len(self.active_positions),
                'closed': len(self.pnl_tracker['positions']),
                'win_rate': self.calculate_win_rate()
            },
            'risk_metrics': {
                'max_drawdown': self.calculate_max_drawdown(),
                'sharpe_ratio': self.calculate_sharpe_ratio(),
                'narrative_exposure': self.calculate_narrative_exposure()
            }
        }
    
    def calculate_win_rate(self) -> float:
        """Calculate win rate of closed positions"""
        if not self.pnl_tracker['positions']:
            return 0.0
        wins = sum(1 for p in self.pnl_tracker['positions'] if p['pnl'] > 0)
        return wins / len(self.pnl_tracker['positions'])
    
    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        # Simplified - would track equity curve
        return 0.15  # Placeholder
    
    def calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio"""
        # Simplified - would use actual returns
        return 1.5  # Placeholder
    
    def calculate_narrative_exposure(self) -> Dict[str, float]:
        """Calculate exposure to different narrative categories"""
        exposure = {}
        for position in self.active_positions.values():
            narrative_id = position['trade']['narrative_id']
            narrative = self.narrative_engine.narrative_assets.get(narrative_id)
            if narrative:
                # Categorize narrative
                if "BRICS" in narrative.content:
                    exposure['geopolitical'] = exposure.get('geopolitical', 0) + position['trade']['size']
                elif "AI" in narrative.content:
                    exposure['technology'] = exposure.get('technology', 0) + position['trade']['size']
                elif "collapse" in narrative.content:
                    exposure['systemic_risk'] = exposure.get('systemic_risk', 0) + position['trade']['size']
        
        return exposure

async def run_unified_arbitrage():
    """Run the complete arbitrage system"""
    print("🚀 LAUNCHING UNIFIED NARRATIVE-CAPITAL ARBITRAGE SYSTEM")
    print("=" * 60)
    
    # Initialize narrative engine
    narrative_engine = NarrativeVolatilityEngine()
    
    # Create sample narratives (would be real-time feed in production)
    sample_narratives = [
        "BRICS nations announce new gold-backed currency timeline",
        "AI researchers claim consciousness breakthrough imminent",
        "Federal Reserve hints at unprecedented policy shift",
        "Major tech company faces narrative collapse after scandal",
        "Decentralized governance movement gains institutional backing"
    ]
    
    for i, content in enumerate(sample_narratives):
        narrative = NarrativeAsset(
            id=f"NARR_{i:03d}",
            content=content,
            origin_platform="twitter",
            timestamp=datetime.now(),
            belief_penetration=np.random.uniform(0.2, 0.7),
            liquidity_score=np.random.uniform(0.4, 0.9),
            volatility_30d=np.random.uniform(0.1, 0.5)
        )
        narrative_engine.narrative_assets[narrative.id] = narrative
        narrative_engine.create_liquidity_pool(narrative.id, 50000)
    
    # Initialize arbitrage system
    arbitrage_system = UnifiedArbitrageSystem(narrative_engine)
    
    # Start monitoring task
    monitor_task = asyncio.create_task(arbitrage_system.monitor_and_rebalance())
    
    # Main trading loop
    for cycle in range(10):  # 10 cycles for demo
        print(f"\n📍 ARBITRAGE CYCLE {cycle + 1}")
        print("-" * 40)
        
        # Scan for opportunities
        signals = await arbitrage_system.scan_arbitrage_universe()
        print(f"🔍 Found {len(signals)} arbitrage signals")
        
        if signals:
            # Display top signals
            print("\n📊 Top Arbitrage Opportunities:")
            for signal in signals[:3]:
                print(f"   {signal.narrative_id} <-> {signal.financial_asset}")
                print(f"   Type: {signal.signal_type}")
                print(f"   Expected Profit: ${signal.expected_profit:.2f}")
                print(f"   Risk Score: {signal.risk_score:.2f}")
                print()
            
            # Execute strategies
            await arbitrage_system.execute_arbitrage_strategy(signals)
        
        # Update narrative states (simulate market movement)
        for narrative in narrative_engine.narrative_assets.values():
            # Random walk
            change = np.random.normal(0, 0.03)
            narrative.belief_penetration = max(0.05, min(0.95, narrative.belief_penetration + change))
            narrative.price_history.append(narrative.belief_penetration)
            narrative.volatility_30d = narrative_engine.calculate_narrative_volatility(narrative)
            narrative.coherence_rating = narrative_engine.rate_narrative_coherence(narrative)
        
        # Calculate NVX
        nvx = narrative_engine.calculate_nvx_index()
        print(f"\n📈 NVX Index: {nvx:.2f}")
        
        # Show performance
        if cycle > 0:
            report = arbitrage_system.generate_performance_report()
            print(f"\n💰 Performance Update:")
            print(f"   Total P&L: ${report['pnl']['total']:.2f}")
            print(f"   Active Positions: {report['positions']['active']}")
            print(f"   Win Rate: {report['positions']['win_rate']:.1%}")
        
        await asyncio.sleep(5)  # Wait between cycles
    
    # Final report
    print("\n" + "=" * 60)
    print("📊 FINAL ARBITRAGE REPORT")
    print("=" * 60)
    final_report = arbitrage_system.generate_performance_report()
    print(json.dumps(final_report, indent=2, default=str))
    
    # Cancel monitoring
    monitor_task.cancel()

if __name__ == "__main__":
    asyncio.run(run_unified_arbitrage())