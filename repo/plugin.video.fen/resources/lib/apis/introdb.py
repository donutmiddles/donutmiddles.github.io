# -*- coding: utf-8 -*-
from caches.introdb_cache import episode_intros_cache_object
from modules.kodi_utils import make_session
# from modules.kodi_utils import logger

session = make_session('https://api.introdb.app/')
get_url = 'https://api.introdb.app/segments?imdb_id=%s&season=%s&episode=%s'

class IntroDB:
	def get_data(self, imdb_id, season, episode):
		return episode_intros_cache_object(self._get, get_url % (imdb_id, season, episode))

	def _get(self, url):
		return session.get(url, timeout=5)

episode_intros = IntroDB()
