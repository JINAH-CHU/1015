import time
import pyupbit
import datetime

access = "dk7LxaxOTXx9SxoGQxbBZ2UJ6xsNxfWC6VLPQGFU"
secret = "u3h6PXli0QYtrUd0cBOrKO84iFUvF9xxNfxrBkQJ"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# def get_balance(ticker):
#     """잔고 조회"""
#     balances = upbit.get_balances()
#     for b in balances:
#         if b['currency'] == ticker:
#             if b['balance'] is not None:
#                 return float(b['balance'])
#             else:
#                 return 0
#     return 0

# def get_current_price(ticker):
#     """현재가 조회"""
#     return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        print("현재시각",now)
        start_time = get_start_time("KRW-AXS") # 9시
        #print(start_time)
        end_time = start_time + datetime.timedelta(hours=31)
        print("종료시각",end_time)

        # if 9시부터 다음날 8시 50분 50초
        if now < end_time:
            axs_target_price = get_target_price("KRW-AXS", 0.5)
            xrp_target_price = get_target_price("KRW-XRP", 0.5)
            
            axs_current_price= pyupbit.get_current_price("KRW-AXS")
            xrp_current_price= pyupbit.get_current_price("KRW-XRP")

            print("KRW-AXS target:", axs_target_price)
            print("KRW-AXS current:", axs_current_price)
            print("KRW-XRP target:", xrp_target_price)
            print("KRW-XRP current:", xrp_current_price)
            # current_price = get_current_price("KRW-AXS")

            krw = upbit.get_balance("KRW")
            print("KRW in my account", krw)
            if axs_target_price < axs_current_price:
                if krw > 5000:
                    upbit.buy_market_order("KRW-AXS", 10000)#krw*0.9995) #수수료
                    print("AXS in my account:", upbit.get_balance("AXS"))
            if xrp_target_price < xrp_current_price:
                if krw > 5000:
                    upbit.buy_market_order("KRW-XRP", 10000)     
                    print("XRP in my account:",upbit.get_balance("XRP"))   
        else:
            axs = upbit.get_balance("AXS")
            xrp = upbit.get_balance("XRP")
            if axs > 0.025:
                upbit.sell_market_order("KRW-AXS", axs*0.9995)
            if xrp > 4:
                upbit.sell_market_order("KRW-XRP", xrp*0.9995)
        time.sleep(10)
    except Exception as e:
        print(e)
        time.sleep(1)