# -*- coding: utf-8 -*-
from caches.base_cache import BaseCache
# from modules.kodi_utils import logger

intro_db = BaseCache('intro_db', 'intro_data')

def episode_intros_cache_object(function, url, json=True):
	cache = intro_db.get_no_expiry(url)
	if cache is not None: return cache
	if json: result = function(url).json()
	else: result = function(url)
	intro_db.set_no_expiry(url, result)
	return result