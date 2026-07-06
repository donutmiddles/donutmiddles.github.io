# -*- coding: utf-8 -*-
import sys
from threading import Thread
from apis.trakt_api import trakt_get_lists, trakt_search_lists, get_trakt_list_contents
from indexers.movies import Movies
from indexers.tvshows import TVShows
from indexers.seasons import single_seasons
from indexers.episodes import build_single_episode
from modules import kodi_utils
from modules.utils import paginate_list
from modules.settings import paginate, page_limit, widget_hide_next_page
# logger = kodi_utils.logger

def search_trakt_lists(params):
	def _builder():
		for item in lists:
			try:
				list_key = item['type']
				list_info = item[list_key]
				if list_key == 'officiallist': continue
				item_count = list_info['item_count']
				if list_info['privacy'] == 'private' or item_count == 0: continue
				list_name, user, list_id = list_info['name'], list_info['username'], list_info['ids']['trakt']
				if not list_id: continue
				display = '%s | [I]%s (x%s)[/I]' % (list_name, user, str(item_count))
				description = item['list']['description']
				url = build_url({'mode': 'trakt.list.build_trakt_list', 'list_id': list_id, 'list_name': list_name, 'iconImage': 'trakt', 'name': list_name})
				cm = [('[B]Add to Shortcut Folder[/B]', 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_known', 'url': url}))]
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': fanart})
				info_tag = listitem.getVideoInfoTag(True)
				info_tag.setPlot(description)
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	handle, search_title, trakt_icon, fanart = int(sys.argv[1]), '', kodi_utils.get_icon('trakt'), kodi_utils.get_addon_fanart()
	build_url, make_listitem = kodi_utils.build_url, kodi_utils.make_listitem
	try:
		mode = params.get('mode')
		page = params.get('new_page', '1')
		search_title = params.get('key_id') or params.get('query')
		lists, pages = trakt_search_lists(search_title, page)
		kodi_utils.add_items(handle, list(_builder()))
		if pages > page:
			new_page = str(int(page) + 1)
			kodi_utils.add_dir(handle, {'mode': mode, 'key_id': search_title, 'new_page': new_page}, 'Next Page (%s) >>' % new_page,
								'nextpage', kodi_utils.get_icon('nextpage_landscape'))
	except: pass
	kodi_utils.set_content(handle, 'files')
	kodi_utils.set_category(handle, search_title.capitalize())
	kodi_utils.end_directory(handle)
	kodi_utils.set_view_mode('view.main')

def get_trakt_user_lists(params):
	def _process():
		for _list in lists:
			try:
				cm = []
				cm_append = cm.append
				item = _list['list']
				item_count = item.get('item_count', 0)
				if item_count == 0: continue
				list_name, list_id = item['name'], item['ids']['trakt']
				if not list_id: continue
				if item['type'] == 'official': user = 'Trakt Official'
				else:
					try: user = item['user']['ids']['slug']
					except: user = 'Unknown'
				sort_by, sort_how =  item['sort_by'], item['sort_how']
				display = '%s | [I]%s (x%s)[/I]' % (list_name, user, str(item_count))
				description = item['description']
				url_params = {'mode': 'trakt.list.build_trakt_list', 'list_id': list_id, 'list_name': list_name, 'iconImage': 'trakt', 'name': list_name}
				url = build_url(url_params)
				listitem = make_listitem()
				cm_append(('[B]Add to Shortcut Folder[/B]', 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_known', 'url': url})))
				listitem.addContextMenuItems(cm)
				listitem.setLabel(display)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': fanart})
				info_tag = listitem.getVideoInfoTag(True)
				info_tag.setPlot(description)
				yield (url, listitem, True)
			except: pass
	handle, trakt_icon, fanart = int(sys.argv[1]), kodi_utils.get_icon('trakt'), kodi_utils.get_addon_fanart()
	build_url, make_listitem = kodi_utils.build_url, kodi_utils.make_listitem
	try:
		list_type, list_mode = params.get('list_type'), params.get('list_mode')
		page = params.get('new_page', '1')
		new_page = str(int(page) + 1)
		lists = trakt_get_lists(list_type, list_mode, page)
		kodi_utils.add_items(handle, list(_process()))
		kodi_utils.add_dir(handle, {'mode': 'trakt.list.get_trakt_user_lists', 'list_type': list_type, 'list_mode': list_mode, 'new_page': new_page},
									'Next Page (%s) >>' % new_page, 'nextpage', kodi_utils.get_icon('nextpage_landscape'))
	except: pass
	kodi_utils.set_content(handle, 'files')
	kodi_utils.set_category(handle, params.get('category_name', 'Trakt Lists'))
	kodi_utils.end_directory(handle)
	kodi_utils.set_view_mode('view.main')

def build_trakt_list(params):
	def _process(function, _list, _type):
		if not _list['list']: return
		if _type in ('movies', 'tvshows'): item_list_extend(function(_list).worker())
		elif _type == 'seasons': item_list_extend(function(_list['list']))
		else: item_list_extend(function('episode.trakt_list', _list['list']))
	def _paginate_list(data, page_no, paginate_start):
		if paginate_enabled:
			limit = page_limit(is_external)
			data, total_pages = paginate_list(data, page_no, limit, paginate_start)
			if is_external: paginate_start = limit
		else: total_pages = 1
		return data, total_pages, paginate_start
	handle, is_external, list_name, content = int(sys.argv[1]), kodi_utils.external(), params.get('list_name'), 'movies'
	hide_next_page = is_external and widget_hide_next_page()
	try:
		threads, item_list = [], []
		item_list_extend = item_list.extend
		paginate_enabled = paginate(is_external)
		page_no, paginate_start = int(params.get('new_page', '1')), int(params.get('paginate_start', '0'))
		if page_no == 1 and not is_external: kodi_utils.set_property('fen.exit_params', kodi_utils.folder_path())
		list_id = params.get('list_id')
		result = get_trakt_list_contents(list_id)
		process_list, total_pages, paginate_start = _paginate_list(result, page_no, paginate_start)
		all_movies = [i for i in process_list if i['type'] == 'movie']
		all_tvshows = [i for i in process_list if i['type'] == 'show']
		all_seasons = [i for i in process_list if i['type'] == 'season']
		all_episodes = [i for i in process_list if i['type'] == 'episode']
		movie_list = {'list': [(i['order'], i['media_ids']) for i in all_movies], 'id_type': 'trakt_dict', 'custom_order': 'true'}
		tvshow_list = {'list': [(i['order'], i['media_ids']) for i in all_tvshows], 'id_type': 'trakt_dict', 'custom_order': 'true'}
		season_list = {'list': all_seasons}
		episode_list = {'list': all_episodes}
		content = max([('movies', len(all_movies)), ('tvshows', len(all_tvshows)), ('seasons', len(all_seasons)), ('episodes', len(all_episodes))], key=lambda k: k[1])[0]
		for item in ((Movies, movie_list, 'movies'), (TVShows, tvshow_list, 'tvshows'),
					(single_seasons, season_list, 'seasons'), (build_single_episode, episode_list, 'episodes')):
			threaded_object = Thread(target=_process, args=item)
			threaded_object.start()
			threads.append(threaded_object)
		[i.join() for i in threads]
		item_list.sort(key=lambda k: k[1])
		kodi_utils.add_items(handle, [i[0] for i in item_list])
		if total_pages > page_no and not hide_next_page:
			new_page = str(page_no + 1)
			url_params = {'mode': 'trakt.list.build_trakt_list', 'list_name': list_name, 'list_id': list_id, 'paginate_start': paginate_start, 'new_page': new_page}
			kodi_utils.add_dir(handle, url_params,  'Next Page (%s) >>' % new_page, 'nextpage', kodi_utils.get_icon('nextpage_landscape'))
	except: pass
	kodi_utils.set_content(handle, content)
	kodi_utils.set_category(handle, list_name)
	kodi_utils.end_directory(handle, cacheToDisc=False if is_external else True)
	if not is_external: kodi_utils.set_view_mode('view.%s' % content, content, is_external)
