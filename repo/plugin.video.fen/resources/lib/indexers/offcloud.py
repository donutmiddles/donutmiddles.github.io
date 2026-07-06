# -*- coding: utf-8 -*-
import sys
from apis.offcloud_api import Offcloud
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, normalize
from modules import kodi_utils
# logger = kodi_utils.logger

def oc_cloud():
	def _builder():
		for count, item in enumerate(cloud_files, 1):
			try:
				cm = []
				cm_append = cm.append
				name = clean_file_name(normalize(item['fileName']))
				folder_id = item['requestId']
				delete_params = {'mode': 'offcloud.delete', 'folder_id': folder_id}
				url_params = {'mode': 'offcloud.browse_oc_cloud', 'folder_id': folder_id}
				display = '%02d | [B]FOLDER[/B] | [I]%s [/I]' % (count, name.upper())
				cm_append(('[B]Delete[/B]','RunPlugin(%s)' % kodi_utils.build_url(delete_params)))
				url = kodi_utils.build_url(url_params)
				listitem = kodi_utils.make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
				info_tag = listitem.getVideoInfoTag(True)
				info_tag.setPlot(' ')
				yield (url, listitem, True)
			except: pass
	icon, fanart = kodi_utils.get_icon('offcloud'), kodi_utils.get_addon_fanart()
	try:
		cloud_files = Offcloud.user_cloud()
		cloud_files = [i for i in cloud_files if i['status'] == 'downloaded']
		cloud_files.sort(key=lambda k: k['fileName'])
	except: cloud_files = []
	handle = int(sys.argv[1])
	kodi_utils.add_items(handle, list(_builder()))
	kodi_utils.set_content(handle, 'files')
	kodi_utils.end_directory(handle, cacheToDisc=False)
	kodi_utils.set_view_mode('view.premium')

def browse_oc_cloud(folder_id):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				cm = []
				if '/' in item['path']: name = clean_file_name(item['path'].split('/')[1]).upper()
				else: name = clean_file_name(item['path']).upper()
				size = float(int(item['size']))/1073741824
				display = '%02d | [B]FILE[/B] | %.2f GB | [I]%s [/I]' % (count, size, name)
				url_link = item['url']
				url_params = {'mode': 'playback.video', 'url': url_link, 'obj': 'video'}
				down_file_params = {'mode': 'downloader.runner', 'name': name, 'url': url_link, 'action': 'cloud.offcloud', 'image': icon}
				cm.append(('[B]Download File[/B]','RunPlugin(%s)' % kodi_utils.build_url(down_file_params)))
				url = kodi_utils.build_url(url_params)
				listitem = kodi_utils.make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	icon, fanart = kodi_utils.get_icon('offcloud'), kodi_utils.get_addon_fanart()
	try:
		files = Offcloud.user_cloud_info(folder_id)['files']
		files = [i for i in files if i['path'].lower().endswith(tuple(supported_video_extensions()))]
	except: files = []
	handle = int(sys.argv[1])
	kodi_utils.add_items(handle, list(_builder()))
	kodi_utils.set_content(handle, 'files')
	kodi_utils.end_directory(handle)
	kodi_utils.set_view_mode('view.premium')

def oc_delete(folder_id):
	if not kodi_utils.confirm_dialog(): return
	result = Offcloud.delete_torrent(folder_id)
	if not result: return kodi_utils.ok_dialog(text='Error')
	Offcloud.clear_cache()
	kodi_utils.execute_builtin('Container.Refresh')

def oc_account_info():
	try:
		kodi_utils.show_busy_dialog()
		account_info = Offcloud.account_info()
		customer_id = account_info['user_id']
		expires = account_info['expiration_date']
		premium = account_info['is_premium']
		can_download = account_info['can_download']
		body = []
		append = body.append
		append('[B]Customer ID:[/B] %s' % customer_id)
		append('[B]Expires:[/B] %s' % expires)
		append('[B]Premium:[/B] %s' % premium)
		append('[B]Download Active:[/B] %s' % can_download)
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text('OFFCLOUD', '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()
