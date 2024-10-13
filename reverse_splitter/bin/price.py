import yfinance as yf

# https://github.com/ranaroussi/yfinance/wiki/Ticker
# https://pypi.org/project/yfinance/
# https://medium.com/@kasperjuunge/yfinance-10-ways-to-get-stock-data-with-python-6677f49e8282

def get_last_prices(tickers=[]):
    data = yf.download(tickers, rounding=True, period='1d', prepost=False)
    res = {}
    for t in tickers:
        try:
            res[t] = str(data['Close'][t].iloc[0])
        except:
            res[t] = 'Error'
        
    return res
        
if __name__ == '__main__':
    print(get_last_prices(['SIFY', 'MSFT', 'GOOG']))