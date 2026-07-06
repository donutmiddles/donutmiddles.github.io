# -*- coding: utf-8 -*-
from modules.kodi_utils import external
from urllib.parse import parse_qsl
# from modules.kodi_utils import logger

def sys_exit_check(): return external()

def routing(sys):
	params = dict(parse_qsl(sys.argv[2][1:], keep_blank_values=True))
	mode = params.get('mode', 'navigator.main')
	if 'navigator.' in mode:
		from indexers.navigator import Navigator
		return exec('Navigator(params).%s()' % mode.split('.')[1])
	if 'menu_editor.' in mode:
		from modules.menu_editor import MenuEditor
		return exec('MenuEditor(params).%s()' % mode.split('.')[1])
	if 'personal_lists.' in mode:
		from indexers import personal_lists
		return exec('personal_lists.%s(params)' % mode.split('.')[1])
	if 'easynews.' in mode:
		from indexers import easynews
		return exec('easynews.%s(params)' % mode.split('.')[1])
	if 'playback.' in mode:
		if mode == 'playback.media':
			from modules.sources import Sources
			return Sources().playback_prep(params)
		from modules.player import FenPlayer
		return FenPlayer().run(params.get('url', None), params.get('obj', None))
	if 'choice' in mode:
		from indexers import dialogs
		return exec('dialogs.%s(params)' % mode)
	if 'trakt.' in mode:
		if '.list' in mode:
			from indexers import trakt_lists
			return exec('trakt_lists.%s(params)' % mode.split('.')[2])
		from apis import trakt_api
		return exec('trakt_api.%s(params)' % mode.split('.')[1])
	if 'build' in mode:
		if mode == 'build_movie_list':
			from indexers.movies import Movies
			return Movies(params).fetch_list()
		if mode == 'build_tvshow_list':
			from indexers.tvshows import TVShows
			return TVShows(params).fetch_list()
		if mode == 'build_season_list':
			from indexers.seasons import build_season_list
			return build_season_list(params)
		if mode == 'build_episode_list':
			from indexers.episodes import build_episode_list
			return build_episode_list(params)
		if mode == 'build_single_episode':
			from indexers.episodes import build_single_episode
			return build_single_episode(params)
		if mode == 'build_next_episode_manager':
			from modules.episode_tools import build_next_episode_manager
			return build_next_episode_manager()
		if 'random.' in mode:
			from indexers.random_lists import RandomLists
			return RandomLists(params).run_random()
	if 'watched_status.' in mode:
		if mode == 'watched_status.mark_episode':
			from modules.watched_status import mark_episode
			return mark_episode(params)
		if mode == 'watched_status.mark_season':
			from modules.watched_status import mark_season
			return mark_season(params)
		if mode == 'watched_status.mark_tvshow':
			from modules.watched_status import mark_tvshow
			return mark_tvshow(params)
		if mode == 'watched_status.mark_movie':
			from modules.watched_status import mark_movie
			return mark_movie(params)
		if mode == 'watched_status.erase_bookmark':
			from modules.watched_status import erase_bookmark
			return erase_bookmark(params.get('media_type'), params.get('tmdb_id'), params.get('season', ''), params.get('episode', ''), params.get('refresh', 'false'))
	if 'search.' in mode:
		if mode == 'search.get_key_id':
			from modules.search import get_key_id
			return get_key_id(params)
		if mode == 'search.clear_search':
			from modules.search import clear_search
			return clear_search()
		if mode == 'search.remove':
			from modules.search import remove_from_search
			return remove_from_search(params)
		if mode == 'search.clear_all':
			from modules.search import clear_all
			return clear_all(params.get('setting_id'), params.get('refresh', 'false'))
	if 'real_debrid' in mode:
		if mode == 'real_debrid.rd_cloud':
			from indexers.real_debrid import rd_cloud
			return rd_cloud()
		if mode == 'real_debrid.rd_downloads':
			from indexers.real_debrid import rd_downloads
			return rd_downloads()
		if mode == 'real_debrid.browse_rd_cloud':
			from indexers.real_debrid import browse_rd_cloud
			return browse_rd_cloud(params.get('id'))
		if mode == 'real_debrid.resolve_rd':
			from indexers.real_debrid import resolve_rd
			return resolve_rd(params)
		if mode == 'real_debrid.rd_account_info':
			from indexers.real_debrid import rd_account_info
			return rd_account_info()
		if mode == 'real_debrid.authenticate':
			from apis.real_debrid_api import RealDebridAPI
			return RealDebridAPI().auth()
		if mode == 'real_debrid.revoke_authentication':
			from apis.real_debrid_api import RealDebridAPI
			return RealDebridAPI().revoke()
		if mode == 'real_debrid.delete':
			from indexers.real_debrid import rd_delete
			return rd_delete(params.get('id'), params.get('cache_type'))
	if 'premiumize' in mode:
		if mode == 'premiumize.pm_cloud':
			from indexers.premiumize import pm_cloud
			return pm_cloud(params.get('id', None), params.get('folder_name', None))
		if mode == 'premiumize.pm_transfers':
			from indexers.premiumize import pm_transfers
			return pm_transfers()
		if mode == 'premiumize.pm_account_info':
			from indexers.premiumize import pm_account_info
			return pm_account_info()
		if mode == 'premiumize.authenticate':
			from apis.premiumize_api import PremiumizeAPI
			return PremiumizeAPI().auth()
		if mode == 'premiumize.revoke_authentication':
			from apis.premiumize_api import PremiumizeAPI
			return PremiumizeAPI().revoke()
		if mode == 'premiumize.rename':
			from indexers.premiumize import pm_rename
			return pm_rename(params.get('file_type'), params.get('id'), params.get('name'))
		if mode == 'premiumize.delete':
			from indexers.premiumize import pm_delete
			return pm_delete(params.get('file_type'), params.get('id'))
	if 'offcloud' in mode:
		if mode == 'offcloud.oc_cloud':
			from indexers.offcloud import oc_cloud
			return oc_cloud()
		if mode == 'offcloud.browse_oc_cloud':
			from indexers.offcloud import browse_oc_cloud
			return browse_oc_cloud(params.get('folder_id'))
		if mode == 'offcloud.resolve_oc':
			from indexers.offcloud import resolve_oc
			return resolve_oc(params)
		if mode == 'offcloud.oc_account_info':
			from indexers.offcloud import oc_account_info
			return oc_account_info()
		if mode == 'offcloud.authenticate':
			from apis.offcloud_api import OffcloudAPI
			return OffcloudAPI().auth()
		if mode == 'offcloud.revoke_authentication':
			from apis.offcloud_api import OffcloudAPI
			return OffcloudAPI().revoke()
		if mode == 'offcloud.delete':
			from indexers.offcloud import oc_delete
			return oc_delete(params.get('folder_id'))
	if 'torbox' in mode:
		if mode == 'torbox.tb_cloud':
			from indexers.torbox import tb_cloud
			return tb_cloud()
		if mode == 'torbox.browse_tb_cloud':
			from indexers.torbox import browse_tb_cloud
			return browse_tb_cloud(params.get('folder_id'), params.get('media_type'))
		if mode == 'torbox.resolve_tb':
			from indexers.torbox import resolve_tb
			return resolve_tb(params)
		if mode == 'torbox.tb_account_info':
			from indexers.torbox import tb_account_info
			return tb_account_info()
		if mode == 'torbox.authenticate':
			from apis.torbox_api import TorBoxAPI
			return TorBoxAPI().auth()
		if mode == 'torbox.revoke_authentication':
			from apis.torbox_api import TorBoxAPI
			return TorBoxAPI().revoke()
		if mode == 'torbox.delete':
			from indexers.torbox import tb_delete
			return tb_delete(params.get('folder_id'), params.get('media_type'))
	if '_cache' in mode:
		from caches import base_cache
		if mode == 'clear_cache':
			return base_cache.clear_cache(params.get('cache'))
		if mode == 'clear_all_cache':
			return base_cache.clear_all_cache()
		if mode == 'clean_databases_cache':
			return base_cache.clean_databases()
		if mode == 'check_databases_integrity_cache':
			return base_cache.check_databases_integrity()
	if '_image' in mode:
		from indexers.images import Images
		return Images().run(params)
	if '_text' in mode:
		if mode == 'show_text':
			from modules.kodi_utils import show_text
			return show_text(params.get('heading'), params.get('text', None), params.get('file', None),
							params.get('font_size', 'small'), params.get('kodi_log', 'false') == 'true')
		if mode == 'show_text_media':
			from modules.kodi_utils import show_text_media
			return show_text(params.get('heading'), params.get('text', None), params.get('file', None), params.get('meta'), {})
	if 'settings_manager.' in mode:
		from caches import settings_cache
		return exec('settings_cache.%s(params)' % mode.split('.')[1])
	if 'data_sync_manager.' in mode:
		from caches import data_sync_cache
		return exec('data_sync_cache.%s(params)' % mode.split('.')[1])
	if 'downloader.' in mode:
		from modules import downloader
		return exec('downloader.%s(params)' % mode.split('.')[1])
	if 'updater' in mode:
		from modules import updater
		return exec('updater.%s()' % mode.split('.')[1])
	##EXTRA modes##
	if mode == 'set_view':
		from modules.kodi_utils import set_view
		return kodi_utils.set_view(params.get('view_type'))
	if mode == 'sync_settings':
		from caches.settings_cache import sync_settings
		return sync_settings(params)
	if mode == 'kodi_refresh':
		from modules.kodi_utils import kodi_refresh
		return kodi_refresh()
	if mode == 'refresh_widgets':
		from modules.kodi_utils import refresh_widgets
		return refresh_widgets()
	if mode == 'manual_add_magnet_to_cloud':
		from modules.debrid import manual_add_magnet_to_cloud
		return manual_add_magnet_to_cloud(params)
	if mode == 'upload_logfile':
		from modules.kodi_utils import upload_logfile
		return upload_logfile(params)
	if mode == 'downloader':
		from modules.downloader import runner
		return runner(params)
	if mode == 'debrid.browse_packs':
		from modules.sources import Sources
		return Sources().debridPacks(params.get('provider'), params.get('name'), params.get('magnet_url'), params.get('info_hash'))
	if mode == 'open_settings':
		from modules.kodi_utils import open_settings
		return open_settings()
	if mode == 'hide_unhide_progress_items':
		from modules.watched_status import hide_unhide_progress_items
		return hide_unhide_progress_items(params)
	if mode == 'open_external_scraper_settings':
		from modules.kodi_utils import external_scraper_settings
		return external_scraper_settings()
