# -*- coding: utf-8 -*-

def get_years(start_year):
	from datetime import datetime
	current_year = datetime.now().year
	return [{'name': str(year), 'id': year} for year in range(current_year, start_year - 1, -1)]

def get_decades(start_decade):
	from datetime import datetime
	current_year = datetime.now().year
	current_decade = (current_year // 10) * 10
	return [{'name': '%ss' % decade, 'id': decade} for decade in range(current_decade, start_decade - 1, -10)]

def years_movies():
	return get_years(1900)

def years_tvshows():
	return get_years(1944)

def decades_movies():
	return get_decades(1900)

def decades_tvshows():
	return get_decades(1940)

def movie_certifications():
	return [
{'name': 'G', 'id': 'G'}, {'name': 'PG', 'id': 'PG'}, {'name': 'PG-13', 'id': 'PG-13'},
{'name': 'R', 'id': 'R'}, {'name': 'NC-17', 'id': 'NC-17'}, {'name': 'NR', 'id': 'NR'}
	]

def languages():
	return [
{'name': 'Arabic', 'id': 'ar'}, {'name': 'Bosnian', 'id': 'bs'}, {'name': 'Bulgarian', 'id': 'bg'}, {'name': 'Chinese', 'id': 'zh'}, {'name': 'Croatian', 'id': 'hr'},
{'name': 'Dutch', 'id': 'nl'}, {'name': 'English', 'id': 'en'}, {'name': 'Finnish', 'id': 'fi'}, {'name': 'French', 'id': 'fr'}, {'name': 'German', 'id': 'de'},
{'name': 'Greek', 'id': 'el'}, {'name': 'Hebrew', 'id': 'he'}, {'name': 'Hindi', 'id': 'hi'}, {'name': 'Hungarian', 'id': 'hu'}, {'name': 'Icelandic', 'id': 'is'},
{'name': 'Italian', 'id': 'it'}, {'name': 'Japanese', 'id': 'ja'}, {'name': 'Korean', 'id': 'ko'}, {'name': 'Macedonian', 'id': 'mk'}, {'name': 'Norwegian', 'id': 'no'},
{'name': 'Persian', 'id': 'fa'}, {'name': 'Polish', 'id': 'pl'}, {'name': 'Portuguese', 'id': 'pt'}, {'name': 'Punjabi', 'id': 'pa'}, {'name': 'Romanian', 'id': 'ro'},
{'name': 'Russian', 'id': 'ru'}, {'name': 'Serbian', 'id': 'sr'}, {'name': 'Slovenian', 'id': 'sl'}, {'name': 'Spanish', 'id': 'es'}, {'name': 'Swedish', 'id': 'sv'},
{'name': 'Turkish', 'id': 'tr'}, {'name': 'Ukrainian', 'id': 'uk'}, {'name': 'Vietnamese', 'id': 'vi'}
	]

def language_choices():
	return {
'None': 'None',              'Afrikaans': 'afr',            'Albanian': 'alb',             'Arabic': 'ara',
'Armenian': 'arm',           'Basque': 'baq',               'Bengali': 'ben',              'Bosnian': 'bos',
'Breton': 'bre',             'Bulgarian': 'bul',            'Burmese': 'bur',              'Catalan': 'cat',
'Chinese': 'chi',            'Croatian': 'hrv',             'Czech': 'cze',                'Danish': 'dan',
'Dutch': 'dut',              'English': 'eng',              'Esperanto': 'epo',            'Estonian': 'est',
'Finnish': 'fin',            'French': 'fre',               'Galician': 'glg',             'Georgian': 'geo',
'German': 'ger',             'Greek': 'ell',                'Hebrew': 'heb',               'Hindi': 'hin',
'Hungarian': 'hun',          'Icelandic': 'ice',            'Indonesian': 'ind',           'Italian': 'ita',
'Japanese': 'jpn',           'Kazakh': 'kaz',               'Khmer': 'khm',                'Korean': 'kor',
'Latvian': 'lav',            'Lithuanian': 'lit',           'Luxembourgish': 'ltz',        'Macedonian': 'mac',
'Malay': 'may',              'Malayalam': 'mal',            'Manipuri': 'mni',             'Mongolian': 'mon',
'Montenegrin': 'mne',        'Norwegian': 'nor',            'Occitan': 'oci',              'Persian': 'per',
'Polish': 'pol',             'Portuguese': 'por',           'Portuguese(Brazil)': 'pob',   'Romanian': 'rum',
'Russian': 'rus',            'Serbian': 'scc',              'Sinhalese': 'sin',            'Slovak': 'slo',
'Slovenian': 'slv',          'Spanish': 'spa',              'Swahili': 'swa',              'Swedish': 'swe',
'Syriac': 'syr',             'Tagalog': 'tgl',              'Tamil': 'tam',                'Telugu': 'tel',
'Thai': 'tha',               'Turkish': 'tur',              'Ukrainian': 'ukr',            'Urdu': 'urd',
'Vietnamese': 'vie'
	}

def movie_genres():
	return [
{'name': 'Action', 'id': '28', 'icon': 'genre_action'}, {'name': 'Adventure', 'id': '12', 'icon': 'genre_adventure'}, {'name': 'Animation', 'id': '16', 'icon': 'genre_animation'},
{'name': 'Comedy', 'id': '35', 'icon': 'genre_comedy'}, {'name': 'Crime', 'id': '80', 'icon': 'genre_crime'}, {'name': 'Documentary', 'id': '99', 'icon': 'genre_documentary'},
{'name': 'Drama', 'id': '18', 'icon': 'genre_drama'}, {'name': 'Family', 'id': '10751', 'icon': 'genre_family'}, {'name': 'Fantasy', 'id': '14', 'icon': 'genre_fantasy'},
{'name': 'History', 'id': '36', 'icon': 'genre_history'}, {'name': 'Horror', 'id': '27', 'icon': 'genre_horror'}, {'name': 'Music', 'id': '10402', 'icon': 'genre_music'},
{'name': 'Mystery', 'id': '9648', 'icon': 'genre_mystery'}, {'name': 'Romance', 'id': '10749', 'icon': 'genre_romance'},
{'name': 'Science Fiction', 'id': '878', 'icon': 'genre_scifi'}, {'name': 'TV Movie', 'id': '10770', 'icon': 'genre_soap'}, {'name': 'Thriller', 'id': '53', 'icon': 'genre_thriller'},
{'name': 'War', 'id': '10752', 'icon': 'genre_war'}, {'name': 'Western', 'id': '37', 'icon': 'genre_western'}
	]

def tvshow_genres():
	return [
{'name': 'Action & Adventure', 'id': '10759', 'icon': 'genre_action'}, {'name': 'Animation', 'id': '16', 'icon': 'genre_animation'},
{'name': 'Comedy', 'id': '35', 'icon': 'genre_comedy'}, {'name': 'Crime', 'id': '80', 'icon': 'genre_crime'}, {'name': 'Documentary', 'id': '99', 'icon': 'genre_documentary'},
{'name': 'Drama', 'id': '18', 'icon': 'genre_drama'}, {'name': 'Family', 'id': '10751', 'icon': 'genre_family'}, {'name': 'Kids', 'id': '10762', 'icon': 'genre_kids'},
{'name': 'Mystery', 'id': '9648', 'icon': 'genre_mystery'}, {'name': 'News', 'id': '10763', 'icon': 'genre_news'}, {'name': 'Reality', 'id': '10764', 'icon': 'genre_reality'},
{'name': 'Sci-Fi & Fantasy', 'id': '10765', 'icon': 'genre_scifi'}, {'name': 'Soap', 'id': '10766', 'icon': 'genre_soap'}, {'name': 'Talk', 'id': '10767', 'icon': 'genre_talk'},
{'name': 'War & Politics', 'id': '10768', 'icon': 'genre_war'}, {'name': 'Western', 'id': '37', 'icon': 'genre_western'}
	]

def movie_sorts():
	return [
{'name': 'Popularity (asc)', 'id': '&sort_by=popularity.asc'}, {'name': 'Popularity (desc)', 'id': '&sort_by=popularity.desc'},
{'name': 'Release Date (asc)', 'id': '&sort_by=primary_release_date.asc'}, {'name': 'Release Date (desc)', 'id': '&sort_by=primary_release_date.desc'},
{'name': 'Total Revenue (asc)', 'id': '&sort_by=revenue.asc'}, {'name': 'Total Revenue (desc)', 'id': '&sort_by=revenue.desc'},
{'name': 'Title (asc)', 'id': '&sort_by=original_title.asc'}, {'name': 'Title (desc)', 'id': '&sort_by=original_title.desc'},
{'name': 'Rating (asc)', 'id': '&sort_by=vote_average.asc'}, {'name': 'Rating (desc)', 'id': '&sort_by=vote_average.desc'},
{'name': 'Random', 'id': '[random]'}
	]

def tvshow_sorts():
	return [
{'name': 'Popularity (asc)', 'id': '&sort_by=popularity.asc'}, {'name': 'Popularity (desc)', 'id': '&sort_by=popularity.desc'},
{'name': 'First Aired (asc)', 'id': '&sort_by=first_air_date.asc'}, {'name': 'First Aired (desc)', 'id': '&sort_by=first_air_date.desc'},
{'name': 'Rating (asc)', 'id': '&sort_by=vote_average.asc'}, {'name': 'Rating (desc)', 'id': '&sort_by=vote_average.desc'},
{'name': 'Random', 'id': '[random]'}
	]

def discover_items():
	return {
'with_year_start': {'label': 'Year Start', 'key': 'with_year_start', 'display_key': 'with_year_start_display', 'action': 'years',
'url_insert_movie': '&primary_release_date.gte=%s-01-01', 'url_insert_tvshow': '&first_air_date.gte=%s-01-01', 'name_value': ' | %s onwards', 'icon': 'calender'},
'with_year_end': {'label': 'Year End', 'key': 'with_year_end', 'display_key': 'with_year_end_display', 'action': 'years',
'url_insert_movie': '&primary_release_date.lte=%s-12-31', 'url_insert_tvshow': '&first_air_date.lte=%s-12-31', 'name_value': ' | up to %s', 'icon': 'calender'},
'with_genres': {'label': 'With Genres', 'key': 'with_genres', 'display_key': 'with_genres_display', 'action': 'genres',
'url_insert': '&with_genres=%s', 'name_value': ' | %s', 'icon': 'genres'},
'without_genres': {'label': 'Without Genres', 'key': 'without_genres', 'display_key': 'without_genres_display', 'action': 'genres',
'url_insert': '&without_genres=%s', 'name_value': ' | exclude %s', 'icon': 'genres'},
'with_certification': {'label': 'Certification', 'key': 'with_certification', 'display_key': 'with_certification_display', 'action': 'certifications',
'url_insert': '&certification_country=US&certification=%s', 'name_value': ' | %s', 'limited': 'movie', 'icon': 'certifications'},
'with_certification_and_lower': {'label': 'Certification (& lower)', 'key': 'with_certification_and_lower', 'display_key': 'with_certification_and_lower_display',
'action': 'certification_and_lowers', 'url_insert': '&certification_country=US&certification.lte=%s', 'name_value': ' | %s', 'limited': 'movie', 'icon': 'certifications'},
'with_language': {'label': 'Language', 'key': 'with_language', 'display_key': 'with_language_display', 'action': 'languages',
'url_insert': '&with_original_language=%s', 'name_value': ' | %s', 'icon': 'languages'},	
'with_keywords': {'label': 'With Keywords', 'key': 'with_keywords', 'display_key': 'with_keywords_display', 'action': 'keywords',
'url_insert': '&with_keywords=%s', 'name_value': ' | Keywords: %s', 'icon': 'fantasy'},
'with_rating': {'label': 'Minimum Rating', 'key': 'with_rating', 'display_key': 'with_rating_display', 'action': 'ratings',
'url_insert': '&vote_average.gte=%s', 'name_value': ' | %s+', 'icon': 'most_watched'},
'with_rating_votes': {'label': 'Minimum Number of Votes', 'key': 'with_rating_votes', 'display_key': 'with_rating_votes_display', 'action': 'votes',
'url_insert': '&vote_count.gte=%s', 'name_value': ' | %s votes', 'icon': 'most_voted'},
'with_cast': {'label': 'Include Cast', 'key': 'with_cast', 'display_key': 'with_cast_display', 'action': 'casts',
'url_insert': '&with_cast=%s', 'name_value': ' | with %s', 'limited': 'movie', 'icon': 'people'},
'with_sort': {'label': 'Sort By', 'key': 'with_sort', 'display_key': 'with_sort_display', 'action': 'sort',
'url_insert': '%s', 'name_value': ' | %s', 'icon': 'lists'},
'with_released': {'label': 'Released Only', 'key': 'with_released', 'display_key': 'with_released_display', 'action': 'released',
'url_insert_movie': '&primary_release_date.lte=%s', 'url_insert_tvshow': '&include_null_first_air_dates=false&first_air_date.lte=%s', 'name_value': ' | Released Only', 'icon': 'dvd'},
'with_adult': {'label': 'Include Adult', 'key': 'with_adult', 'display_key': 'with_adult_display', 'action': 'adult',
'url_insert': '&include_adult=%s', 'name_value': ' | Include Adult', 'limited': 'movie', 'icon': 'romance'},
	}

def color_palette():
	return [
'FFFFFFE3', 'FFFFFAE6', 'FFFEF5E6', 'FFFEF0E5', 'FFFEEBE5', 'FFFFEFEF', 'FFFFE6EA', 'FFFFE6F1', 'FFFEE6F4', 'FFFFE6FB', 'FFFEE6FE', 'FFFAE6FF', 'FFF4E6FF', 'FFF0E6FF', 'FFEAE7FC',
'FFE6E7FC', 'FFE6EBFF', 'FFE7F0FF', 'FFE7F5FF', 'FFE7FAFF', 'FFE6FFFF', 'FFE6FFFB', 'FFE7FEF4', 'FFE7FFF1', 'FFE6FFEA', 'FFE7FFE7', 'FFEBFFF3', 'FFF1FFE6', 'FFF5FFE6', 'FFFBFFE6',
'FFFFFFFF', 'FFFFFFCB', 'FFFEFACA', 'FFFFEACB', 'FFFFE0CC', 'FFFED6CC', 'FFFFCACD', 'FFFFCCD5', 'FFFFCDE0', 'FFFFCCEB', 'FFFFCBF5', 'FFFECCFD', 'FFF6CBFF', 'FFECCCFE', 'FFE0CCFF',
'FFD6CCFE', 'FFCCCCFE', 'FFCDD6FF', 'FFCAE1FF', 'FFCCEBFF', 'FFCEF4FD', 'FFCAFFFF', 'FFCCFFF6', 'FFCBFEEB', 'FFCCFFE0', 'FFCCFFD6', 'FFCDFFCC', 'FFD7FFCB', 'FFE1FFCD', 'FFEBFFCC',
'FFF5FFCB', 'FFEFEFEF', 'FFFEFFB3', 'FFFFF1B2', 'FFFFE0B2', 'FFFDD2B2', 'FFFFC2B3', 'FFFFB3B3', 'FFFFB2C2', 'FFFFB3D1', 'FFFFB3E1', 'FFFFB2F4', 'FFFFB3FE', 'FFF0B3FF', 'FFE1B2FF',
'FFD2B3FF', 'FFC1B3FE', 'FFB4B3FF', 'FFB3C1FE', 'FFB2D1FF', 'FFB3E0FF', 'FFB2F0FF', 'FFB3FFFF', 'FFB3FFF0', 'FFB4FFE0', 'FFB3FFD1', 'FFB4FEC3', 'FFB3FFB4', 'FFC2FFB2', 'FFD1FFB4',
'FFE0FFB3', 'FFF1FFB4', 'FFE0E0E0', 'FFFEFF99', 'FFFFEB9A', 'FFFED699', 'FFFFC299', 'FFFFAD98', 'FFFF9899', 'FFFF99AE', 'FFFF99C1', 'FFFE99D5', 'FFFF99EC', 'FFFF99FF', 'FFEB99FF',
'FFD699FF', 'FFC299FF', 'FFAE99FF', 'FF9A99FF', 'FF98ADFE', 'FF9AC2FF', 'FF98D6FF', 'FF99EBFF', 'FF99FFFF', 'FF99FFEA', 'FF99FFD7', 'FF9AFFC3', 'FF99FFAC', 'FF99FF99', 'FFADFF99',
'FFC2FF98', 'FFD6FF99', 'FFEAFF98', 'FFD0D0D0', 'FFFFFF80', 'FFFFE681', 'FFFFCC80', 'FFFFB381', 'FFFF9980', 'FFFE8081', 'FFFF8199', 'FFFF80B3', 'FFFF80CD', 'FFFF80E7', 'FFFC81FE',
'FFE680FF', 'FFCC7FFF', 'FFB380FF', 'FF9980FF', 'FF807FFE', 'FF8099FE', 'FF7FB3FF', 'FF80CCFE', 'FF80E6FF', 'FF7FFFFE', 'FF7FFEE0', 'FF80FFCC', 'FF80FFB2', 'FF80FF98', 'FF81FF81',
'FF99FF80', 'FFB3FF80', 'FFCCFF80', 'FFE6FF80', 'FFC0C0C0', 'FFFFFF6B', 'FFFEE066', 'FFFFC267', 'FFFFA366', 'FFFF8566', 'FFFF6766', 'FFFF6685', 'FFFF66A4', 'FFFF66C1', 'FFFF66E0',
'FFFF66FF', 'FFE166FF', 'FFC366FF', 'FFA366FF', 'FF8566FF', 'FF6665FE', 'FF6785FF', 'FF66A3FE', 'FF65C2FF', 'FF65E0FF', 'FF65FFFF', 'FF66FFE0', 'FF65FFC1', 'FF66FFA4', 'FF65FF85',
'FF66FF66', 'FF84FF66', 'FFA2FF66', 'FFC2FF66', 'FFE0FF66', 'FFAFAFAF', 'FFFFFF4D', 'FFFFDB4E', 'FFFFB84E', 'FFFF944C', 'FFFF714D', 'FFFF4D4D', 'FFFF4D6F', 'FFFE4D93', 'FFFE4DB7',
'FFFE4DDB', 'FFFF4DFF', 'FFDC4DFF', 'FFB84DFF', 'FF944EFF', 'FF704DFF', 'FF4D4CFF', 'FF4D70FE', 'FF4D94FE', 'FF4DB8FF', 'FF4DDBFF', 'FF4DFFFF', 'FF4DFFDB', 'FF4EFFB9', 'FF4EFF95',
'FF4DFE70', 'FF4CFF4C', 'FF70FF4D', 'FF94FF4D', 'FFB8FE4D', 'FFDAFF4D', 'FF8C8C8C', 'FFFFFF33', 'FFFFD634', 'FFFFAD33', 'FFFF8532', 'FFFF5C33', 'FFFF3334', 'FFFF335C', 'FFFF3287',
'FFFF33AE', 'FFFF33D6', 'FFFE33FF', 'FFD633FE', 'FFAD34FF', 'FF8534FF', 'FF5D33FF', 'FF3233FF', 'FF325CFE', 'FF3285FF', 'FF33ADFF', 'FF33D6FF', 'FF33FFFE', 'FF32FFD6', 'FF34FFAD',
'FF33FF84', 'FF32FF5C', 'FF34FF33', 'FF5CFF34', 'FF85FE33', 'FFADFE33', 'FFD5FF33', 'FF7C7C7C', 'FFFFFF19', 'FFFFD119', 'FFFFA418', 'FFFF751A', 'FFFF4719', 'FFFF1919', 'FFFF1947',
'FFFF1874', 'FFFF19A3', 'FFFF19D1', 'FFFF19FF', 'FFD019FF', 'FFA219FF', 'FF751AFE', 'FF4719FF', 'FF1819FF', 'FF1947FF', 'FF1974FF', 'FF19A3FE', 'FF18D1FF', 'FF19FFFF', 'FF19FFD1',
'FF19FFA4', 'FF18FF75', 'FF19FF47', 'FF19FF19', 'FF48FF19', 'FF76FF19', 'FFA3FE1A', 'FFD1FF19', 'FF6B6B6B', 'FFFFFF00', 'FFFFCC00', 'FFFE9900', 'FFFF6600', 'FFFF3300', 'FFFE0000',
'FFFE0032', 'FFFF0066', 'FFFF0198', 'FFFF00CC', 'FFFF00FE', 'FFCC00FF', 'FF9A00FF', 'FF6601FF', 'FF3300FF', 'FF0000FE', 'FF0033FF', 'FF0166FF', 'FF0097FE', 'FF00CCFF', 'FF00FFFF',
'FF01FFCD', 'FF00FF99', 'FF00FE67', 'FF00FF33', 'FF00FF01', 'FF33FF00', 'FF65FF00', 'FF99FE00', 'FFCCFF00', 'FF5D5D5D', 'FFE8E500', 'FFE6B800', 'FFE68B00', 'FFE65C01', 'FFE72E00',
'FFE60000', 'FFE6002E', 'FFE6005B', 'FFE80183', 'FFE600B8', 'FFE600E6', 'FFB700E6', 'FF8900E6', 'FF5C01E5', 'FF2E00E6', 'FF0000E6', 'FF012EE1', 'FF005BE7', 'FF008AE5', 'FF00B8E6',
'FF00E6E6', 'FF00E6B7', 'FF00E78B', 'FF00E65F', 'FF00E532', 'FF00E600', 'FF2FE600', 'FF5DE600', 'FF8AE501', 'FFB8E600', 'FF4F4F4F', 'FFCDCC00', 'FFCDA301', 'FFCA7B02', 'FFCC5200',
'FFCC2900', 'FFCC0001', 'FFCD0029', 'FFCE0052', 'FFCC007B', 'FFCD00A3', 'FFCB00CC', 'FFA300CB', 'FF7A01CC', 'FF5201CC', 'FF2A00D0', 'FF0000CC', 'FF0029CB', 'FF0052CC', 'FF007ACD',
'FF00A3CC', 'FF00CCCB', 'FF00CCA3', 'FF01CC7A', 'FF03CB51', 'FF00CC29', 'FF01CC00', 'FF29CC01', 'FF52CB00', 'FF7ACB00', 'FFA2CC00', 'FF434343', 'FFB4B300', 'FFB38E00', 'FFB36B00',
'FFB34700', 'FFB32501', 'FFB30101', 'FFB40025', 'FFB40047', 'FFB4006B', 'FFB5008B', 'FFB300B3', 'FF8F00B2', 'FF6B00B2', 'FF4700B4', 'FF2300B2', 'FF0000B2', 'FF0025B4', 'FF0047B3',
'FF006BB3', 'FF008EB2', 'FF00B3B2', 'FF00B38E', 'FF00B36C', 'FF00B346', 'FF00B324', 'FF00B300', 'FF24B301', 'FF47B200', 'FF6CB201', 'FF90B301', 'FF373737', 'FF999A00', 'FF987A00',
'FF995C01', 'FF9A3D00', 'FF9A1F00', 'FF990100', 'FF99001F', 'FF9A003E', 'FF99005B', 'FF9A007A', 'FF990099', 'FF7B0099', 'FF5D0099', 'FF3D0099', 'FF1F0099', 'FF000098', 'FF011F99',
'FF003D98', 'FF005C99', 'FF007A99', 'FF009999', 'FF00997A', 'FF00995B', 'FF00993E', 'FF00991F', 'FF009900', 'FF1E9900', 'FF3C9900', 'FF5C9900', 'FF7A9900', 'FF2E2E2E', 'FF7F8000',
'FF7F6601', 'FF804C00', 'FF803201', 'FF801A01', 'FF800000', 'FF800019', 'FF800033', 'FF80004B', 'FF810065', 'FF81007F', 'FF660080', 'FF4C007F', 'FF33007F', 'FF1A0080', 'FF010080',
'FF011A7F', 'FF003480', 'FF004C80', 'FF00667F', 'FF008081', 'FF008067', 'FF037F4B', 'FF008033', 'FF00801B', 'FF008001', 'FF1A8000', 'FF338000', 'FF4C8001', 'FF668100', 'FF242424',
'FF656600', 'FF675201', 'FF653D00', 'FF672900', 'FF661400', 'FF660000', 'FF660015', 'FF660028', 'FF65003C', 'FF660053', 'FF660066', 'FF550069', 'FF3D0067', 'FF290066', 'FF150067',
'FF010066', 'FF001465', 'FF012966', 'FF003D66', 'FF005267', 'FF006766', 'FF006651', 'FF00663E', 'FF01662A', 'FF006613', 'FF006600', 'FF146600', 'FF296600', 'FF3D6600', 'FF516600',
'FF181818', 'FF4B4C00', 'FF4C3E01', 'FF4D2E00', 'FF4C1F00', 'FF4D0F00', 'FF4C0000', 'FF4C000F', 'FF4B001F', 'FF4C002E', 'FF4C003E', 'FF4C004B', 'FF3D004D', 'FF2E004B', 'FF1F004C',
'FF0E004B', 'FF01004C', 'FF000E4B', 'FF001F4D', 'FF012E4D', 'FF003D4C', 'FF004C4C', 'FF004D3D', 'FF004C2E', 'FF004C1E', 'FF004C0E', 'FF004C01', 'FF0F4C00', 'FF204C01', 'FF2D4C00',
'FF3E4C01', 'FF000000'
	]

# def mood_matrix():
# 	return {
# 'RESTLESS & HYPERACTIVE': {
# 'Adrenaline-Seeking': {
# 	'description': 'You want a frantic heart rate and non-stop momentum.',
# 	'keywords': ['adrenaline', 'non-stop-action', 'car-chase', 'high-octane', 'action-hero']},
# 'Aggressive & Cathartic': {
# 	'description': 'You need to release bottled-up anger or frustration.',
# 	'keywords': ['catharsis', 'violence', 'fistfight', 'brawl', 'rage']},
# 'Competitive': {
# 	'description': 'You feel driven by winning, rivalry, and intense stakes.',
# 	'keywords': ['rivalry', 'competition', 'tournament', 'underdog', 'sports-match']},
# 'Rebellious': {
# 	'description': 'You want to defy authority and break the rules.',
# 	'keywords': ['rebellion', 'anti-authoritarian', 'teen-rebel', 'defiance', 'outlaw']},
# 'Vengeful': {
# 	'description': 'You are harboring spite and want to see scores settled.',
# 	'keywords': ['revenge', 'vendetta', 'eye-for-an-eye', 'vigilante', 'seeking-justice']},
# 'Anxious & Panicked': {
# 	'description': 'You want to match your internal jitteriness with a tense ticking clock.',
# 	'keywords': ['ticking-clock', 'suspense', 'race-against-time', 'panic', 'countdown']},
# 'Invincible': {
# 	'description': 'You want to feel powerful, unstoppable, and deeply confident.',
# 	'keywords': ['overpowering', 'superhuman-strength', 'badass', 'unstoppable-force', 'one-man-army']},
# 'Vigilante': {
# 	'description': 'You feel righteously indignant and want to see immediate justice.',
# 	'keywords': ['vigilante-justice', 'street-justice', 'self-defense', 'urban-vigilante', 'retribution']},
# 'Overwhelmed': {
# 	'description': 'You want chaotic, fast-paced sensory overload to distract your brain.',
# 	'keywords': ['chaos', 'sensory-overload', 'fast-paced', 'frenzy', 'manic-pacing']},
# 'Escapist Thrill': {
# 	'description': 'You need pure, unthinking physical excitement.',
# 	'keywords': ['action-hero', 'blockbuster', 'popcorn-movie', 'stunt', 'explosion']}
# 	},
# 'JOYFUL & COMFORT-SEEKING': {
# 'Serene & Cozy': {
# 	'description': 'You want a warm blanket for the soul with zero stakes.',
# 	'keywords': ['feel-good', 'wholesome', 'cozy', 'heartwarming', 'low-stakes']},
# 'Giddy': {
# 	'description': 'You want romantic butterfly feelings and blushing smiles.',
# 	'keywords': ['romance', 'falling-in-love', 'first-love', 'crush', 'romantic-comedy']},
# 'Whimsical': {
# 	'description': 'You feel playful, imaginative, and light.',
# 	'keywords': ['whimsical', 'quirky', 'magic-realism', 'fairytale', 'eccentricity']},
# 'Nostalgic Comfort': {
# 	'description': 'You want to feel the safety of childhood and simpler times.',
# 	'keywords': ['nostalgia', 'childhood-memories', 'retro', 'coming-of-age', 'sentimental']},
# 'Optimistic': {
# 	'description': 'You need a reminder that humanity is inherently good.',
# 	'keywords': ['optimism', 'hope', 'kindness', 'humanity', 'happy-ending']},
# 'Grateful': {
# 	'description': 'You want to feel warm appreciation for family and friends.',
# 	'keywords': ['friendship', 'family-bonds', 'brotherhood', 'loyalty', 'camaraderie']},
# 'Amused & Silly': {
# 	'description': 'You just want to laugh at ridiculous, low-effort nonsense.',
# 	'keywords': ['slapstick-comedy', 'parody', 'goofy', 'absurd-humor', 'silly']},
# 'Inspirational': {
# 	'description': 'You want to feel motivated to take on the world.',
# 	'keywords': ['inspiration', 'triumph-of-the-human-spirit', 'motivation', 'overcoming-adversity', 'success']},
# 'Social & Connected': {
# 	'description': 'You want to feel part of a tight-knit community or workplace.',
# 	'keywords': ['small-town-life', 'workplace-dynamics', 'community', 'ensemble-cast', 'neighbors']},
# 'Carefree': {
# 	'description': 'You need to completely switch off your brain and responsibilities.',
# 	'keywords': ['escapism', 'mindless-fun', 'road-trip', 'summer-vacation', 'lighthearted']}
# 	},
# 'SAD & INTROSPECTIVE': {
# 'Mournful': {
# 	'description': 'You are grieving a loss and need to cry it out.',
# 	'keywords': ['grief', 'mourning', 'loss-of-loved-one', 'death', 'sadness']},
# 'Heartbroken': {
# 	'description': 'You feel the sting of romantic rejection or a breakup.',
# 	'keywords': ['heartbreak', 'unrequited-love', 'breakup', 'divorce', 'failed-romance']},
# 'Lonely': {
# 	'description': 'You want to feel seen in your isolation and disconnect from others.',
# 	'keywords': ['loneliness', 'alienation', 'isolation', 'solitude', 'social-disconnect']},
# 'Existential Dread': {
# 	'description': 'You are questioning your purpose and the meaning of life.',
# 	'keywords': ['existentialism', 'existential-dread', 'meaning-of-life', 'nihilism', 'futility']},
# 'Nostalgic Ache': {
# 	'description': 'You feel a painful, beautiful longing for things that are gone.',
# 	'keywords': ['melancholy', 'longing', 'yearning', 'lost-love', 'reminiscing']},
# 'Emotionally Exhausted': {
# 	'description': 'You feel drained and want a slow, quiet, low-stimulus story.',
# 	'keywords': ['slow-paced', 'minimalist', 'quiet', 'low-energy', 'slow-cinema']},
# 'Regretful': {
# 	'description': 'You are dwelling on past mistakes and "what ifs".',
# 	'keywords': ['regret', 'guilt', 'remorse', 'missed-opportunity', 'past-haunting']},
# 'Sombre & Muted': {
# 	'description': 'You want to sit quietly with a heavy, grey, rain-like mood.',
# 	'keywords': ['stark', 'bleak', 'austere', 'gloomy', 'muted-colors']},
# 'Bittersweet': {
# 	'description': 'You are feeling a complex mix of happiness and sadness at once.',
# 	'keywords': ['bittersweet', 'mixed-emotions', 'poignant', 'sweet-sorrow', 'touching']},
# 'Melancholic Awe': {
# 	'description': 'You want to feel small against a beautiful, tragic universe.',
# 	'keywords': ['tragedy', 'poetic-justice', 'sublime', 'epic-scale', 'haunting']}
# 	},
# 'DREAMY & SENSORY-DRIVEN': {
# 'Trance-Like': {
# 	'description': 'You want to be hypnotised by rhythm, visuals, and music.',
# 	'keywords': ['hypnotic', 'trance', 'rhythmic-visuals', 'dream-logic', 'ambient-music']},
# 'Brooding': {
# 	'description': 'You want to lean into a dark, moody, rain-slicked aesthetic.',
# 	'keywords': ['neo-noir', 'brooding-protagonist', 'rain-slicked-streets', 'cynical-tone', 'shadowy']},
# 'Eerie & Unsettled': {
# 	'description': 'You want a creeping, skin-crawling chill that is not a jump scare.',
# 	'keywords': ['creepy', 'unsettling', 'foreboding', 'dread', 'sinister-atmosphere']},
# 'Sentimental Haze': {
# 	'description': 'You want to feel like you are drifting through a warm summer memory.',
# 	'keywords': ['surrealism', 'hazy', 'impressionistic', 'memory-sequence', 'dreamscape']},
# 'Stark & Isolated': {
# 	'description': 'You feel cold, clean, and want minimalistic, empty spaces.',
# 	'keywords': ['isolation', 'minimalism', 'barren-landscape', 'stark-visuals', 'remote-setting']},
# 'Psychedelic': {
# 	'description': 'You want to feel visually intoxicated by vibrant, surreal colors.',
# 	'keywords': ['psychedelic', 'hallucination', 'vibrant-colors', 'trippy', 'altered-state']},
# 'Gothic Romance': {
# 	'description': 'You feel a dark, passionate, and macabre romanticism.',
# 	'keywords': ['gothic', 'macabre-romance', 'decaying-mansion', 'dark-passion', 'morbid']},
# 'Retro-Longing': {
# 	'description': 'You are romanticising a time period you never actually lived through.',
# 	'keywords': ['period-piece', 'stylized-history', 'vintage-aesthetic', 'retro-chic', 'yesteryear']},
# 'Urban Solitude': {
# 	'description': 'You want the specific vibe of being alone in a massive, neon city.',
# 	'keywords': ['urban-setting', 'neon-lighting', 'city-at-night', 'loner', 'metropolis']},
# 'Hypnotic Dread': {
# 	'description': 'You want to be slowly pulled under by a heavy, inescapable vibe.',
# 	'keywords': ['atmospheric', 'slow-burn', 'heavy-mood', 'immersion', 'creeping-dread']}
# 	},
# 'CURIOSE & INTELLECTUALLY STIMULATED': {
# 'Morally Conflicted': {
# 	'description': 'You want to debate what is right and wrong.',
# 	'keywords': ['moral-dilemma', 'ethical-crisis', 'grey-morality', 'impossible-choice', 'conscience']},
# 'Cynical': {
# 	'description': 'You are feeling critical of society, politics, and power structures.',
# 	'keywords': ['cynicism', 'misanthropy', 'corrupt-system', 'disillusionment', 'pessimism']},
# 'Empathetic': {
# 	'description': 'You want to deeply understand complex human behavior.',
# 	'keywords': ['character-study', 'psychological-portrait', 'human-nature', 'introspective', 'deep-empathy']},
# 'Inquisitive': {
# 	'description': 'You feel like a detective wanting to piece together a real-world puzzle.',
# 	'keywords': ['investigation', 'mystery-solving', 'whodunit', 'clue', 'puzzle-solving']},
# 'Philosophical': {
# 	'description': 'You want your core beliefs about humanity challenged.',
# 	'keywords': ['philosophical', 'intellectual', 'thought-experiment', 'metaphysical', 'existential-theme']},
# 'Skeptical': {
# 	'description': 'You want to question authority, conspiracies, and hidden truths.',
# 	'keywords': ['conspiracy', 'paranoia', 'government-coverup', 'whistleblower', 'hidden-truth']},
# 'Judicial': {
# 	'description': 'You want to weigh evidence and debate fairness and justice.',
# 	'keywords': ['courtroom-drama', 'legal-battle', 'lawyer', 'trial', 'miscarriage-of-justice']},
# 'Scientifically Curious': {
# 	'description': 'You want to ponder logic, tech ethics, and human advancement.',
# 	'keywords': ['artificial-intelligence', 'hard-sci-fi', 'futurism', 'technology-ethics', 'scientific-discovery']},
# 'Spiritually Searching': {
# 	'description': 'You are seeking answers about faith, doubt, and the soul.',
# 	'keywords': ['spirituality', 'crisis-of-faith', 'religion', 'theological', 'divine-intervention']},
# 'Culturally Awakened': {
# 	'description': 'You want to deeply absorb the struggles of another social class.',
# 	'keywords': ['social-commentary', 'class-struggle', 'political-statement', 'cultural-divide', 'inequality']}
# 	},
# 'TIME-TRAVELLING ESCAPISM': {
# 'Regal & Elite': {
# 	'description': 'You want to feel the opulence and high-society drama of royalty.',
# 	'keywords': ['royalty', 'monarchy', 'court-intrigue', 'aristocracy', 'period-drama']},
# 'Gritty & Primal': {
# 	'description': 'You want to strip away modern life for mud, swords, and survival.',
# 	'keywords': ['medieval-times', 'sword-and-sandal', 'feudal-politics', 'brutal-history', 'primal']},
# 'Mid-Century Nostalgia': {
# 	'description': 'You want the crisp style and social shifts of the 1950s/60s.',
# 	'keywords': ['1950s', '1960s', 'mid-century', 'post-war-boom', 'vintage-fashion']},
# 'Frontier Hardship': {
# 	'description': 'You feel rugged and want the isolation of the dusty wild west.',
# 	'keywords': ['wild-west', 'frontier-life', 'outlaw', 'cowboy', 'desert-landscape']},
# 'Wartime Camaraderie': {
# 	'description': 'You want to feel the intense brotherly bonds born of crisis.',
# 	'keywords': ['world-war-two', 'world-war-one', 'soldier', 'trench-warfare', 'brother-in-arms']},
# 'Jazz-Age Hedonism': {
# 	'description': 'You want to escape to a world of reckless glamour and party energy.',
# 	'keywords': ['1920s', 'roaring-twenties', 'jazz-age', 'flapper', 'prohibition']},
# 'Ancient Mysticism': {
# 	'description': 'You want to feel the mythic weight of lost empires.',
# 	'keywords': ['ancient-history', 'lost-empire', 'mythology', 'greece-or-rome', 'biblical-epic']},
# 'Post-War Resilience': {
# 	'description': 'You want to see people rebuilding their lives from scratch.',
# 	'keywords': ['post-war', 'reconstruction', 'aftermath', 'rebuilding-life', 'historical-fallout']},
# 'Biographical Empathy': {
# 	'description': 'You want to intimately walk in the shoes of a real historical figure.',
# 	'keywords': ['biography', 'historical-figure', 'true-story', 'biopic', 'real-life-events']},
# 'Victorian Restraint': {
# 	'description': 'You want the tension of hidden desires and strict societal rules.',
# 	'keywords': ['victorian-era', 'repressed-desire', 'social-etiquette', 'costume-drama', '19th-century']}
# 	},
# 'REBELLIOUS & EDGY': {
# 'Absurdist': {
# 	'description': 'You feel like nothing makes sense, so you want to embrace total nonsense.',
# 	'keywords': ['absurdist', 'nonsense', 'surreal-comedy', 'bizarre', 'weird']},
# 'Spiteful Satire': {
# 	'description': 'You want to see the rich, powerful, or annoying get mocked viciously.',
# 	'keywords': ['satire', 'black-comedy', 'mockery', 'irony', 'lampoon']},
# 'Cringe-Seeking': {
# 	'description': 'You want to squirm in awkward discomfort for comedic release.',
# 	'keywords': ['cringe-comedy', 'social-awkwardness', 'second-hand-embarrassment', 'uncomfortable-situation', 'deadpan']},
# 'Anarchic': {
# 	'description': 'You feel like burning down conventional structures and rules.',
# 	'keywords': ['anarchism', 'anti-establishment', 'subversive-art', 'chaos-agent', 'nihilistic-humor']},
# 'Macabre Curiosity': {
# 	'description': 'You are fascinated by the grotesque, weird, and forbidden.',
# 	'keywords': ['macabre', 'morbid', 'dark-themes', 'bizarre-creations', 'grotesque']},
# 'Campy': {
# 	'description': 'You want to enjoy things that are intentionally trashy, loud, and theatrical.',
# 	'keywords': ['cult-film', 'campy', 'cheesy', 'theatrical', 'b-movie']},
# 'Subversive': {
# 	'description': 'You want your expectations completely flipped and mocked.',
# 	'keywords': ['subversion', 'genre-deconstruction', 'breaking-the-fourth-wall', 'unconventional', 'subverting-expectations']},
# 'Anti-Establishment': {
# 	'description': 'You feel pure rage toward corporate greed and capitalism.',
# 	'keywords': ['anti-capitalism', 'corporate-greed', 'class-warfare', 'protest', 'social-rebellion']},
# 'Shock-Seeking': {
# 	'description': 'You want to see boundaries pushed to their absolute limit.',
# 	'keywords': ['provocative', 'controversial', 'shock-value', 'transgressive', 'boundary-pushing']},
# 'Unapologetically Weird': {
# 	'description': 'You want to celebrate eccentric outsiders who do not fit in.',
# 	'keywords': ['eccentric', 'outsider', 'misfit', 'unconventional-lifestyle', 'quirky-character']}
# 	},
# 'MIND-BOGGLED & DISORIENTED': {
# 'Paranoid': {
# 	'description': 'You feel like you cannot trust anyone around you.',
# 	'keywords': ['paranoia', 'trust-issues', 'conspiracy-theory', 'whos-watching-me', 'psychological-thriller']},
# 'Doubtful': {
# 	'description': 'You feel like your own senses and memories are lying to you.',
# 	'keywords': ['psychological', 'altered-perception', 'hallucination', 'mental-illusion', 'distorted-reality']},
# 'Trapped (Time)': {
# 	'description': 'You feel stuck in a rut and want to see a literal time loop.',
# 	'keywords': ['time-loop', 'time-travel-paradox', 'predestination', 'stuck-in-time', 'temporal-anomaly']},
# 'Spatially Trapped': {
# 	'description': 'You feel claustrophobic and want to see a single-room survival puzzle.',
# 	'keywords': ['trapped-in-a-single-room', 'claustrophobia', 'bottle-episode', 'survival-puzzle', 'confined-space']},
# 'Gaslit': {
# 	'description': 'You want to experience the psychological tension of being manipulated.',
# 	'keywords': ['gaslighting', 'psychological-manipulation', 'mind-games', 'deception', 'mental-abuse']},
# 'Vertigo': {
# 	'description': 'You want to feel the dizzying sensation of shifting timelines.',
# 	'keywords': ['nonlinear-timeline', 'flashback', 'fragmented-narrative', 'time-jump', 'interwoven-stories']},
# 'Existential Confusion': {
# 	'description': 'You want to wonder if your reality is actually a simulation.',
# 	'keywords': ['simulated-reality', 'virtual-reality', 'philosophical-sci-fi', 'matrix-like', 'existential-crisis']},
# 'Obsessive': {
# 	'description': 'You feel consumed by a mystery and want to track a descent into madness.',
# 	'keywords': ['obsession', 'descent-into-madness', 'fixation', 'manic-behavior', 'monomania']},
# 'Schizophrenic Flow': {
# 	'description': 'You want to experience an unreliable narrators chaotic mind.',
# 	'keywords': ['unreliable-narrator', 'subjective-camera', 'internal-monologue', 'fragmented-mind', 'mind-bending']},
# 'Identity Crisis': {
# 	'description': 'You are questioning who you really are at your core.',
# 	'keywords': ['identity-crisis', 'amnesia', 'double-life', 'imposter-syndrome', 'existential-identity']}
# 	}
# 	}
category_1 = {
'Adrenaline-Seeking': {
	'description': 'You want a frantic heart rate and non-stop momentum.',
	'keywords': ['adrenaline', 'non-stop-action', 'car-chase', 'high-octane', 'action-hero']},
'Aggressive & Cathartic': {
	'description': 'You need to release bottled-up anger or frustration.',
	'keywords': ['catharsis', 'violence', 'fistfight', 'brawl', 'rage']},
'Competitive': {
	'description': 'You feel driven by winning, rivalry, and intense stakes.',
	'keywords': ['rivalry', 'competition', 'tournament', 'underdog', 'sports-match']},
'Rebellious': {
	'description': 'You want to defy authority and break the rules.',
	'keywords': ['rebellion', 'anti-authoritarian', 'teen-rebel', 'defiance', 'outlaw']},
'Vengeful': {
	'description': 'You are harboring spite and want to see scores settled.',
	'keywords': ['revenge', 'vendetta', 'eye-for-an-eye', 'vigilante', 'seeking-justice']},
'Anxious & Panicked': {
	'description': 'You want to match your internal jitteriness with a tense ticking clock.',
	'keywords': ['ticking-clock', 'suspense', 'race-against-time', 'panic', 'countdown']},
'Invincible': {
	'description': 'You want to feel powerful, unstoppable, and deeply confident.',
	'keywords': ['overpowering', 'superhuman-strength', 'badass', 'unstoppable-force', 'one-man-army']},
'Vigilante': {
	'description': 'You feel righteously indignant and want to see immediate justice.',
	'keywords': ['vigilante-justice', 'street-justice', 'self-defense', 'urban-vigilante', 'retribution']},
'Overwhelmed': {
	'description': 'You want chaotic, fast-paced sensory overload to distract your brain.',
	'keywords': ['chaos', 'sensory-overload', 'fast-paced', 'frenzy', 'manic-pacing']},
'Escapist Thrill': {
	'description': 'You need pure, unthinking physical excitement.',
	'keywords': ['action-hero', 'blockbuster', 'popcorn-movie', 'stunt', 'explosion']}
	}
category_2 = {
'Serene & Cozy': {
	'description': 'You want a warm blanket for the soul with zero stakes.',
	'keywords': ['feel-good', 'wholesome', 'cozy', 'heartwarming', 'low-stakes']},
'Giddy': {
	'description': 'You want romantic butterfly feelings and blushing smiles.',
	'keywords': ['romance', 'falling-in-love', 'first-love', 'crush', 'romantic-comedy']},
'Whimsical': {
	'description': 'You feel playful, imaginative, and light.',
	'keywords': ['whimsical', 'quirky', 'magic-realism', 'fairytale', 'eccentricity']},
'Nostalgic Comfort': {
	'description': 'You want to feel the safety of childhood and simpler times.',
	'keywords': ['nostalgia', 'childhood-memories', 'retro', 'coming-of-age', 'sentimental']},
'Optimistic': {
	'description': 'You need a reminder that humanity is inherently good.',
	'keywords': ['optimism', 'hope', 'kindness', 'humanity', 'happy-ending']},
'Grateful': {
	'description': 'You want to feel warm appreciation for family and friends.',
	'keywords': ['friendship', 'family-bonds', 'brotherhood', 'loyalty', 'camaraderie']},
'Amused & Silly': {
	'description': 'You just want to laugh at ridiculous, low-effort nonsense.',
	'keywords': ['slapstick-comedy', 'parody', 'goofy', 'absurd-humor', 'silly']},
'Inspirational': {
	'description': 'You want to feel motivated to take on the world.',
	'keywords': ['inspiration', 'triumph-of-the-human-spirit', 'motivation', 'overcoming-adversity', 'success']},
'Social & Connected': {
	'description': 'You want to feel part of a tight-knit community or workplace.',
	'keywords': ['small-town-life', 'workplace-dynamics', 'community', 'ensemble-cast', 'neighbors']},
'Carefree': {
	'description': 'You need to completely switch off your brain and responsibilities.',
	'keywords': ['escapism', 'mindless-fun', 'road-trip', 'summer-vacation', 'lighthearted']}
	}
category_3 = {
'Mournful': {
	'description': 'You are grieving a loss and need to cry it out.',
	'keywords': ['grief', 'mourning', 'loss-of-loved-one', 'death', 'sadness']},
'Heartbroken': {
	'description': 'You feel the sting of romantic rejection or a breakup.',
	'keywords': ['heartbreak', 'unrequited-love', 'breakup', 'divorce', 'failed-romance']},
'Lonely': {
	'description': 'You want to feel seen in your isolation and disconnect from others.',
	'keywords': ['loneliness', 'alienation', 'isolation', 'solitude', 'social-disconnect']},
'Existential Dread': {
	'description': 'You are questioning your purpose and the meaning of life.',
	'keywords': ['existentialism', 'existential-dread', 'meaning-of-life', 'nihilism', 'futility']},
'Nostalgic Ache': {
	'description': 'You feel a painful, beautiful longing for things that are gone.',
	'keywords': ['melancholy', 'longing', 'yearning', 'lost-love', 'reminiscing']},
'Emotionally Exhausted': {
	'description': 'You feel drained and want a slow, quiet, low-stimulus story.',
	'keywords': ['slow-paced', 'minimalist', 'quiet', 'low-energy', 'slow-cinema']},
'Regretful': {
	'description': 'You are dwelling on past mistakes and "what ifs."',
	'keywords': ['regret', 'guilt', 'remorse', 'missed-opportunity', 'past-haunting']},
'Sombre & Muted': {
	'description': 'You want to sit quietly with a heavy, grey, rain-like mood.',
	'keywords': ['stark', 'bleak', 'austere', 'gloomy', 'muted-colors']},
'Bittersweet': {
	'description': 'You are feeling a complex mix of happiness and sadness at once.',
	'keywords': ['bittersweet', 'mixed-emotions', 'poignant', 'sweet-sorrow', 'touching']},
'Melancholic Awe': {
	'description': 'You want to feel small against a beautiful, tragic universe.',
	'keywords': ['tragedy', 'poetic-justice', 'sublime', 'epic-scale', 'haunting']}
	}
category_4 = {
'Trance-Like': {
	'description': 'You want to be hypnotised by rhythm, visuals, and music.',
	'keywords': ['hypnotic', 'trance', 'rhythmic-visuals', 'dream-logic', 'ambient-music']},
'Brooding': {
	'description': 'You want to lean into a dark, moody, rain-slicked aesthetic.',
	'keywords': ['neo-noir', 'brooding-protagonist', 'rain-slicked-streets', 'cynical-tone', 'shadowy']},
'Eerie & Unsettled': {
	'description': 'You want a creeping, skin-crawling chill that is not a jump scare.',
	'keywords': ['creepy', 'unsettling', 'foreboding', 'dread', 'sinister-atmosphere']},
'Sentimental Haze': {
	'description': 'You want to feel like you are drifting through a warm summer memory.',
	'keywords': ['surrealism', 'hazy', 'impressionistic', 'memory-sequence', 'dreamscape']},
'Stark & Isolated': {
	'description': 'You feel cold, clean, and want minimalistic, empty spaces.',
	'keywords': ['isolation', 'minimalism', 'barren-landscape', 'stark-visuals', 'remote-setting']},
'Psychedelic': {
	'description': 'You want to feel visually intoxicated by vibrant, surreal colors.',
	'keywords': ['psychedelic', 'hallucination', 'vibrant-colors', 'trippy', 'altered-state']},
'Gothic Romance': {
	'description': 'You feel a dark, passionate, and macabre romanticism.',
	'keywords': ['gothic', 'macabre-romance', 'decaying-mansion', 'dark-passion', 'morbid']},
'Retro-Longing': {
	'description': 'You are romanticising a time period you never actually lived through.',
	'keywords': ['period-piece', 'stylized-history', 'vintage-aesthetic', 'retro-chic', 'yesteryear']},
'Urban Solitude': {
	'description': 'You want the specific vibe of being alone in a massive, neon city.',
	'keywords': ['urban-setting', 'neon-lighting', 'city-at-night', 'loner', 'metropolis']},
'Hypnotic Dread': {
	'description': 'You want to be slowly pulled under by a heavy, inescapable vibe.',
	'keywords': ['atmospheric', 'slow-burn', 'heavy-mood', 'immersion', 'creeping-dread']}
	}
category_5 = {
'Morally Conflicted': {
	'description': 'You want to debate what is right and wrong.',
	'keywords': ['moral-dilemma', 'ethical-crisis', 'grey-morality', 'impossible-choice', 'conscience']},
'Cynical': {
	'description': 'You are feeling critical of society, politics, and power structures.',
	'keywords': ['cynicism', 'misanthropy', 'corrupt-system', 'disillusionment', 'pessimism']},
'Empathetic': {
	'description': 'You want to deeply understand complex human behavior.',
	'keywords': ['character-study', 'psychological-portrait', 'human-nature', 'introspective', 'deep-empathy']},
'Inquisitive': {
	'description': 'You feel like a detective wanting to piece together a real-world puzzle.',
	'keywords': ['investigation', 'mystery-solving', 'whodunit', 'clue', 'puzzle-solving']},
'Philosophical': {
	'description': 'You want your core beliefs about humanity challenged.',
	'keywords': ['philosophical', 'intellectual', 'thought-experiment', 'metaphysical', 'existential-theme']},
'Skeptical': {
	'description': 'You want to question authority, conspiracies, and hidden truths.',
	'keywords': ['conspiracy', 'paranoia', 'government-coverup', 'whistleblower', 'hidden-truth']},
'Judicial': {
	'description': 'You want to weigh evidence and debate fairness and justice.',
	'keywords': ['courtroom-drama', 'legal-battle', 'lawyer', 'trial', 'miscarriage-of-justice']},
'Scientifically Curious': {
	'description': 'You want to ponder logic, tech ethics, and human advancement.',
	'keywords': ['artificial-intelligence', 'hard-sci-fi', 'futurism', 'technology-ethics', 'scientific-discovery']},
'Spiritually Searching': {
	'description': 'You are seeking answers about faith, doubt, and the soul.',
	'keywords': ['spirituality', 'crisis-of-faith', 'religion', 'theological', 'divine-intervention']},
'Culturally Awakened': {
	'description': 'You want to deeply absorb the struggles of another social class.',
	'keywords': ['social-commentary', 'class-struggle', 'political-statement', 'cultural-divide', 'inequality']}
	}
category_6 = {
'Regal & Elite': {
	'description': 'You want to feel the opulence and high-society drama of royalty.',
	'keywords': ['royalty', 'monarchy', 'court-intrigue', 'aristocracy', 'period-drama']},
'Gritty & Primal': {
	'description': 'You want to strip away modern life for mud, swords, and survival.',
	'keywords': ['medieval-times', 'sword-and-sandal', 'feudal-politics', 'brutal-history', 'primal']},
'Mid-Century Nostalgia': {
	'description': 'You want the crisp style and social shifts of the 1950s/60s.',
	'keywords': ['1950s', '1960s', 'mid-century', 'post-war-boom', 'vintage-fashion']},
'Frontier Hardship': {
	'description': 'You feel rugged and want the isolation of the dusty wild west.',
	'keywords': ['wild-west', 'frontier-life', 'outlaw', 'cowboy', 'desert-landscape']},
'Wartime Camaraderie': {
	'description': 'You want to feel the intense brotherly bonds born of crisis.',
	'keywords': ['world-war-two', 'world-war-one', 'soldier', 'trench-warfare', 'brother-in-arms']},
'Jazz-Age Hedonism': {
	'description': 'You want to escape to a world of reckless glamour and party energy.',
	'keywords': ['1920s', 'roaring-twenties', 'jazz-age', 'flapper', 'prohibition']},
'Ancient Mysticism': {
	'description': 'You want to feel the mythic weight of lost empires.',
	'keywords': ['ancient-history', 'lost-empire', 'mythology', 'greece-or-rome', 'biblical-epic']},
'Post-War Resilience': {
	'description': 'You want to see people rebuilding their lives from scratch.',
	'keywords': ['post-war', 'reconstruction', 'aftermath', 'rebuilding-life', 'historical-fallout']},
'Biographical Empathy': {
	'description': 'You want to intimately walk in the shoes of a real historical figure.',
	'keywords': ['biography', 'historical-figure', 'true-story', 'biopic', 'real-life-events']},
'Victorian Restraint': {
	'description': 'You want the tension of hidden desires and strict societal rules.',
	'keywords': ['victorian-era', 'repressed-desire', 'social-etiquette', 'costume-drama', '19th-century']}
	}
category_7 = {
'Absurdist': {
	'description': 'You feel like nothing makes sense, so you want to embrace total nonsense.',
	'keywords': ['absurdist', 'nonsense', 'surreal-comedy', 'bizarre', 'weird']},
'Spiteful Satire': {
	'description': 'You want to see the rich, powerful, or annoying get mocked viciously.',
	'keywords': ['satire', 'black-comedy', 'mockery', 'irony', 'lampoon']},
'Cringe-Seeking': {
	'description': 'You want to squirm in awkward discomfort for comedic release.',
	'keywords': ['cringe-comedy', 'social-awkwardness', 'second-hand-embarrassment', 'uncomfortable-situation', 'deadpan']},
'Anarchic': {
	'description': 'You feel like burning down conventional structures and rules.',
	'keywords': ['anarchism', 'anti-establishment', 'subversive-art', 'chaos-agent', 'nihilistic-humor']},
'Macabre Curiosity': {
	'description': 'You are fascinated by the grotesque, weird, and forbidden.',
	'keywords': ['macabre', 'morbid', 'dark-themes', 'bizarre-creations', 'grotesque']},
'Campy': {
	'description': 'You want to enjoy things that are intentionally trashy, loud, and theatrical.',
	'keywords': ['cult-film', 'campy', 'cheesy', 'theatrical', 'b-movie']},
'Subversive': {
	'description': 'You want your expectations completely flipped and mocked.',
	'keywords': ['subversion', 'genre-deconstruction', 'breaking-the-fourth-wall', 'unconventional', 'subverting-expectations']},
'Anti-Establishment': {
	'description': 'You feel pure rage toward corporate greed and capitalism.',
	'keywords': ['anti-capitalism', 'corporate-greed', 'class-warfare', 'protest', 'social-rebellion']},
'Shock-Seeking': {
	'description': 'You want to see boundaries pushed to their absolute limit.',
	'keywords': ['provocative', 'controversial', 'shock-value', 'transgressive', 'boundary-pushing']},
'Unapologetically Weird': {
	'description': 'You want to celebrate eccentric outsiders who do not fit in.',
	'keywords': ['eccentric', 'outsider', 'misfit', 'unconventional-lifestyle', 'quirky-character']}
	}
category_8 = {
'Paranoid': {
	'description': 'You feel like you cannot trust anyone around you.',
	'keywords': ['paranoia', 'trust-issues', 'conspiracy-theory', 'whos-watching-me', 'psychological-thriller']},
'Doubtful': {
	'description': 'You feel like your own senses and memories are lying to you.',
	'keywords': ['psychological', 'altered-perception', 'hallucination', 'mental-illusion', 'distorted-reality']},
'Trapped (Time)': {
	'description': 'You feel stuck in a rut and want to see a literal time loop.',
	'keywords': ['time-loop', 'time-travel-paradox', 'predestination', 'stuck-in-time', 'temporal-anomaly']},
'Spatially Trapped': {
	'description': 'You feel claustrophobic and want to see a single-room survival puzzle.',
	'keywords': ['trapped-in-a-single-room', 'claustrophobia', 'bottle-episode', 'survival-puzzle', 'confined-space']},
'Gaslit': {
	'description': 'You want to experience the psychological tension of being manipulated.',
	'keywords': ['gaslighting', 'psychological-manipulation', 'mind-games', 'deception', 'mental-abuse']},
'Vertigo': {
	'description': 'You want to feel the dizzying sensation of shifting timelines.',
	'keywords': ['nonlinear-timeline', 'flashback', 'fragmented-narrative', 'time-jump', 'interwoven-stories']},
'Existential Confusion': {
	'description': 'You want to wonder if your reality is actually a simulation.',
	'keywords': ['simulated-reality', 'virtual-reality', 'philosophical-sci-fi', 'matrix-like', 'existential-crisis']},
'Obsessive': {
	'description': 'You feel consumed by a mystery and want to track a descent into madness.',
	'keywords': ['obsession', 'descent-into-madness', 'fixation', 'manic-behavior', 'monomania']},
'Schizophrenic Flow': {
	'description': 'You want to experience an unreliable narrators chaotic mind.',
	'keywords': ['unreliable-narrator', 'subjective-camera', 'internal-monologue', 'fragmented-mind', 'mind-bending']},
'Identity Crisis': {
	'description': 'You are questioning who you really are at your core.',
	'keywords': ['identity-crisis', 'amnesia', 'double-life', 'imposter-syndrome', 'existential-identity']}
	}

def mood_matrix():
	return {
'RESTLESS & HYPERACTIVE': category_1,
'JOYFUL & COMFORT-SEEKING': category_2,
'SAD & INTROSPECTIVE': category_3,
'DREAMY & SENSORY-DRIVEN': category_4,
'CURIOSITY & INTELLECTUALLY_STIMULATED': category_5,
'TIME-TRAVELLING ESCAPISM': category_6,
'REBELLIOUS & EDGY': category_7,
'MIND-BOGGLED & DISORIENTED': category_8
}