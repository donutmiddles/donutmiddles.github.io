# -*- coding: utf-8 -*-
import sys
from caches.navigator_cache import navigator_cache as nc
from caches.settings_cache import get_setting, set_setting
from modules import kodi_utils as k, settings as s
# logger = k.logger

class Navigator:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.category_name = self.params_get('name', 'Fen')
		self.list_name = self.params_get('action', 'RootList')
		self.is_external = k.external()
		self.make_listitem = k.make_listitem
		self.build_url = k.build_url
		self.add_item = k.add_item
		self.get_icon = k.get_icon
		self.fanart = k.get_addon_fanart()
		self.run_plugin = 'RunPlugin(%s)'

	def main(self):
		def _process():
			for count, item in enumerate(browse_list):
				try:
					url = self.build_url(item)
					icon = item.get('iconImage', '')
					if not icon.startswith('http'):
						icon = self.get_icon(icon)
						item['iconImage'] = icon
					listitem = self.make_listitem()
					listitem.setLabel(item.get('name', ''))
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon, 'landscape': icon})
					info_tag = listitem.getVideoInfoTag(True)
					info_tag.setPlot(' ')
					if not self.is_external:
						cm_items = [
						('[B]Move[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.move', 'active_list': self.list_name, 'position': count})),
						('[B]Remove[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.remove', 'active_list': self.list_name, 'position': count})),
						('[B]Add Content[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.add', 'active_list': self.list_name, 'position': count})),
						('[B]Restore Menu[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.restore', 'active_list': self.list_name, 'position': count})),
						('[B]Check for New Menu Items[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.update', 'active_list': self.list_name, 'position': count})),
						('[B]Reload Menu[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.reload', 'active_list': self.list_name, 'position': count})),
						('[B]Browse Removed items[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.browse', 'active_list': self.list_name, 'position': count})),
						('[B]Add to Shortcut Folder[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_add_known', 'url': url}))]
						listitem.addContextMenuItems(cm_items)
					yield ((url, listitem, True), count)
				except: pass
		if self.params_get('full_list', 'false') == 'true': browse_list = nc.get_main_lists(self.list_name)[0]
		else: browse_list = nc.currently_used_list(self.list_name)
		results = sorted(list(_process()), key=lambda k: k[1])
		k.add_items(int(sys.argv[1]), [i[0] for i in results])
		self.end_directory()

	def my_lists(self):
		self.add({'mode': 'navigator.discover'}, 'Discover', 'discover')
		self.add({'mode': 'navigator.favorites'}, 'Favorites', 'favorites')
		self.add({'mode': 'navigator.shortcut_folders'}, 'Shortcut Folders', 'folder')
		self.add({'mode': 'personal_lists.get_personal_lists'}, 'Personal Lists', 'lists')
		self.add({'mode': 'navigator.trakt_lists_public'}, 'Trakt Public Lists', 'trakt')
		self.add({'mode': 'navigator.random_lists'}, 'Random Lists', 'random')
		self.end_directory()

	def favorites(self):
		self.add({'mode': 'build_movie_list', 'action': 'favorites_movies', 'name': 'Movies'}, 'Movies', 'movies')
		self.add({'mode': 'build_tvshow_list', 'action': 'favorites_tvshows', 'name': 'TV Shows'}, 'TV Shows', 'tv'),
		self.add({'mode': 'favorite_people_list_image_results', 'isFolder': 'false', 'name': 'People'}, 'People', 'empty_person')
		self.end_directory()

	def trakt_lists_public(self):
		self.add({'mode': 'trakt.list.get_trakt_user_lists', 'list_type': 'trending', 'list_mode': 'personal', 'category_name': 'Trending User Lists'},
				'Trending User Lists', 'trakt')
		self.add({'mode': 'trakt.list.get_trakt_user_lists', 'list_type': 'popular', 'list_mode': 'personal', 'category_name': 'Popular User Lists'},
				'Popular User Lists', 'trakt')
		self.add({'mode': 'trakt.list.get_trakt_user_lists', 'list_type': 'trending', 'list_mode': 'official', 'category_name': 'Trending Official Lists'},
				'Trending Official Lists', 'trakt')
		self.add({'mode': 'trakt.list.get_trakt_user_lists', 'list_type': 'popular', 'list_mode': 'official', 'category_name': 'Popular Official Lists'},
				'Popular Official Lists', 'trakt')
		self.add({'mode': 'navigator.search_history', 'action': 'trakt_lists'}, 'Search User Lists', 'search')
		self.end_directory()

	def discover(self):
		self.add({'mode': 'navigator.discover_contents', 'media_type': 'movie'}, 'Movies', 'movies')
		self.add({'mode': 'navigator.discover_contents', 'media_type': 'tvshow'}, 'TV Shows', 'tv')
		self.end_directory()

	def random_lists(self):
		self.add({'mode': 'navigator.build_random_lists', 'menu_type': 'movie'}, 'Random Movie Lists', 'movies')
		self.add({'mode': 'navigator.build_random_lists', 'menu_type': 'tvshow'}, 'Random TV Show Lists', 'tv')
		self.add({'mode': 'navigator.build_random_lists', 'menu_type': 'personal_lists'}, 'Random Personal Lists', 'lists')
		self.end_directory()

	def people(self):
		self.add({'mode': 'tmdb_people_list_image_results', 'action': 'popular', 'isFolder': 'false', 'name': 'Popular'}, 'Popular', 'popular')
		self.add({'mode': 'tmdb_people_list_image_results', 'action': 'day', 'isFolder': 'false', 'name': 'Trending'}, 'Trending', 'trending')
		self.add({'mode': 'tmdb_people_list_image_results', 'action': 'week', 'isFolder': 'false', 'name': 'Trending This Week'}, 'Trending This Week', 'trending_recent')
		self.end_directory()

	def services(self):
		if s.authorized_debrid_check('rd'): self.add({'mode': 'navigator.real_debrid'}, 'Real Debrid', 'realdebrid')
		if s.authorized_debrid_check('pm'): self.add({'mode': 'navigator.premiumize'}, 'Premiumize', 'premiumize')
		if s.authorized_debrid_check('tb'): self.add({'mode': 'navigator.torbox'}, 'TorBox', 'torbox')
		if s.authorized_debrid_check('oc'): self.add({'mode': 'navigator.offcloud'}, 'Off Cloud', 'offcloud')
		if s.easynews_authorized(): self.add({'mode': 'navigator.easynews'}, 'Easynews', 'easynews')
		self.end_directory()

	def easynews(self):
		self.add({'mode': 'navigator.search_history', 'action': 'easynews_video'}, 'Search Videos', 'search')
		self.add({'mode': 'navigator.search_history', 'action': 'easynews_image'}, 'Search Images', 'search')
		self.add({'mode': 'easynews.account_info', 'isFolder': 'false'}, 'Account Info', 'easynews')
		self.end_directory()

	def real_debrid(self):
		self.add({'mode': 'real_debrid.rd_cloud'}, 'Cloud Storage', 'realdebrid')
		self.add({'mode': 'real_debrid.rd_downloads'}, 'History', 'realdebrid')
		self.add({'mode': 'real_debrid.rd_account_info', 'isFolder': 'false'}, 'Account Info', 'realdebrid')
		self.end_directory()

	def premiumize(self):
		self.add({'mode': 'premiumize.pm_cloud'}, 'Cloud Storage', 'premiumize')
		self.add({'mode': 'premiumize.pm_transfers'}, 'History', 'premiumize')
		self.add({'mode': 'premiumize.pm_account_info', 'isFolder': 'false'}, 'Account Info', 'premiumize')
		self.end_directory()

	def offcloud(self):
		self.add({'mode': 'offcloud.oc_cloud'}, 'Cloud Storage', 'offcloud')
		self.add({'mode': 'offcloud.oc_account_info', 'isFolder': 'false'}, 'Account Info', 'offcloud')
		self.end_directory()

	def torbox(self):
		self.add({'mode': 'torbox.tb_cloud'}, 'Cloud Storage', 'torbox')
		self.add({'mode': 'torbox.tb_account_info', 'isFolder': 'false'}, 'Account Info', 'torbox')
		self.end_directory()

	def search(self):
		self.add({'mode': 'navigator.search_history', 'action': 'movie', 'name': 'Search History Movies'}, 'Search Movies', 'movies')
		self.add({'mode': 'navigator.search_history', 'action': 'tvshow', 'name': 'Search History TV Shows'}, 'Search TV Shows', 'tv')
		self.add({'mode': 'navigator.search_history', 'action': 'people', 'name': 'Search History People'}, 'Search People', 'people')
		self.add({'mode': 'navigator.search_history', 'action': 'tmdb_keyword_movie', 'name': 'Search History Keywords (Movies)'}, 'Search Keywords (Movies)', 'tmdb')
		self.add({'mode': 'navigator.search_history', 'action': 'tmdb_keyword_tvshow', 'name': 'Search History Keywords (TV Shows)'}, 'Search Keywords (TV Shows)', 'tmdb')
		self.add({'mode': 'navigator.search_history', 'action': 'trakt_lists'}, 'Search Trakt User Lists', 'search')
		if s.easynews_authorized():
			self.add({'mode': 'navigator.search_history', 'action': 'easynews_video'}, 'Search Easynews Videos', 'easynews')
			self.add({'mode': 'navigator.search_history', 'action': 'easynews_image'}, 'Search Easynews Images', 'easynews')
		self.end_directory()

	def downloads(self):
		self.add({'mode': 'downloader.manager', 'name': 'Download Manager', 'isFolder': 'false'}, 'Download Manager', 'downloads')
		self.add({'mode': 'downloader.viewer', 'folder_type': 'movie', 'name': 'Movies'}, 'Movies', 'movies')
		self.add({'mode': 'downloader.viewer', 'folder_type': 'episode', 'name': 'TV Shows'}, 'TV Shows', 'tv')
		self.add({'mode': 'downloader.viewer', 'folder_type': 'premium', 'name': 'Premium Files'}, 'Premium Files', 'premium')
		self.add({'mode': 'browser_image', 'folder_path': s.download_directory('image'), 'isFolder': 'false'}, 'Images', 'people')
		self.end_directory()

	def tools(self):
		self.add({'mode': 'navigator.settings_manager'}, 'Settings Utilities', 'settings2')
		self.add({'mode': 'navigator.data_sync_manager'}, 'Data Sync Utilities', 'backup')
		self.add({'mode': 'navigator.update_utils'}, 'Update Utilities', 'settings2')
		self.add({'mode': 'navigator.maintenance'}, 'Database & Cache Maintenance', 'settings2')
		self.add({'mode': 'navigator.log_utils'}, 'Log Utils', 'settings2')
		self.add({'mode': 'navigator.set_view_modes'}, 'Set Views', 'settings2')
		self.add({'mode': 'build_next_episode_manager'}, 'TV Shows Progress Manager', 'settings2')
		self.add({'mode': 'language_invoker_choice', 'isFolder': 'false'}, 'Toggle Language Invoker (ADVANCED!!)', 'settings2')
		self.end_directory()

	def settings_manager(self):
		self.add({'mode': 'open_settings', 'isFolder': 'false'}, 'Open Settings', 'settings')
		self.add({'mode': 'sync_settings', 'silent': 'false', 'isFolder': 'false'}, 'Remake Settings Cache', 'settings')
		self.end_directory()

	def data_sync_manager(self):
		self.add({'mode': 'data_sync_manager.full_sync', 'silent': 'false', 'isFolder': 'false'}, 'Force Data Sync', 'backup')
		self.add({'mode': 'data_sync_manager.full_import', 'silent': 'false', 'isFolder': 'false'}, 'Force Data Import', 'backup')
		self.add({'mode': 'data_sync_manager.full_export', 'silent': 'false', 'isFolder': 'false'}, 'Force Data Export', 'backup')
		self.end_directory()

	def maintenance(self):
		self.add({'mode': 'check_databases_integrity_cache', 'isFolder': 'false'}, 'Check for Corrupt Databases', 'settings2')
		self.add({'mode': 'clean_databases_cache', 'isFolder': 'false'}, 'Clean Databases', 'settings2')
		self.add({'mode': 'clear_all_cache', 'isFolder': 'false'}, 'Clear All Cache (Excluding Favorites)', 'settings2')
		self.add({'mode': 'clear_favorites_choice', 'isFolder': 'false'}, 'Clear Favorites Cache', 'settings2')
		self.add({'mode': 'search.clear_search', 'isFolder': 'false'}, 'Clear Search History Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'main', 'isFolder': 'false'}, 'Clear Main Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'meta', 'isFolder': 'false'}, 'Clear Meta Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'list', 'isFolder': 'false'}, 'Clear Lists Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'ai_functions', 'isFolder': 'false'}, 'Clear AI Data Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'imdb', 'isFolder': 'false'}, 'Clear IMDb Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'internal_scrapers', 'isFolder': 'false'}, 'Clear Internal Scrapers Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'external_scrapers', 'isFolder': 'false'}, 'Clear External Scrapers Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'rd_cloud', 'isFolder': 'false'}, 'Clear Real Debrid Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'pm_cloud', 'isFolder': 'false'}, 'Clear Premiumize Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'oc_cloud', 'isFolder': 'false'}, 'Clear Off Cloud Cache', 'settings2')
		self.add({'mode': 'clear_cache', 'cache': 'tb_cloud', 'isFolder': 'false'}, 'Clear TorBox Cache', 'settings2')
		self.end_directory()

	def set_view_modes(self):
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.main', 'content': '', 'name': 'menus'}, 'Set Menus', 'folder')
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.movies', 'content': 'movies'}, 'Set Movies', 'movies')
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.tvshows', 'content': 'tvshows'}, 'Set TV Shows', 'tv')
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.seasons', 'content': 'seasons'}, 'Set Seasons', 'ontheair')
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.episodes', 'content': 'episodes'}, 'Set Episodes', 'next_episodes')
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.episodes_single', 'content': 'episodes', 'name': 'episode lists'}, 'Set Episode Lists', 'calender')
		self.add({'mode': 'navigator.choose_view', 'view_type': 'view.premium', 'content': 'files', 'name': 'premium files'}, 'Set Premium Files', 'premium')
		self.end_directory()

	def update_utils(self):
		self.add({'mode': 'updater.update_check', 'isFolder': 'false'}, 'Check For Updates', 'github')
		self.add({'mode': 'updater.rollback_check', 'isFolder': 'false'}, 'Rollback to a Previous Version', 'github')
		self.end_directory()

	def log_utils(self):
		log_location = k.translate_path('special://logpath/kodi.log')
		self.add({'mode': 'show_text', 'heading': 'Kodi Log Viewer', 'file': log_location, 'kodi_log': 'true', 'isFolder': 'false'}, 'Kodi Log Viewer', 'lists')
		self.add({'mode': 'upload_logfile', 'isFolder': 'false'}, 'Upload Kodi Log to Pastebin', 'lists')
		self.end_directory()

	def certifications(self):
		from modules.meta_lists import movie_certifications as function
		mode, action = 'build_movie_list', 'tmdb_movies_certifications'
		for i in function(): self.add({'mode': mode, 'action': action, 'key_id': i['id'], 'name': i['name']}, i['name'], 'certifications')
		self.end_directory()

	def languages(self):
		from modules.meta_lists import languages as function
		mode, action = 'build_movie_list', 'tmdb_movies_languages'
		for i in function(): self.add({'mode': mode, 'action': action, 'key_id': i['id'], 'name': i['name']}, i['name'], 'languages')
		self.end_directory()

	def years(self):
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie':
			from modules.meta_lists import years_movies as function
			mode, action = 'build_movie_list', 'tmdb_movies_year'
		else:
			from modules.meta_lists import years_tvshows as function
			mode, action = 'build_tvshow_list', 'tmdb_tv_year'
		for i in function(): self.add({'mode': mode, 'action': action, 'key_id': i['id'], 'name': i['name']}, i['name'], 'calender')
		self.end_directory()

	def genres(self):
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie':
			from modules.meta_lists import movie_genres as function
			mode, action = 'build_movie_list', 'tmdb_movies_genres'
		else:
			from modules.meta_lists import tvshow_genres as function
			mode, action = 'build_tvshow_list', 'tmdb_tv_genres'
		for i in function(): self.add({'mode': mode, 'action': action, 'key_id': i['id'], 'name': i['name']}, i['name'], i['icon'])
		self.end_directory()

	def search_history(self):
		from urllib.parse import unquote
		from caches.main_cache import main_cache
		search_mode_dict = {
		'movie': ('movie_queries', {'mode': 'search.get_key_id', 'media_type': 'movie', 'isFolder': 'false'}),
		'tvshow': ('tvshow_queries', {'mode': 'search.get_key_id', 'media_type': 'tv_show', 'isFolder': 'false'}),
		'people': ('people_queries', {'mode': 'search.get_key_id', 'search_type': 'people', 'isFolder': 'false'}),
		'tmdb_keyword_movie': ('keyword_tmdb_movie_queries', {'mode': 'search.get_key_id', 'search_type': 'tmdb_keyword', 'media_type': 'movie', 'isFolder': 'false'}),
		'tmdb_keyword_tvshow': ('keyword_tmdb_tvshow_queries', {'mode': 'search.get_key_id', 'search_type': 'tmdb_keyword', 'media_type': 'tvshow', 'isFolder': 'false'}),
		'easynews_video': ('easynews_video_queries', {'mode': 'search.get_key_id', 'search_type': 'easynews_video', 'isFolder': 'false'}),
		'easynews_image': ('easynews_image_queries', {'mode': 'search.get_key_id', 'search_type': 'easynews_image', 'isFolder': 'false'}),
		'trakt_lists': ('trakt_list_queries', {'mode': 'search.get_key_id', 'search_type': 'trakt_lists', 'isFolder': 'false'})}
		setting_id, action_dict = search_mode_dict[self.list_name]
		url_params = dict(action_dict)
		data = main_cache.get(setting_id) or []
		self.add(action_dict, '[B]NEW SEARCH...[/B]', 'new')
		for i in data:
			try:
				key_id = unquote(i)
				url_params['key_id'] = key_id
				url_params['setting_id'] = setting_id
				cm_items = [('[B]Remove from history[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'search.remove', 'setting_id':setting_id, 'key_id': key_id})),
							('[B]Clear All History[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'search.clear_all', 'setting_id':setting_id, 'refresh': 'true'}))]
				self.add(url_params, key_id, 'calender', cm_items=cm_items)
			except: pass
		self.category_name = self.params_get('name') or 'History'
		self.end_directory()

	def keyword_results(self):
		from apis.tmdb_api import tmdb_keywords_by_query
		media_type, key_id = self.params_get('media_type'), self.params_get('key_id') or self.params_get('query')
		try: page_no = int(self.params_get('new_page', '1'))
		except: page_no = self.params_get('new_page')
		mode = 'build_movie_list' if media_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movie_keyword_results' if media_type == 'movie' else 'tmdb_tv_keyword_results'
		data = tmdb_keywords_by_query(key_id, page_no)
		results = data['results']
		for item in results:
			name = item['name'].upper()
			self.add({'mode': mode, 'action': action, 'key_id': item['id'], 'iconImage': 'tmdb', 'category_name': name}, name, iconImage='tmdb')
		if data['total_pages'] > page_no:
			new_page = {'mode': 'navigator.keyword_results', 'key_id': key_id, 'category_name': self.category_name, 'new_page': str(data['page'] + 1)}
			self.add(new_page, 'Next Page (%s) >>' % new_page['new_page'], 'nextpage', False)
		self.category_name = 'Search Results for %s' % key_id.upper()
		self.end_directory()

	def choose_view(self):
		handle = int(sys.argv[1])
		content = self.params['content']
		view_type, name = self.params['view_type'], self.params.get('name') or content
		self.add({'mode': 'navigator.set_view', 'view_type': view_type, 'name': name, 'isFolder': 'false'}, 'Set view and then click here', 'settings')
		k.set_content(handle, content)
		k.end_directory(handle)
		k.set_view_mode(view_type, content, False)

	def set_view(self):
		set_setting(self.params['view_type'], str(k.current_window_object().getFocusId()))
		k.notification('%s: %s' % (self.params['name'].upper(), k.get_infolabel('Container.Viewmode').upper()), time=500)

	def shortcut_folders(self):
		folders = nc.get_shortcut_folders()
		if folders:
			for i in folders:
				name = i[0]
				convert_sr = '[B]Remove Random[/B]' if '[COLOR red][RANDOM][/COLOR]' in name else '[B]Make Random[/B]'
				cm_items = [('[B]Rename[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_rename'})),
							('[B]Delete Folder[/B]' , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_delete'})),
							('[B]Make New Folder[/B]' , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_make'})),
							(convert_sr , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_convert', 'name': name}))]
				self.add({'mode': 'navigator.build_shortcut_folder_contents', 'name': name, 'iconImage': 'folder'}, name, 'folder', cm_items=cm_items)
		else: self.add({'mode': 'menu_editor.shortcut_folder_make', 'isFolder': 'false'}, '[I]Make New Folder...[/I]', 'new')
		self.category_name = 'Shortcut Folders'
		self.end_directory()

	def build_shortcut_folder_contents(self):
		list_name = self.params_get('name')
		is_random = '[COLOR red][RANDOM][/COLOR]' in list_name
		contents = nc.get_shortcut_folder_contents(list_name)
		folder_icon = self.get_icon('folder')
		if is_random:
			from indexers.random_lists import random_shortcut_folders
			return random_shortcut_folders(list_name.replace(' [COLOR red][RANDOM][/COLOR]', ''), contents)
		if contents:
			for count, item in enumerate(contents):
				item_get = item.get
				iconImage = item_get('iconImage', None)
				icon = iconImage
				if iconImage:
					if iconImage.startswith('http') or 'plugin.video.fen' in iconImage: original_image = True
					else: original_image = False
				else: icon, original_image = folder_icon, False
				cm_items = [
				('[B]Move[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_edit', 'active_list': list_name, 'position': count, 'action': 'move'})),
				('[B]Remove[/B]' , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_edit', 'active_list': list_name, 'position': count, 'action': 'remove'})),
				('[B]Add Content[/B]' , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_add', 'name': list_name})),
				('[B]Rename[/B]' , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_edit', 'active_list': list_name, 'position': count, 'action': 'rename'})),
				('[B]Clear All[/B]' , self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_edit', 'active_list': list_name, 'position': count, 'action': 'clear'}))]
				self.add(item, item_get('name'), icon, original_image, cm_items=cm_items)
		elif is_random: pass
		else: self.add({'mode': 'menu_editor.shortcut_folder_add', 'name': list_name, 'isFolder': 'false'}, '[I]Add Content...[/I]', 'new')
		self.end_directory()

	def discover_contents(self):
		from caches.discover_cache import discover_cache
		action, media_type = self.params_get('action', ''), self.params_get('media_type')
		if not action:
			results = discover_cache.get_all(media_type)
			if not results and not self.is_external: self.add({'mode': 'discover_choice', 'media_type': media_type, 'isFolder': 'false'}, '[I]Make New Discover List...[/I]', 'new')
			else:
				if media_type == 'movie': mode, action = 'build_movie_list', 'tmdb_movies_discover'
				else: mode, action = 'build_tvshow_list', 'tmdb_tv_discover'
				for item in results:
					name, data = item['id'], item['data']
					cm_items = [
					('[B]Make New Discover List[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'discover_choice', 'media_type': media_type, 'isFolder': 'false'})),
					('[B]Remove from history[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'navigator.discover_contents', 'action':'delete_one', 'name': name})),
					('[B]Clear All History[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'navigator.discover_contents', 'action':'clear_cache', 'media_type': media_type}))]
					if '[random]' in data:
						self.add({'mode': 'random.%s' % mode, 'action': action, 'name': name, 'url': data, 'new_page': 'random', 'random': 'true'},
									name, 'discover', cm_items=cm_items)
					else: self.add({'mode': mode, 'action': action, 'name': name, 'url': data}, name, 'discover', cm_items=cm_items)
			self.end_directory()
		else:
			if action == 'delete_one': discover_cache.delete_one(self.params_get('name'))
			elif action == 'clear_cache': discover_cache.clear_cache(media_type)
			k.container_refresh()

	def exit_media_menu(self):
		params = k.get_property('fen.exit_params')
		if params: return k.container_refresh_input(params)

	def build_random_lists(self):
		random_list_dict = {
		'movie': ('Random Movie Lists', nc.random_movie_lists), 'tvshow': ('Random TV Show Lists', nc.random_tvshow_lists),
		'personal_lists': ('Random Personal Lists', nc.random_personal_lists)}
		self.category_name, function = random_list_dict[self.params_get('menu_type')]
		func = function()
		for item in func: self.add(item, item['name'], item['iconImage'])
		self.end_directory()

	def add(self, url_params, list_name, iconImage='folder', original_image=False, cm_items=[]):
		isFolder = url_params.get('isFolder', 'true') == 'true'
		try:
			if original_image: icon = iconImage
			else: icon = self.get_icon(iconImage)
		except: pass
		url_params['iconImage'] = icon
		url = self.build_url(url_params)
		listitem = self.make_listitem()
		listitem.setLabel(list_name)
		listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon, 'landscape': icon})
		info_tag = listitem.getVideoInfoTag(True)
		info_tag.setPlot(' ')
		if not self.is_external:
			if isFolder:
				url_params.update({'iconImage': iconImage, 'name': list_name})
				folder_item = ('[B]Add to Shortcut Folder[/B]', self.run_plugin % self.build_url({'mode': 'menu_editor.shortcut_folder_add_known', 'url': self.build_url(url_params)}))
				if cm_items: cm_items.append(folder_item)
				else: cm_items = [folder_item]
			listitem.addContextMenuItems(cm_items)
		self.add_item(int(sys.argv[1]), url, listitem, isFolder)

	def end_directory(self):
		handle = int(sys.argv[1])
		k.set_content(handle, '')
		k.set_category(handle, self.category_name)
		k.end_directory(handle)
		k.set_view_mode('view.main', '')
