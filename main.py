import pandas as pd
import get_stock_CSV as stockcsv
import combine_stocks_CSV as combine_Stocks
import predict

try:
    stockcsv.controller()
except Exception as e:
    pass

combine_Stocks.combine_stocks()

predict.predict()