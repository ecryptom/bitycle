from strategies.models import Candle_pattern

# candle1={"color":"red","length":{"above_shadow":[0,5],"body":[90,100],"bottom_shadow":[0,5]},"open":{"operation":">","attribute":"close_price"},"close":{"operation":"<","attribute":"open_price"},"high":{"operation":">","attribute":"low_price"},"low":None}
# candle1={"color":"red","length":{"above_shadow":[0,5],"body":[90,100],"bottom_shadow":[0,5]},"open":{"operation":">","attribute":"close_price"},"close":{"operation":"<","attribute":"open_price"},"high":{"operation":">","attribute":"low_price"},"low":None}

candle1={"color":"green","length":{"above_shadow":[0,5],"body":[90,100],"bottom_shadow":[0,5]},"open":None,"close":None,"high":None,"low":None}



for pattern_q in Candle_pattern.objects.all():
    for market in pattern_q.markets.all():
        patterns = pattern_q.get_patterns()
        candle_class = pattern_q.get_candle_class()
        candles = list(candle_class.objects.filter(market=market))[-len(patterns)-1:]

        for i in range(len(patterns)):
            pattern = patterns[i]
            candle = candles[i+1]
            pre_candle = candles[i]

            check = True

            color = 'green' if candle.close_price > candle.open_price else 'red'
            top_body = max(candle.close_price, candle.open_price)
            bottom_body = min(candle.close_price, candle.open_price)

            if pattern['color']:
                if pattern['color'] != color:
                    check = False
                    break

            if pattern['length']:
                length = candle.high_price - candle.low_price
                if pattern['length'].get('above_shadow'):
                    above_shadow = candle.high_price - top_body
                    # print('above_shadow_percent', (above_shadow/length)*100, candle.id)
                    if not (pattern['length']['above_shadow'][0] < (above_shadow/length)*100 < pattern['length']['above_shadow'][1]):
                        check = False
                        break
                if pattern['length'].get('bottom_shadow'):
                    bottom_shadow = bottom_body - candle.low_price
                    # print('bottom_shadow_percent', (bottom_shadow/length)*100)
                    if not (pattern['length']['bottom_shadow'][0] < (bottom_shadow/length)*100 < pattern['length']['bottom_shadow'][1]):
                        check = False
                        break
                if pattern['length'].get('body'):
                    body = top_body - bottom_body
                    # print('body_percent', (body/length)*100)
                    if not (pattern['length']['body'][0] < (body/length)*100 < pattern['length']['body'][1]):
                        check = False
                        break

            if pattern['open']:
                pre_candle_value =  getattr(pre_candle, pattern['open']['attribute'])
                if pattern['open']['operation'] == '>':
                    if pre_candle_value >= candle.open_price:
                        check = False
                        break
                elif pattern['open']['operation'] == '<':
                    if pre_candle_value <= candle.open_price:
                        check = False
                        break

            if pattern['close']:
                pre_candle_value =  getattr(pre_candle, pattern['close']['attribute'])
                if pattern['close']['operation'] == '>':
                    if pre_candle_value >= candle.close_price:
                        check = False
                        break
                elif pattern['close']['operation'] == '<':
                    if pre_candle_value <= candle.close_price:
                        check = False
                        break

            if pattern['high']:
                pre_candle_value =  getattr(pre_candle, pattern['high']['attribute'])
                if pattern['high']['operation'] == '>':
                    if pre_candle_value >= candle.high_price:
                        check = False
                        break
                elif pattern['high']['operation'] == '<':
                    if pre_candle_value <= candle.high_price:
                        check = False
                        break

            if pattern['low']:
                pre_candle_value =  getattr(pre_candle, pattern['low']['attribute'])
                if pattern['low']['operation'] == '>':
                    if pre_candle_value >= candle.low_price:
                        check = False
                        break
                elif pattern['low']['operation'] == '<':
                    if pre_candle_value <= candle.low_price:
                        check = False
                        break



        print(market.name, check)

