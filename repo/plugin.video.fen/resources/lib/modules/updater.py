# -*- coding: utf-8 -*-
import json
import requests
import shutil
from os import path
from caches.settings_cache import get_setting
from modules.utils import string_alphanum_to_num, unzip
from modules import kodi_utils 
# logger = kodi_utils.logger

def get_location(insert=''):
	username = get_setting('fen.update.username')
	return 'https://github.com/%s/%s.github.io/raw/main/packages/%s' % (username, username, insert)

def get_versions():
	try:
		result = requests.get(get_location('fen_version'))
		if result.status_code != 200: return None, None
		online_version = result.text.replace('\n', '')
		current_version = kodi_utils.addon_version()
		return current_version, online_version
	except: return None, None

def version_check(current_version, online_version):
	return string_alphanum_to_num(current_version) != string_alphanum_to_num(online_version)

def update_check(action=4):
	if action == 3: return
	current_version, online_version = get_versions()
	if not current_version: return
	if not version_check(current_version, online_version):
		if action == 4: return kodi_utils.ok_dialog(heading='Fen Updater', text='Installed Version: [B]%s[/B][CR]Online Version: [B]%s[/B][CR][CR] %s' \
			% (current_version, online_version, '[B]No Update Available[/B]'))
		return
	if action in (0, 4):
		if not kodi_utils.confirm_dialog(heading='Fen Updater', text='Installed Version: [B]%s[/B][CR]Online Version: [B]%s[/B][CR][CR] %s' \
			% (current_version, online_version, '[B]An Update is Available[/B][CR]Perform Update?'), ok_label='Yes', cancel_label='No'): return
	if action == 1: kodi_utils.notification('Fen Update Occuring', icon=kodi_utils.get_icon('downloads'))
	elif action == 2: return kodi_utils.notification('Fen Update Available', icon=kodi_utils.get_icon('downloads'))
	return update_addon(online_version, action)

def rollback_check():
	current_version = get_versions()[0]
	username = get_setting('fen.update.username')
	url = 'https://api.github.com/repos/%s/%s.github.io/contents/packages' % (username, username)
	kodi_utils.show_busy_dialog()
	results = requests.get(url)
	kodi_utils.hide_busy_dialog()
	if results.status_code != 200: return kodi_utils.ok_dialog(heading='Fen Updater', text='Error rolling back.[CR]Please install rollback manually')
	results = results.json()
	results = [i['name'].split('-')[1].replace('.zip', '') for i in results if 'plugin.video.fen' in i['name'] \
				and not i['name'].split('-')[1].replace('.zip', '') == current_version]
	if not results: return kodi_utils.ok_dialog(heading='Fen Updater', text='No previous versions found.[CR]Please install rollback manually')
	results.sort(reverse=True)
	list_items = [{'line1': item, 'icon': kodi_utils.get_icon('downloads')} for item in results]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Choose Rollback Version'}
	rollback_version = kodi_utils.select_dialog(results, **kwargs)
	if rollback_version == None: return
	if not kodi_utils.confirm_dialog(heading='Fen Updater',
		text='Are you sure?[CR]Version [B]%s[/B] will overwrite your current installed version.' % rollback_version): return
	update_addon(rollback_version, 5)

def update_addon(new_version, action):
	kodi_utils.close_all_dialog()
	kodi_utils.execute_builtin('ActivateWindow(Home)', True)
	kodi_utils.notification('Fen Performing Rollback' if action == 5 else 'Fen Performing Update', icon=kodi_utils.get_icon('downloads'))
	zip_name = 'plugin.video.fen-%s.zip' % new_version
	url = get_location(zip_name)
	kodi_utils.show_busy_dialog()
	result = requests.get(url, stream=True)
	kodi_utils.hide_busy_dialog()
	if result.status_code != 200: return kodi_utils.ok_dialog(heading='Fen Updater', text='Error Updating.[CR]Please install new update manually')
	zip_location = path.join(kodi_utils.translate_path('special://home/addons/packages/'), zip_name)
	with open(zip_location, 'wb') as f: shutil.copyfileobj(result.raw, f)
	shutil.rmtree(path.join(kodi_utils.translate_path('special://home/addons/'), 'plugin.video.fen'))
	success = unzip(zip_location, kodi_utils.translate_path('special://home/addons/'), kodi_utils.translate_path('special://home/addons/plugin.video.fen/'))
	kodi_utils.delete_file(zip_location)
	if not success: return kodi_utils.ok_dialog(heading='Fen Updater', text='Error Updating.[CR]Please install new update manually')
	if action in (0, 4, 5):
		success_text = 'rolled back' if action == 5 else 'updated'
		kodi_utils.ok_dialog(heading='Fen Updater', text='[CR]Success.[CR]Fen %s to version [B]%s[/B]' % (success_text, new_version))
	kodi_utils.update_local_addons()
	kodi_utils.disable_enable_addon()
	kodi_utils.update_kodi_addons_db()
	kodi_utils.refresh_widgets()
