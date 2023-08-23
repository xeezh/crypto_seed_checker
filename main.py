import sys
import asyncio
import configparser
from time import sleep
from chains import BSC, ETH, AVAX, Optimism, Fantom, Polygon, Arbitrum
from address import Address
from concurrent.futures import ProcessPoolExecutor
from loguru import logger


async def thread(seed, token_list, min_tx_count, offset):
    addr = Address.address_from_seed(seed)
    # logger.debug(f'Started -> {addr[0]}')

    chain_list = [
        BSC.BSC(token_list['BSC'], offset),
        ETH.ETH(token_list['ETH'], offset),
        AVAX.AVAX(token_list['AVAX'], offset),
        Optimism.Optimism(token_list['Optimism'], offset),
        Polygon.Polygon(token_list['Polygon'], offset),
        Arbitrum.Arbitrum(token_list['Arbitrum'], offset),
        Fantom.Fantom(token_list['Fantom'], offset)
    ]

    coroutines = []
    for chain in chain_list:
        coroutines.append(chain.get_transactions(addr))

    good = False
    for i in range(len(coroutines)):
        if not good:
            coroutines[i] = await coroutines[i]
            if coroutines[i] > min_tx_count:
                good = True
        else:
            coroutines[i].close()

    if good:
        with open('files/good.txt', 'a', encoding='utf-8') as f:
            f.write(seed + '\n')
            logger.success(f'Good -> {addr[0]}')
    else:
        logger.debug(f'Done -> {addr[0]}')


def wrapper(async_func, *args):
    asyncio.run(async_func(*args))


async def main():
    with open('files/seed.txt', encoding='utf-8') as f:
        seed_list = map(str.rstrip, f.readlines())

    config = configparser.ConfigParser()
    config.read("config.ini")

    token_list = {
        'BSC': config['Tokens']['BSC'],
        'ETH': config['Tokens']['ETH'],
        'AVAX': config['Tokens']['AVAX'],
        'Optimism': config['Tokens']['Optimism'],
        'Polygon': config['Tokens']['Polygon'],
        'Arbitrum': config['Tokens']['Arbitrum'],
        'Fantom': config['Tokens']['Fantom']
    }

    workers = int(config['Params']['threads'])
    offset = int(config['Params']['list_offset'])
    min_tx_count = int(config['Params']['min_tx_count'])
    loop = asyncio.new_event_loop()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for seed in seed_list:
            loop.run_in_executor(executor, wrapper, thread, seed, token_list, min_tx_count, offset)


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | > <white>{message}</white>")
    asyncio.run(main())
    input('\n\nDone!\nPress any key..')
