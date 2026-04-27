from src.blockchain import BlockChainClient
import random
import time

def main():
    nodes = [BlockChainClient(f"Node{i}") for i in range(4)]
    for node in nodes:
        node.peers = [p for p in nodes if p != node]
    n = 0
    while n < 20:
        for activeNode in nodes:
            action = random.choice(["send", "mine", "idle"])
            
            if action == "send":
                target = random.choice([n for n in nodes if n != activeNode])
                amount = random.randint(1, 50)
                print(f"{activeNode.name} sending {amount} to {target.name}")
                activeNode.transmitTxn(activeNode.name, target.name, amount)
                
            elif action == "mine":
                activeNode.mine()
                
            elif action == "idle":
                print(f"{activeNode.name} is idling...")
        n += 1        
        print(f"--- End of Cycle: {n} ---")
        time.sleep(2)
