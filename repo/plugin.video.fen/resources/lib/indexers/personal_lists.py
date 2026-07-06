# -*- coding: utf-8 -*-
import sys
import json
from random import shuffle
from threading import Thread
from urllib.parse import unquote
from caches.personal_lists_cache import personal_lists_cache
from indexers.movies import Movies
from indexers.tvshows import TVShows
from modules import kodi_utils, settings
from modules.utils import paginate_list, sort_for_article
# logger = kodi_utils.logger

def get_personal_lists(params):
	def _process():
		for item in data:
			try:
				list_name, sort_order, list_total = item['name'], item['sort_order'], item['total']
				display = '%s [I](x%02d)[/I]' % (list_name, list_total)
				mode = 'random.build_personal_lists_contents' if random else 'personal_lists.build_personal_list'
				url_params = {'mode': mode, 'list_name': list_name, 'category_name': list_name, 'sort_order': sort_order, 'name': list_name}
				if random: url_params['random'] = 'true'
				url = build_url(url_params)
				cm = [('[B]Make New List[/B]', 'RunPlugin(%s)' % build_url({'mode': 'personal_lists.make_new_personal_list'})),
				('[B]Edit Properties[/B]', 'RunPlugin(%s)' % build_url({'mode': 'personal_lists.adjust_personal_list_properties', 'list_name': list_name, 'sort_order': sort_order})),
				('[B]Delete List[/B]', 'RunPlugin(%s)' % build_url({'mode': 'personal_lists.delete_personal_list', 'list_name': list_name})),
				('[B]Add to Shortcut Folder[/B]', 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_known', 'url': url}))]
				listitem = kodi_utils.make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': background, 'banner': background})
				info_tag = listitem.getVideoInfoTag(True)
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	def _new_process():
		url = build_url({'mode': 'personal_lists.make_new_personal_list'})
		new_icon = kodi_utils.get_icon('new')
		listitem = kodi_utils.make_listitem()
		listitem.setLabel('[I]Make New Personal List...[/I]')
		listitem.setArt({'icon': new_icon, 'poster': new_icon, 'thumb': new_icon, 'fanart': background, 'banner': background})
		info_tag = listitem.getVideoInfoTag(True)
		info_tag.setPlot(' ')
		yield (url, listitem, False)
	icon, background = kodi_utils.get_icon('lists'), kodi_utils.get_addon_fanart()
	build_url = kodi_utils.build_url
	random = params.get('random', 'false') == 'true'
	handle = int(sys.argv[1])
	try:
		data = get_all_personal_lists()
		if data: result = list(_process())
		else: result = list(_new_process())
		kodi_utils.add_items(handle, result)
	except: pass
	kodi_utils.set_content(handle, 'files')
	kodi_utils.set_category(handle, 'Personal Lists')
	kodi_utils.end_directory(handle)
	kodi_utils.set_view_mode('view.main')

def build_personal_list(params):
	def _process(function, _list):
		item_list_extend(function(_list).worker())
	def _paginate_list(data, page_no, paginate_start):
		if use_result: total_pages = 1
		elif paginate_enabled:
			limit = settings.page_limit(is_external)
			data, total_pages = paginate_list(data, page_no, limit, paginate_start)
			if is_external: paginate_start = limit
		else: total_pages = 1
		return data, total_pages, paginate_start
	handle, is_external = int(sys.argv[1]), kodi_utils.external()
	hide_next_page = is_external and settings.widget_hide_next_page()
	try:
		threads, item_list, content = [], [], 'movies'
		item_list_extend = item_list.extend
		paginate_enabled = settings.paginate(is_external)
		use_result = 'result' in params
		list_name, sort_order = params.get('list_name'), params.get('sort_order')
		page_no, paginate_start = int(params.get('new_page', '1')), int(params.get('paginate_start', '0'))
		new_params = {'mode': 'personal_lists.build_personal_list', 'list_name': list_name, 'sort_order': sort_order, 'paginate_start': paginate_start}
		if page_no == 1 and not is_external: kodi_utils.set_property('fen.exit_params', kodi_utils.folder_path())
		if use_result: result = params.get('result', [])
		else: result = get_personal_list(params)
		process_list, total_pages, paginate_start = _paginate_list(result, page_no, paginate_start)
		movie_list = {'list': [(c, i['media_id']) for c, i in enumerate(process_list) if i['type'] == 'movie'], 'custom_order': 'true'}
		tvshow_list = {'list': [(c, i['media_id']) for c, i in enumerate(process_list) if i['type'] == 'tvshow'], 'custom_order': 'true'}
		content = 'movies' if len(movie_list['list']) > len(tvshow_list['list']) else 'tvshows'
		for item in ((Movies, movie_list), (TVShows, tvshow_list)):
			if not item[1]['list']: continue
			threaded_object = Thread(target=_process, args=item)
			threaded_object.start()
			threads.append(threaded_object)
		[i.join() for i in threads]
		item_list.sort(key=lambda k: k[1])
		if use_result: return content, [i[0] for i in item_list]
		kodi_utils.add_items(handle, [i[0] for i in item_list])
		if total_pages > page_no and not hide_next_page:
			new_page = str(page_no + 1)
			new_params['new_page'] = new_page
			kodi_utils.add_dir(handle, new_params, 'Next Page (%s) >>' % new_page, 'nextpage', kodi_utils.get_icon('nextpage_landscape'))
	except: pass
	kodi_utils.set_content(handle, content)
	kodi_utils.set_category(handle, list_name)
	kodi_utils.end_directory(handle, cacheToDisc=False if is_external else True)
	if not is_external: kodi_utils.set_view_mode('view.%s' % content, content, is_external)

def get_all_personal_lists():
	contents = personal_lists_cache.get_lists()
	try: contents = sort_for_article(contents, 'name')
	except: pass
	return contents

def delete_personal_list(params):
	list_name = params.get('list_name', '')
	if not kodi_utils.confirm_dialog(heading='Personal Lists', text='Delete [B]%s[/B] Personal List?' % list_name): return
	if personal_lists_cache.delete_list(list_name): return kodi_utils.kodi_refresh()
	kodi_utils.notification('Error Deleting List', 3000)

def delete_personal_list_contents(params):
	list_name = params.get('list_name', '')
	if not list_change_warning(list_name): return
	if personal_lists_cache.delete_list_contents(list_name): return
	kodi_utils.notification('Error Deleting List Contents', 3000)

def get_personal_list(params):
	list_name, sort_order = params['list_name'], params['sort_order']
	contents = personal_lists_cache.get_list(list_name)
	try:
		if sort_order == 'None': pass
		elif sort_order in ('5', 'shuffle'): shuffle(contents)
		elif sort_order in ('', '0'): contents = sort_for_article(contents, 'title')
		elif sort_order in ('1', '2'): contents.sort(key=lambda k: int(k['date_added']), reverse=sort_order != '1')
		else: contents.sort(key=lambda k: (k['release_date'] is None, k['release_date']), reverse=sort_order != '3')
	except: pass
	return contents

def make_new_personal_list(params):
	is_retry = params.get('is_retry', False)
	list_name = personal_list_name()
	if list_name == None: return None
	if not unique_list_check(list_name): return make_new_personal_list(params)
	sort_order = personal_sort_order()
	if sort_order == None: return None
	success = personal_lists_cache.make_list(list_name, sort_order)
	if not success:
		kodi_utils.notification('Error Creating List', 3000)
		return None
	if any([kodi_utils.path_check('get_personal_lists') or kodi_utils.external()]): kodi_utils.kodi_refresh()
	return list_name

def unique_list_check(list_name):
	contents = personal_lists_cache.get_lists()
	list_names = [i['name'] for i in contents]
	if list_name in list_names:
		kodi_utils.ok_dialog('Personal Lists', 'List Already Exists[CR]Choose a different name')
		return False
	return True

def adjust_personal_list_properties(params):
	sort_order_dict = {'0': 'Title', '1': 'Date Added (asc)', '2': 'Date Added (desc)', '3': 'Release Date (asc)', '4': 'Release Date (desc)', '5': 'Shuffle'}
	list_name, sort_order = params.get('list_name', ''), params.get('sort_order', '')
	choices = [('Change Name', 'Currently [B]%s[/B]' % (list_name), 'list_name'),
				('Change Sort Order', 'Currently [B]%s[/B]' % sort_order_dict.get(sort_order, 'None'), 'sort_order'),
				('Empty List Contents', 'Delete All Contents of %s' % list_name, 'empty_contents')]
	list_items = [{'line1': item[0], 'line2': item[1] or item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Personal List Properties', 'multi_line': 'true', 'narrow_window': 'true'}
	action = kodi_utils.select_dialog([i[2] for i in choices], **kwargs)
	if action == None: return kodi_utils.kodi_refresh() if params.get('refresh', 'false') == 'true' else None
	if action == 'list_name':
		new_name = personal_list_name(list_name)
		if new_name == None: return adjust_personal_list_properties(params)
		personal_lists_cache.update_single_detail('name', new_name, list_name)
		params.update({'list_name': new_name, 'refresh': 'true'})
	elif action == 'sort_order':
		new_sort_order = personal_sort_order()
		if new_sort_order == None: return adjust_personal_list_properties(params)
		personal_lists_cache.update_single_detail('sort_order', new_sort_order, list_name)
		params.update({'sort_order': new_sort_order, 'refresh': 'true'})
	elif action == 'empty_contents':
		delete_personal_list_contents({'list_name': list_name})
		params.update({'refresh': 'true'})
	return adjust_personal_list_properties(params)

def personal_list_name(list_name=''):
	new_name = kodi_utils.kodi_dialog().input('Please Choose a Name for the New List', defaultt=list_name)
	if not new_name: return None
	new_name = unquote(new_name)
	return new_name

def personal_sort_order():
	choices = [('Title (asc)', '0'), ('Date Added (asc)', '1'), ('Date Added (desc)', '2'), ('Release Date (asc)', '3'), ('Release Date (desc)', '4'), ('Shuffle', '5')]
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'List Sort Order', 'narrow_window': 'true'}
	sort_order = kodi_utils.select_dialog([i[1] for i in choices], **kwargs)
	if sort_order == None: return None
	return sort_order

def list_change_warning(list_name, text='[B]CAUTION!!![/B][CR][CR]This will change the contents of [B]%s[/B]. Continue?'):
	return kodi_utils.confirm_dialog(heading='Personal Lists', text=text % list_name, ok_label='Yes', cancel_label='No')