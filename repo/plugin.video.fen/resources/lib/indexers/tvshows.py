# -*- coding: utf-8 -*-
import sys
import json
from modules.metadata import tvshow_meta
from modules.utils import get_datetime, get_current_timestamp, paginate_list, TaskPool, manual_function_import
from modules import kodi_utils, settings, watched_status
# logger = kodi_utils.logger

class TVShows:
	tmdb_main = ('tmdb_tv_popular', 'tmdb_tv_popular_today', 'tmdb_tv_premieres')
	trakt_main = ('trakt_tv_trending', 'trakt_tv_trending_recent')
	special = ('tmdb_tv_year', 'tmdb_tv_recommendations', 'tmdb_tv_genres', 'tmdb_tv_search', 'tmdb_tv_keyword_results', 'tmdb_tv_keyword_results_direct', 'ai_similar')
	personal = {'in_progress_tvshows': ('modules.watched_status', 'get_in_progress_tvshows'), 'watched_tvshows': ('modules.watched_status', 'get_watched_items'),
				'favorites_tvshows': ('caches.favorites_cache', 'get_favorites')}
	
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.category_name = self.params_get('category_name', None) or self.params_get('name', None) or 'TV Shows'
		self.id_type, self.list, self.action = self.params_get('id_type', 'tmdb_id'), self.params_get('list', []), self.params_get('action', None)
		self.tmdb_api_key = settings.tmdb_api_key()
		self.items, self.new_page, self.total_pages, self.is_external = [], {}, None, kodi_utils.external()
		if self.is_external: self.widget_hide_next_page = settings.widget_hide_next_page()
		else: self.widget_hide_next_page = False
		self.custom_order = self.params_get('custom_order', 'false') == 'true'
		self.paginate_start = int(self.params_get('paginate_start', '0'))
		self.append = self.items.append

	def fetch_list(self):
		handle = int(sys.argv[1])
		try:
			is_random = self.params_get('random', 'false') == 'true'
			try: page_no = int(self.params_get('new_page', '1'))
			except: page_no = self.params_get('new_page')
			if page_no == 1 and not self.is_external:
				folder_path = kodi_utils.folder_path()
				if not any([x in folder_path for x in ('build_season_list', 'build_episode_list')]): kodi_utils.set_property('fen.exit_params', folder_path)
			if self.action in self.personal: var_module, import_function = self.personal[self.action]
			else: var_module, import_function = 'apis.%s_api' % self.action.split('_')[0], self.action
			try: function = manual_function_import(var_module, import_function)
			except: pass
			if self.action in self.tmdb_main:
				data = function(page_no)
				results = data['results']
				self.list = [i['id'] for i in results]
				if not is_random and data['total_pages'] > page_no: self.new_page = {'new_page': str(page_no + 1)}
			elif self.action in self.trakt_main:
				self.id_type = 'trakt_dict'
				data = function(page_no)
				try: self.list = [i['show']['ids'] for i in data]
				except: self.list = [i['ids'] for i in data]
				if not is_random and self.action != 'trakt_recommendations': self.new_page = {'new_page': str(page_no + 1)}
			elif self.action in self.special:
				key_id = self.params_get('key_id')
				if not key_id: return
				data = function(key_id, page_no)
				results = data['results']
				self.list = [i['id'] for i in results]
				if not is_random and data['total_pages'] > page_no: self.new_page = {'new_page': str(page_no + 1), 'key_id': key_id}
			elif self.action in self.personal:
				data = function('tvshow', page_no)
				data, total_pages = self.paginate_list(data, page_no)
				self.list = [i['media_id'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				if total_pages > page_no: self.new_page = {'new_page': str(page_no + 1), 'paginate_start': self.paginate_start}
			elif self.action == 'tmdb_tv_discover':
				url = self.params_get('url')
				data = function(url, page_no)
				results = data['results']
				self.list = [i['id'] for i in results]
				if data['total_pages'] > page_no: self.new_page = {'url': url, 'new_page': str(data['page'] + 1)}
			elif self.action == 'trakt_tv_related':
				self.id_type = 'trakt_dict'
				key_id = self.params_get('key_id')
				if not key_id.startswith('tt'): key_id = tvshow_meta('tmdb_id', key_id, self.tmdb_api_key, get_datetime())['imdb_id']
				data = function(key_id)
				self.list = [i['ids'] for i in data]
			elif self.action == 'imdb_more_like_this':
				from apis.imdb_api import imdb_more_like_this
				self.id_type = 'imdb_id'
				key_id = self.params_get('key_id')
				if self.params_get('get_imdb'):
					key_id = tvshow_meta('tmdb_id', key_id, self.tmdb_api_key, get_datetime(), get_current_timestamp())['imdb_id']
				self.list = imdb_more_like_this(key_id)
			kodi_utils.add_items(handle, self.worker())
			if self.new_page and not self.widget_hide_next_page:
				self.new_page.update({'mode': 'build_tvshow_list', 'action': self.action, 'category_name': self.category_name})
				kodi_utils.add_dir(handle, self.new_page, 'Next Page (%s) >>' % self.new_page['new_page'], 'nextpage', kodi_utils.get_icon('nextpage_landscape'))
		except: pass
		kodi_utils.set_content(handle, 'tvshows')
		kodi_utils.set_category(handle, self.category_name)
		kodi_utils.end_directory(handle, cacheToDisc=False if self.is_external else True)
		if not self.is_external: kodi_utils.set_view_mode('view.tvshows', 'tvshows', self.is_external)

	def build_tvshow_content(self, _position, _id):
		try:
			meta = tvshow_meta(self.id_type, _id, self.tmdb_api_key, self.current_date, self.current_time)
			if not meta or 'blank_entry' in meta: return
			cm = []
			cm_append = cm.append
			cm_extend = cm.extend
			listitem = self.make_listitem()
			set_properties = listitem.setProperties
			meta_get = meta.get
			premiered = meta_get('premiered')
			trailer, title, year = meta_get('trailer'), meta_get('title'), meta_get('year') or '2050'
			tvdb_id, imdb_id = meta_get('tvdb_id'), meta_get('imdb_id')
			if self.rpdb_api_key:
				try: poster = meta_get('rpdb_poster') % self.rpdb_api_key + self.rpdb_format
				except: poster = meta_get('poster') or self.poster_empty
			else: poster = meta_get('poster') or self.poster_empty
			fanart = meta_get('fanart') or self.fanart_empty
			clearlogo, landscape = meta_get('clearlogo') or '', meta_get('landscape') or ''
			thumb = poster or landscape or fanart
			tmdb_id, total_seasons, total_aired_eps = meta_get('tmdb_id'), meta_get('total_seasons'), meta_get('total_aired_eps')
			unaired = total_aired_eps == 0
			if unaired: progress, playcount, total_watched, total_unwatched = 0, 0, 0, total_aired_eps
			else:
				playcount, total_watched, total_unwatched = watched_status.get_watched_status_tvshow(self.watched_info.get(str(tmdb_id), None), total_aired_eps)
				if total_watched: progress = watched_status.get_progress_status_tvshow(total_watched, total_aired_eps)
				else: progress = 0
				visible_progress = '0' if progress == 100 else progress
			extras_params = self.build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow'})
			if total_seasons == 1: url_params = self.build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 1})
			else: url_params = self.build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
			if self.open_extras:
				cm_append(['extras', ('[B]Browse[/B]', 'Container.Update(%s)' % url_params)])
				url_params = extras_params
			else: cm_append(['extras', ('[B]Extras[/B]', 'RunPlugin(%s)' % extras_params)])
			cm_extend([
			['cast', ('[B]Cast[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'tmdb_cast_dialog_image_results', 'media_type': 'tvshow', 'tmdb_id': tmdb_id}))],
			['more_info', ('[B]More Info[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'media_extra_info_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id}))],
			['options', ('[B]Options[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'options_menu_choice', 'content': 'tvshow', 'tmdb_id': tmdb_id, 'poster': poster}))],
			['browse_more', ('[B]Browse More[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'browse_more_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id, 'imdb_id': imdb_id,
				'title': title, 'poster': poster}))],
			['personal_manager', ('[B]Personal Lists Manager[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'personallists_manager_choice', 'list_type': 'tvshow', 'tmdb_id': tmdb_id,
				'title': title, 'premiered': premiered, 'current_time': self.current_time, 'icon': poster}))],
			['favorites_manager', ('[B]Favorites Manager[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'favorites_manager_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id,
				'title': title}))]
					])
			if not playcount and not unaired:
				cm_append(['mark_watched', ('[B]Mark Watched[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'watched_status.mark_tvshow', 'action': 'mark_as_watched',
																			'title': title,'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id}))])
			if progress:
				cm_append(['mark_watched', ('[B]Mark Unwatched[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'watched_status.mark_tvshow', 'action': 'mark_as_unwatched',
																			'title': title, 'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id}))])
			set_properties({'watchedepisodes': str(total_watched), 'unwatchedepisodes': str(total_unwatched)})
			set_properties({'watchedprogress': visible_progress, 'totalepisodes': str(total_aired_eps), 'totalseasons': str(total_seasons)})
			if not self.is_external: cm_append(['exit', ('[B]Exit TV Show List[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'navigator.exit_media_menu'}))])
			if self.is_external:
				cm_extend([['refresh', ('[B]Refresh Widgets[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'refresh_widgets'}))],
						['reload', ('[B]Reload Widgets[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'kodi_refresh'}))]])
			cm = self.context_menu(cm)
			info_tag = listitem.getVideoInfoTag(True)
			info_tag.setMediaType('tvshow')
			info_tag.setTitle(title)
			info_tag.setTvShowTitle(title)
			info_tag.setOriginalTitle(meta_get('original_title'))
			info_tag.setUniqueIDs({'imdb': imdb_id, 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)}), info_tag.setIMDBNumber(imdb_id)
			info_tag.setPlot(meta_get('plot'))
			info_tag.setPlaycount(playcount)
			info_tag.setGenres(meta_get('genre'))
			info_tag.setYear(int(year))
			listitem.setLabel(title)
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'clearlogo': clearlogo, 'landscape': landscape, 'thumb': thumb, 'icon': landscape,
							'tvshow.poster': poster, 'tvshow.clearlogo': clearlogo})
			self.append(((url_params, listitem, self.is_folder), _position))
		except: pass

	def worker(self):
		self.kodi_actor, self.make_listitem, self.build_url = kodi_utils.kodi_actor(), kodi_utils.make_listitem, kodi_utils.build_url
		self.poster_empty, self.fanart_empty = kodi_utils.get_icon('box_office'), kodi_utils.addon_fanart()
		self.current_date, self.current_time = get_datetime(), get_current_timestamp()
		rpdb_info = settings.rpdb_info('tvshow')
		self.rpdb_api_key, self.rpdb_format = rpdb_info['rpdb_api_key'], rpdb_info['rpdb_format']
		self.open_extras = settings.media_open_action('tvshow') == 1
		self.cm_sort_order = settings.cm_sort_order()
		self.custom_cm_menu = self.cm_sort_order != settings.cm_default_order()
		self.is_folder = False if self.open_extras else True
		self.watched_info = watched_status.watched_info_tvshow(watched_status.get_database())
		self.window_command = 'ActivateWindow(Videos,%s,return)' if self.is_external else 'Container.Update(%s)'
		if self.custom_order:
			threads = TaskPool().tasks(self.build_tvshow_content, self.list, min(len(self.list), settings.max_threads()))
			[i.join() for i in threads]
		else:
			threads = TaskPool().tasks_enumerate(self.build_tvshow_content, self.list, min(len(self.list), settings.max_threads()))
			[i.join() for i in threads]
			self.items.sort(key=lambda k: k[1])
			self.items = [i[0] for i in self.items]
		return self.items

	def context_menu(self, context_menu_items):
		if self.custom_cm_menu:
			try: context_menu_items = sorted([i for i in context_menu_items if i[0] in self.cm_sort_order], key=lambda k: self.cm_sort_order[k[0]])
			except: pass
		return [i[1] for i in context_menu_items]

	def paginate_list(self, data, page_no):
		if settings.paginate(self.is_external):
			limit = settings.page_limit(self.is_external)
			data, total_pages = paginate_list(data, page_no, limit, self.paginate_start)
			if self.is_external: self.paginate_start = limit
		else: total_pages = 1
		return data, total_pages
