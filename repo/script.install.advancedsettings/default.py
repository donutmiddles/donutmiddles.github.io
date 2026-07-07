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


def install_advancedsettings():
    if not xbmcvfs.exists(SOURCE_FILE):
        msg = "Bundled advancedsettings.xml was not found."
        log(msg, xbmc.LOGERROR)
        xbmcgui.Dialog().ok(ADDON_NAME, msg)
        return

    if xbmcvfs.exists(DEST_FILE):
        backup_file = DEST_FILE + ".bak-" + time.strftime("%Y%m%d-%H%M%S")

        if not xbmcvfs.copy(DEST_FILE, backup_file):
            msg = "Could not back up the existing advancedsettings.xml file."
            log(msg, xbmc.LOGERROR)
            xbmcgui.Dialog().ok(ADDON_NAME, msg)
            return

        overwrite = xbmcgui.Dialog().yesno(
            ADDON_NAME,
            "An existing advancedsettings.xml file was found.",
            "A backup has been created.",
            "Do you want to overwrite it with the bundled file?"
        )

        if not overwrite:
            notify("Install cancelled. Existing file was left unchanged.")
            log("Install cancelled by user.")
            return

    if not xbmcvfs.copy(SOURCE_FILE, DEST_FILE):
        msg = "Could not copy advancedsettings.xml to the Kodi profile folder."
        log(msg, xbmc.LOGERROR)
        xbmcgui.Dialog().ok(ADDON_NAME, msg)
        return

    log("advancedsettings.xml installed to %s" % DEST_FILE)

    xbmcgui.Dialog().ok(
        ADDON_NAME,
        "advancedsettings.xml has been installed.",
        "Restart Kodi for the changes to take effect."
    )


if __name__ == "__main__":
    install_advancedsettings()
