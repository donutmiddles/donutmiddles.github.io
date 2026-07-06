# -*- coding: utf-8 -*-
from caches.base_cache import connect_database
from modules.kodi_utils import get_property, set_property, clear_property
# from modules.kodi_utils import logger

class NavigatorCache:
	root_list = [
	{'name': 'Movies', 'mode': 'navigator.main', 'action': 'MovieList', 'iconImage': 'movies'},
	{'name': 'TV Shows', 'mode': 'navigator.main', 'action': 'TVShowList', 'iconImage': 'tv'},
	{'name': 'People', 'mode': 'navigator.people', 'iconImage': 'genre_family'},
	{'name': 'My Lists', 'mode': 'navigator.my_lists', 'iconImage': 'lists'},
	{'name': 'Search', 'mode': 'navigator.search', 'iconImage': 'search'},
	{'name': 'Downloads', 'mode': 'navigator.downloads', 'iconImage': 'downloads'},
	{'name': 'Services', 'mode': 'navigator.services', 'iconImage': 'premium'},
	{'name': 'Tools', 'mode': 'navigator.tools', 'iconImage': 'settings2'}
				]
	movie_list = [
	{'name': 'Trending', 'mode': 'build_movie_list', 'action': 'trakt_movies_trending', 'random_support': 'true', 'iconImage': 'trending'},
	{'name': 'Trending Recent', 'mode': 'build_movie_list', 'action': 'trakt_movies_trending_recent', 'random_support': 'true', 'iconImage': 'trending_recent'},
	{'name': 'Popular', 'mode': 'build_movie_list', 'action': 'tmdb_movies_popular', 'random_support': 'true', 'iconImage': 'popular'},
	{'name': 'Popular Today', 'mode': 'build_movie_list', 'action': 'tmdb_movies_popular_today', 'random_support': 'true', 'iconImage': 'popular_today'},
	{'name': 'Premieres', 'mode': 'build_movie_list', 'action': 'tmdb_movies_premieres', 'random_support': 'true', 'iconImage': 'fresh'},
	{'name': 'Genres', 'mode': 'navigator.genres', 'menu_type': 'movie', 'random_support': 'true', 'iconImage': 'genres'},
	{'name': 'Languages', 'mode': 'navigator.languages', 'menu_type': 'movie', 'random_support': 'true', 'iconImage': 'languages'},
	{'name': 'Years', 'mode': 'navigator.years', 'menu_type': 'movie', 'random_support': 'true', 'iconImage': 'calender'},
	{'name': 'Certifications', 'mode': 'navigator.certifications', 'menu_type': 'movie', 'random_support': 'true', 'iconImage': 'certifications'},
	{'name': 'Watched', 'mode': 'build_movie_list', 'action': 'watched_movies', 'iconImage': 'watched_1'},
	{'name': 'In Progress', 'mode': 'build_movie_list', 'action': 'in_progress_movies', 'iconImage': 'player'}
				]
	tvshow_list = [
	{'name': 'Trending', 'mode': 'build_tvshow_list', 'action': 'trakt_tv_trending', 'random_support': 'true', 'iconImage': 'trending'},
	{'name': 'Trending Recent', 'mode': 'build_tvshow_list', 'action': 'trakt_tv_trending_recent', 'random_support': 'true', 'iconImage': 'trending_recent'},
	{'name': 'Popular', 'mode': 'build_tvshow_list', 'action': 'tmdb_tv_popular', 'random_support': 'true', 'iconImage': 'popular'},
	{'name': 'Popular Today', 'mode': 'build_tvshow_list', 'action': 'tmdb_tv_popular_today', 'random_support': 'true', 'iconImage': 'popular_today'},
	{'name': 'Premieres', 'mode': 'build_tvshow_list', 'action': 'tmdb_tv_premieres', 'random_support': 'true', 'iconImage': 'fresh'},
	{'name': 'Genres', 'mode': 'navigator.genres', 'menu_type': 'tvshow', 'random_support': 'true', 'iconImage': 'genres'},
	{'name': 'Years', 'mode': 'navigator.years', 'menu_type': 'tvshow', 'random_support': 'true', 'iconImage': 'calender'},
	{'name': 'Watched', 'mode': 'build_tvshow_list', 'action': 'watched_tvshows', 'iconImage': 'watched_1'},
	{'name': 'In Progress', 'mode': 'build_tvshow_list', 'action': 'in_progress_tvshows', 'iconImage': 'in_progress_tvshow'},
	{'name': 'In Progress Episodes', 'mode': 'build_single_episode', 'list_type': 'progress', 'iconImage': 'player'},
	{'name': 'Next Episodes', 'mode': 'build_single_episode', 'list_type': 'next', 'iconImage': 'next_episodes'}
				]

	main_menus = {'RootList': root_list, 'MovieList': movie_list, 'TVShowList': tvshow_list}
	
	def get_main_lists(self, list_name):
		default_contents = self.get_memory_cache(list_name, 'default')
		if not default_contents:
			default_contents = self.get_list(list_name, 'default')
			if default_contents == None:
				self.rebuild_database()
				return self.get_main_lists(list_name)
			try: edited_contents = self.get_list(list_name, 'edited')
			except: edited_contents = None
		else:
			edited_contents = self.get_memory_cache(list_name, 'edited')
		return default_contents, edited_contents

	def get_list(self, list_name, list_type):
		contents = None
		try:
			dbcon = connect_database('navigator_db')
			contents = eval(dbcon.execute('SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?', (list_name, list_type)).fetchone()[0])
			self.set_memory_cache(list_name, list_type, contents)
		except: pass
		return contents

	def set_list(self, list_name, list_type, list_contents):
		dbcon = connect_database('navigator_db')
		dbcon.execute('INSERT OR REPLACE INTO navigator VALUES (?, ?, ?)', (list_name, list_type, repr(list_contents)))
		self.set_memory_cache(list_name, list_type, list_contents)

	def delete_list(self, list_name, list_type):
		dbcon = connect_database('navigator_db')
		dbcon.execute('DELETE FROM navigator WHERE list_name=? and list_type=?', (list_name, list_type))
		self.delete_memory_cache(list_name, list_type)
		dbcon.execute('VACUUM')
	
	def get_memory_cache(self, list_name, list_type):
		try: return eval(get_property(self._get_list_prop(list_type) % list_name))
		except: return None
	
	def set_memory_cache(self, list_name, list_type, list_contents):
		set_property(self._get_list_prop(list_type) % list_name, repr(list_contents))

	def delete_memory_cache(self, list_name, list_type):
		clear_property(self._get_list_prop(list_type) % list_name)

	def get_shortcut_folders(self):
		try:
			dbcon = connect_database('navigator_db')
			folders = dbcon.execute('SELECT list_name, list_contents FROM navigator WHERE list_type = ?', ('shortcut_folder',)).fetchall()
			folders = sorted([(str(i[0]), eval(i[1])) for i in folders], key=lambda s: s[0].lower())
		except: folders = []
		return folders

	def get_shortcut_folder_contents(self, list_name):
		try:
			dbcon = connect_database('navigator_db')
			contents = eval(dbcon.execute('SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?', (list_name, 'shortcut_folder')).fetchone()[0])
		except: contents = []
		return contents

	def currently_used_list(self, list_name):
		try: used_list = self.get_memory_cache(list_name, 'edited') or self.get_memory_cache(list_name, 'default') \
						or self.get_list(list_name, 'edited') or self.get_list(list_name, 'default')
		except: used_list = []
		if not used_list:
			self.rebuild_database()
			used_list = NavigatorCache.main_menus[list_name]
		return used_list

	def rebuild_database(self):
		dbcon = connect_database('navigator_db')
		main_items = NavigatorCache.main_menus.items()
		for list_name, list_contents in main_items: self.set_list(list_name, 'default', list_contents)

	def _get_list_prop(self, list_type):
		return {'default': 'fen_%s_default', 'edited': 'fen_%s_edited', 'shortcut_folder': 'fen_%s_shortcut_folder'}[list_type]
	
	def random_movie_lists(self):
		movie_random_converts = {'navigator.genres': 'tmdb_movies_genres',  'navigator.languages': 'tmdb_movies_languages', 'navigator.years': 'tmdb_movies_year',
							'navigator.certifications': 'tmdb_movies_certifications'}
		return [dict(i, **{'mode': 'random.build_movie_list', 'action': i.get('action') or movie_random_converts[i['mode']],
							'random': 'true', 'name': 'Movies Random %s' % i['name'], 'menu_type': 'movie'}) for i in NavigatorCache.movie_list if 'random_support' in i]
	
	def random_tvshow_lists(self):
		tvshow_random_converts = {'navigator.genres': 'tmdb_tv_genres', 'navigator.years': 'tmdb_tv_year'}
		return [dict(i, **{'mode': 'random.build_tvshow_list', 'action': i.get('action') or tvshow_random_converts[i['mode']],
							'random': 'true', 'name': 'TV Shows Random %s' % i['name'], 'menu_type': 'tvshow'}) for i in NavigatorCache.tvshow_list if 'random_support' in i]
	
	def random_personal_lists(self):
		return [
			{'mode': 'personal_lists.get_personal_lists', 'name': 'Personal Lists (All)', 'iconImage': 'lists', 'random': 'true'},
			{'mode': 'random.build_personal_lists', 'name': 'Random Personal Lists (Single)', 'iconImage': 'lists', 'random': 'true'}
				]

navigator_cache = NavigatorCache()
