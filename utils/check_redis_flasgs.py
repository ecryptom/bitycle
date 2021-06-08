import redis, time
from datetime import datetime


redis_db = redis.Redis()

# check is_candle_updater_active flag
t = float(redis_db.get('candle_updater_time'))
if time.time() - t > 600:
    redis_db.set('is_candle_updater_active', 'False')
    print(f'1min crashed at {datetime.now()}')


# check is_5min_candle_creator_active flag
t = float(redis_db.get('5min_candle_creator_time'))
if time.time() - t > 25*60:
    redis_db.set('is_5min_candle_creator_active', 'False')
    print(f'5min crashed at {datetime.now()}')


# check is_15min_candle_creator_active flag
t = float(redis_db.get('15min_candle_creator_time'))
if time.time() - t > 25*60:
    redis_db.set('is_15min_candle_creator_active', 'False')
    print(f'15min crashed at {datetime.now()}')


# check is_1hour_candle_creator_active flag
t = float(redis_db.get('1hour_candle_creator_time'))
if time.time() - t > 70*60:
    redis_db.set('is_1hour_candle_creator_active', 'False')
    print(f'1hour crashed at {datetime.now()}')


# check is_4hour_candle_creator_active flag
t = float(redis_db.get('4hour_candle_creator_time'))
if time.time() - t > 250*60:
    redis_db.set('is_4hour_candle_creator_active', 'False')
    print(f'4hour crashed at {datetime.now()}')


# check is_1day_candle_creator_active flag
t = float(redis_db.get('1day_candle_creator_time'))
if time.time() - t > 25*3600:
    redis_db.set('is_1day_candle_creator_active', 'False')
    print(f'1day crashed at {datetime.now()}')


# check is_1week_candle_creator_active flag
t = float(redis_db.get('1week_candle_creator_time'))
if time.time() - t > 8*24*3600:
    redis_db.set('is_1week_candle_creator_active', 'False')
    print(f'1week crashed at {datetime.now()}')
