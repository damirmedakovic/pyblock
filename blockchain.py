from hashlib import sha256
import time


class Blockchain:


    def __init__(self):

        self.history = []
        self.pending_transactions = []
        self.history.append(Block(0, time.time(), {}, "0"))



    def new_block(self):

        return Block(len(self.history), time.time(), self.pending_transactions, self.history[-1].hash_block())



    def push_transaction(self, sender_address, reciever_address, amount):

        transaction = Transaction(sender_address, reciever_address, amount)
        self.pending_transactions.append(transaction)


    def last_block(self):
        return self.history[-1]


    def mine(self, difficulty=4, max_iterations=pow(10, 8)):

        mining_block = self.new_block()
        i = 0

        while i < max_iterations:

            i += 1

            if mining_block.hash_block()[0:difficulty] == "0"*difficulty:

                print("New block mined with hash: ")
                print(mining_block.hash_block())
                self.history.append(mining_block)
                self.pending_transactions = []
                return 1

            elif i >= max_iterations:

                print("Max iterations reached. No block was mined.")
                return 0

            else:
                if i % 1000000 == 0:
                    print(f"{i/1000000} million nonces tried...")
                mining_block.block["nonce"] += 1



class Block:

    def __init__(self, index, timestamp, transactions, previous_hash):

        self.block = {"index": index, "timestamp":timestamp, "transactions": transactions, "previous_hash":previous_hash, "nonce": 0}


    def to_string(self):

        print("index: {}, timestamp: {}, previous_hash: {}, nonce: {}".format(self.block["index"], self.block["timestamp"], self.block["previous_hash"], self.block["nonce"]))
        for tr in self.block["transactions"]:
            print(tr.to_string())

    def hash_block(self):

        hashf = sha256()
        hashf.update(str(self.block["nonce"]).encode('utf-8') + str(self.block["index"]).encode('utf-8') + str(self.block["timestamp"]).encode('utf-8') + str(self.block["transactions"]).encode('utf-8') + str(self.block["previous_hash"]).encode('utf-8'))
        return hashf.hexdigest()


class Transaction:

    def __init__(self, sender_address, reciever_address, amount):

        self.sender_address = sender_address
        self.reciever_address = reciever_address
        self.amount = amount


    def to_string(self):

        print(f"sender address: {self.sender_address}, reciever address: {self.reciever_address}, amount: {self.amount}")



if __name__ == "__main__":

    #Testing

    #Create a blockchain with only a genesis block
    blockchain = Blockchain()
    #Mine a couple of blocks and add some transactions
    blockchain.mine()
    blockchain.push_transaction("Me", "You", 5)
    blockchain.mine()
    blockchain.push_transaction("You", "Me", 10)
    blockchain.mine()
    blockchain.mine()
    blockchain.mine()
    #The blockchain now consists of four immutable blocks
    print([x.to_string() for x in blockchain.history[1:]])


