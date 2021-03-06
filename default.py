import sys
from urllib.parse import unquote_plus
import xbmc
import xbmcaddon
import xbmcgui
from lib.storage import HistoryData

ADDON = xbmcaddon.Addon()
LANGUAGE = ADDON.getLocalizedString
CWD = ADDON.getAddonInfo('path')

if (__name__ == '__main__'):
    try:
        params = dict(arg.split('=') for arg in sys.argv[1].split('&'))
    except:
        params = {}
    searchstring = unquote_plus(params.get('searchstring',''))
    defaultsearchstring = ADDON.getSettingString('defaultsearchstring')
    defaultsearchlast = ADDON.getSettingBool('defaultsearchlast')
    hidewatched = None
    cancelled = False
    if searchstring:
        del params['searchstring']
    else:
        searchstring = defaultsearchstring
        if (defaultsearchlast):
            history = HistoryData().load()

            if (len(history) > 0):
                searchstring = next(reversed(history)) # last item in dict
                xbmc.log("Loaded search string from history: %s" % searchstring, xbmc.LOGDEBUG)
        window_id = xbmcgui.getCurrentWindowId()
        if (window_id >= 13000):
            # Addon might be open, try getting the current runtime options
            win = xbmcgui.Window(window_id)
            searchstring = win.getProperty('GlobalSearch.SearchString')
            hidewatched = win.getProperty('GlobalSearch.HideWatched')
            hidewatched = hidewatched == 'True' if hidewatched != '' else None
        keyboard = xbmc.Keyboard(searchstring, LANGUAGE(32101), False)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            searchstring = keyboard.getText()
        else:
            # keyboard dialog closed, cancel search
            cancelled = True

    if not cancelled and searchstring:
        from lib import gui
        ui = gui.GUI('script-globalsearch.xml', CWD, 'default', '1080i', True, searchstring=searchstring, hidewatched=hidewatched, params=params)
        ui.doModal()
        del ui
