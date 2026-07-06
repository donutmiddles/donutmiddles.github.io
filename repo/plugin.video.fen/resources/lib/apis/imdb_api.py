# -*- coding: utf-8 -*-
import re
import json
import requests
from html import unescape
from caches.base_cache import connect_database
from caches.main_cache import cache_object
from caches.settings_cache import get_setting
from modules.dom_parser import parseDOM
from modules.kodi_utils import sleep
from modules.utils import remove_accents, replace_html_codes, normalize
# from modules.kodi_utils import logger

GQL_URL  = 'https://graphql.imdb.com/'
GQL_HEADERS = {
	'Content-Type': 'application/json',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
	'Accept': 'application/json', 'Origin': 'https://www.imdb.com', 'Referer': 'https://www.imdb.com/',
	'x-imdb-client-name': 'imdb-web-next-localized', 'x-imdb-user-language': 'en-US', 'x-imdb-user-country': 'US'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36', 'Accept-Language':'en-us,en;q=0.5'}

def _clean(text):
	if not text: return ''
	text = text.replace('<br/><br/>', '\n').replace('<br/>', '\n').replace('<br>', '\n')
	text = re.sub(r'<a[^>]*>', '', text).replace('</a>', '')
	text = re.sub(r'<[^>]+>', '', text)
	text = replace_html_codes(text)
	text = remove_accents(text)
	return text.strip()

def imdb_photos(imdb_id):
	def _process(foo):
		imdb_list = []
		imdb_list_append = imdb_list.append
		try:
			payload = {'query': query, 'variables': {'id': imdb_id}}
			result = requests.post(GQL_URL, json=payload, headers=GQL_HEADERS, timeout=10).json()
			edges = result['data'][data_key]['images']['edges']
		except: edges = []
		count = 1
		for edge in edges:
			try:
				url = edge['node']['url']
				if '@@' in url: insert = '@@'
				else: insert = '@'
				try: thumb = url.split(insert)[0] + '%s._V1_UX300_QL75_.jpg' % insert
				except: continue
				caption = edge['node']['caption']['plainText']
				imdb_list_append({'name': '%s_%03d' % (caption, count), 'path': url, 'thumb': thumb})
				count += 1
			except: pass
		return imdb_list
	if imdb_id.startswith('tt'): query, data_key = 'query($id: ID!){title(id:$id){titleText{text}images(first:1000){edges{node{id url caption {plainText}}}}}}', 'title'
	else: query, data_key = 'query($id:ID!){name(id:$id){nameText{text}images(first:1000){edges{node{id url caption {plainText}}}}}}', 'name'
	string = 'imdb_photos_%s' % imdb_id
	return cache_object(_process, string, 'foo', False, 168)

def imdb_video_info(imdb_id):
	def _process(foo):
		videos = []
		videos_append = videos.append
		res_dict = {'DEF_1080p': '1080p', 'DEF_720p': '720p', 'DEF_480p': '480p', 'DEF_240p':'240p'}
		try:
			payload = {'query': 'query($id: ID!){video(id: $id){id name{value}playbackURLs{url videoDefinition}}}', 'variables': {'id': imdb_id}}
			result = requests.post(GQL_URL, json=payload, headers=GQL_HEADERS, timeout=10).json()
			name = result['data']['video']['name']['value']
			for i in result['data']['video']['playbackURLs']:
				try:
					try: resolution = res_dict[i['videoDefinition']]
					except: continue
					videos_append({'url': i['url'], 'name': name, 'resolution': resolution})
				except: pass
		except: videos = []
		return videos
	string = 'imdb_video_info_%s' % imdb_id
	return cache_object(_process, string, 'foo', False, 168)

def imdb_extras(imdb_id):
	def _process(foo):
		trivia, blunders, reviews, quotes, faqs, parentsguide, videos = [], [], [], [], [], [], []
		payload = {'query': query, 'variables': {'id': imdb_id}}
		result = requests.post(GQL_URL, json=payload, headers=GQL_HEADERS, timeout=10)
		result = result.json().get('data', {}).get('title', {})
		try:
			count = 1
			for i in result['faqs']['edges']:
				try:
					question, answer = unescape(_clean(i['node']['question']['plaidHtml'])), unescape(_clean(i['node']['answer']['plaidHtml']))
					faqs.append('[B]FAQS %02d.[/B][CR][CR][B]%s[/B][CR][CR]%s' % (count, question, answer))
					count += 1
				except: pass
		except: pass
		try:
			for i in result['primaryVideos']['edges']:
				video_id = i['node']['id']
				video_name = unescape(_clean(i['node']['name']['value']))
				video_content = i['node']['contentType']['displayName']['value']
				video_thumb = i['node']['thumbnail']['url']
				if '@@' in video_thumb: insert = '@@'
				else: insert = '@'
				try: thumb = video_thumb.split(insert)[0] + '%s._V1_UX480_CR0,0,480,360.jpg' % insert
				except: thumb = video_thumb
				videos.append({'id': video_id, 'name': video_name, 'content': video_content, 'thumb': thumb})
		except: pass
		try:
			count = 1
			for i in sorted(result['reviews']['edges'], key=lambda k: k['node']['submissionDate'], reverse=True):
				try:
					content = unescape(_clean(i['node']['text']['originalText']['plaidHtml']))
					if not content: continue
					try: spoiler = i['node']['spoiler']
					except: spoiler = False
					try:
						rating = i['node']['authorRating']
						rating = str(rating) if rating is not None else '-'
					except: rating = '-'
					try: title = i['node']['summary']['originalText']
					except: title = '-----'
					try: date = i['node']['submissionDate']
					except: date = '-----'
					review = '[B]%02d. [I]%s/10 - %s - %s[/I][/B][CR][CR]%s' % (count, rating, date, title, content)
					if spoiler: review = '[B][COLOR red][CONTAINS SPOILERS][/COLOR][CR][/B]' + review
					reviews.append(review)
					count += 1
				except: pass
		except: pass
		try:
			count = 1
			for i in sorted(result['trivia']['edges'], key=lambda k: k['node']['interestScore']['usersVoted'], reverse=True):
				try: trivia.append('[B]TRIVIA %02d.[/B][CR][CR]%s' % (count, unescape(_clean(i['node']['displayableArticle']['body']['plaidHtml']))))
				except: pass
				count += 1
		except: pass
		try:
			count = 1
			for i in sorted(result['goofs']['edges'], key=lambda k: k['node']['interestScore']['usersVoted'], reverse=True):
				try: blunders.append('[B]BLUNDERS %02d.[/B][CR][CR]%s' % (count, unescape(_clean(i['node']['displayableArticle']['body']['plaidHtml']))))
				except: pass
				count += 1
		except: pass
		try:
			count = 1
			for i in result['quotes']['edges']:
				try:
					block_lines = ['[B]QUOTES %02d.[/B]' % count]
					isSpoiler = i['node']['isSpoiler']
					if isSpoiler: block_lines.append('[B][COLOR red][CONTAINS SPOILERS][/COLOR]')
						
					for i in i['node']['lines']:
						construct_line = []
						stageDirection = i['stageDirection']
						characters = i['characters']
						text = i['text']
						if isSpoiler: construct_line.append('[B][COLOR red][CONTAINS SPOILERS][/COLOR][CR][/B]')
						if characters: construct_line.append(', '.join('[B]%s[/B]' % unescape(_clean(i['name']['nameText']['text'].upper())) for i in characters))
						if stageDirection: construct_line.append('[I][%s][/I]' % unescape(_clean(stageDirection)))
						if text: construct_line.append(unescape(_clean(text)))
						formatted_line = '[CR]'.join(construct_line)
						block_lines.append(formatted_line)
					quotes.append('[CR][CR]'.join(block_lines))
					count += 1
				except: pass
		except: pass
		try:
			title_converter = {'nudity': 'Sex & Nudity', 'violence': 'Violence & Gore', 'profanity': 'Profanity',
								'alcohol': 'Alcohol, Drugs & Smoking', 'frightening': 'Frightening & Intense Scenes'}
			for i in result['parentsGuide']['categories']:
				try:
					title = title_converter[i['category']['id'].lower()]
					ranking = i['severity']['id'].replace('Votes', '')
					try:
						listings = [unescape(_clean(x['node']['text']['plaidHtml'])) for x in i['guideItems']['edges']]
						content = '\n\n'.join(['%02d. %s' % (count, i) for count, i in enumerate(listings, 1)])
					except: content, listings = [], []
					total_count = len(listings)
					parentsguide.append({'title': title, 'ranking': ranking, 'content': content, 'total_count': total_count})
				except: pass
		except: pass
		return {'reviews': reviews, 'trivia': trivia, 'blunders': blunders, 'quotes': quotes, 'faqs': faqs, 'videos': videos, 'parentsguide': parentsguide}
	query = ('query($id:ID!){title(id:$id){titleText{text}'
	'primaryVideos(first:50){edges{node{id name{value}contentType{displayName{value}}thumbnail{url}}}}'
	'quotes(first:50){edges{node{isSpoiler lines{stageDirection text characters{name{nameText{text}}}}}}}'
	'trivia(first:50){edges{node{displayableArticle{body{plaidHtml}}interestScore{usersVoted}}}}'
	'goofs(first:50){edges{node{displayableArticle{body{plaidHtml}}interestScore{usersVoted}}}}faqs(first:50){edges{node{id question{plaidHtml}answer{plaidHtml}}}}'
	'reviews(first:50){edges{node{spoiler author{nickName}authorRating summary{originalText}text{originalText{plaidHtml}}submissionDate}}}'
	'parentsGuide{categories{category{id}guideItems(first:10){edges{node{isSpoiler text{plaidHtml}}}}severity{id votedFor}}}}}')
	string = 'imdb_extras_%s' % imdb_id
	return cache_object(_process, string, 'foo', False, 168)

def imdb_people(imdb_id):
	def _process(foo):
		trivia, quotes, videos = [], [], []
		payload = {'query': query, 'variables': {'id': imdb_id}}
		result = requests.post(GQL_URL, json=payload, headers=GQL_HEADERS, timeout=10)
		result = result.json().get('data', {}).get('name', {})
		try:
			for i in result['primaryVideos']['edges']:
				try:
					video_id = i['node']['id']
					video_name = unescape(_clean(i['node']['name']['value']))
					video_content = i['node']['contentType']['displayName']['value']
					video_thumb = i['node']['thumbnail']['url']
					if '@@' in video_thumb: insert = '@@'
					else: insert = '@'
					try: thumb = video_thumb.split(insert)[0] + '%s._V1_UX480_CR0,0,480,360.jpg' % insert
					except: thumb = video_thumb
					videos.append({'id': video_id, 'name': video_name, 'content': video_content, 'thumb': thumb})
				except: pass
		except: pass
		try:
			count = 1
			for i in result['quotes']['edges']:
				try:
					text = '[B]QUOTES %02d.[/B][CR][CR]%s' % (count, unescape(_clean(i['node']['text']['plaidHtml'])))
					quotes.append(text)
					count += 1
				except: pass
		except: pass
		try:
			for count, i in enumerate(result['trivia']['edges'], 1):
				try: trivia.append('[B]TRIVIA %02d.[/B][CR][CR]%s' % (count, unescape(_clean(i['node']['text']['plaidHtml']))))
				except: pass
		except: pass
		return {'trivia': trivia, 'quotes': quotes, 'videos': videos}
	query = ('query($id:ID!){name(id:$id){nameText{text}'
	'primaryVideos(first:50){edges{node{id name{value}contentType{displayName{value}}thumbnail{url}}}}'
	'trivia(first:50){edges{node{text{plaidHtml}}}}quotes(first:50){edges{node{text{plaidHtml}}}}}}')
	string = 'imdb_people_%s' % imdb_id
	return cache_object(_process, string, 'foo', False, 168)

def imdb_more_like_this(imdb_id):
	def _process(foo):
		imdb_list = []
		imdb_list_append = imdb_list.append
		try:
			payload = {'query': 'query($id:ID!){title(id:$id){moreLikeThisTitles(first:20){edges{node{id}}}}}', 'variables': {'id': imdb_id}}
			result = requests.post(GQL_URL, json=payload, headers=GQL_HEADERS, timeout=10).json()
			for i in result['data']['title']['moreLikeThisTitles']['edges']:
				try:
					_id = i['node']['id']
					if _id.startswith('tt'): imdb_list_append(_id)
				except: pass
			imdb_list = [i for n, i in enumerate(imdb_list) if i not in imdb_list[n + 1:]]
		except: pass
		return imdb_list
	string = 'imdb_more_like_this_%s' % imdb_id
	return cache_object(_process, string, 'foo', False, 168)

def imdb_people_id(actor_name):
	def _process(foo):
		imdb_id = ''
		try:
			url, url_backup = 'https://sg.media-imdb.com/suggests/%s/%s.json' % (name[0], name.replace(' ', '%20')), 'https://www.imdb.com/search/name/?name=%s' % name
			result = requests.get(url, timeout=5)
			results = json.loads(re.sub(r'imdb\$(.+?)\(', '', result.text)[:-1])['d']
			imdb_id = [i['id'] for i in results if i['id'].startswith('nm') and i['l'].lower() == name][0]
		except: imdb_id = ''
		if not imdb_id:
			try:
				result = requests.get(url_backup, timeout=10, headers=headers)
				result = remove_accents(result.text)
				result = result.replace('\n', ' ')
				result = parseDOM(result, 'div', attrs={'class': 'lister-item-image'})[0]
				imdb_id = re.search(r'href="/name/(.+?)"', result, re.DOTALL).group(1)
			except: pass
		return imdb_id
	name = actor_name.lower()
	string = 'imdb_people_id_%s' % name
	return cache_object(_process, string, 'foo', False, 8736)

def imdb_year_check(imdb_id):
	def _process(foo):
		imdb_list = []
		try:
			result = requests.get('https://v2.sg.media-imdb.com/suggestion/t/%s.json' % imdb_id, timeout=5).json()
			imdb_list = [str(i['y']) for i in result['d'] if i['id'] == imdb_id][0]
		except: pass
		return imdb_list
	string = 'imdb_year_check%s' % imdb_id
	return cache_object(_process, string, 'foo', False, 720)

def clear_imdb_cache(silent=False):
	try:
		dbcon = connect_database('maincache_db')
		results = dbcon.execute("SELECT id FROM maincache WHERE id LIKE ?", ('imdb_%',)).fetchall()
		dbcon.execute("DELETE FROM maincache WHERE id LIKE ?", ('imdb_%',))
		return True
	except: return False

def refresh_imdb_meta_data(imdb_id):
	try:
		insert1, insert2 = '%%%s' % imdb_id, '%%%s_%%' % imdb_id
		dbcon = connect_database('maincache_db')
		dbcon.execute("DELETE FROM maincache WHERE id LIKE ?", (insert1,))
		dbcon.execute("DELETE FROM maincache WHERE id LIKE ?", (insert2,))
		return True
	except: return False
