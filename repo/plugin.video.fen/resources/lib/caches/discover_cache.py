# -*- coding: utf-8 -*-
from caches.base_cache import connect_database
from caches.data_sync_cache import data_sync_wrapper
# from modules.kodi_utils import logger

class DiscoverCache:
	@data_sync_wrapper('discover_db')
	def insert_one(self, _id, db_type, data):
		dbcon = connect_database('discover_db')
		dbcon.execute('INSERT OR REPLACE INTO discover VALUES (?, ?, ?)', (_id, db_type, data))

	@data_sync_wrapper('discover_db')
	def delete_one(self, _id):
		dbcon = connect_database('discover_db')
		dbcon.execute('DELETE FROM discover where id=?', (_id,))
		dbcon.execute('VACUUM')

	def get_all(self, db_type):
		dbcon = connect_database('discover_db')
		all_lists = reversed(dbcon.execute('SELECT * FROM discover WHERE db_type == ?', (db_type,)).fetchall())
		return [{'id': i[0], 'data': i[2]} for i in all_lists]

	@data_sync_wrapper('discover_db')
	def clear_cache(self, db_type):
		dbcon = connect_database('discover_db')
		dbcon.execute('DELETE FROM discover WHERE db_type=?', (db_type,))
		dbcon.execute('VACUUM')

discover_cache = DiscoverCache()
