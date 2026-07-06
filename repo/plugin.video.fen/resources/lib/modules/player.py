# -*- coding: utf-8 -*-
import xbmc
import json
from threading import Thread
from datetime import timedelta
from apis.introdb import episode_intros
from apis.trakt_api import make_trakt_slug
from caches.settings_cache import get_setting
from modules import kodi_utils as ku, settings as st, watched_status as ws
# logger = ku.logger

class FenPlayer(xbmc.Player):
	def __init__ (self):
		xbmc.Player.__init__(self)

	def run(self, url=None, obj=None):
		ku.hide_busy_dialog()
		self.clear_playback_properties()
		if not url: return self.run_error()
		try: return self.play_video(url, obj)
		except: return self.run_error()

	def play_video(self, url, obj):
		self.set_constants(url, obj)
		ku.volume_checker()
		self.play(self.url, self.make_listing())
		if not self.is_generic:
			self.check_playback_start()
			if self.playback_successful: self.monitor()
			else:
				self.obj.playback_successful = self.playback_successful
				self.obj.cancel_all_playback = self.cancel_all_playback
				if self.cancel_all_playback: self.kill_dialog()
				self.stop()
			try: del self.kodi_monitor
			except: pass

	def check_playback_start(self):
		resolve_percent = 0
		provider = self.playing_item['scrape_provider']
		retry_active = 'retry_active' in self.playing_item
		while self.playback_successful is None:
			ku.hide_busy_dialog()
			if not self.obj.progress_dialog: self.playback_successful = True
			elif self.obj.progress_dialog.skip_resolved(): self.playback_successful = False
			elif self.obj.progress_dialog.iscanceled() or self.kodi_monitor.abortRequested(): self.cancel_all_playback, self.playback_successful = True, False
			elif provider == 'easynews' and not retry_active and resolve_percent >= 18.0: self.playback_successful = False
			elif resolve_percent >= 100: self.playback_successful = False
			elif ku.get_visibility('Window.IsTopMost(okdialog)'):
				ku.execute_builtin('SendClick(okdialog, 11)')
				self.playback_successful = False
			elif self.isPlayingVideo():
				try:
					if self.getTotalTime() not in ('0.0', '', 0.0, None) and ku.get_visibility('Window.IsActive(fullscreenvideo)'): self.playback_successful = True
				except: pass
			resolve_percent = round(resolve_percent + 26.0/100, 1)
			self.obj.progress_dialog.update_resolver(percent=resolve_percent)
			ku.sleep(50)

	def playback_close_dialogs(self):
		self.obj.playback_successful = True
		self.kill_dialog()
		ku.sleep(200)
		ku.close_all_dialog()

	def monitor(self):
		try:
			ensure_dialog_dead, total_check_time = False, 0
			if self.media_type == 'episode':
				play_random_continual = self.obj.random_continual
				play_random = self.obj.random
				disable_autoplay_next_episode = self.obj.disable_autoplay_next_episode
				if disable_autoplay_next_episode: ku.notification('Scrape with Custom Values - Autoplay Next Episode Cancelled', 4500)
				if any((play_random_continual, play_random, disable_autoplay_next_episode)): self.autoplay_nextep = False
				else: self.autoplay_nextep = self.obj.autoplay_nextep
			else:
				show_stinger = st.stingers_show()
				play_random_continual, self.autoplay_nextep = False, False
			while total_check_time <= 30 and not ku.get_visibility('Window.IsActive(fullscreenvideo)'):
				ku.sleep(100)
				total_check_time += 0.10
			ku.hide_busy_dialog()
			ku.sleep(1000)
			self.showSubtitles(True)
			while self.isPlayingVideo():
				try:
					if not ensure_dialog_dead:
						ensure_dialog_dead = True
						self.playback_close_dialogs()
					ku.sleep(1000)
					try: self.total_time, self.curr_time = self.getTotalTime(), self.getTime()
					except: ku.sleep(250); continue
					self.current_point = round(float(self.curr_time/self.total_time * 100), 1)
					if self.current_point >= 90:
						if play_random_continual: self.run_random_continual(); break
						if not self.media_marked: self.media_watched_marker()
					if self.media_type == 'episode':
						if self.obj.intro_checklist: self.run_episode_intro()
						if self.autoplay_nextep:
							if not self.nextep_info_gathered: self.info_next_ep()
							if round(self.total_time - self.curr_time) <= self.start_prep: return self.run_next_ep()
					elif show_stinger and not self.movie_stingers_run: 
						final_chapter = self.final_chapter(75) or 90
						if self.current_point >= final_chapter: self.run_movie_stingers()
				except: pass
			ku.hide_busy_dialog()
			if not self.media_marked: self.media_watched_marker()
			self.clear_playback_properties()
		except:
			ku.hide_busy_dialog()
			self.obj.playback_successful = False
			self.obj.cancel_all_playback = True
			return self.kill_dialog()

	def make_listing(self):
		listitem = ku.make_listitem()
		listitem.setPath(self.url)
		listitem.setContentLookup(False)
		info_tag = listitem.getVideoInfoTag(True)
		info_tag.setFilenameAndPath(self.url)
		if self.is_generic: info_tag.setMediaType('video')
		else:
			self.tmdb_id, self.imdb_id, self.tvdb_id = self.meta_get('tmdb_id', ''), self.meta_get('imdb_id', ''), self.meta_get('tvdb_id', '')
			self.title, self.year = self.meta_get('title'), self.meta_get('year')
			self.season, self.episode = self.meta_get('season', ''), self.meta_get('episode', '')
			poster, clearlogo = self.meta_get('poster') or ku.get_icon('box_office'), self.meta_get('clearlogo') or ''
			genre, tagline = self.meta_get('genre', ''), self.meta_get('tagline')
			plot = self.meta_get('plot') or self.meta_get('tvshow_plot') or ''
			listitem.setLabel(self.title)
			listitem.setArt({'poster': poster, 'icon': poster, 'clearlogo': clearlogo})
			if self.media_type == 'movie': display_title, unique_ids, = self.title, {'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id)}
			else:
				display_title, unique_ids = self.meta_get('ep_name'), {'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id), 'tvdb': str(self.tvdb_id)}
				info_tag.setTvShowTitle(self.title), info_tag.setSeason(self.season), info_tag.setEpisode(self.episode)
			info_tag.setPlot(plot), info_tag.setYear(int(self.year)), info_tag.setTagLine(tagline), info_tag.setGenres(genre), info_tag.setIMDBNumber(self.imdb_id)
			info_tag.setTitle(display_title), info_tag.setMediaType(self.media_type), info_tag.setUniqueIDs(unique_ids)
			self.set_resume_point(listitem)
			self.set_playback_properties()
		return listitem

	def media_watched_marker(self, force_watched=False):
		self.media_marked = True
		try:
			if self.current_point >= 90 or force_watched:
				watched_function = ws.mark_movie if self.media_type == 'movie' else ws.mark_episode
				watched_params = {'action': 'mark_as_watched', 'tmdb_id': self.tmdb_id, 'title': self.title, 'year': self.year, 'season': self.season, 'episode': self.episode,
									'tvdb_id': self.tvdb_id, 'from_playback': 'true'}
				Thread(target=self.run_media_progress, args=(watched_function, watched_params)).start()
			else:
				ku.clear_property('fen.random_episode_history')
				if self.current_point >= 5:
					progress_params = {'media_type': self.media_type, 'tmdb_id': self.tmdb_id, 'curr_time': self.curr_time, 'total_time': self.total_time,
									'title': self.title, 'season': self.season, 'episode': self.episode, 'from_playback': 'true'}
					Thread(target=self.run_media_progress, args=(ws.set_bookmark, progress_params)).start()
		except: pass

	def run_media_progress(self, function, params):
		try: function(params)
		except: pass

	def run_episode_intro(self):
		for current in self.obj.intro_checklist:
			seek_time, text = None, None
			other = 'intro' if current == 'recap' else 'recap'
			curr_run, curr_start, curr_end = getattr(self, '%s_run' % current), getattr(self.obj, 'start_%s' % current), getattr(self.obj, 'end_%s' % current)
			other_run, other_start, other_end = getattr(self, '%s_run' % other), getattr(self.obj, 'start_%s' % other), getattr(self.obj, 'end_%s' % other)
			if not curr_run:
				if self.curr_time >= curr_start:
					setattr(self, '%s_run' % current, True)
					if not other_run and other_start is not None:
						if curr_end > other_end:
							setattr(self, '%s_run' % other, True)
							seek_time, text = curr_end, '%s & %s' % (current.upper(), other.upper())
						elif other_start - curr_end < 5:
							setattr(self, '%s_run' % other, True)
							seek_time, text = other_end, '%s & %s' % (current.upper(), other.upper())
						else: seek_time, text = curr_end, current.upper()
					else: seek_time, text = curr_end, current.upper()
					if seek_time - self.curr_time < 3: seek_time, text = None, 'RECAP & INTRO passed'
			self.obj.intro_checklist = [i for i in self.obj.intro_checklist if not getattr(self, '%s_run' % i)]

			if seek_time:
				self.seekTime(seek_time)
				text = 'Skip %s: [B]END %s[/B]' % (text, str(timedelta(seconds=seek_time)))
			if text: ku.notification(text, 5000)

	def run_next_ep(self):
		from modules.episode_tools import EpisodeTools
		if not self.media_marked: self.media_watched_marker(force_watched=True)
		EpisodeTools(self.meta, self.nextep_settings).auto_nextep()

	def run_random_continual(self):
		from modules.episode_tools import EpisodeTools
		if not self.media_marked: self.media_watched_marker(force_watched=True)
		EpisodeTools(self.meta).play_random_continual(False)

	def run_movie_stingers(self):
		self.movie_stingers_run = True
		stinger_keys = self.meta.get('stinger_keys', None)
		if not stinger_keys:
			try:
				keywords = self.meta.get('keywords', [])
				stinger_keys = [i['name'] for i in keywords['keywords'] if i['name'] in ('duringcreditsstinger', 'aftercreditsstinger')]
				self.meta['stinger_keys'] = stinger_keys
			except: pass
		if stinger_keys:
			from windows.base_window import open_window
			Thread(target=lambda: open_window(('windows.playback_notifications', 'StingersNotification'), 'playback_notifications.xml', meta=self.meta)).start()

	def set_resume_point(self, listitem):
		if self.playback_percent > 0.0: listitem.setProperty('StartPercent', str(self.playback_percent))

	def info_next_ep(self):
		self.nextep_info_gathered = True
		try:
			percentage, start_outro, final_chapter = None, self.obj.start_outro, self.final_chapter(90)
			if start_outro is not None and round(self.total_time - start_outro) > 10: percentage = 100 - round(start_outro/self.total_time * 100)
			if not percentage and final_chapter: percentage = 100 - final_chapter
			if not percentage: percentage = 5
		except: percentage = 5
		window_time = round((percentage/100) * self.total_time)
		self.start_prep = int(get_setting('fenlight.results.timeout', '60')) + window_time
		self.nextep_settings = {'window_time': window_time, 'play_type': 'autoplay_nextep'}

	def final_chapter(self, threshhold):
		try:
			final_chapter = float(ku.get_infolabel('Player.Chapters').split(',')[-1])
			if final_chapter >= threshhold: return final_chapter
		except: pass
		return None

	def kill_dialog(self):
		try: self.obj._kill_progress_dialog()
		except: ku.close_all_dialog()

	def set_constants(self, url, obj):
		self.url = url
		self.obj = obj
		self.is_generic = self.obj == 'video'
		if not self.is_generic:
			self.meta = self.obj.meta
			self.meta_get, self.kodi_monitor, self.playback_percent = self.meta.get, ku.kodi_monitor(), self.obj.playback_percent or 0.0
			self.playing_filename = self.obj.playing_filename
			self.media_marked, self.nextep_info_gathered, self.movie_stingers_run = False, False, False
			self.playback_successful, self.cancel_all_playback = None, False
			self.playing_item = self.obj.playing_item
			self.media_type = self.meta_get('media_type')
			if self.media_type == 'episode': self.recap_run, self.intro_run = False, False

	def set_playback_properties(self):
		try:
			trakt_ids = {'tmdb': self.tmdb_id, 'imdb': self.imdb_id, 'slug': make_trakt_slug(self.title)}
			if self.media_type == 'episode': trakt_ids['tvdb'] = self.tvdb_id
			ku.set_property('script.trakt.ids', json.dumps(trakt_ids))
			if self.playing_filename: ku.set_property('subs.player_filename', self.playing_filename)
		except: pass

	def clear_playback_properties(self):
		ku.clear_property('fen.window_stack')
		ku.clear_property('script.trakt.ids')
		ku.clear_property('subs.player_filename')

	def run_error(self):
		try: self.obj.playback_successful = False
		except: pass
		self.clear_playback_properties()
		ku.notification('Playback Failed', 3500)
		return False
