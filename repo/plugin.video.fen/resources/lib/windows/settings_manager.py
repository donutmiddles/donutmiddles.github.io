# -*- coding: utf-8 -*-
from caches.base_cache import database_locations
from caches.data_sync_cache import data_sync_by_local_timestamp_wrapper
from windows.base_window import BaseDialog
# from modules.kodi_utils import logger

class SettingsManager(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, *args)
		self.control_id = None
	
	@data_sync_by_local_timestamp_wrapper('settings_db')
	def run(self):
		self.doModal()
		self.clearProperties()

class SettingsManagerFolders(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, *args)

	def run(self):
		self.doModal()
		self.clearProperties()
