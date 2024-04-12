from brownie import accounts, web3, interface, config, Arb


swaptype_string = ["V2V2","V2V3","V3V2","V3V3"]
swaptype_int = [0,1,2,3]

min_pecentage_profit = 0.0015

Arbitrage = interface.Arb(config["Arb"]["polygon-main"]) 
Arbi_est = web3.eth.contract( address = config["Arb"]["polygon-main"], abi = Arb.abi )

def trade(amountIn, maxOut, maxIn, base_token, token1):
    account = accounts.add(config["wallets"]["from_key"])



    V_1st_trade = maxOut[1][-2:]
    V_2nd_trade = maxIn[1][-2:]

    index = swaptype_string.index(V_1st_trade + V_2nd_trade)

    swaptype = swaptype_int[index]

    Router1 = config["router"][maxOut[1]]
    Router2 = config["router"][maxIn[1]]
    tokenIn_Address = web3.toChecksumAddress(base_token["address"])
    tokenOut_Address = web3.toChecksumAddress(token1["address"])
    fee1 = maxOut[2]
    fee2 = maxIn[2]
    amountOutMin1 = 0
    amountOutmin2 = 0

    base_symbol = base_token["symbol"]
    token1_symbol = token1["symbol"]
    profit = maxIn[0]-amountIn

    if "feeOnToken" in token1:
        try:
            estimated_gas = Arbi_est.functions.feeOnToken(Router1, Router2, tokenIn_Address, tokenOut_Address,fee1,fee2, amountIn, amountOutMin1, amountOutmin2, swaptype).estimateGas({"from":account.address})
            profit_min = estimated_gas*base_token["conversion"]*100000000000
        except ValueError as e:
            profit_min = int(min_pecentage_profit*amountIn)
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"Exception: {e}")
            profit_min = int(min_pecentage_profit*amountIn)

        print(f"Profit: {profit}, Profit_min: {profit_min}")

        if profit>profit_min:

            print(f"for {amountIn}{base_symbol} in {maxOut[1]}-> {maxOut[0]} {token1_symbol} in {maxIn[1]} -> {maxIn[0]} {base_symbol}  ")

            try:
                Arbitrage.feeOnToken(Router1, Router2, tokenIn_Address, tokenOut_Address,fee1,fee2, amountIn, amountOutMin1, amountOutmin2, swaptype, {"from":account})
            except ValueError as e:
                print(f'Error:{e}')
            except AttributeError as e:
                print(f'AtributeError: {e}')
            except Exception as e:
                print(f'Exception: {e}')     

            
        # else:
        #     print("Profit not possible because of tx fees")
            
        return

        






    if swaptype == 0: #V2V2SWAP
        try:
            estimated_gas = Arbi_est.functions.V2V2Swap(Router1, Router2, tokenIn_Address, tokenOut_Address, amountIn, amountOutMin1, amountOutmin2).estimateGas({"from":account.address})
            profit_min = estimated_gas*base_token["conversion"]*100000000000
        except ValueError as e:
            profit_min = int(min_pecentage_profit*amountIn)
            print(f"ValueError: {e}")
            
        except Exception as e:
            print(f"Exception: {e}")
            profit_min = int(min_pecentage_profit*amountIn)
            

        print(f"Profit: {profit}, Profit_min: {profit_min}")

        if profit>profit_min:
            
            print(f"for {amountIn}{base_symbol} in {maxOut[1]}-> {maxOut[0]} {token1_symbol} in {maxIn[1]} -> {maxIn[0]} {base_symbol}  ")

            try:
                Arbitrage.V2V2Swap(Router1, Router2, tokenIn_Address, tokenOut_Address, amountIn, amountOutMin1, amountOutmin2, {"from":account})
            except ValueError as e:
                print(f'Error:{e}')
            except AttributeError as e:
                print(f'AtributeError: {e}')
            except Exception as e:
                print(f'Exception: {e}')     

        # else:
        #     print("Profit not possible because of tx fees")

    elif swaptype == 1: #V2V3SWAP
        try:
            estimated_gas = Arbi_est.functions.V2V3Swap(Router1, Router2, tokenIn_Address, tokenOut_Address, fee2,  amountIn, amountOutMin1, amountOutmin2).estimateGas({"from":account.address})
            profit_min = estimated_gas*base_token["conversion"]*100000000000
        except ValueError as e:
            profit_min = int(min_pecentage_profit*amountIn)
            print(f"ValueError: {e}")

        except Exception as e:
            print(f"Exception: {e}")
            profit_min = int(min_pecentage_profit*amountIn)

        print(f"Profit: {profit}, Profit_min: {profit_min}")

        if profit>profit_min:
            print(f"for {amountIn}{base_symbol} in {maxOut[1]}-> {maxOut[0]} {token1_symbol} in {maxIn[1]} -> {maxIn[0]} {base_symbol}  ")
            try:
                Arbitrage.V2V3Swap(Router1, Router2, tokenIn_Address, tokenOut_Address,fee2, amountIn, amountOutMin1, amountOutmin2, {"from":account})
            except ValueError as e:
                print(f'Error:{e}')
            except AttributeError as e:
                print(f'AtributeError: {e}')
            except Exception as e:
                print(f'Exception: {e}')     

        # else:
        #     print("Profit not possible because of tx fees")

    elif swaptype == 2: #V3V2SWAP
        try:
            estimated_gas = Arbi_est.functions.V3V2Swap(Router1, Router2, tokenIn_Address, tokenOut_Address, fee1,  amountIn, amountOutMin1, amountOutmin2).estimateGas({"from":account.address})
            profit_min = estimated_gas*base_token["conversion"]*100000000000
        except ValueError as e:
            profit_min = int(min_pecentage_profit*amountIn)
            print(f"ValueError: {e}")

        except Exception as e:
            print(f"Exception: {e}")
            profit_min = int(min_pecentage_profit*amountIn)

        print(f"Profit: {profit}, Profit_min: {profit_min}")

        if profit>profit_min:
            print(f"for {amountIn}{base_symbol} in {maxOut[1]}-> {maxOut[0]} {token1_symbol} in {maxIn[1]} -> {maxIn[0]} {base_symbol}  ")
            try:
                Arbitrage.V3V2Swap(Router1, Router2, tokenIn_Address, tokenOut_Address,fee1, amountIn, amountOutMin1, amountOutmin2, {"from":account})
            except ValueError as e:
                print(f'Error:{e}')
            except AttributeError as e:
                print(f'AtributeError: {e}')
            except Exception as e:
                print(f'Exception: {e}')     

        # else:
        #     print("Profit not possible because of tx fees")

    elif swaptype == 3: #V3V2SWAP
        try:
            estimated_gas = Arbi_est.functions.V3V3Swap(Router1, Router2, tokenIn_Address, tokenOut_Address, fee1, fee2,  amountIn, amountOutMin1, amountOutmin2).estimateGas({"from":account.address})
            profit_min = estimated_gas*base_token["conversion"]*100000000000
        except ValueError as e:
            profit_min = int(min_pecentage_profit*amountIn)
            print(f"ValueError: {e}")

        except Exception as e:
            print(f"Exception: {e}")
            profit_min = int(min_pecentage_profit*amountIn)

        print(f"Profit: {profit}, Profit_min: {profit_min}")
        
        if profit>profit_min:
            print(f"for {amountIn}{base_symbol} in {maxOut[1]}-> {maxOut[0]} {token1_symbol} in {maxIn[1]} -> {maxIn[0]} {base_symbol}  ")
            try:
                Arbitrage.V3V3Swap(Router1, Router2, tokenIn_Address, tokenOut_Address,fee1,fee2, amountIn, amountOutMin1, amountOutmin2, {"from":account})
            except ValueError as e:
                print(f'Error:{e}')
            except AttributeError as e:
                print(f'AtributeError: {e}')
            except Exception as e:
                print(f'Exception: {e}')     

        # else:
        #     print("Profit not possible because of tx fees")

    




# struct ArbData {
#         address Router1;
#         address Router2;
#         address base_token;
#         address token1;
#         uint256 amountIn;
#         uint256 profit_min;
#         uint8 swaptype;
#         uint24 fee1;
#         uint24 fee2;
#         bool feeOnToken;
#         uint256 amountOutMin1;
#         uint256 amountOutMin2;
#     }


    # ArbData = {"Router1":Router1,
    #            "Router2":Router2,
    #            "base_token":web3.toChecksumAddress(base_token["address"]),
    #            "token1":web3.toChecksumAddress(token1["address"]),
    #            "amountIn":amountIn,
    #            "profit_min":0,   #profit_min
    #            "swaptype":swaptype,
    #            "fee1":maxOut[2],
    #            "fee2":maxIn[2],
    #            "feeOnToken":feeOnToken,
    #            "amountOutMin1":amountOutMin1,
    #            "amountOutMin2":amountOutmin2}
    

    #encoded_input = Arbitrage.swap.encode_input(ArbData)
    # Arbi_est = web3.eth.contract( address = config["Arb"]["polygon-main"], abi = Arb.abi )

    

    # profit = maxIn[0]-amountIn

    # try:
    #     estimated_gas = Arbi_est.functions.swap(ArbData).estimateGas({"from":account.address})
    #     profit_min = estimated_gas*100000000000*base_token["conversion"]
    # except ValueError as e:
    #     profit_min = int(0.0015*amountIn)
    #     print(f"ValueError: {e}")
    #     print(f"profit min: {profit_min}")
    # except Exception as e:
    #     print(f"Exception: {e}")
    #     profit_min = int(0.0015*amountIn)
    #     print(f"profit min: {profit_min}")

    




    # print(f"profit: {profit}, estimated gas: {profit_min}")

    # if profit>profit_min:


    #     ArbData = [Router1,
    #            Router2,
    #            base_token["address"],
    #            token1["address"],
    #            amountIn,
    #            profit_min,   #profit_min
    #            swaptype,
    #            maxOut[2],
    #            maxIn[2],
    #            feeOnToken,
    #            amountOutMin1,
    #            amountOutmin2
    #            ]

    #     try:
    #         tx = Arbitrage.swap(ArbData, {'from':account})
    #         tx.wait(4)
    #     except ValueError as e:
    #         print(f'Error:{e}')
    #     except AttributeError as e:
    #         print(f'AtributeError: {e}')
    #     except Exception as e:
    #         print(f'Exception: {e}')
            
    # else:
    #     print("Profit not possible because of tx fees")


    







