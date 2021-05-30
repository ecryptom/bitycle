import redis, time
from datetime import datetime


redis_db = redis.Redis()

# check is_candle_updater_active flag
t = float(redis_db.get('candle_updater_time'))
if time.time() - t > 600:
    redis_db.set('is_candle_updater_active', 'False')
    print(f'crashed at {datetime.now()}')

