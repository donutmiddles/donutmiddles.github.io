# -*- coding: utf-8 -*-
import sys
import json
from modules.metadata import movie_meta, movieset_meta
from modules.utils import get_datetime, get_current_timestamp, paginate_list, jsondate_to_datetime, TaskPool, manual_function_import
from modules import kodi_utils, settings, watched_status
# logger = kodi_utils.logger

class Movies:
	tmdb_main = ('tmdb_movies_popular', 'tmdb_movies_popular_today', 'tmdb_movies_premieres')
	trakt_main = ('trakt_movies_trending', 'trakt_movies_trending_recent')
	special = ('tmdb_movies_languages', 'tmdb_movies_year', 'tmdb_movies_certifications', 'tmdb_movies_recommendations',
				'tmdb_movies_genres', 'tmdb_movies_search', 'tmdb_movie_keyword_results', 'tmdb_movie_keyword_results_direct', 'ai_similar')
	personal = {'in_progress_movies': ('modules.watched_status', 'get_in_progress_movies'), 'favorites_movies': ('caches.favorites_cache', 'get_favorites'),
				'watched_movies': ('modules.watched_status', 'get_watched_items')}

	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.category_name = self.params_get('category_name', None) or self.params_get('name', None) or 'Movies'
		self.id_type, self.list, self.action = self.params_get('id_type', 'tmdb_id'), self.params_get('list', []), self.params_get('action', None)
		self.tmdb_api_key = settings.tmdb_api_key()
		self.items, self.new_page, self.total_pages, self.is_external = [], {}, None, kodi_utils.external()
		if self.is_external: self.widget_hide_next_page = settings.widget_hide_next_page()
		else: self.widget_hide_next_page = False
		self.custom_order = self.params_get('custom_order', 'false') == 'true'
		self.paginate_start = int(self.params_get('paginate_start', '0'))
		self.append = self.items.append
		self.movieset_list_active = False

	def fetch_list(self):
		handle = int(sys.argv[1])
		try:
			try: page_no = int(self.params_get('new_page', '1'))
			except: page_no = self.params_get('new_page')
			if self.action in self.personal: var_module, import_function = self.personal[self.action]
			else: var_module, import_function = 'apis.%s_api' % self.action.split('_')[0], self.action
			try: function = manual_function_import(var_module, import_function)
			except: pass
			if page_no == 1 and not self.is_external: kodi_utils.set_property('fen.exit_params', kodi_utils.folder_path())
			if self.action in self.tmdb_main:
				data = function(page_no)
				results = data['results']
				self.list = [i['id'] for i in results]
				if data['total_pages'] > page_no: self.new_page = {'new_page': str(data['page'] + 1)}
			elif self.action in self.trakt_main:
				self.id_type = 'trakt_dict'
				data = function(page_no)
				try: self.list = [i['movie']['ids'] for i in data]
				except: self.list = [i['ids'] for i in data]
				self.new_page = {'new_page': str(page_no + 1)}
			elif self.action in self.special:
				key_id = self.params_get('key_id') or self.params_get('query')
				if not key_id: return
				data = function(key_id, page_no)
				results = data['results']
				self.list = [i['id'] for i in results]
				if data['total_pages'] > page_no: self.new_page = {'new_page': str(data['page'] + 1), 'key_id': key_id}
			elif self.action in self.personal:
				data = function('movie', page_no)
				data, total_pages = self.paginate_list(data, page_no)
				self.list = [i['media_id'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				if total_pages > page_no: self.new_page = {'new_page': str(page_no + 1), 'paginate_start': self.paginate_start}
			elif self.action == 'tmdb_movies_discover':
				url = self.params_get('url')
				data = function(url, page_no)
				results = data['results']
				self.list = [i['id'] for i in results]
				if data['total_pages'] > page_no: self.new_page = {'url': url, 'new_page': str(data['page'] + 1)}
			elif self.action  == 'tmdb_movies_sets':
				self.movieset_list_active = True
				data = sorted(movieset_meta(self.params_get('key_id'), self.tmdb_api_key)['parts'], key=lambda k: k['release_date'] or '2050')
				self.list = [i['id'] for i in data]
			elif self.action == 'trakt_movies_related':
				self.id_type = 'trakt_dict'
				key_id = self.params_get('key_id')
				if not key_id.startswith('tt'): key_id = movie_meta('tmdb_id', key_id, self.tmdb_api_key, get_datetime())['imdb_id']
				data = function(key_id)
				self.list = [i['ids'] for i in data]
			elif self.action == 'imdb_more_like_this':
				from apis.imdb_api import imdb_more_like_this
				self.id_type = 'imdb_id'
				key_id = self.params_get('key_id')
				if self.params_get('get_imdb'):
					key_id = movie_meta('tmdb_id', key_id, self.tmdb_api_key, get_datetime(), get_current_timestamp())['imdb_id']
				self.list = imdb_more_like_this(key_id)
			kodi_utils.add_items(handle, self.worker())
			if self.new_page and not self.widget_hide_next_page:
					self.new_page.update({'mode': 'build_movie_list', 'action': self.action, 'category_name': self.category_name})
					kodi_utils.add_dir(handle, self.new_page, 'Next Page (%s) >>' % self.new_page['new_page'], 'nextpage', kodi_utils.get_icon('nextpage_landscape'))
		except: pass
		kodi_utils.set_content(handle, 'movies')
		kodi_utils.set_category(handle, self.category_name)
		kodi_utils.end_directory(handle, cacheToDisc=False if self.is_external else True)
		if not self.is_external: kodi_utils.set_view_mode('view.movies', 'movies', self.is_external)
		
	def build_movie_content(self, _position, _id):
		try:
			meta = movie_meta(self.id_type, _id, self.tmdb_api_key, self.current_date, self.current_time)
			if not meta or 'blank_entry' in meta: return
			listitem = self.make_listitem()
			cm = []
			cm_append = cm.append
			cm_extend = cm.extend
			set_properties = listitem.setProperties
			clearprog_params, watched_status_params = '', ''
			meta_get = meta.get
			premiered = meta_get('premiered')
			title, year = meta_get('title'), meta_get('year') or '2050'
			tmdb_id, imdb_id = meta_get('tmdb_id'), meta_get('imdb_id')
			str_tmdb_id = str(tmdb_id)
			if self.rpdb_api_key:
				try: poster = meta_get('rpdb_poster') % self.rpdb_api_key + self.rpdb_format
				except: poster = meta_get('poster') or self.poster_empty
			else: poster = meta_get('poster') or self.poster_empty
			fanart = meta_get('fanart') or self.fanart_empty
			clearlogo, landscape = meta_get('clearlogo') or '', meta_get('landscape') or ''
			thumb = poster or landscape or fanart
			movieset_id, movieset_name = meta_get('extra_info').get('collection_id', ''), meta_get('extra_info').get('collection_name', '')
			first_airdate = jsondate_to_datetime(premiered, '%Y-%m-%d', True)
			duration = meta_get('duration')
			belongs_to_movieset = 'true' if all([movieset_id, movieset_name]) else 'false'
			movieset_active = self.open_movieset and belongs_to_movieset == 'true'
			if not first_airdate or self.current_date < first_airdate: unaired = True
			else: unaired = False
			progress = watched_status.get_progress_status_movie(self.bookmarks, str_tmdb_id)
			playcount = watched_status.get_watched_status_movie(self.watched_info, str_tmdb_id)
			play_params = self.build_url({'mode': 'playback.media', 'media_type': 'movie', 'tmdb_id': tmdb_id})
			extras_params = self.build_url({'mode': 'extras_menu_choice', 'media_type': 'movie', 'tmdb_id': tmdb_id})
			if self.open_extras or movieset_active: cm_append(['extras', ('[B]Play[/B]', 'RunPlugin(%s)' % play_params)])
			if not self.open_extras or movieset_active: cm_append(['extras', ('[B]Extras[/B]', 'RunPlugin(%s)' % extras_params)])
			if movieset_active: url_params = self.build_url({'mode': 'open_movieset_choice', 'key_id': movieset_id, 'name': movieset_name})
			elif self.open_extras: url_params = extras_params
			else: url_params = play_params
			cm_extend([
			['cast', ('[B]Cast[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'tmdb_cast_dialog_image_results', 'media_type': 'movie', 'tmdb_id': tmdb_id}))],
			['more_info', ('[B]More Info[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'media_extra_info_choice', 'media_type': 'movie', 'tmdb_id': tmdb_id}))],
			['options', ('[B]Options[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'options_menu_choice', 'content': 'movie', 'tmdb_id': tmdb_id, 'poster': poster}))],
			['browse_more', ('[B]Browse More[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'browse_more_choice', 'media_type': 'movie', 'tmdb_id': tmdb_id, 'imdb_id': imdb_id,
				'title': title, 'poster': poster, 'movieset_name': movieset_name, 'movieset_id': movieset_id}))],
			['personal_manager', ('[B]Personal Lists Manager[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'personallists_manager_choice', 'list_type': 'movie', 'tmdb_id': tmdb_id,
				'title': title,'premiered': premiered, 'current_time': self.current_time, 'icon': poster}))],
			['favorites_manager', ('[B]Favorites Manager[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'favorites_manager_choice', 'media_type': 'movie', 'tmdb_id': tmdb_id,
				'title': title}))]
					])
			if playcount:
				cm_append(['mark_watched', ('[B]Mark Unwatched[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'watched_status.mark_movie', 'action': 'mark_as_unwatched',
											'tmdb_id': tmdb_id, 'title': title}))])
			elif not unaired:
				cm_append(['mark_watched', ('[B]Mark Watched[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'watched_status.mark_movie', 'action': 'mark_as_watched',
											'tmdb_id': tmdb_id, 'title': title}))])
			if progress:
				cm_append(['mark_watched', ('[B]Clear Progress[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'watched_status.erase_bookmark', 'media_type': 'movie',
											'tmdb_id': tmdb_id, 'refresh': 'true'}))])
			if not self.is_external: cm_append(['exit', ('[B]Exit Movie List[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'navigator.exit_media_menu'}))])
			if self.is_external:
				cm_extend([['refresh', ('[B]Refresh Widgets[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'refresh_widgets'}))],
						['reload', ('[B]Reload Widgets[/B]', 'RunPlugin(%s)' % self.build_url({'mode': 'kodi_refresh'}))]])
			cm = self.context_menu(cm)
			info_tag = listitem.getVideoInfoTag(True)
			info_tag.setMediaType('movie')
			info_tag.setTitle(title)
			info_tag.setOriginalTitle(meta_get('original_title'))
			info_tag.setGenres(meta_get('genre'))
			info_tag.setDuration(duration)
			info_tag.setPlaycount(playcount)
			info_tag.setPlot(meta_get('plot'))
			info_tag.setUniqueIDs({'imdb': imdb_id, 'tmdb': str_tmdb_id})
			info_tag.setIMDBNumber(imdb_id), info_tag.setPremiered(premiered)
			info_tag.setYear(int(year))
			if progress:
				info_tag.setResumePoint(watched_status.get_resume_seconds(progress, duration))
				set_properties({'WatchedProgress': progress})
			listitem.setLabel(title)
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'clearlogo': clearlogo, 'landscape': landscape, 'thumb': thumb})
			set_properties({'belongs_to_collection': belongs_to_movieset})
			self.append(((url_params, listitem, False), _position))
		except: pass

	def worker(self):
		self.kodi_actor, self.make_listitem, self.build_url = kodi_utils.kodi_actor(), kodi_utils.make_listitem, kodi_utils.build_url
		self.poster_empty, self.fanart_empty = kodi_utils.get_icon('box_office'), kodi_utils.addon_fanart()
		self.current_date, self.current_time = get_datetime(), get_current_timestamp()
		self.cm_sort_order = settings.cm_sort_order()
		self.custom_cm_menu = self.cm_sort_order != settings.cm_default_order()
		rpdb_info = settings.rpdb_info('movie')
		self.rpdb_api_key, self.rpdb_format = rpdb_info['rpdb_api_key'], rpdb_info['rpdb_format']
		watched_db = watched_status.get_database()
		self.watched_info, self.bookmarks = watched_status.watched_info_movie(watched_db), watched_status.get_bookmarks_movie(watched_db)
		self.window_command = 'ActivateWindow(Videos,%s,return)' if self.is_external else 'Container.Update(%s)'
		open_action = settings.media_open_action('movie')
		self.open_movieset = open_action in (2, 3) and not self.movieset_list_active
		self.open_extras = open_action in (1, 3)
		if self.custom_order:
			threads = TaskPool().tasks(self.build_movie_content, self.list, min(len(self.list), settings.max_threads()))
			[i.join() for i in threads]
		else:
			threads = TaskPool().tasks_enumerate(self.build_movie_content, self.list, min(len(self.list), settings.max_threads()))
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
