import pybroker as pb
from pybroker import Strategy, StrategyConfig, ExecContext
from pybroker.ext.data import AKShare
import numpy as np
from pybroker.indicator import indicator
import pandas as pd

akshare = AKShare()
pb.enable_data_source_cache('akshare')

# df = akshare.query(symbols = ['688039', '688088', '002230'],
#                    start_date = '2025-01-01',
#                    end_date   = '2025-06-09'
#                    )

my_config = StrategyConfig(initial_cash = 50000)
strategy = Strategy(data_source = AKShare(), start_date = '20250101', end_date = '20250609', config = my_config)

def macd_calc(ctx: ExecContext) ->None:
    fast = 12
    slow = 26
    signal = 9
    # print(ctx.symbol, ctx.date, ctx.close)
    ema_fast    = pd.Series(ctx.close).ewm(span = fast, adjust = False).mean()
    ema_slow    = pd.Series(ctx.close).ewm(span = slow, adjust = False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span = signal, adjust = False).mean()
    histogram   = macd_line - signal_line 
    #print(ctx.symbol, pd.to_datetime(ctx.date[-1]).strftime('%Y-%m-%d'), ema_fast.round(2).values, ema_slow.round(2).values, dif.round(2).values)
    return macd_line, signal_line, histogram

def macd_strategy(ctx: ExecContext) ->None:
    pos = ctx.long_pos()
    macd_line, signal_line, histogram = macd_calc(ctx)
    current_macd    = macd_line.iloc[-1]
    previous_macd   = macd_line.iloc[-2]
    current_signal  = signal_line.iloc[-1]
    previous_signal = signal_line.iloc[-2]

    # 金叉买入信号
    if current_macd > current_signal and previous_macd < previous_signal:
        if not pos:
            ctx.buy_shares = ctx.calc_target_shares(0.8)
            #print(f"买入信号: {ctx.symbol} - 日期: {ctx.date}")
    elif current_macd < current_signal and previous_macd > previous_signal:
        if pos:
            ctx.sell_all_shares()
            #print(f"卖出信号: {ctx.symbol} - 日期: {ctx.date}")

#strategy.add_execution(fn = macd_calc, symbols=['688039', '688088', '002230'])
strategy.add_execution(fn = macd_strategy, symbols=['002230'])
result = strategy.backtest(warmup = 2)

print("\n==== 回测结果 ====")
print(result)
print(f"总收益率: {result.metrics.total_return_pct:.2f}%")
print(f"最大回撤: {result.metrics.max_drawdown_pct:.2f}%")
print(f"夏普比率: {result.metrics.sharpe:.2f}")