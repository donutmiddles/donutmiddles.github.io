# -*- coding: utf-8 -*-
import time
import re, requests
from caches.main_cache import cache_object
from caches.settings_cache import get_setting, set_many
from modules.utils import copy2clip, make_qrcode
from modules.source_utils import supported_video_extensions, seas_ep_filter, extras
from modules import kodi_utils
# logger = kodi_utils.logger

class OffcloudAPI:
	def __init__(self):
		self.token = get_setting('oc.token')

	def auth(self):
		self.token = ''
		line = '%s[CR]%s[CR]%s'
		response = requests.post('https://offcloud.com/oauth/device/code', timeout=20)
		result = response.json()
		expires_in = result['expires_in']
		user_code = result['user_code']
		auth_url = result.get('verification_uri')
		auth_url_complete = result.get('verification_uri_complete')
		expires_in = result['expires_in']
		sleep_interval = int(result['interval'])
		qr_code = make_qrcode(auth_url_complete) or ''
		copy2clip(auth_url_complete)
		content = 'Authorize Debrid Services[CR]Navigate to: [B]%s[/B][CR]Enter the following code: [B]%s[/B]' % (auth_url, user_code)
		progressDialog = kodi_utils.progress_dialog('OffCloud Authorize', qr_code)
		progressDialog.update(content, 0)
		data = {'device_code': result['device_code'], 'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'}
		start, time_passed = time.time(), 0
		while not progressDialog.iscanceled() and time_passed < expires_in and not self.token:
			kodi_utils.sleep(1000 * sleep_interval)
			response = requests.post('https://offcloud.com/oauth/token', json=data, timeout=20)
			if response.ok:
				try:
					progressDialog.close()
					result = response.json()
					self.token = str(result['access_token'])
				except:
					 ok_dialog(text='Error')
					 break
			else:
				time_passed = time.time() - start
				progress = int(100 * time_passed/float(expires_in))
				progressDialog.update(content, progress)
				continue
		try: progressDialog.close()
		except: pass
		if self.token:
			response = requests.get('https://offcloud.com/api/account/info', params= {'key': self.token}, timeout=20)
			result = response.json()
			set_many([('oc.token', self.token), ('oc.account_id', str(result['user_id'])), ('oc.enabled', 'true')])
			kodi_utils.ok_dialog(text='Success')

	def revoke(self):
		set_many([('oc.token', 'empty_setting'), ('oc.enabled', 'false'), ('oc.account_id', 'empty_setting')])
		kodi_utils.ok_dialog(text='Off Cloud Authorization Reset')

	def _get(self, url):
		response = requests.get('https://offcloud.com/api/' + url, headers=self.headers(), timeout=20)
		try: result = response.json() if 'json' in response.headers.get('Content-Type', '') else response
		except: result = {}
		return result 

	def _post(self, url, post_data=None):
		response = requests.post('https://offcloud.com/api/' + url, json=post_data, headers=self.headers(), timeout=20)
		try: result = response.json() if 'json' in response.headers.get('Content-Type', '') else response
		except: result = {}
		return result 

	def headers(self):
		return {'Authorization': 'Bearer %s' % self.token}

	def account_info(self):
		return self._get('account/info')

	def torrent_info(self, request_id):
		return self._get('cloud/explore/%s?format=detailed' % request_id)

	def user_cloud_info(self, request_id):
		return cache_object(self._get, 'oc_user_cloud_info_%s' % request_id, 'cloud/explore/%s?format=detailed' % request_id, False, 0.03)

	def delete_torrent(self, request_id):
		result = self._get('cloud/remove/%s' % request_id)
		return True if result is not None and result['success'] else False

	def unrestrict_link(self, link):
		return link

	def check_cache(self, hashes):
		return self._post('cache/info', {'urls': ['magnet:?xt=urn:btih:%s' % i for i in hashes]})

	def instant_transfer(self, magnet):
		return self._post('cache/download', {'url': magnet})

	def add_magnet(self, magnet):
		return self._post('cloud', {'url': magnet})

	def create_transfer(self, magnet):
		result = self.add_magnet(magnet)
		return result.get('requestId', '')

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		try:
			file_url = None
			correct_files = []
			append = correct_files.append
			extensions = supported_video_extensions()
			content = self.instant_transfer(magnet_url)
			valid_results = [i for i in content if any(i.get('url').lower().endswith(x) for x in extensions)]
			if len(valid_results) == 0: return
			if season:
				extras_filter = extras()
				episode_title = re.sub(r'[^A-Za-z0-9-]+', '.', title.replace('\'', '').replace('&', 'and').replace('%', '.percent')).lower()
				for item in valid_results:
					if seas_ep_filter(season, episode, item['filename']): append(item)
					if len(correct_files) == 0: continue
					for i in correct_files:
						compare_link = seas_ep_filter(season, episode, i['filename'], split=True)
						compare_link = re.sub(episode_title, '', compare_link)
						if not any(x in compare_link for x in extras_filter):
							file_url = i['url']
							break
			else:
				file_url = max(valid_results, key=lambda x: int(x.get('size'))).get('url', None)
				if not any(file_url.lower().endswith(x) for x in extensions): file_url = None
			if file_url:
				if store_to_cloud: Thread(target=self.create_transfer, args=(magnet_url,)).start()
				return file_url
		except: return None

	def display_magnet_pack(self, magnet_url, info_hash):
		try:
			end_results = []
			append = end_results.append
			extensions = supported_video_extensions()
			content = self.instant_transfer(magnet_url)
			valid_results = [i for i in content if any(i.get('url').lower().endswith(x) for x in extensions)]
			for item in valid_results:
				if any(item.get('url').lower().endswith(x) for x in extensions) and not item.get('url', '') == '':
					try: path = item['filename'].split('/')[-1]
					except: path = item['filename']
					append({'link': item['url'], 'filename': path, 'size': item['size']})
			return end_results
		except: return None


	def user_cloud(self):
		return cache_object(self._get, 'oc_user_cloud', 'cloud/history', False, 0.50)

	def clear_cache(self, clear_hashes=True):
		try:
			from caches.debrid_cache import debrid_cache
			from caches.base_cache import connect_database
			dbcon = connect_database('maincache_db')
			user_cloud_success = False
			# USER CLOUD
			try:
				try:
					cache = dbcon.execute("""SELECT data FROM maincache WHERE id LIKE ?""", ('oc_user_cloud_info_%',)).fetchall()
					user_cloud_info_caches = [eval(i[0])['id'] for i in cache['files']]
				except:
					user_cloud_success = True
				if not user_cloud_success:
					dbcon.execute("""DELETE FROM maincache WHERE id=?""", ('oc_user_cloud',))
					for i in user_cloud_info_caches:
						dbcon.execute("""DELETE FROM maincache WHERE id=?""", ('oc_user_cloud_info_%s' % i,))
					user_cloud_success = True
			except: user_cloud_success = False
			# # DOWNLOAD LINKS
			# try:
			# 	dbcon.execute("""DELETE FROM maincache WHERE id=?""", ('oc_transfers_list',))
			# 	download_links_success = True
			# except: download_links_success = False
			download_links_success = True
			# HASH CACHED STATUS
			if clear_hashes:
				try:
					debrid_cache.clear_debrid_results('oc')
					hash_cache_status_success = True
				except: hash_cache_status_success = False
			else: hash_cache_status_success = True
			# except: return False
			if False in (user_cloud_success, download_links_success, hash_cache_status_success): return False
			return True
		except: return False

Offcloud = OffcloudAPI()

