# -*- coding: utf-8 -*-
# created by Venom for Fenomscrapers (2-10-2024) ud (updated 05/22/24)
'''
	Fenomscrapers Project
'''

from json import loads as jsloads
import re
from cocoscrapers.modules import client
from cocoscrapers.modules import source_utils
from cocoscrapers.modules import cache
from cocoscrapers.modules import log_utils
from cocoscrapers.modules import control

class source:
	priority = 1
	pack_capable = True
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "https://torrentio.elfhosted.com"
		self.movieSearch_link = '/stream/movie/%s.json'
		self.tvSearch_link = '/stream/series/%s:%s:%s.json'
		self.bypass_filter = control.setting('knightcrawler.bypass_filter')
		self.min_seeders = 0

	def _get_files(self, url):
		if self.get_pack_files: return []
		results = client.request(url, timeout=10)
		files = jsloads(results)['streams']
		return files

	def sources(self, data, hostDict):
		self.get_pack_files = False
		sources = []
		if not data:
			control.homeWindow.clearProperty('cocoscrapers.knightcrawler.performing_single_scrape')
			return sources
		sources_append = sources.append
		try:
			aliases = data['aliases']
			year = data['year']
			imdb = data['imdb']
			if 'tvshowtitle' in data:
				control.homeWindow.setProperty('cocoscrapers.knightcrawler.performing_single_scrape', 'true')
				title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ').replace('$', 's')
				episode_title = data['title']
				season = data['season']
				episode = data['episode']
				hdlr = 'S%02dE%02d' % (int(season), int(episode))
				years = None
				url = '%s%s' % (self.base_link, self.tvSearch_link % (imdb, season, episode))
				files = cache.get(self._get_files, 10, url)
			else:
				title = data['title'].replace('&', 'and').replace('/', ' ').replace('$', 's')
				episode_title = None
				hdlr = year
				years = [str(int(year)-1), str(year), str(int(year)+1)]
				url = '%s%s' % (self.base_link, self.movieSearch_link % imdb)
				files = self._get_files(url)
			control.homeWindow.clearProperty('cocoscrapers.knightcrawler.performing_single_scrape')
			_INFO = re.compile(r'💾.*')
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			control.homeWindow.clearProperty('cocoscrapers.knightcrawler.performing_single_scrape')
			source_utils.scraper_error('KNIGHTCRAWLER')
			return sources

		for file in files:
			try:
				hash = file['infoHash']
				file_title = file['title'].split('\n')
				file_info = [x for x in file_title if _INFO.match(x)][0]
				#updated by ud to fix elf hosted title format change.
				name = source_utils.clean_name(file_title[1])

				if self.bypass_filter == 'false':
					if not source_utils.check_title(title, aliases, name.replace('.(Archie.Bunker', ''), hdlr, year, years): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name) 
				try:
					seeders = int(re.search(r'(\d+)', file_info).group(1))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', file_info).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources_append({'provider': 'knightcrawler', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
											'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				control.homeWindow.clearProperty('cocoscrapers.knightcrawler.performing_single_scrape')
				source_utils.scraper_error('KNIGHTCRAWLER')
		return sources

	def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		self.get_pack_files = True
		sources = []
		if not data: return sources
		count, finished_single_scrape = 0, False
		control.sleep(2000)
		while count < 10000 and not finished_single_scrape:
			finished_single_scrape = control.homeWindow.getProperty('cocoscrapers.knightcrawler.performing_single_scrape') != 'true'
			control.sleep(100)
			count += 100
		if not finished_single_scrape: return sources
		sources_append = sources.append
		try:
			title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ').replace('$', 's')
			aliases = data['aliases']
			imdb = data['imdb']
			year = data['year']
			season = data['season']
			url = '%s%s' % (self.base_link, self.tvSearch_link % (imdb, season, data['episode']))
			files = cache.get(self._get_files, 10, url)
			_INFO = re.compile(r'💾.*')
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('KNIGHTCRAWLER')
			return sources

		for file in files:
			try:
				hash = file['infoHash']
				file_title = file['title'].split('\n')
				file_info = [x for x in file_title if _INFO.match(x)][0]
				name = source_utils.clean_name(file_title[0])
				if self.bypass_filter == 'true': bypass_filter = True
    
				episode_start, episode_end = 0, 0
				if not search_series:
					if not bypass_filter:
						valid, episode_start, episode_end = source_utils.filter_season_pack(title, aliases, year, season, name.replace('.(Archie.Bunker', ''))
						if not valid: continue
					package = 'season'

				elif search_series:
					if not bypass_filter:
						valid, last_season = source_utils.filter_show_pack(title, aliases, imdb, year, season, name.replace('.(Archie.Bunker', ''), total_seasons)
						if not valid: continue
					else: last_season = total_seasons
					package = 'show'

				name_info = source_utils.info_from_name(name, title, year, season=season, pack=package)
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
				try:
					seeders = int(re.search(r'(\d+)', file_info).group(1))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', file_info).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'knightcrawler', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if search_series: item.update({'last_season': last_season})
				elif episode_start: item.update({'episode_start': episode_start, 'episode_end': episode_end}) # for partial season packs
				sources_append(item)
			except:
				source_utils.scraper_error('KNIGHTCRAWLER')
		return sources