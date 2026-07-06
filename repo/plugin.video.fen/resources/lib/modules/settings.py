# -*- coding: utf-8 -*-
from caches.base_cache import database_snyc_items
from caches.settings_cache import get_setting, default_setting_values
from modules.kodi_utils import translate_path, get_property, extras_order_default, context_menu_defaults
# from modules.kodi_utils import logger

def tmdb_api_key():
	return get_setting('fen.tmdb_api', '')

def trakt_client():
	return get_setting('fen.trakt.client', '')

def trakt_secret():
	return get_setting('fen.trakt.secret', '')

def store_resolved_to_cloud(debrid_service, pack):
	setting_value = int(get_setting('fen.store_resolved_to_cloud.%s' % debrid_service.lower(), '0'))
	return setting_value in (1, 2) if pack else setting_value == 1

def enabled_debrids_check(debrid_service):
	if not get_setting('fen.%s.enabled' % debrid_service) == 'true': return False
	return authorized_debrid_check(debrid_service)

def authorized_debrid_check(debrid_service):
	if get_setting('fen.%s.token' % debrid_service) in (None, '', 'empty_setting'): return False
	return True

def playback_settings():
	return (int(get_setting('fen.playback.watched_percent', '90')), int(get_setting('fen.playback.resume_percent', '5')))

def limit_resolve():
	return get_setting('fen.playback.limit_resolve', 'false') == 'true'

def movies_directory():
	return translate_path(get_setting('fen.movies_directory'))
	
def tv_show_directory():
	return translate_path(get_setting('fen.tv_shows_directory'))

def download_directory(media_type):
	download_directories_dict = {'movie': 'fen.movie_download_directory', 'episode': 'fen.tvshow_download_directory', 'thumb_url': 'fen.image_download_directory',
								'image_url': 'fen.image_download_directory','image': 'fen.image_download_directory', 'premium': 'fen.premium_download_directory',
								None: 'fen.premium_download_directory', 'None': False}
	return translate_path(get_setting(download_directories_dict[media_type]))

def ai_model_active():
	if get_setting('fen.google_api', 'empty_setting') not in (None, 'None', '', 'empty_setting'): return True
	if get_setting('fen.groq_api', 'empty_setting') not in (None, 'None', '', 'empty_setting'): return True
	return False

def ai_model_order():
	return get_setting('fen.ai_model.order', 'gemini-2.5-flash-lite,llama-3.3-70b-versatile,gemma-3-27b-it,llama-3.1-8b-instant').split(',')

def ai_model_limit():
	return max(1, int(get_setting('fen.ai_model.limit', '10')))

def show_unaired_watchlist():
	return get_setting('fen.show_unaired_watchlist', 'true') == 'true'

def source_folders_directory(media_type, source):
	setting = 'fen.%s.movies_directory' % source if media_type == 'movie' else 'fen.%s.tv_shows_directory' % source
	if get_setting(setting) not in ('', 'None', None): return translate_path( get_setting(setting))
	else: return False

def paginate(is_home):
	paginate_lists = int(get_setting('fen.paginate.lists', '0'))
	if is_home: return paginate_lists in (2, 3)
	else: return paginate_lists in (1, 3)

def page_limit(is_home):	
	return int(get_setting({True: 'fen.paginate.limit_widgets', False: 'fen.paginate.limit_addon'}[is_home], '20'))

def ignore_results_filter():
	return int(get_setting('fen.results.ignore_filter', '0'))

def quality_filter(setting):
	return get_setting('fen.%s' % setting).split(', ')

def sort_to_top_filter(autoplay):
    return {0: False, 1: False if autoplay else True, 2: True if autoplay else False, 3: True}[int(get_setting('fen.filter.sort_to_top', '0'))]

def preferred_filters():
    setting = get_setting('fen.filter.preferred_filters')
    if setting in ('empty_setting', ''): return []
    return setting.split(', ')

def include_prerelease_results():
	return int(get_setting('fen.filter.prerelease', '0')) == 0

def skip_episode_intros():
	return int(get_setting('fen.skip_episode_intros', '0'))

def stingers_show():
	return get_setting('fen.stinger_alert.show', 'false') == 'true'

def auto_play(media_type):
	return get_setting('fen.auto_play_%s' % media_type, 'false') == 'true'

def autoplay_next_episode():
	if auto_play('episode') and get_setting('fen.autoplay_next_episode', 'false') == 'true': return True
	else: return False

def filter_status(filter_type):
	return int(get_setting('fen.filter.%s' % filter_type, '0'))

def lists_sort_order(setting):
	return int(get_setting('fen.sort.%s' % setting, '0'))

def single_ep_display_format(is_external):
	if is_external: setting, default = 'fen.single_ep_display_widget', '1'
	else: setting, default = 'fen.single_ep_display', ''
	return int(get_setting(setting, default))

def easynews_active():
	if get_setting('fen.provider.easynews', 'false') == 'true': easynews_status = easynews_authorized()
	else: easynews_status = False
	return easynews_status

def easynews_authorized():
	easynews_user = get_setting('fen.easynews_user', 'empty_setting')
	easynews_password = get_setting('fen.easynews_password', 'empty_setting')
	if easynews_user in ('empty_setting', '') or easynews_password in ('empty_setting', ''): easynews_status = False
	else: easynews_status = True
	return easynews_status

def extras_enable_extra_ratings():
	return get_setting('fen.extras.enable_extra_ratings', 'true') == 'true'

def extras_enabled_ratings():
	return get_setting('fen.extras.enabled_ratings', 'Meta, Tom/Critic, Tom/User, IMDb, TMDb').split(', ')

def extras_enable_item_ratings():
	return get_setting('fen.extras.enable_item_ratings', 'false') =='true'

def extras_enabled():
	defaults = extras_order_default()
	setting = get_setting('fen.extras.enabled', None)
	if setting in ('', None, 'noop', []): setting = defaults
	split_setting = setting.split(',')
	return [int(i) for i in split_setting if i in defaults]

def extras_order():
	defaults = extras_order_default()
	setting = get_setting('fen.extras.order', None)
	if setting in ('', None, 'noop', []): setting = defaults
	split_setting = setting.split(',')
	return [int(i) for i in split_setting if i in defaults]

def cm_enabled():
	defaults = context_menu_defaults()
	setting = get_setting('fen.context_menu.enabled', defaults)
	if setting in ('', None, 'noop', '[]'): return defaults.split(',')
	return setting.split(',')

def cm_current_order():
	defaults = context_menu_defaults()
	setting = get_setting('fen.context_menu.order', defaults)
	if setting in ('', None, 'noop', '[]'): return defaults.split(',')
	return setting.split(',')

def check_prescrape_sources(scraper, media_type):
	if scraper in ('easynews', 'rd_cloud', 'pm_cloud', 'oc_cloud', 'tb_cloud', 'folders'): return get_setting('fen.check.%s' % scraper) == 'true'
	if get_setting('fen.check.%s' % scraper) == 'true' and auto_play(media_type): return True
	else: return False

def external_scraper_info():
	module = get_setting('fen.external_scraper.module')
	if module in ('empty_setting', ''): return None, ''
	return module, module.split('.')[-1]

def filter_by_name(scraper):
	if get_property('fs_filterless_search') == 'true': return False
	return get_setting('fen.%s.title_filter' % scraper, 'false') == 'true'

def easynews_language_filter():
	enabled = get_setting('fen.easynews.filter_lang') == 'true'
	if enabled: filters = get_setting('fen.easynews.lang_filters').split(', ')
	else: filters = []
	return enabled, filters

def results_sort_order():
	return (
			lambda k: (k['quality_rank'], k['provider_rank'], -k['size_rank']), #Quality, Provider, Size
			lambda k: (k['quality_rank'], -k['size_rank'], k['provider_rank']), #Quality, Size, Provider
			lambda k: (k['provider_rank'], k['quality_rank'], -k['size_rank']), #Provider, Quality, Size
			lambda k: (k['provider_rank'], -k['size_rank'], k['quality_rank']), #Provider, Size, Quality
			lambda k: (-k['size_rank'], k['quality_rank'], k['provider_rank']), #Size, Quality, Provider
			lambda k: (-k['size_rank'], k['provider_rank'], k['quality_rank'])  #Size, Provider, Quality
			)[int(get_setting('fen.results.sort_order', '1'))]

def active_internal_scrapers():
	settings = ['provider.external', 'provider.easynews', 'provider.folders']
	settings_append = settings.append
	for item in [('rd', 'provider.rd_cloud'), ('pm', 'provider.pm_cloud'), ('oc', 'provider.oc_cloud'), ('tb', 'provider.tb_cloud')]:
		if enabled_debrids_check(item[0]): settings_append(item[1])
	active = [i.split('.')[1] for i in settings if get_setting('fen.%s' % i) == 'true']
	return active

def provider_sort_ranks():
	pm_priority = int(get_setting('fen.pm.priority', '6'))
	oc_priority = int(get_setting('fen.oc.priority', '7'))
	en_priority = int(get_setting('fen.en.priority', '8'))
	rd_priority = int(get_setting('fen.rd.priority', '9'))
	tb_priority = int(get_setting('fen.tb.priority', '10'))
	return {'easynews': en_priority, 'real-debrid': rd_priority, 'premiumize.me': pm_priority, 'offcloud': oc_priority, 'torbox': tb_priority,
	'rd_cloud': rd_priority, 'pm_cloud': pm_priority, 'oc_cloud': oc_priority, 'tb_cloud': tb_priority, 'folders': 0}

def auto_resume(media_type, autoplay_status):
	return {0: False, 1: True, 2: autoplay_status}[int(get_setting('fen.auto_resume_%s' % media_type))]

def scraping_settings():
	highlight_type = int(get_setting('fen.highlight.type', '0'))
	if highlight_type == 2:
		highlight = get_setting('fen.scraper_single_highlight', 'FF008EB2')
		return {'highlight_type': 1, '4k': highlight, '1080p': highlight, '720p': highlight, 'sd': highlight}
	easynews_highlight, debrid_cloud_highlight, folders_highlight = '', '', ''
	rd_highlight, pm_highlight, tb_highlight = '', '', ''
	highlight_4K, highlight_1080P, highlight_720P, highlight_SD = '', '', '', ''
	if highlight_type == 0:
		easynews_highlight = get_setting('fen.provider.easynews_highlight', 'FF00B3B2')
		debrid_cloud_highlight = get_setting('fen.provider.debrid_cloud_highlight', 'FF7A01CC')
		folders_highlight = get_setting('fen.provider.folders_highlight', 'FFB36B00')
		rd_highlight = get_setting('fen.provider.rd_highlight', 'FF3C9900')
		pm_highlight = get_setting('fen.provider.pm_highlight', 'FFFF3300')
		oc_highlight = get_setting('fen.provider.oc_highlight', 'FF008EB2')
		tb_highlight = get_setting('fen.provider.tb_highlight', 'FF01662A')
	else:
		highlight_4K = get_setting('fen.scraper_4k_highlight', 'FFFF00FE')
		highlight_1080P = get_setting('fen.scraper_1080p_highlight', 'FFE6B800')
		highlight_720P = get_setting('fen.scraper_720p_highlight', 'FF3C9900')
		highlight_SD = get_setting('fen.scraper_SD_highlight', 'FF0166FF')
	return {'highlight_type': highlight_type, 'real-debrid': rd_highlight, 'premiumize': pm_highlight, 'torbox': tb_highlight, 'offcloud': oc_highlight,
			'rd_cloud': debrid_cloud_highlight, 'pm_cloud': debrid_cloud_highlight, 'oc_cloud': debrid_cloud_highlight,
			'tb_cloud': debrid_cloud_highlight, 'easynews': easynews_highlight, 'folders': folders_highlight,
			'4k': highlight_4K, '1080p': highlight_1080P, '720p': highlight_720P, 'sd': highlight_SD}

def omdb_api_key():
	return get_setting('fen.omdb_api', 'empty_setting')

def max_threads():
	if not get_setting('fen.limit_concurrent_threads', 'false') == 'true': return 60
	return int(get_setting('fen.max_threads', '60'))

def widget_hide_next_page():
	return get_setting('fen.widget_hide_next_page', 'false') == 'true'

def date_offset():
	return int(get_setting('fen.datetime.offset', '0')) + 5

def media_open_action(media_type):
	return int(get_setting('fen.media_open_action_%s' % media_type, '0'))

def nextep_limit():
	return int(get_setting('fen.nextep.limit', '20'))

def nextep_include_favorites():
	return get_setting('fen.nextep.include_favorites', 'false') == 'true'

def update_delay():
	return int(get_setting('fen.update.delay', '45'))

def update_action():
	return int(get_setting('fen.update.action', '2'))

def cm_sort_order():
	try: setting = {i: c for c, i in enumerate([i for i in cm_current_order() if i in cm_enabled()])}
	except: setting = cm_default_order()
	return setting

def cm_default_order():
	return {i: c for c, i in enumerate(default_setting_values('context_menu.order')['setting_default'].split(','))}

def rpdb_info(media_type):
	if media_type == 'extras': active = extras_enable_item_ratings()
	else: active = int(get_setting('fen.rpdb_enabled', '0')) in {'movie': (1, 3), 'tvshow': (2, 3)}[media_type]
	if active: return {'rpdb_api_key': get_setting('fen.rpdb_api'), 'rpdb_format': get_setting('fen.rpdb_format')}
	else: return {'rpdb_api_key': None, 'rpdb_format': None}

def datasync_location():
	location = get_setting('fen.datasync.location', 'empty_setting')
	if location in (None, 'empty_setting', 'None', ''): return None
	return location

def database_sync_included():
	defaults = ','.join(database_snyc_items())
	result = get_setting('fen.datasync.sync_databases', defaults)
	return result.split(',')

def database_autosync():
	return get_setting('fen.datasync.autosync', 'false') == 'true'

def database_autosync_interval():
	return int(get_setting('datasync.autosync_timer', '30')) * 60
