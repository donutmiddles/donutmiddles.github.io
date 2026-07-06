# -*- coding: utf-8 -*-
from caches.base_cache import connect_database, get_timestamp
from caches.data_sync_cache import data_sync_wrapper
# from modules.kodi_utils import logger

class PersonalListsCache:
	@data_sync_wrapper('personal_lists_db')
	def make_list(self, list_name, sort_order):
		try:
			time_stamp = get_timestamp()
			dbcon = connect_database('personal_lists_db')
			dbcon.execute('INSERT OR REPLACE INTO personal_lists VALUES (?, ?, ?, ?, ?, ?)',
						(list_name, repr([]), 0, time_stamp, sort_order, time_stamp))
			return True
		except: return False

	@data_sync_wrapper('personal_lists_db')
	def delete_list(self, list_name):
		try:
			dbcon = connect_database('personal_lists_db')
			dbcon.execute('DELETE FROM personal_lists WHERE name=?', (list_name,))
			dbcon.execute('VACUUM')
			return True
		except: return False

	@data_sync_wrapper('personal_lists_db')
	def delete_list_contents(self, list_name):
		try:
			dbcon = connect_database('personal_lists_db')
			dbcon.execute('UPDATE personal_lists SET contents=?, total=? WHERE name=?', (repr([]), '0', list_name))
			return True
		except: return False

	@data_sync_wrapper('personal_lists_db')
	def update_single_detail(self, set_prop, new_value, list_name):
		try:
			dbcon = connect_database('personal_lists_db')
			dbcon.execute('UPDATE personal_lists SET %s=? WHERE name=?' % set_prop, (new_value, list_name))
		except: pass

	def get_lists(self):
		try:
			dbcon = connect_database('personal_lists_db')
			all_lists = dbcon.execute('SELECT name, total, created, sort_order, updated FROM personal_lists').fetchall()
			return [{'name': str(i[0]), 'total': i[1], 'created_at': i[2], 'sort_order': i[3], 'updated': i[4]} for i in all_lists]
		except: return []

	def get_list(self, list_name, dbcon=None):
		content = []
		try:
			if not dbcon: dbcon = connect_database('personal_lists_db')
			content = eval(dbcon.execute('SELECT contents FROM personal_lists WHERE name=?', (list_name,)).fetchone()[0])
		except: pass
		return content

	@data_sync_wrapper('personal_lists_db')
	def add_remove_list_item(self, list_name, action, new_contents):
		try:
			dbcon = connect_database('personal_lists_db')
			contents = self.get_list(list_name, dbcon=dbcon)
			if action == 'add':
				if [str(i['media_id']) for i in contents if str(new_contents['media_id']) == str(i['media_id'])]: return 'Item Already in [B]%s[/B]' % list_name
				command = 'UPDATE personal_lists SET contents=?, total=total+1, updated=? WHERE name=?'
				contents.append(new_contents)
			else:
				if not [str(i['media_id']) for i in contents if str(new_contents) == str(i['media_id'])]: return 'Item Not in [B]%s[/B]' % list_name
				command = 'UPDATE personal_lists SET contents=?, total=total-1, updated=? WHERE name=?'
				contents = [i for i in contents if not str(i['media_id']) == str(new_contents)]
			dbcon.execute(command, (repr(contents), get_timestamp(), list_name))
			return 'Success'
		except: return 'Error'

personal_lists_cache = PersonalListsCache()
