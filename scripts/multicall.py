from brownie import config,  interface, web3, Contract
from .helpful_scripts import get_max_excluding_none, load_json, find_last_index


QuickABI = load_json("interfaces/quoter.json")
camelotQuoter = Contract.from_abi('quickswapQuoter', config["quoter"]["camelot"], QuickABI)
RamsesQuoter = interface.IQuoterV2(config["quoter"]["ramses"])
uniswapQuoter = interface.IQuoter(config["quoter"]["uniswap"])
sushiswapQuoter = interface.IQuoterV2(config["quoter"]["sushiswap"])
UniswapV2Router = interface.IUniswapV2Router02(config["router"]["UniswapV2"])
SushiswapV2Router = interface.IUniswapV2Router02(config["router"]["SushiswapV2"])
CamelotV2Router = interface.IUniswapV2Router02(config["router"]["CamelotV2"])
TraderJoeQuoter = interface.LBQuoter(config['quoter']['traderjoe'])

Multicall = interface.IMulticall3(config["multicall"])

UniswapV3 =  ["UniswapV3"]
SushiswapV3 = ["SushiswapV3"]
RamsesV3 = ["RamsesV3"]


V2string = ["CamelotV3","UniswapV2", "SushiswapV2", "CamelotV2", "TraderjoeV2"]




fees = [100, 500, 3000, 10000]
fees_l=len(fees)
RamsesFees = [50,100,250,500,3000,10000]



Routers = fees_l*UniswapV3 + fees_l*SushiswapV3  +len(RamsesFees)*RamsesV3 + V2string 

Last_index = find_last_index(Routers)


fees_output = fees*2 + RamsesFees+ [0, 0, 0, 0, 0]

# struct Call3 {
#     // Target contract to call.
#     address target;
#     // If false, the entire call will revert if the call fails.
#     bool allowFailure;
#     // Data to call on the target contract.
#     bytes callData;
# }

n_calls = len(Routers)




def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_prices(tokensIn, tokenOut, amountIn):

    calls = []

    for i, tokenIn in enumerate(tokensIn):
        path = [tokenIn, tokenOut[i]]


        #       UNISWAPV3 CALLS
        for fee in fees:
            encoded = uniswapQuoter.quoteExactInputSingle.encode_input(tokenIn, tokenOut[i], fee, amountIn[i], 0)
            calls.append([uniswapQuoter.address, True, encoded])




        #       SUSHISWAPV3 CALLS
        for fee in fees:
            QuoteExactInputSingleParams =[
                    tokenIn,
                    tokenOut[i],
                    amountIn[i],
                    fee,
                    0
                ]
            encoded = sushiswapQuoter.quoteExactInputSingle.encode_input(QuoteExactInputSingleParams)

            calls.append([sushiswapQuoter.address, True, encoded])

        #       RAMSES V3 CALLS

        for fee in RamsesFees:
            QuoteExactInputSingleParams =[
                tokenIn,
                tokenOut[i],
                amountIn[i],
                fee,
                0
            ]
            encoded = RamsesQuoter.quoteExactInputSingle.encode_input(QuoteExactInputSingleParams)

            calls.append([RamsesQuoter.address, True, encoded])

        #       CAMELOTV3 CALL
            
        encoded = camelotQuoter.quoteExactInputSingle.encode_input(tokenIn, tokenOut[i], amountIn[i], 0)
        calls.append([camelotQuoter.address, True, encoded])


        #       UNISWAP V2 CALL
        encoded = UniswapV2Router.getAmountsOut.encode_input(amountIn[i], path)
        calls.append([UniswapV2Router.address, True, encoded])

        #       QUICKSWAP V2 CALL
        encoded = SushiswapV2Router.getAmountsOut.encode_input(amountIn[i], path)
        calls.append([SushiswapV2Router.address, True, encoded])

        #       CAMELOT V2 CALL

        encoded = CamelotV2Router.getAmountsOut.encode_input(amountIn[i], path)
        calls.append([CamelotV2Router.address, True, encoded])

        #       TRADERJOE V2.1 CALL

        encoded = TraderJoeQuoter.findBestPathFromAmountIn.encode_input(path, amountIn[i])
        calls.append([TraderJoeQuoter.address, True, encoded])


    try:
        results = Multicall.aggregate3.call(calls)
    except Exception as e:
        print(f"Failed Multicall: {e}")
        return False


    

    results = list(chunk(results, n_calls))

    #   Decoding


    all_results = []
    

    for i, tokenIn in enumerate(tokensIn):

        decoded_results = []

        for j, result in enumerate(results[i]):

            if result[0] == False:
                decoded_results.append(None)
                continue

            if j<Last_index["UniswapV3"]+1:
                decoded = uniswapQuoter.quoteExactInputSingle.decode_output(result[1])
                decoded_results.append(decoded)
            elif j<Last_index["SushiswapV3"]+1:
                decoded = sushiswapQuoter.quoteExactInputSingle.decode_output(result[1])
                decoded_results.append(decoded[0])
            elif j<Last_index["RamsesV3"]+1:
                decoded = RamsesQuoter.quoteExactInputSingle.decode_output(result[1])
                decoded_results.append(decoded[0])
            elif j<Last_index["CamelotV3"]+1:
                decoded = camelotQuoter.quoteExactInputSingle.decode_output(result[1])
                decoded_results.append(decoded)
            elif j<Last_index["CamelotV2"]+1:
                decoded = UniswapV2Router.getAmountsOut.decode_output(result[1])
                decoded_results.append(decoded[1])
            else:
                decoded = TraderJoeQuoter.findBestPathFromAmountIn.decode_output(result[1])
                decoded_results.append(decoded[4][1])

            



        all_results.append(decoded_results)
    


    return all_results








def get_max(tokensIn, tokenOut, amountIn, n_base_tokens):

    amountsOut = get_prices(tokensIn, tokenOut, amountIn)


    if amountsOut == False:
        return False
    
    amountsOut = list(chunk(amountsOut, n_base_tokens))
    n_tokens = len(amountsOut)



    #print(amountsOut)

    array_tokens =[]

    for j in range(n_tokens):
        array_base_tokens=[]
        for i in range(n_base_tokens):
            max = get_max_excluding_none(amountsOut[j][i])
            array_max=[]
            if max[1]:
                array_max.append(None)
                array_base_tokens.append(array_max)
                continue
            else:
                index = amountsOut[j][i].index(max[0])
                array_max= [max[0],Routers[index], fees_output[index]]
                array_base_tokens.append(array_max)
        
        array_tokens.append(array_base_tokens)



    return array_tokens


    



