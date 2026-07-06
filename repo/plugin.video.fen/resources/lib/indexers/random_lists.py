# -*- coding: utf-8 -*-
import sys
import json
import random
from caches.random_widgets_cache import RandomWidgets
from indexers.movies import Movies
from indexers.tvshows import TVShows
from modules import meta_lists
from modules.settings import paginate, page_limit, max_threads
from modules import kodi_utils
from modules.utils import manual_function_import, TaskPool
# logger = kodi_utils.logger

def get_persistent_content(database, key, is_external):
	results, refresh_cache, key = None, True, 'random_list.%s' % key
	if not is_external: refresh_cache = False
	else:
		try:
			results = database.get(key)
			if results: refresh_cache = False
		except: pass
	return results, refresh_cache

def set_persistent_content(database, key, data):
	database.set('random_list.%s' % key, data, 24)

class RandomLists():
	movie_main = ('tmdb_movies_popular', 'tmdb_movies_popular_today', 'tmdb_movies_premieres')
	movie_trakt_main = ('trakt_movies_trending', 'trakt_movies_trending_recent', 'trakt_recommendations')
	movie_special_main = {'tmdb_movies_languages': meta_lists.languages, 'tmdb_movies_year': meta_lists.years_movies, 'tmdb_movies_certifications': meta_lists.movie_certifications,
						'tmdb_movies_genres': meta_lists.movie_genres}
	tvshow_main = ('tmdb_tv_popular', 'tmdb_tv_popular_today', 'tmdb_tv_premieres')
	tvshow_trakt_main = ('trakt_tv_trending', 'trakt_tv_trending_recent', 'trakt_recommendations')
	tvshow_special_main = {'tmdb_tv_year': meta_lists.years_tvshows, 'tmdb_tv_genres': meta_lists.tvshow_genres}

	def __init__(self, params):
		self.database = RandomWidgets()
		self.handle = int(sys.argv[1])
		self.params = params
		self.params_get = self.params.get
		self.mode = self.params_get('mode').replace('random.', '')
		self.action = self.params_get('action')
		self.menu_type = self.params_get('menu_type', None) or ('movie' if 'movie' in self.mode else 'tvshow' if 'tvshow' in self.mode else '')
		self.base_list_name = self.params_get('name')
		self.params.update({'mode': self.mode, 'action': self.action, 'menu_type': self.menu_type, 'base_list_name': self.base_list_name})
		self.is_external = kodi_utils.external()
		self.folder_name = self.params_get('folder_name', None)
		if self.menu_type == 'movie': self.function, self.view_mode, self.content_type = Movies, 'view.movies', 'movies'
		else: self.function, self.view_mode, self.content_type = TVShows, 'view.tvshows', 'tvshows'
		self.category_name, self.list_items, self.random_results = '', [], []
		self.max_range, self.sample_size = 10, 3

	def run_random(self):
		if self.action in self.movie_main: return self.random_main()
		if self.action in self.tvshow_main: return self.random_main()
		if self.action in self.movie_trakt_main: return self.random_trakt_main()
		if self.action in self.tvshow_trakt_main: return self.random_trakt_main()
		if self.action in self.movie_special_main: return self.random_special_main()
		if self.action in self.tvshow_special_main: return self.random_special_main()
		if self.mode == 'build_personal_lists': return self.random_personal_lists()
		if self.mode == 'build_personal_lists_contents': return self.personal_lists_contents()
		if self.action in ('tmdb_movies_discover', 'tmdb_tv_discover'): return self.random_discover()

	def random_main(self):
		random_list, cache_to_memory = get_persistent_content(self.database, self.action, self.is_external)
		if not random_list:
			list_function = self.get_function()
			threads = TaskPool().tasks(lambda x: self.random_results.extend(list_function(x)['results']), self.get_sample(), max_threads())
			[i.join() for i in threads]
			random_list = random.sample(self.random_results, min(len(self.random_results), 20))
			if cache_to_memory: set_persistent_content(self.database, self.action, random_list)
		self.params['list'] = [i['id'] for i in random_list]
		self.list_items = self.function(self.params).worker()
		self.category_name = self.params_get('category_name', None) or self.base_list_name or ''
		self.make_directory()

	def random_trakt_main(self):
		random_list, cache_to_memory = get_persistent_content(self.database, self.action, self.is_external)
		function_key, list_key = ('movies', 'movie') if self.menu_type == 'movie' else ('shows', 'show')
		if not random_list:
			list_function = self.get_function()
			threads = TaskPool().tasks(lambda x: self.random_results.extend(list_function(x)),
										[function_key,] if self.action == 'trakt_recommendations' else self.get_sample(), max_threads())
			[i.join() for i in threads]
			random_list = random.sample(self.random_results, min(len(self.random_results), 20))
			if cache_to_memory: set_persistent_content(self.database, self.action, random_list)
		try: self.params['list'] = [i[list_key]['ids'] for i in random_list]
		except: self.params['list'] = [i['ids'] for i in random_list]
		self.params['id_type'] = 'trakt_dict'
		self.list_items = self.function(self.params).worker()
		self.category_name = self.params_get('category_name', None) or self.base_list_name or ''
		self.make_directory()

	def random_special_main(self):
		random_list, cache_to_memory = get_persistent_content(self.database, self.action, self.is_external)
		if not random_list:
			list_function = self.get_function()
			choice_list = self.movie_special_main if self.menu_type == 'movie' else self.tvshow_special_main
			info = random.choice(choice_list[self.action]())
			list_name = info['name']
			threads = TaskPool().tasks(lambda x: self.random_results.extend(list_function(info['id'], x)['results']), self.get_sample(), max_threads())
			[i.join() for i in threads]
			result = random.sample(self.random_results, min(len(self.random_results), 20))
			if cache_to_memory: set_persistent_content(self.database, self.action, {'name': list_name, 'result': result})
		else: list_name, result = random_list['name'], random_list['result']
		self.params['list'] = [i['id'] for i in result]
		self.list_items = self.function(self.params).worker()
		self.category_name = list_name
		self.make_directory()

	def random_personal_lists(self):
		from indexers.personal_lists import get_personal_list, build_personal_list, get_all_personal_lists
		random_list, cache_to_memory = get_persistent_content(self.database, self.mode, self.is_external)
		if not random_list:
			self.random_results = [i for i in get_all_personal_lists() if i['total']]
			random_list = random.choice(self.random_results)
			list_name = random_list['name']
			random_list['list_name'] = list_name
			result = get_personal_list(random_list)
			random.shuffle(result)
			if paginate(self.is_external): data = random.sample(result, min(len(result), page_limit(self.is_external)))
			else: data = random.sample(result, len(result))
			result = [dict(i, **{'order': c}) for c, i in enumerate(data)]
			url_params = {'base_list_name':list_name, 'list_name': list_name, 'result': result}
			content_type, self.list_items = build_personal_list(url_params)
			if cache_to_memory: set_persistent_content(self.database, self.mode, {'name': list_name, 'result': result})
		else:
			list_name, result = random_list['name'], random_list['result']
			url_params = {'base_list_name':list_name, 'list_name': list_name, 'result': result}
			content_type, self.list_items = build_personal_list(url_params)
		self.category_name = list_name or ''
		self.view_mode, self.content_type = 'view.%s' % content_type, content_type
		self.make_directory()

	def personal_lists_contents(self):
		from indexers.personal_lists import get_personal_list, build_personal_list
		list_name = self.params.get('list_name')
		random_list, cache_to_memory = get_persistent_content(self.database, '%s-%s' % (self.mode, list_name), self.is_external)
		if not random_list:
			result = get_personal_list(self.params)
			random.shuffle(result)
			if paginate(self.is_external): result = random.sample(result, min(len(result), page_limit(self.is_external)))
			result = [dict(i, **{'order': c}) for c, i in enumerate(result)]
			url_params = {'base_list_name':list_name, 'list_name': list_name, 'result': result}
			content_type, self.list_items = build_personal_list(url_params)
			if cache_to_memory: set_persistent_content(self.database, '%s-%s' % (self.mode, list_name), {'name': list_name, 'result': result})
		else:
			list_name, result = random_list['name'], random_list['result']
			url_params = {'base_list_name':list_name, 'list_name': list_name, 'result': result}
			content_type, self.list_items = build_personal_list(url_params)
		self.category_name = self.base_list_name or list_name or ''
		self.view_mode, self.content_type = 'view.%s' % content_type, content_type
		self.make_directory()

	def random_discover(self):
		url = self.params_get('url', None)
		if not url: return
		random_list, cache_to_memory = get_persistent_content(self.database, url, self.is_external)
		if not random_list:
			list_function = self.get_function()
			threads = TaskPool().tasks(lambda x: self.random_results.extend(list_function(url, x)['results']), self.get_sample(), max_threads())
			[i.join() for i in threads]
			if paginate(self.is_external): random_list = random.sample(self.random_results, min(len(self.random_results), page_limit(self.is_external)))
			else: random_list = random.sample(self.random_results, len(self.random_results))
			if cache_to_memory: set_persistent_content(self.database, url, random_list)
		self.params['list'] = [i['id'] for i in random_list]
		self.list_items = self.function(self.params).worker()
		self.category_name = self.params_get('category_name', None) or self.base_list_name or ''
		self.make_directory()

	def make_directory(self, next_page_params={}):
		kodi_utils.add_items(self.handle, self.list_items)
		if next_page_params:
			kodi_utils.add_dir(self.handle, next_page_params, 'Browse Into %s >>' \
					% (next_page_params.get('category_name', None) or next_page_params.get('name', None) or self.content_type), 'nextpage', kodi_utils.get_icon('nextpage_landscape'))
		kodi_utils.set_content(self.handle, self.content_type)
		kodi_utils.set_category(self.handle, self.category_name)
		kodi_utils.end_directory(self.handle, cacheToDisc=False if self.is_external else True)
		if self.is_external:
			if self.folder_name: kodi_utils.set_property('fen.%s' % self.folder_name, self.category_name)
			else: kodi_utils.set_property('fen.%s' % self.base_list_name, self.category_name)
		else: kodi_utils.set_view_mode(self.view_mode, self.content_type, self.is_external)

	def get_function(self):
		return manual_function_import('apis.%s_api' % self.action.split('_')[0], self.action)

	def get_sample(self):
		return random.sample(range(1, self.max_range), self.sample_size)

def random_shortcut_folders(folder_name, random_results):
	random_check = kodi_utils.random_valid_type_check()
	random_results = [i for i in random_results if i['mode'].replace('random.', '') in random_check]
	database = RandomWidgets()
	is_external = kodi_utils.external()
	random_list, cache_to_memory = get_persistent_content(database, 'random_shortcut_folders_%s' % folder_name, is_external)
	if not random_list:
		if len(random_results) > 1: random_list = random.choice(random_results)
		else: random_list = random_results[0]
		random_list.update({'folder_name': folder_name, 'mode': random_list['mode'].replace('random.', '')})
		if cache_to_memory: set_persistent_content(database, 'random_shortcut_folders_%s' % folder_name, random_list)
	if random_list.get('random') == 'true': return RandomLists(random_list).run_random()
	if random_list.get('action') in ('tmdb_movies_discover', 'tmdb_tv_discover'): return RandomLists(random_list).run_random()
	menu_type = random_check[random_list['mode']]
	list_name = random_list.get('list_name', None) or random_list.get('name', None) or 'Random'
	if is_external: kodi_utils.set_property('fen.%s' % folder_name, list_name)
	if menu_type == 'movie':
		return Movies(random_list).fetch_list()
	if menu_type == 'tvshow':
		return TVShows(random_list).fetch_list()
	if menu_type == 'season':
		from indexers.seasons import build_season_list
		return build_season_list(random_list)
	if menu_type == 'episode':
		from indexers.episodes import build_episode_list
		return build_episode_list(random_list)
	if menu_type == 'single_episode':
		from indexers.episodes import build_single_episode
		return build_single_episode(kodi_utils.random_episodes_check()[random_list['mode']], random_list)
	if menu_type == 'personal_list':
		from indexers.personal_lists import build_personal_list
		return build_personal_list(random_list)
	return kodi_utils.end_directory(int(sys.argv[1]))
