from gm.api import *

set_token('20299c0ebc53b8170fe2165dc05fbb12a8008d1f')
arcvideo = history(symbol='SHSE.688039', frequency='1d', 
                   start_time='2025-01-01', end_time='2025-07-01', 
                   fields='open, close, low, high, eob', 
                   adjust = ADJUST_PREV, df = True)
                
hs300 = history('SHSE.000300', frequency='1d', 
                start_time='2025-01-01', end_time='2025-07-01',
                fields='open, close, low, high, eob', 
                adjust = ADJUST_PREV, df = True)
#print(hs300)

hs300[['open', 'close']].plot(figsize=(12, 6), style='-o')