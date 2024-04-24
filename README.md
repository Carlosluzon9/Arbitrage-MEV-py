This repository uses brownie-eth and python 3.9.

This arbitrage bot is intended to work on Arbitrum L2 chain.

Once you have python 3.9 and brownie-eth installed, you should create an environment file .env with the addresses of the different quoters and routers from DEX's with the names used in brownie-config.yaml

After that, deploy the Arbitrage contract with scripts/deploy.py, send tokens with scripts/retrieve_tokens.py and start doing arbitrage with scripts/Arbitrage_detector.py 



