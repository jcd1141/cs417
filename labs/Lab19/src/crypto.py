"""
Lab 19: API Requests and Caching

Fetch cryptocurrency prices from CoinGecko and cache them locally.
"""

import time
import requests


# CoinGecko API base URL
BASE_URL = "https://api.coingecko.com/api/v3"


def get_price(coin_id: str, api_key: str) -> float:
    """
    Fetch the current USD price of a single cryptocurrency.

    Args:
        coin_id: CoinGecko coin identifier (e.g., "bitcoin", "ethereum")
        api_key: CoinGecko Demo API key

    Returns:
        The current price in USD as a float.

    Raises:
        RuntimeError: If the API response status code is not 200.
    """
    # TODO: Task 1
    # 1. Make a GET request to BASE_URL + "/simple/price"
    #    with params: ids, vs_currencies, x_cg_demo_api_key
    # 2. Check status code — raise RuntimeError if not 200
    # 3. Parse JSON and return the USD price as a float
    url = f"{BASE_URL}/simple/price"

    response = requests.get(
        url,
        params={
            "ids": coin_id,
            "vs_currencies": "usd",
            "x_cg_demo_api_key": api_key
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Request failed with status code {response.status_code}")

    data = response.json()
    return float(data[coin_id]["usd"])


def get_prices_batch(coin_ids: list, api_key: str) -> dict:
    """
    Fetch USD prices for multiple coins in a single API call.

    Args:
        coin_ids: List of CoinGecko coin identifiers
        api_key: CoinGecko Demo API key

    Returns:
        Dictionary mapping coin_id to USD price.
        Example: {"bitcoin": 65432.10, "ethereum": 3456.78}

    Raises:
        RuntimeError: If the API response status code is not 200.
    """
    # TODO: Task 2
    # 1. Join coin_ids into a comma-separated string
    # 2. Make ONE GET request with the joined string as "ids"
    # 3. Check status code
    # 4. Parse JSON and flatten into {coin_id: price} dict
    url = f"{BASE_URL}/simple/price"

    response = requests.get(
        url,
        params={
            "ids": ",".join(coin_ids),
            "vs_currencies": "usd",
            "x_cg_demo_api_key": api_key
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"Request failed with status code {response.status_code}")

    data = response.json()

    return {coin_id: float(data[coin_id]["usd"]) for coin_id in coin_ids}


class CoinCache:
    """
    A time-aware cache for cryptocurrency prices.

    Stores prices with timestamps and serves them back
    until they expire (based on TTL).
    """

    def __init__(self, ttl_seconds: int = 60):
        """
        Initialize the cache.

        Args:
            ttl_seconds: How many seconds a cached entry stays fresh.
        """
        self.ttl_seconds = ttl_seconds
        self._store = {}
        self.hits = 0
        self.misses = 0

    def put(self, coin_id: str, price: float):
        """
        Store a price in the cache with a timestamp.

        Args:
            coin_id: The coin identifier
            price: The USD price to cache
        """
        self._store[coin_id] = {
            "price": price,
            "timestamp": time.time()
        }

    def get(self, coin_id: str):
        """
        Retrieve a cached price if it exists and hasn't expired.

        Args:
            coin_id: The coin identifier

        Returns:
            The cached price as a float, or None if not found / expired.
        """
        if coin_id not in self._store:
            self.misses += 1
            return None

        entry = self._store[coin_id]

        if time.time() - entry["timestamp"] > self.ttl_seconds:
            self.misses += 1
            return None

        self.hits += 1
        return entry["price"]

def get_price_cached(coin_id: str, api_key: str, cache: CoinCache) -> float:
    """
    Fetch a coin's price, using the cache when possible.

    Cache-aside pattern:
    1. Check the cache
    2. On hit — return cached price, skip the API
    3. On miss — fetch from API, store in cache, return price

    Args:
        coin_id: CoinGecko coin identifier
        api_key: CoinGecko Demo API key
        cache: A CoinCache instance

    Returns:
        The USD price as a float.
    """
    cached_price = cache.get(coin_id)

    if cached_price is not None:
        return cached_price

    price = get_price(coin_id, api_key)
    cache.put(coin_id, price)
    return price