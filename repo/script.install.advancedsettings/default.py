# -*- coding: utf-8 -*-

import os
import time

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs


ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_NAME = ADDON.getAddonInfo("name")

SOURCE_FILE = xbmcvfs.translatePath(
    os.path.join(
        ADDON.getAddonInfo("path"),
        "resources",
        "data",
        "advancedsettings.xml"
    )
)

DEST_FILE = xbmcvfs.translatePath("special://profile/advancedsettings.xml")


def notify(message, level=xbmcgui.NOTIFICATION_INFO, seconds=5000):
    xbmcgui.Dialog().notification(ADDON_NAME, message, level, seconds)


def log(message, level=xbmc.LOGINFO):
    xbmc.log("[%s] %s" % (ADDON_ID, message), level)


def show_ok(message):
    xbmcgui.Dialog().ok(ADDON_NAME, message)


def install_advancedsettings():
    if not xbmcvfs.exists(SOURCE_FILE):
        msg = "Bundled advancedsettings.xml was not found."
        log(msg, xbmc.LOGERROR)
        show_ok(msg)
        return

    if xbmcvfs.exists(DEST_FILE):
        backup_file = DEST_FILE + ".bak-" + time.strftime("%Y%m%d-%H%M%S")

        if not xbmcvfs.copy(DEST_FILE, backup_file):
            msg = "Could not back up the existing advancedsettings.xml file."
            log(msg, xbmc.LOGERROR)
            show_ok(msg)
            return

        overwrite = xbmcgui.Dialog().yesno(
            ADDON_NAME,
            "Existing advancedsettings.xml found.\n\nA backup was created.\n\nOverwrite it now?",
            "Cancel",
            "Install"
        )

        if not overwrite:
            notify("Install cancelled.")
            log("Install cancelled by user.")
            return

    if not xbmcvfs.copy(SOURCE_FILE, DEST_FILE):
        msg = "Could not copy advancedsettings.xml to the Kodi profile folder."
        log(msg, xbmc.LOGERROR)
        show_ok(msg)
        return

    log("advancedsettings.xml installed to %s" % DEST_FILE)

    show_ok(
        "advancedsettings.xml installed.\n\nRestart Kodi for changes to take effect."
    )


if __name__ == "__main__":
    install_advancedsettings()
