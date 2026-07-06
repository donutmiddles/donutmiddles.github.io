# -*- coding: utf-8 -*-
from xbmc import Monitor
import json
import inspect
from time import time
from threading import Thread
from caches.data_sync_cache import full_sync
from caches.settings_cache import get_setting, set_setting
from modules import kodi_utils

pause_services_prop = 'fen.pause_services'
firstrun_update_prop = 'fen.firstrun_update'
current_skin_prop = 'fen.current_skin'

class SetAddonConstants:
	def run(self):
		kodi_utils.logger('Fen', 'SetAddonConstants Service Starting')
		import random
		addon_items = [
			('fen.addon_version', kodi_utils.addon_info('version')),
			('fen.addon_path', kodi_utils.addon_info('path')),
			('fen.addon_profile', kodi_utils.translate_path(kodi_utils.addon_info('profile'))),
			('fen.addon_icon', kodi_utils.translate_path(kodi_utils.addon_info('icon'))),
			('fen.addon_fanart', kodi_utils.addon_fanart())
					]
		for item in addon_items: kodi_utils.set_property(*item)
		return kodi_utils.logger('Fen', 'SetAddonConstants Service Finished')

class DatabaseMaintenance:
	def run(self):
		kodi_utils.logger('Fen', 'DatabaseMaintenance Service Starting')
		from caches.base_cache import check_databases_integrity
		check_databases_integrity(silent=True)
		return kodi_utils.logger('Fen', 'DatabaseMaintenance Service Finished')

class SettingsSync:
	def run(self):
		kodi_utils.logger('Fen', 'SettingsSync Service Starting')
		from caches.settings_cache import sync_settings
		sync_settings()
		full_sync()
		return kodi_utils.logger('Fen', 'SettingsSync Service Finished')

class DataSync:
	def run(self):
		kodi_utils.logger('Fen', 'DataSync Service Starting')
		from modules.settings import database_autosync, database_autosync_interval
		monitor, player = kodi_utils.kodi_monitor(), kodi_utils.kodi_player()
		wait_for_abort, is_playing = monitor.waitForAbort, player.isPlayingVideo
		while not monitor.abortRequested():
			sync_interval = database_autosync_interval()
			wait_for_abort(sync_interval)
			if database_autosync():
				while kodi_utils.get_property(pause_services_prop) == 'true' or is_playing(): wait_for_abort(10)
				full_sync()
		try: del monitor
		except: pass
		try: del player
		except: pass
		return kodi_utils.logger('Fen', 'DataSync Service Finished')

class OnUpdateChanges:
	def run(self):
		kodi_utils.logger('Fen', 'OnUpdateChanges Service Starting')
		try:
			for method in list(filter(lambda x: x[0] != 'run', inspect.getmembers(OnUpdateChanges, predicate=inspect.isfunction))):
				if not get_setting('fen.updatechecks.%s' % method[0], 'false') == 'true':
					method[1](self)
					set_setting('updatechecks.%s' % method[0], 'true')
		except: pass
		return kodi_utils.logger('Fen', 'OnUpdateChanges Service Finished')

class CustomWindowsPrepare:
	def run(self):
		kodi_utils.logger('Fen', 'CustomWindowsPrepare Service Starting')
		from windows.base_window import FontUtils, ExtrasUtils
		monitor, player = kodi_utils.kodi_monitor(), kodi_utils.kodi_player()
		wait_for_abort, is_playing = monitor.waitForAbort, player.isPlayingVideo
		kodi_utils.clear_property(current_skin_prop)
		ExtrasUtils().run()
		font_utils = FontUtils()
		while not monitor.abortRequested():
			font_utils.execute_custom_fonts()
			wait_for_abort(20)
		try: del monitor
		except: pass
		try: del player
		except: pass
		return kodi_utils.logger('Fen', 'CustomWindowsPrepare Service Finished')

class UpdateCheck:
	def run(self):
		if kodi_utils.get_property(firstrun_update_prop) == 'true': return
		kodi_utils.logger('Fen', 'UpdateCheck Service Starting')
		from modules.updater import update_check
		from modules.settings import update_action, update_delay
		end_pause = time() + update_delay()
		monitor, player = kodi_utils.kodi_monitor(), kodi_utils.kodi_player()
		wait_for_abort, is_playing = monitor.waitForAbort, player.isPlayingVideo
		while not monitor.abortRequested():
			while time() < end_pause: wait_for_abort(1)
			while kodi_utils.get_property(pause_services_prop) == 'true' or is_playing(): wait_for_abort(1)
			update_check(update_action())
			break
		kodi_utils.set_property(firstrun_update_prop, 'true')
		try: del monitor
		except: pass
		try: del player
		except: pass
		return kodi_utils.logger('Fen', 'UpdateCheck Service Finished')

class WidgetRefresher:
	def run(self):
		kodi_utils.logger('Fen', 'WidgetRefresher Service Starting')
		from time import time
		monitor, player = kodi_utils.kodi_monitor(), kodi_utils.kodi_player()
		wait_for_abort, self.is_playing = monitor.waitForAbort, player.isPlayingVideo
		wait_for_abort(10)
		self.set_next_refresh(time())
		while not monitor.abortRequested():
			try:
				wait_for_abort(10)
				offset = int(get_setting('fen.widget_refresh_timer', '60'))
				if offset != self.offset:
					self.set_next_refresh(time())
					continue
				if self.condition_check(): continue
				if self.next_refresh < time():
					kodi_utils.logger('Fen', 'WidgetRefresher Service - Widgets Refreshed')
					kodi_utils.refresh_widgets()
					self.set_next_refresh(time())
			except: pass
		try: del monitor
		except: pass
		try: del player
		except: pass
		return kodi_utils.logger('Fen', 'WidgetRefresher Service Finished')

	def condition_check(self):
		if not self.external(): return True
		if self.next_refresh == None or self.is_playing() or kodi_utils.get_property(pause_services_prop) == 'true': return True
		if kodi_utils.get_property('fen.window_loaded') == 'true': return True 
		try:
			window_stack = json.loads(kodi_utils.get_property('fen.window_stack'))
			if window_stack or window_stack == []: return True
		except: pass
		return False

	def set_next_refresh(self, _time):
		self.offset = int(get_setting('fen.widget_refresh_timer', '60'))
		if self.offset: self.next_refresh = _time + (self.offset*60)
		else: self.next_refresh = None

	def external(self):
		return 'plugin' not in kodi_utils.get_infolabel('Container.PluginName')

class MainMonitor(Monitor):
	def __init__ (self):
		Monitor.__init__(self)
		self.startServices()

	def startServices(self):
		try: SetAddonConstants().run()
		except Exception as e: kodi_utils.logger('Error SetAddonConstants', str(e))
		try: DatabaseMaintenance().run()
		except Exception as e: kodi_utils.logger('Error DatabaseMaintenance', str(e))
		try: SettingsSync().run()
		except Exception as e: kodi_utils.logger('Error SettingsSync', str(e))
		try: OnUpdateChanges().run()
		except Exception as e: kodi_utils.logger('Error OnUpdateChanges', str(e))
		Thread(target=DataSync().run).start()
		Thread(target=CustomWindowsPrepare().run).start()
		Thread(target=UpdateCheck().run).start()
		Thread(target=WidgetRefresher().run).start()

	def onNotification(self, sender, method, data):
		if method in ('GUI.OnScreensaverActivated', 'System.OnSleep'):
			kodi_utils.set_property(pause_services_prop, 'true')
			kodi_utils.logger('OnNotificationActions', 'PAUSING Fen Services Due to Device Sleep')
		elif method in ('GUI.OnScreensaverDeactivated', 'System.OnWake'):
			kodi_utils.clear_property(pause_services_prop)
			kodi_utils.logger('OnNotificationActions', 'UNPAUSING Fen Services Due to Device Awake')

kodi_utils.logger('Fen', 'Main Monitor Service Starting')
MainMonitor().waitForAbort()
kodi_utils.logger('Fen', 'Main Monitor Service Finished')
