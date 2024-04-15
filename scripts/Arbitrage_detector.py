from .helpful_scripts import load_json, from_readable_amount, to_readable_amount
from .multicall import get_max
from .send_transaction import trade
import time



def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]






def analysis():
    base_tokens = load_json('base_tokens_onlyweth.json')
    tokens_arbitrum = load_json('token_list.json')
    tokens_arbitrum_list = list(chunk(tokens_arbitrum["tokens"], 6))
    del tokens_arbitrum


    while True:

        n_base_tokens = len(base_tokens["tokens"])
        
        for token1_list in tokens_arbitrum_list:
            n_token1 = len(token1_list)      
            base_token_addr_list = []
            token1_addr_list = []
            amountsIn =[]

            for token1 in token1_list:

                for token in base_tokens["tokens"]:
                    

                    base_token_addr_list.append(token["address"])
                    amountsIn.append(from_readable_amount(token["amount_min"],token["decimals"]))
                    token1_addr_list.append(token1["address"])

            
            maxOut = get_max(base_token_addr_list, token1_addr_list, amountsIn, n_base_tokens) 

            #print(maxOut)
            if maxOut == False:
                continue

            amountsIn = list(chunk(amountsIn,n_base_tokens))

            amountsIn2 = []

            for j in range(n_token1):
                for i in range(n_base_tokens):
                    amountsIn2.append(maxOut[j][i][0])

            maxIn = get_max(token1_addr_list, base_token_addr_list, amountsIn2, n_base_tokens)

            if maxIn == False:
                continue

            for j, token1 in enumerate(token1_list):
                
                token1_symbol = token1["symbol"]
                token1_decimals = token1["decimals"]

                for i, base_token in enumerate(base_tokens["tokens"]):

            
                    base_symbol = base_token["symbol"]
                    
                    if maxIn[j][i] == [None]:
                        # print(f"No trade found for {token1_symbol}/{base_symbol}")
                        continue
                    
                    
                    readableAmountsIn = to_readable_amount(amountsIn[j][i], base_token["decimals"])
                    readableAmountOut = to_readable_amount(maxOut[j][i][0], token1_decimals)
                    readableAmountIn = to_readable_amount(maxIn[j][i][0], base_token["decimals"])
                    #print(f"For {readableAmountsIn} {base_symbol} in {maxOut[j][i][1]}  you get {readableAmountOut} {token1_symbol}")
                    #print(f"For {readableAmountOut} {token1_symbol} in {maxIn[j][i][1]}  you get {readableAmountIn} {base_symbol}")
                    

                    
                    if maxIn[j][i][0] > amountsIn[j][i]*1.00035:
                        
                        print(f"For {readableAmountsIn} {base_symbol} in {maxOut[j][i][1]}  you get {readableAmountOut} {token1_symbol}")
                        print(f"For {readableAmountOut} {token1_symbol} in {maxIn[j][i][1]}  you get {readableAmountIn} {base_symbol}")
                        trade(amountsIn[j][i], maxOut[j][i], maxIn[j][i], base_token, token1)
                        #readable_profit = to_readable_amount(profit_min, base_decimals)
                        #print(f"MIN PROFIT: {readable_profit}")
        
        time.sleep(0.5)
                    
            
            
            




def main():
    analysis()