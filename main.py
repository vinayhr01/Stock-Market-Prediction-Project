import pandas as pd
import get_stock_CSV as stockcsv
import combine_stocks_CSV as combine_Stocks

stockcsv.download_csv()

combine_Stocks.combine_stocks()