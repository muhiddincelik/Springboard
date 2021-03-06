from datetime import timedelta, datetime
import pandas as pd
import yfinance as yf

report_date = datetime.now().date()

link = 'https://springboardairflow.blob.core.windows.net/airflow/AAPL_2021-03-04_data.csv'


symbol = 'TSLA'
link2 = f'https://springboardairflow.blob.core.windows.net/airflow/{symbol}_{report_date}_data.csv'
df = pd.read_csv(link)
print()



# # Declaring the start date
# start = datetime.now().date() - timedelta(days=1)
# end = datetime.now().date() - timedelta(days=0)
#
#
# # Function to download data from Yahoo Finance
# def download_data(symbol='AAPL'):
#     start_date = datetime.now().date()
#     tsla_df = yf.download(symbol, start=start, end=end, interval='1m')
#     tsla_df.to_csv(f"{symbol}_{start}_data.csv")
#     return print('Done.')
#
#
# if __name__ == '__main__':
#     download_data()
