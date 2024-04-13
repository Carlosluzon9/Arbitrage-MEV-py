import math
import json
import os






def sqrtPricex96toQuote(sqrtPriceX96):
    ratiox192=math.pow(sqrtPriceX96, 2)
    quote=ratiox192/(math.pow(2,192))
    return quote


def find_last_index(data):
  last_seen = {}
  for i, value in enumerate(data):
    last_seen[value] = i  # Update last seen index for the value
  return last_seen





def get_max_excluding_none(data):

  # Filter out None values using filter
  if data == [None]*len(data):
    zeroLength = True
    return [None, zeroLength]
  else:
     zeroLength = False 

  filtered_data = filter(lambda x: x is not None, data)
  filtered_data = list(filtered_data)
  # Use max() on the filtered list, handling potential emptiness
  return [max(filtered_data, default=None), zeroLength]
    


def load_json(ruta):
    ruta_real = os.path.join(os.getcwd(), ruta)
    with open(ruta_real, "r") as f:
        datos = json.load(f)
    return datos

def to_readable_amount(amount, decimals):
   readableAmount= amount/(10**decimals)
   return readableAmount

def from_readable_amount(amount, decimals):
   wei= int(amount * (10**decimals))
   return wei

