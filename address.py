from mnemonic import Mnemonic
from web3 import Web3


class Address:
    @staticmethod
    def address_from_seed(seed):
        w3 = Web3()
        w3.eth.account.enable_unaudited_hdwallet_features()
        a = w3.eth.account.from_mnemonic(seed)
        return [a.address, seed]