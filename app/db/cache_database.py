import os
import pickle

from redis import Redis
from sqlalchemy.orm.query import Query


def get_redis() -> Redis | None:
    # return Redis(host='localhost', port='6379', decode_responses=False)
    return Redis.from_url('redis://{name}:{port}'.format(
        name=os.getenv('REDIS_NAME', 'redis'),
        port=os.getenv('REDIS_PORT', '6379')
    ), decode_responses=False)


def delete_cache(keywords: list[str], cache: Redis) -> None:
    for keyword in keywords:
        cache.delete(keyword)


def create_cache(keyword: str, db_data: list[dict[str, str | int]] | Query, cache: Redis) -> None:
    cache.set(keyword, pickle.dumps(db_data))


def read_cache(keyword: str, cache: Redis) -> list[dict[str, str | int]] | None:
    result = cache.get(keyword)
    if result is None:
        return None
    return pickle.loads(result)


def delete_kids_cache(keyword: str, cache: Redis) -> None:
    for i in cache.scan_iter(keyword):
        delete_cache(i, cache)
