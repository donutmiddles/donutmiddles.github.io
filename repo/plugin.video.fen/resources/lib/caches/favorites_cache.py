# -*- coding: utf-8 -*-
from caches.base_cache import connect_database
from caches.data_sync_cache import data_sync_wrapper
from modules.utils import sort_for_article
# from modules.kodi_utils import logger

class FavoritesCache:
	@data_sync_wrapper('favorites_db')
	def set_favorite(self, media_type, tmdb_id, title):
		try:
			dbcon = connect_database('favorites_db')
			dbcon.execute('INSERT INTO favorites VALUES (?, ?, ?)', (media_type, str(tmdb_id), title))
			return True
		except: return False

	@data_sync_wrapper('favorites_db')
	def delete_favorite(self, media_type, tmdb_id, title):
		try:
			dbcon = connect_database('favorites_db')
			dbcon.execute('DELETE FROM favorites where db_type=? and tmdb_id=?', (media_type, str(tmdb_id)))
			return True
		except: return False

	@data_sync_wrapper('favorites_db')
	def get_favorites(self, media_type):
		dbcon = connect_database('favorites_db')
		favorites = dbcon.execute('SELECT tmdb_id, title FROM favorites WHERE db_type=?', (media_type,)).fetchall()
		return [{'tmdb_id': str(i[0]), 'title': str(i[1])} for i in favorites]

	def clear_favorites(self, media_type):
		dbcon = connect_database('favorites_db')
		dbcon.execute('DELETE FROM favorites WHERE db_type=?', (media_type,))
		dbcon.execute('VACUUM')

favorites_cache = FavoritesCache()

def get_favorites(media_type, dummy_arg):
	data = favorites_cache.get_favorites(media_type)
	data = sort_for_article(data, 'title')
	return [{'media_id': i['tmdb_id'], 'title': i['title']} for i in data]
