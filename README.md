# Arbitrage bot for Arbitrum chain

This repository uses [brownie-eth](https://eth-brownie.readthedocs.io/en/stable/install.html) and python 3.9.

This arbitrage bot is intended to work on Arbitrum L2 chain.

## Setup

1. Create a .env file containing the deployment addresses for the quoter and router contracts of the protocols used in brownie-config.yaml
2. Add your private key to the .env file

## Usage

1. Deploy the Arbitrage contract with [deploy](scripts/deploy.py)
2. Send the base tokens with [retrieve_tokens](scripts/retrieve_tokens.py) 
3. Approve handlersa using the function approve_handlers in [retrieve_tokens](scripts/retrieve_tokens.py) 
4. Start doing arbitrage with [Arbitrage_detector](scripts/Arbitrage_detector.py)
 



