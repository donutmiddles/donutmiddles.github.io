# -*- coding: utf-8 -*-
import os
from modules import kodi_utils
from caches.base_cache import database_locations, locations, database_snyc_items
from caches.settings_cache import get_setting, set_setting
from modules.settings import datasync_location, database_sync_included, database_autosync
# logger = kodi_utils.logger

def full_import(params={}):
	silent = params.get('silent', 'true') == 'true'
	for database in database_snyc_items(): import_single(database)
	if not silent: kodi_utils.ok_dialog(heading='Data Sync', text='Import Performed')

def full_export(params={}):
	silent = params.get('silent', 'true') == 'true'
	for database in database_snyc_items(): export_single(database)
	if not silent: kodi_utils.ok_dialog(heading='Data Sync', text='Export Performed')

def full_sync(params={}):
	if not database_autosync(): return
	silent = params.get('silent', 'true') == 'true'
	for database in database_snyc_items():
		file_path, location, sync_included_databases, remote_database_available = data_sync_info(database)
		run_sync, import_first = check_sync_status(database, file_path, location, sync_included_databases, remote_database_available)
		if not run_sync: continue
		if import_first: import_single(database, location)
		export_single(database, location)
	if not silent: kodi_utils.ok_dialog(heading='Data Sync', text='Data Sync Performed')

def import_single(database, location=None):
	if not location:
		file_path, location, sync_included_databases, remote_database_available = data_sync_info(database)
		run_sync, import_first = check_sync_status(database, file_path, location, sync_included_databases, remote_database_available)
		if not run_sync: return
	kodi_utils.copy_file(join_path(location, database_name(database)), database_locations(database))
	set_setting('datasync.%s' % database, str(detect_timestamp(database, location)))

def export_single(database, location=None):
	if not location:
		file_path, location, sync_included_databases, remote_database_available = data_sync_info(database)
		run_sync, import_first = check_sync_status(database, file_path, location, sync_included_databases, remote_database_available)
		if not run_sync: return
	kodi_utils.copy_file(database_locations(database), join_path(location, database_name(database)))
	set_setting('datasync.%s' % database, str(detect_timestamp(database, location)))

def detect_timestamp(database, location=None):
	if location: db_file = join_path(location, database_name(database))
	else: db_file = database_locations(database)
	return kodi_utils.last_modified_time_for_file(db_file)

def join_path(path1, path2):
	return os.path.join(path1, path2)

def path_exists(path):
	return kodi_utils.path_exists(join_path(path, ''))

def database_name(database):
	return locations()[database]

def current_datasync_databases(location):
	try: current_databases = kodi_utils.list_dirs(location)[1]
	except: current_databases = []
	return current_databases

def data_sync_info(database):
	file_path, location, sync_included_databases, remote_database_available = None, None, None, False
	if not database_autosync(): file_path, location, sync_included_databases, remote_database_available
	file_path = datasync_location()
	if not file_path: return file_path, location, sync_included_databases, remote_database_available
	sync_included_databases = database_sync_included()
	if not database in sync_included_databases: return file_path, location, sync_included_databases, remote_database_available
	location = join_path(file_path, 'fen_databases')
	remote_database_available = database in [i for i in sync_included_databases if database_name(i) in current_datasync_databases(location)]
	return file_path, location, sync_included_databases, remote_database_available

def check_sync_status(database, file_path, location, sync_included_databases, remote_database_available):
	import_first = False
	run_sync = not any(x is None for x in [file_path, location, sync_included_databases])
	if run_sync and remote_database_available: import_first = detect_timestamp(database, location) > int(get_setting('fen.datasync.%s' % database))
	return run_sync, import_first

def data_sync_wrapper(database):
	def decorator(func):
		def wrapper(*args, **kwargs):
			perform_sync = kwargs.pop('perform_sync', True)
			if perform_sync:
				file_path, location, sync_included_databases, remote_database_available = data_sync_info(database)
				run_sync, import_first = check_sync_status(database, file_path, location, sync_included_databases, remote_database_available)
				if import_first: import_single(database, location)
			result = func(*args, **kwargs)
			if perform_sync and run_sync: export_single(database, location)
			return result
		return wrapper
	return decorator

def data_sync_by_local_timestamp_wrapper(database):
	def decorator(func):
		def wrapper(*args, **kwargs):
			start_timestamp = detect_timestamp(database)
			result = func(*args, **kwargs)
			end_timestamp = detect_timestamp(database)
			if start_timestamp != end_timestamp:
				file_path, location, sync_included_databases, remote_database_available = data_sync_info(database)
				run_sync, import_first = check_sync_status(database, file_path, location, sync_included_databases, remote_database_available)
				if run_sync: export_single(database, location)
			return result
		return wrapper
	return decorator
