# -*- coding: utf-8 -*-
import sys
from modules import kodi_utils, settings, watched_status as ws
from modules.metadata import tvshow_meta, episodes_meta
from modules.utils import jsondate_to_datetime, adjust_premiered_date, make_day, get_datetime, get_current_timestamp, title_key, date_difference, TaskPool
# logger = kodi_utils.logger

def build_episode_list(params):
	def _process():
		for item in episodes_data:
			try:
				cm = []
				cm_append = cm.append
				cm_extend = cm.extend
				listitem = make_listitem()
				set_properties = listitem.setProperties
				item_get = item.get
				season, episode, ep_name = item_get('season'), item_get('episode'), item_get('title')
				season_special = season == 0
				episode_date, premiered = adjust_premiered_date(item_get('premiered'), adjust_hours)
				episode_type = item_get('episode_type') or ''
				episode_id = item_get('episode_id') or None
				if season_special: playcount, progress = 0, None
				else:
					playcount = ws.get_watched_status_episode(watched_info, (season, episode))
					if total_seasons: progress = ws.get_progress_status_all_episode(bookmarks, season, episode)
					else: progress = ws.get_progress_status_episode(bookmarks, episode)
				thumb, plot, duration = item_get('thumb', None) or show_landscape or show_fanart, item_get('plot') or tvshow_plot, item_get('duration')
				if episode_type:
					status_label, status_highlight = episode_status_dict[episode_type]
					plot = '[COLOR %s]%s[/COLOR][CR]%s' % (status_highlight, status_label, plot)
				if not duration:
					duration = show_duration
					item['duration'] = duration
				if not episode_date or current_date < episode_date:
					display, unaired = '[COLOR red][I]%s[/I][/COLOR]' % ep_name, True
					item['title'] = display
				else: display, unaired = ep_name, False
				play_params = build_url({'mode': 'playback.media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode, 'playcount': playcount,
										'episode_id': episode_id})
				cm_extend([
				['extras', ('[B]Extras[/B]', 'RunPlugin(%s)' % build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'episode'}))],
				['cast', ('[B]Cast[/B]', 'RunPlugin(%s)' % build_url({'mode': 'tmdb_cast_dialog_image_results', 'media_type': 'episode', 'tmdb_id': tmdb_id,
					'season': season, 'episode': episode}))],
				['more_info', ('[B]More Info[/B]', 'RunPlugin(%s)' % build_url({'mode': 'media_extra_info_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id}))],
				['options', ('[B]Options[/B]', 'RunPlugin(%s)' % build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'poster': show_poster,
					'season': season, 'episode': episode}))]
						])
				if not unaired and not season_special:
					if playcount:
						cm_append(['mark_watched', ('[B]Mark Unwatched[/B]', 'RunPlugin(%s)' % build_url({'mode': 'watched_status.mark_episode', 'action': 'mark_as_unwatched',
													'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title}))])
					else: cm_append(['mark_watched', ('[B]Mark Watched[/B]', 'RunPlugin(%s)' % build_url({'mode': 'watched_status.mark_episode', 'action': 'mark_as_watched',
													'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title}))])
					if progress: cm_append(['mark_watched', ('[B]Clear Progress[/B]', 'RunPlugin(%s)' % \
								build_url({'mode': 'watched_status.erase_bookmark', 'media_type': 'episode', 'tmdb_id': tmdb_id,
								'season': season, 'episode': episode, 'refresh': 'true'}))])
				if is_external:
					cm_extend([['refresh', ('[B]Refresh Widgets[/B]', 'RunPlugin(%s)' % build_url({'mode': 'refresh_widgets'}))],
							['reload', ('[B]Reload Widgets[/B]', 'RunPlugin(%s)' % build_url({'mode': 'kodi_refresh'}))]])
				if custom_cm_menu:
					try: cm = sorted([i for i in cm if i[0] in cm_sort_order], key=lambda k: cm_sort_order[k[0]])
					except: pass
				cm = [i[1] for i in cm]
				info_tag = listitem.getVideoInfoTag(True)
				info_tag.setMediaType('episode')
				info_tag.setTitle(display)
				info_tag.setOriginalTitle(orig_title)
				info_tag.setTvShowTitle(title)
				info_tag.setGenres(genre)
				info_tag.setPlaycount(playcount)
				info_tag.setSeason(season)
				info_tag.setEpisode(episode)
				info_tag.setPlot(plot)
				info_tag.setFirstAired(premiered)
				info_tag.setDuration(duration)
				info_tag.setIMDBNumber(imdb_id)
				info_tag.setUniqueIDs({'imdb': imdb_id, 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)})
				if progress and not unaired:
					info_tag.setResumePoint(ws.get_resume_seconds(progress, duration))
					set_properties({'WatchedProgress': progress})
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'poster': show_poster, 'fanart': show_fanart, 'thumb': thumb, 'icon':thumb, 'clearlogo': show_clearlogo, 'landscape': show_landscape,
								'season.poster': season_poster, 'tvshow.poster': show_poster, 'tvshow.clearlogo': show_clearlogo})
				set_properties({'episode_type': episode_type})
				yield (play_params, listitem, False)
			except: pass
	kodi_actor, make_listitem, build_url = kodi_utils.kodi_actor(), kodi_utils.make_listitem, kodi_utils.build_url
	poster_empty, fanart_empty = kodi_utils.get_icon('box_office'), kodi_utils.addon_fanart()
	handle, is_external = int(sys.argv[1]), kodi_utils.external()
	item_list = []
	append = item_list.append
	episode_status_dict = kodi_utils.episode_status()
	adjust_hours = settings.date_offset()
	current_date = get_datetime()
	cm_sort_order = settings.cm_sort_order()
	custom_cm_menu = cm_sort_order != settings.cm_default_order()
	rpdb_info = settings.rpdb_info('tvshow')
	rpdb_api_key, rpdb_format = rpdb_info['rpdb_api_key'], rpdb_info['rpdb_format']
	meta = tvshow_meta('tmdb_id', params.get('tmdb_id'), settings.tmdb_api_key(), current_date)
	meta_get = meta.get
	tmdb_id, tvdb_id, imdb_id, tvshow_plot, orig_title = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id'), meta_get('plot'), meta_get('original_title')
	title, rootname, show_duration, genre = meta_get('title'), meta_get('rootname'), meta_get('duration'), meta_get('genre')
	season = params['season']
	if rpdb_api_key:
		try: show_poster = meta_get('rpdb_poster') % rpdb_api_key + rpdb_format
		except: show_poster = meta_get('poster') or poster_empty
	else: show_poster = meta_get('poster') or poster_empty
	show_fanart = meta_get('fanart') or fanart_empty
	show_clearlogo = meta_get('clearlogo') or ''
	show_landscape = meta_get('landscape') or ''
	watched_db = ws.get_database()
	watched_info = ws.watched_info_episode(tmdb_id, watched_db)
	total_seasons = None
	episodes_data = episodes_meta(season, meta)
	bookmarks = ws.get_bookmarks_episode(tmdb_id, season, watched_db)
	try:
		season_data = meta_get('season_data')
		poster_path = next((i['poster_path'] for i in season_data if i['season_number'] == int(season)), None)
		season_poster = 'https://image.tmdb.org/t/p/w780%s' % poster_path if poster_path is not None else show_poster
	except: season_poster = show_poster
	category_name = 'Season %s' % season
	kodi_utils.add_items(handle, list(_process()))
	kodi_utils.set_sort_method(handle, 'episodes')
	kodi_utils.set_content(handle, 'episodes')
	kodi_utils.set_category(handle, category_name)
	kodi_utils.end_directory(handle, cacheToDisc=False if is_external else True)
	kodi_utils.set_view_mode('view.episodes', 'episodes', is_external)

def build_single_episode(params):
	def _get_category_name():
		try:
			cat_name = {'progress': 'In Progress Episodes','next': 'Next Episodes'}[list_type]
			if isinstance(cat_name, dict): cat_name = cat_name[params.get('recently_aired')]
		except: cat_name = 'Episodes'
		return cat_name
	def _process(_position, ep_data):
		try:
			ep_data_get = ep_data.get
			last_played = ep_data_get('last_played', resinsert)
			meta = tvshow_meta('trakt_dict', ep_data_get('media_ids'), api_key, current_date, current_time)
			if not meta: return
			meta_get = meta.get
			cm = []
			cm_append = cm.append
			cm_extend = cm.extend
			listitem = make_listitem()
			set_properties = listitem.setProperties
			orig_season, orig_episode = ep_data_get('season'), ep_data_get('episode')
			unwatched = ep_data_get('unwatched', False)
			_position = ep_data_get('custom_order', _position)
			tmdb_id, tvdb_id, imdb_id, title = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id'), meta_get('title')
			season_data = meta_get('season_data')
			watched_info = ws.watched_info_episode(meta_get('tmdb_id'), watched_db)
			if list_type == 'next':
				orig_season, orig_episode = ws.get_next(orig_season, orig_episode, watched_info, season_data)
				if not orig_season or not orig_episode: return
			episodes_data = episodes_meta(orig_season, meta)
			if not episodes_data: return
			item = next((i for i in episodes_data if i['episode'] == orig_episode), None)
			if not item: return
			item_get = item.get
			season, episode, ep_name = item_get('season'), item_get('episode'), item_get('title')
			episode_date, premiered = adjust_premiered_date(item_get('premiered'), adjust_hours)
			episode_type = item_get('episode_type') or ''
			episode_id = item_get('episode_id') or None
			if not episode_date or current_date < episode_date:
				if list_type == 'next': return
				unaired = True
			else: unaired = False
			orig_title, rootname, genre = meta_get('original_title'), meta_get('rootname'), meta_get('genre')
			if rpdb_api_key:
				try: show_poster = meta_get('rpdb_poster') % rpdb_api_key + rpdb_format
				except: show_poster = meta_get('poster') or poster_empty
			else: show_poster = meta_get('poster') or poster_empty
			show_fanart = meta_get('fanart') or fanart_empty
			show_clearlogo = meta_get('clearlogo') or ''
			show_landscape = meta_get('landscape') or ''
			try:
				poster_path = next((i['poster_path'] for i in season_data if i['season_number'] == int(season)), None)
				season_poster = 'https://image.tmdb.org/t/p/w780%s' % poster_path if poster_path is not None else show_poster
			except: season_poster = show_poster
			str_season_zfill2, str_episode_zfill2 = str(season).zfill(2), str(episode).zfill(2)
			if display_format == 0: title_str = '%s: ' % title
			else: title_str = ''
			if display_format in (0, 1): seas_ep = '%sx%s - ' % (str_season_zfill2, str_episode_zfill2)
			else: seas_ep = ''
			if not list_type == 'next': playcount = ws.get_watched_status_episode(watched_info, (season, episode))
			if list_type == 'next':
				playcount = 0
				if unwatched: highlight_start, highlight_end = '[COLOR darkgoldenrod]', '[/COLOR]'
				elif unaired: highlight_start, highlight_end = '[COLOR red]', '[/COLOR]'
				else: highlight_start, highlight_end = '', ''
				display = '%s%s%s%s%s' % (title_str, highlight_start, seas_ep, ep_name, highlight_end)
			else: display = '%s%s%s' % (title_str, seas_ep, ep_name)
			thumb, plot, duration = item_get('thumb', None) or show_landscape or show_fanart, item_get('plot') or tvshow_plot, item_get('duration')
			if episode_type:
				status_label, status_highlight = episode_status_dict[episode_type]
				plot = '[COLOR %s]%s[/COLOR][CR]%s' % (status_highlight, status_label, plot)
			if not duration:
				duration = meta_get('duration')
				item['duration'] = duration
			bookmarks = ws.get_bookmarks_episode(tmdb_id, season, watched_db)
			progress = ws.get_progress_status_episode(bookmarks, episode)
			play_params = build_url({'mode': 'playback.media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode, 'playcount': playcount,
									'episode_id': episode_id})
			cm_extend([
			['extras', ('[B]Extras[/B]', 'RunPlugin(%s)' % build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'episode'}))],
			['cast', ('[B]Cast[/B]', 'RunPlugin(%s)' % build_url({'mode': 'tmdb_cast_dialog_image_results', 'media_type': 'episode', 'tmdb_id': tmdb_id,
				'season': season, 'episode': episode}))],
			['more_info', ('[B]More Info[/B]', 'RunPlugin(%s)' % build_url({'mode': 'media_extra_info_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id}))],
			['options', ('[B]Options[/B]', 'RunPlugin(%s)' % build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'poster': show_poster,
				'season': season, 'episode': episode}))],
			['browse_more', ('[B]Browse More[/B]', 'RunPlugin(%s)' % build_url({'mode': 'browse_more_choice', 'media_type': 'single_episode', 'tmdb_id': tmdb_id,
				'season': season, 'poster': show_poster}))]])
			if not unaired:
				if playcount:
					cm_append(['mark_watched', ('[B]Mark Unwatched[/B]', 'RunPlugin(%s)' % build_url({'mode': 'watched_status.mark_episode', 'action': 'mark_as_unwatched',
												'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title}))])
				else: cm_append(['mark_watched', ('[B]Mark Watched[/B]', 'RunPlugin(%s)' % build_url({'mode': 'watched_status.mark_episode', 'action': 'mark_as_watched',
											'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title}))])
				if progress:
					cm_append(['mark_watched', ('[B]Clear Progress[/B]', 'RunPlugin(%s)' % \
								build_url({'mode': 'watched_status.erase_bookmark', 'media_type': 'episode', 'tmdb_id': tmdb_id,
											'season': season, 'episode': episode, 'refresh': 'true'}))])
			if is_external:
				cm_extend([['refresh', ('[B]Refresh Widgets[/B]', 'RunPlugin(%s)' % build_url({'mode': 'refresh_widgets'}))],
						['reload', ('[B]Reload Widgets[/B]', 'RunPlugin(%s)' % build_url({'mode': 'kodi_refresh'}))]])
			if custom_cm_menu:
				try: cm = sorted([i for i in cm if i[0] in cm_sort_order], key=lambda k: cm_sort_order[k[0]])
				except: pass
			cm = [i[1] for i in cm]
			info_tag = listitem.getVideoInfoTag(True)
			info_tag.setMediaType('episode')
			info_tag.setOriginalTitle(orig_title)
			info_tag.setTvShowTitle(title)
			info_tag.setTitle(display)
			info_tag.setGenres(genre)
			info_tag.setPlaycount(playcount)
			info_tag.setSeason(season)
			info_tag.setEpisode(episode)
			info_tag.setPlot(plot)
			info_tag.setFirstAired(premiered)
			info_tag.setDuration(duration)
			info_tag.setIMDBNumber(imdb_id)
			info_tag.setUniqueIDs({'imdb': imdb_id, 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)})
			if progress and not unaired:
				info_tag.setResumePoint(ws.get_resume_seconds(progress, duration))
				set_properties({'WatchedProgress': progress})
			listitem.setLabel(display)
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': show_poster, 'fanart': show_fanart, 'thumb': thumb, 'icon':thumb, 'clearlogo': show_clearlogo, 'landscape': show_landscape,
							'season.poster': season_poster, 'tvshow.poster': show_poster, 'tvshow.clearlogo': show_clearlogo})
			set_properties({'episode_type': episode_type})
			item_list_append({'list_items': (play_params, listitem, False), 'first_aired': premiered, 'name': '%s - %sx%s' % (title, str_season_zfill2, str_episode_zfill2),
							'unaired': unaired, 'last_played': ep_data_get('last_played', resinsert), 'sort_order': _position, 'unwatched': ep_data_get('unwatched')})
		except: pass
	kodi_actor, make_listitem, build_url = kodi_utils.kodi_actor(), kodi_utils.make_listitem, kodi_utils.build_url
	poster_empty, fanart_empty = kodi_utils.get_icon('box_office'), kodi_utils.addon_fanart()
	handle, is_external = int(sys.argv[1]), kodi_utils.external()
	item_list, airing_today, unwatched, return_results = [], [], [], False
	item_list_append = item_list.append
	window_command = 'ActivateWindow(Videos,%s,return)' if is_external else 'Container.Update(%s)'
	episode_status_dict = kodi_utils.episode_status()
	display_format = settings.single_ep_display_format(is_external)
	current_date, current_time, adjust_hours = get_datetime(), get_current_timestamp(), settings.date_offset()
	api_key = settings.tmdb_api_key()
	cm_sort_order = settings.cm_sort_order()
	custom_cm_menu = cm_sort_order != settings.cm_default_order()
	rpdb_info = settings.rpdb_info('tvshow')
	rpdb_api_key, rpdb_format = rpdb_info['rpdb_api_key'], rpdb_info['rpdb_format']
	watched_db = ws.get_database()
	resformat, resinsert = '%Y-%m-%d %H:%M:%S', '2000-01-01 00:00:00'
	list_type = params.get('list_type')
	if list_type == 'next':
		include_favorites = settings.nextep_include_favorites()
		data = ws.get_next_episodes()
		hidden_list = ws.get_hidden_progress_items()
		if hidden_list: data = [i for i in data if not i['media_ids']['tmdb'] in hidden_list]
		if include_favorites:
			from caches.favorites_cache import favorites_cache
			try:
				favorites = favorites_cache.get_favorites('tvshow')
				unwatched.extend([{'media_ids': {'tmdb': int(i['tmdb_id'])}, 'season': 1, 'episode': 0, 'unwatched': True, 'title': i['title']} \
								for i in favorites if not int(i['tmdb_id']) in [x['media_ids']['tmdb'] for x in data]])
			except: pass
			data += unwatched
	elif list_type == 'progress': data = ws.get_in_progress_episodes()
	else: data, return_results = sorted(params, key=lambda i: i['custom_order']), True
	threads = TaskPool().tasks_enumerate(_process, data, min(len(data), settings.max_threads()))
	[i.join() for i in threads]
	if return_results: return [(i['list_items'], i['sort_order']) for i in item_list]
	if list_type == 'next':
		unwatched = sorted([i for i in item_list if i['unwatched']], key=lambda i: title_key(i['name']))
		item_list = sorted([i for i in item_list if not i['unwatched']], key=lambda i: jsondate_to_datetime(i['last_played'], resformat), reverse=True) + unwatched
	else: item_list.sort(key=lambda i: i['sort_order'])
	kodi_utils.add_items(handle, [i['list_items'] for i in item_list])
	kodi_utils.set_content(handle, 'episodes')
	kodi_utils.set_category(handle, _get_category_name())
	kodi_utils.end_directory(handle, cacheToDisc=False)
	kodi_utils.set_view_mode('view.episodes_single', 'episodes', is_external)

