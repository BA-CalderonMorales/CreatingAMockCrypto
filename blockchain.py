import hashlib
import time


class Block:
    """This class works in conjunction with the class BlockChain immediately underneath it. It is used as the
    base for what an individual block on the blockchain should be made up of."""

    #  region Constructor - Block
    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        """Constructor for Block class. Executed when a Block class is initiated, just like in any other Python class.\
        :parameter: self, this refers to the instance of the Block class, making it possible to access the methods \
        and the attributes associated with the class.\
        :parameter: index, this keeps track of the position of the block within the blockchain.\
        :parameter: proof_no, this is the number produced during the creation of a new block (called mining).\
        :parameter: prev_hash, this refers to the hash of the previous block within the chain.\
        :parameter: data, this gives a record of all transactions completed, such as the quantity bought.\
        :parameter: timestamp, this places a timestamp for the transactions."""
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    #  endregion

    #  region Method - Calculate_Hash
    @property
    def calculate_hash(self):
        """Generates the hash of the blocks using the values in the constructor. The SHA-256-bit string representing \
        the contents of the block. This is how security is achieved in blockchains. \
        Every block will have a hash and that hash will rely on the previous block. If someone tries to compromise \
        any chain, the other blocks will have invalid hashes, leading to disruption of the entire blockchain network.\
        :parameter: self.index, takes in the index of the currant Block instance. \
        :parameter: self.proof_no, takes in the index of the currant Block instance. \
        :parameter: self.prev_hash, takes in the index of the currant Block instance. \
        :parameter: self.data, takes in the index of the currant Block instance. \
        :parameter: self.timestamp, takes in the index of the currant Block instance. \
        :return: A 256-bit string representing the contents of the block."""
        block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no,
                                              self.prev_hash, self.data,
                                              self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    #  endregion

    #  region Method - REPR_(SELF)
    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
                                               self.prev_hash, self.data,
                                               self.timestamp)

    #  endregion

    #  region Notes
    """
    Ultimately, a block will could look like this:
    "index": 5,
    "proof_no": 30,
    "prev_hash: 5a27587e8a27d6fe376d4fd9b4edc12c8890346579e5cbf558252b25b8257836
    "transactions":[{'sender':'0', 'recipient':'Firstname Lastname','quantity':1}]
    "timestamp": 1691646469.4696169
    """
    #  endregion


class BlockChain:
    """This class will contain an array of blocks that will build up the blockchain."""

    #  region Constructor - BlockChain
    def __init__(self):
        """Constructor for BlockChain class."""
        self.chain = []  # This variable stores all the Blocks.
        self.current_data = []  # This variable keeps all the completed transactions in the block.
        self.nodes = set()  # This variable will store a set of nodes. (i.e. my_set = {1, 2, 3, ...})
        self.construct_genesis()  # This method will take care of constructing the initial block.

    #  endregion

    #  region Method - Construct_Genesis
    def construct_genesis(self):
        """This method helps build the initial block in the chain. This block is special because it \
        symbolizes the start of the blockchain."""
        self.construct_block(proof_no=0, prev_hash=0)

    #  endregion

    #  region Method - Construct_Block
    def construct_block(self, proof_no, prev_hash):
        """This method is used for creating new blocks in the blockchain.
        :parameter: proof_no, Caller method is passing them in inside of construct_genesis. \
        :parameter: prev_hash, Caller method is passing them in inside of construct_genesis. \
        :return: A constructed block object is returned."""
        block = Block(
            index=len(self.chain),  # This represents the length of the blockchain.
            proof_no=proof_no,  # The caller method passes proof_no and prev_hash
            prev_hash=prev_hash,  # The caller method passes proof_no and prev_hash
            data=self.current_data  # This is used to reset the transaction list on the node.
        )
        """
        More on data=self.current_data:
        If a block has been constructed and the transactions allocated to it, the list is reset \
        to ensure that future transactions are added into this list. And, this process will take \
        place continuously. 
        """
        self.current_data = []  # See descriptions above.
        self.chain.append(block)  # This method joins newly constructed blocks to the chain.
        return block

    #  endregion

    #  region Method - New_Data
    def new_data(self, sender, recipient, quantity):
        """The new_data method is used for adding the data of transactions to a block. It's a very simple
        method: it accepts three parameters (sender's details, receiver's details, and quantity) and
        appends the transaction to self.current_data list. Any time a new block is created, this list is
        allocated to that block and reset once more as explained in the construct_block method. Once the
        transaction has been added to the list, the index of the next block to be created is returned. This
        index is calculated by adding 1 to the index of the current block (which is the last in the blockchain).
        The data will assist a user in submitting the transaction in the future.
        """
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    #  endregion

    #  region Method - (static) Check_Validity
    @staticmethod
    def check_validity(block, prev_block):
        """Checks whether the hash of every block is correct. Also verifies if every block points
        points to the right previous block, through comparing the value of their hashes. If everything
        is correct, then it returns True; otherwise, it returns False."""
        if prev_block.index + 1 != block.index:
            return False
        elif prev_block.calculate_hash != block.prev_hash:
            return False
        elif not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False
        elif block.timestamp <= prev_block.timestamp:
            return False
        return True

    #  endregion

    #  region Method - (static) Proof_Of_Work
    @staticmethod
    def proof_of_work(last_proof):
        """This simple algorithm identifies a number f' such that hash(ff') contains 4 leading zeroes
        f is the previous f' - f' is the new proof."""
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1
            return proof_no

    #  endregion

    #  region Method - (static) Verifying_Proof
    @staticmethod
    def verifying_proof(last_proof, proof):
        # verifying the proof: does hash(last_proof, proof) contain 4 leading 0's?
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    #  endregion

    #  region Method - Latest_Block
    def latest_block(self):
        """This helper method returns the latest block in the blockchain. The latest block is actually the
        current block in the chain."""
        return self.chain[-1]

    #  endregion

    #  region Method - Block_Mining
    def block_mining(self, details_miner):
        self.new_data(
            sender="0",
            recipient=details_miner,
            quantity=1
        )
        last_block = self.latest_block()
        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)
        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)
        return vars(block)

    #  endregion

    #  region Method - Create_Node
    def create_node(self, address):
        self.nodes.add(address)
        return True

    #  endregion

    #  region Method - (static) Obtain_Block_Object
    @staticmethod
    def obtain_block_object(block_data):
        """Obtains block object from the block data."""
        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp']
        )
    #  endregion
