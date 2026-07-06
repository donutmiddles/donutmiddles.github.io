# -*- coding: utf-8 -*-
from caches.base_cache import connect_database
from caches.data_sync_cache import data_sync_wrapper
# from modules.kodi_utils import logger

class EpisodeGroupsCache:
	def get(self, tmdb_id):
		try: data = eval(connect_database('episode_groups_db').execute('SELECT data FROM groups_data WHERE tmdb_id = ?', (str(tmdb_id),)).fetchone()[0])
		except: data = {}
		return data

	@data_sync_wrapper('episode_groups_db')
	def set(self, tmdb_id, data):
		connect_database('episode_groups_db').execute('INSERT OR REPLACE INTO groups_data VALUES (?, ?)', (str(tmdb_id), repr(data)))

	@data_sync_wrapper('episode_groups_db')
	def delete(self, tmdb_id):
		dbcon = connect_database('episode_groups_db')
		dbcon.execute('DELETE FROM groups_data where tmdb_id=?', (str(tmdb_id),))
		dbcon.execute('VACUUM')

	@data_sync_wrapper('episode_groups_db')
	def clear_cache(self):
		dbcon = connect_database('episode_groups_db')
		dbcon.execute('DELETE FROM groups_data')
		dbcon.execute('VACUUM')

episode_groups_cache = EpisodeGroupsCache()
