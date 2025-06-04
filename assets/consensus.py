# consensus.py
import asyncio
import json
from collections import defaultdict

class ConsensusEngine:
    def __init__(self, threshold=3):
        self.signal_votes = defaultdict(list)
        self.threshold = threshold

    async def receive_signal(self, message, redis_conn):
        data = json.loads(message)
        signal_id = f"{data['narrative_id']}_{data['financial_asset']}"
        self.signal_votes[signal_id].append(data['signal_type'])

        if len(self.signal_votes[signal_id]) >= self.threshold:
            print(f"✅ CONSENSUS REACHED on {signal_id}: {self.signal_votes[signal_id]}")
            del self.signal_votes[signal_id]
            await redis_conn.publish("rawe_consensus", json.dumps({"action": "execute", "signal_id": signal_id}))

    async def listen_for_signals(self, redis_conn):
        pubsub = redis_conn.pubsub()
        await pubsub.subscribe("rawe_signals")
        print("🔄 Listening for agent signal broadcasts on 'rawe_signals'...")

        async for message in pubsub.listen():
            if message and message["type"] == "message":
                await self.receive_signal(message["data"], redis_conn)
