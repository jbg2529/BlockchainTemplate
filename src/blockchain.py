from src.lib.block import Block

#PARAMS
difficulty = 3
reward = 10

class BlockChainClient:
    def __init__(self, n: str):
        self.name = n #eventually we'll add public and private keys but for now we work in plaintext
        self.peers = []
        self.mempool = [] #kinda lika a staging area for transactions before they are consolidated into a block
        self.chain = [Block(0, ["Genesis"], "0")]
    
    def transmitTxn(self, fromAdd, toAdd, amt):
        '''
        this function should create a transaction (you can do this in plaintext for now)
        and append it to your mempool and also 'transmit' it to everyone elses mempool.
        '''
        # Create Transaction w/ (sender, reciever, points given)
        transaction = (fromAdd, toAdd, amt)
        # Append Transaction -> mempool
        if transaction not in self.mempool:
            self.mempool.append(transaction)
            for i in range(len(self.peers)):
                # Transmit Transaction
                BlockChainClient(f"Node{i}").mempool.append(transaction)

    def purgeMempool(self, block):
        '''
        You may not need this, but once a block has been mined, you should remove all transactions
        in the block from the mempool.
        '''
        for transaction in block.transactions:
            if transaction in self.mempool:
                self.mempool.remove(transaction)

    def recieveBlock(self, block: Block):
        '''
        The goal here is to verify that the block that this node recieved adheres to 
        the rules of the blockchain (i.e correctly calcukated nonce, right reward, etc.)
        '''
        if block.previousHash != self.chain[-1].hash:
            return

        if block.calculateHash() != block.hash:
            return

        if not block.hash.startswith("0" * difficulty):
            return

        if len(block.transactions) != 11:
            return

        rewardTxn = block.transactions[-1]
        if rewardTxn[0] != "SYSTEM" or rewardTxn[2] != reward:
            return

        self.chain.append(block)
        self.purgeMempool(block)

    def mine(self):
        if len(self.mempool) >= 10:
            print(f"Starting mining process on {self.name}")

            #create a new block, figure out the nonce and transmit it.
            transactions = self.mempool[:10]
            transactions.append(("SYSTEM", self.name, reward))
            newBlock = Block(len(self.chain), transactions, self.chain[-1].hash)

            while not newBlock.hash.startswith("0" * difficulty):
                newBlock.nonce += 1
                newBlock.hash = newBlock.calculateHash()

            self.chain.append(newBlock)
            self.purgeMempool(newBlock)

            for i in self.peers:
                i.recieveBlock(newBlock)
