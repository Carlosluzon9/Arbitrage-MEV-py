# Arbitrage bot for Arbitrum chain

This repository uses [brownie-eth](https://eth-brownie.readthedocs.io/en/stable/install.html) and python 3.9.

This arbitrage bot is intended to work on Arbitrum L2 chain.

Please make sure you understand the code before executing it, it is not commented as of now.

## Setup

1. Create a .env file containing the deployment addresses for the quoter and router contracts of the protocols used in brownie-config.yaml
2. Add your private key to the .env file
3. Configure the arbitrum-main network using brownie networks
4. Set the amount you want to trade with each token in "amount_min" - [base_tokens.json](base_tokens.json) 

## Usage

1. Deploy the Arbitrage contract with [deploy](scripts/deploy.py)  -> brownie run scripts/deploy.py
2. Send the base tokens with [retrieve_tokens](scripts/retrieve_tokens.py) 
3. Approve handlers using the function approve_handlers in [retrieve_tokens](scripts/retrieve_tokens.py) 
4. Start doing arbitrage with [Arbitrage_detector](scripts/Arbitrage_detector.py)  ->brownie run scripts/Arbitrage_detector.py
5. Once done, retrieve tokens with the function retrieve in [retrieve_tokens](scripts/retrieve_tokens.py) 
 



