import hashlib
import time


class Block:

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
