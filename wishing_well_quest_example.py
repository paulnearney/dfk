import logging
import sys
import quest.wishing_well as wishing_well
from web3 import Web3
import time

if __name__ == "__main__":
    log_format = '%(asctime)s|%(name)s|%(levelname)s: %(message)s'

    logger = logging.getLogger("DFK-wishing well quest")
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)

    rpc_server = 'https://api.harmony.one'
    logger.info("Using RPC server " + rpc_server)

    level = wishing_well.quest_level(rpc_server)
    logger.info("Quest level "+str(level))

    hero_id = 1 # <your hero id here>
    stamina = wishing_well.get_current_stamina(hero_id, rpc_server)
    logger.info("Current stamina on hero " + str(hero_id) + ": " + str(stamina))

    with open('<your private key file>') as f:
        private_key = f.readline()
    gas_price_gwei = 10
    
    w3 = Web3(Web3.HTTPProvider(rpc_server))
    account_address = w3.eth.account.privateKeyToAccount(private_key).address
    w3.eth.getTransactionCount(account_address)
    wishing_well.start_quest(hero_id, 5, private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, 30, rpc_server, logger)
    time.sleep(60)
    tx_receipt = wishing_well.complete_quest(hero_id, private_key, w3.eth.getTransactionCount(account_address), gas_price_gwei, 30, rpc_server, logger)

    tears = wishing_well.quest_tears(rpc_server, tx_receipt, logger)
    xp = wishing_well.quest_xp(rpc_server, tx_receipt, logger)
    logger.info("Quest earned " + str(tears) + " tears and " + str(xp) + " xp")


