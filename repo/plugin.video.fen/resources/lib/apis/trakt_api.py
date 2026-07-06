# -*- coding: utf-8 -*-
import requests
from caches.main_cache import cache_object
from caches.lists_cache import lists_cache_object
from modules import kodi_utils, settings
from modules.utils import get_datetime, replace_html_codes, TaskPool, sort_list, jsondate_to_datetime as js2date
# logger = kodi_utils.logger

def get_trakt_list_contents(list_id):
	def _process(dummy):
		data = get_trakt(params)
		sort_by, sort_how = data['sort_by'], data['sort_how']
		data = data['data']
		for i in data:
			if i['type'] == 'season': i['season']['title'] = '%s - %s' % (i['show']['title'], i['season']['title'])
			elif i['type'] == 'episode': i['episode']['title'] = '%s - %s' % (i['show']['title'], i['episode']['title'])
			else: pass
		data = sort_list(sort_by, sort_how, data)
		for c, i in enumerate(data):
			try:
				_type = i['type']
				if _type in ('movie', 'show'):
					r_key = 'released' if _type == 'movie' else 'first_aired'
					data = {'media_ids': i[_type]['ids'], 'title': i[_type]['title'], 'type': _type, 'order': c, 'released': i[_type][r_key], 'media_type': _type}
				elif _type == 'season':
					data = {'tmdb_id': i['show']['ids']['tmdb'], 'season': i[_type]['number'], 'type': _type, 'custom_order': c}
				elif _type == 'episode':
					data = {'media_ids': i['show']['ids'], 'title': i['show']['title'], 'type': _type,
							'season': i[_type]['season'], 'episode': i[_type]['number'], 'custom_order': c}
				results_append(data)
			except: pass
		return results
	string = 'trakt_list_contents_%s' % (list_id)
	params = {'path': '/lists/%s/items', 'path_insert': list_id, 'params': {'extended':'full', 'limit': 999}, 'sort_by_headers': True}
	results = []
	results_append = results.append
	return lists_cache_object(_process, string, params)

def trakt_search_lists(search_title, page_no):
	def _process(dummy_arg):
		return call_trakt('search', params={'type': 'list', 'fields': 'name,description', 'query': search_title, 'limit': 50}, pagination=True, page_no=page_no)
	string = 'trakt_search_lists_%s_%s' % (search_title, page_no)
	return cache_object(_process, string, 'dummy_arg', False, 4)

def trakt_get_lists(list_type, list_mode, page_no='1'):
	string = 'trakt_%s_%s_user_lists_%s' % (list_type, list_mode, page_no)
	params = {'path': 'lists/%s/%s', 'path_insert': (list_type, list_mode), 'params': {'limit': 50}, 'page_no': page_no}
	return lists_cache_object(get_trakt, string, params)

def no_client_key():
	kodi_utils.notification('Please set a valid Trakt Client ID Key')
	return None

def no_secret_key():
	kodi_utils.notification('Please set a valid Trakt Client Secret Key')
	return None

def get_trakt(params):
	result = call_trakt(params['path'] % params.get('path_insert', ''), params=params.get('params', {}), pagination=params.get('pagination', True),
		page_no=params.get('page_no'), sort_by_headers=params.get('sort_by_headers'))
	return result[0] if params.get('pagination', True) else result

def call_trakt(path, params={}, pagination=False, page_no=1, sort_by_headers=False):
	def send_query():
		resp = None
		try:
			resp = requests.get(API_ENDPOINT % path, params=params, headers=headers, timeout=10)
			resp.raise_for_status()
		except Exception as e: kodi_utils.logger('Trakt Error', str(e))
		return resp
	API_ENDPOINT = 'https://api.trakt.tv/%s'
	CLIENT_ID = settings.trakt_client()
	if CLIENT_ID in (None, 'empty_setting', ''): return no_client_key()
	headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
	if pagination: params['page'] = page_no
	response = send_query()
	try: status_code = response.status_code
	except: return None
	headers = response.headers
	if status_code == 401: return None
	elif status_code == 429:
		if 'Retry-After' in headers:
			kodi_utils.sleep(1000 * headers['Retry-After'])
			response = send_query()
	response.encoding = 'utf-8'
	result = response.json() if 'json' in headers.get('Content-Type', '') else response.text
	if sort_by_headers:
		sort_by, sort_how = headers.get('X-Sort-By', 'title'), headers.get('X-Sort-How', 'asc')
		result = {'sort_by': sort_by, 'sort_how': sort_how, 'data': result}
	if pagination: return (result, headers.get('X-Pagination-Page-Count', page_no))
	else: return result

def trakt_movies_related(imdb_id):
	string = 'trakt_movies_related_%s' % imdb_id
	params = {'path': 'movies/%s/related?extended=full', 'path_insert': imdb_id, 'params': {'limit': 20}}
	return lists_cache_object(get_trakt, string, params)

def trakt_movies_trending(page_no):
	string = 'trakt_movies_trending_%s' % page_no
	params = {'path': 'movies/trending/%s', 'params': {'limit': 20}, 'page_no': page_no}
	return lists_cache_object(get_trakt, string, params)

def trakt_movies_trending_recent(page_no):
	current_year = get_datetime().year
	years = '%s-%s' % (str(current_year-1), str(current_year))
	string = 'trakt_movies_trending_recent_%s' % page_no
	params = {'path': 'movies/trending/%s', 'params': {'limit': 20, 'years': years}, 'page_no': page_no}
	return lists_cache_object(get_trakt, string, params)

def trakt_tv_related(imdb_id):
	string = 'trakt_tv_related_%s' % imdb_id
	params = {'path': 'shows/%s/related?extended=full', 'path_insert': imdb_id, 'params': {'limit': 20}}
	return lists_cache_object(get_trakt, string, params)

def trakt_tv_trending(page_no):
	string = 'trakt_tv_trending_%s' % page_no
	params = {'path': 'shows/trending/%s', 'params': {'limit': 20}, 'page_no': page_no}
	return lists_cache_object(get_trakt, string, params)

def trakt_tv_trending_recent(page_no):
	current_year = get_datetime().year
	years = '%s-%s' % (str(current_year-1), str(current_year))
	string = 'trakt_tv_trending_recent_%s' % page_no
	params = {'path': 'shows/trending/%s', 'params': {'years': years, 'limit': 20}, 'page_no': page_no}
	return lists_cache_object(get_trakt, string, params)

def trakt_comments(media_type, imdb_id):
	def _process(foo):
		data = get_trakt(params)
		for count, item in enumerate(data, 1):
			try:
				rating = '%s/10 - ' % item['user_rating'] if item['user_rating'] else ''
				comment = template % \
				(count, rating, item['user']['username'].upper(), js2date(item['created_at'], date_format, True).strftime('%d %B %Y'), replace_html_codes(item['comment']))
				if item['spoiler']: comment = spoiler_template + comment
				all_comments_append(comment)
			except: pass
		return all_comments
	all_comments = []
	all_comments_append = all_comments.append
	template, spoiler_template, date_format = '[B]%02d. [I]%s%s - %s[/I][/B][CR][CR]%s', '[B][COLOR red][CONTAINS SPOILERS][/COLOR][CR][/B]', '%Y-%m-%dT%H:%M:%S.000Z'
	media_type = 'movies' if media_type in ('movie', 'movies') else 'shows'
	string = 'trakt_comments_%s %s' % (media_type, imdb_id)
	params = {'path': '%s/%s/comments', 'path_insert': (media_type, imdb_id), 'params': {'limit': 1000, 'sort': 'likes'}, 'pagination': False}
	return cache_object(_process, string, 'foo', False, 168)

def make_trakt_slug(name):
	import re
	name = name.strip()
	name = name.lower()
	name = re.sub('[^a-z0-9_]', '-', name)
	name = re.sub('--+', '-', name)
	return name
