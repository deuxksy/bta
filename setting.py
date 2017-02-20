from configparser import ConfigParser
import os
import redis

config = ConfigParser()
config.read(os.getenv('ZZIZILY_BTA_CONFIG'))
redis_pool = redis.ConnectionPool(
    host=config['db']['redis.host'],
    port=int(config['db']['redis.port']),
    password=config['db']['redis.password'],
    db=int(config['db']['redis.db']),
)