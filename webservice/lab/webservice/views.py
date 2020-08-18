import hashlib
import requests

from django.http import HttpResponse
from django.shortcuts import render

from django_redis import get_redis_connection

from webservice.models import Counter as DBCounter

EXPECTED_HASH = '212e12ce208de776bbae0b11b6364a7c14232090acce9e1ffe6f97ded44da8fe'
URL = 'https://raw.githubusercontent.com/jbcurtin/astro-cloud/f45d002566e97007f1bdfa7dce9094ec27c3f912/setup.py'
CACHE = get_redis_connection('default')

def hash_url_content(url: str) -> str:
    response = requests.get(url)
    assert response.status_code == 200
    return hashlib.sha256(response.content).hexdigest()


class CacheCounter:
    def __init__(self, key: str) -> None:
        self._key = key

    def __enter__(self):
        self.count = int(CACHE.get(self._key) or 0)

    def __exit__(self, *args, **kwargs):
        self.count = CACHE.set(self._key, self.count)

    def inc(self):
        self.count = self.count + 1


def counter(request):

    cache_counter = CacheCounter('count')
    with cache_counter:
        initial_cache_count = cache_counter.count

    with cache_counter:
        cache_counter.inc()

    with cache_counter:
        inced_cache_count = cache_counter.count

    db_counter = DBCounter.objects.first()
    if db_counter is None:
        db_counter = DBCounter.objects.create()

    db_initial_count = db_counter.count
    db_counter.inc()
    db_inced_count = db_counter.count

    page_hash = hash_url_content(URL)
    template = f'''
Cache Initial Count: {initial_cache_count}
Cache Inced Count: {inced_cache_count}
DB Initial Count: {db_initial_count}
DB Inced Count: {db_inced_count}
Page Content Hash[{page_hash}]
Page Expected Content Hash[{EXPECTED_HASH}]
Page matches?[{page_hash == EXPECTED_HASH}]
'''
    return HttpResponse(template, content_type='text/plain', status=200)
