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

ADDON_PATH = xbmcvfs.translatePath(ADDON.getAddonInfo("path"))

DATA_DIR = xbmcvfs.translatePath(
    os.path.join(
        ADDON_PATH,
        "resources",
        "data"
    )
)

SOURCE_UNIVERSAL = xbmcvfs.translatePath(
    os.path.join(
        DATA_DIR,
        "advancedsettings.xml.universal"
    )
)

SOURCE_SHIELD = xbmcvfs.translatePath(
    os.path.join(
        DATA_DIR,
        "advancedsettings.xml.shield"
    )
)

DEST_FILE = xbmcvfs.translatePath("special://profile/advancedsettings.xml")


def notify(message, level=xbmcgui.NOTIFICATION_INFO, seconds=5000):
    xbmcgui.Dialog().notification(ADDON_NAME, message, level, seconds)


def log(message, level=xbmc.LOGINFO):
    xbmc.log("[%s] %s" % (ADDON_ID, message), level)


def show_ok(message):
    xbmcgui.Dialog().ok(ADDON_NAME, message)


def choose_source_file():
    choice = xbmcgui.Dialog().select(
        ADDON_NAME,
        [
            "NVIDIA Shield",
            "Universal",
            "Cancel"
        ]
    )

    if choice == -1 or choice == 2:
        return None, None

    if choice == 0:
        return SOURCE_SHIELD, "NVIDIA Shield"

    return SOURCE_UNIVERSAL, "Universal"


def backup_existing_file():
    if not xbmcvfs.exists(DEST_FILE):
        return True

    backup_file = DEST_FILE + ".bak-" + time.strftime("%Y%m%d-%H%M%S")

    if not xbmcvfs.copy(DEST_FILE, backup_file):
        msg = "Could not back up the existing advancedsettings.xml file."
        log(msg, xbmc.LOGERROR)
        show_ok(msg)
        return False

    overwrite = xbmcgui.Dialog().yesno(
        ADDON_NAME,
        "Backup created.\n\nOverwrite existing advancedsettings.xml?",
        "Cancel",
        "Install"
    )

    if not overwrite:
        notify("Install cancelled.")
        log("Install cancelled by user.")
        return False

    return True


def install_advancedsettings():
    source_file, profile_name = choose_source_file()

    if not source_file:
        notify("Install cancelled.")
        log("Install cancelled before profile selection.")
        return

    if not xbmcvfs.exists(source_file):
        msg = "%s advancedsettings file was not found." % profile_name
        log(msg, xbmc.LOGERROR)
        show_ok(msg)
        return

    if not backup_existing_file():
        return

    if not xbmcvfs.copy(source_file, DEST_FILE):
        msg = "Could not copy advancedsettings.xml to the Kodi profile folder."
        log(msg, xbmc.LOGERROR)
        show_ok(msg)
        return

    log("%s advancedsettings.xml installed to %s" % (profile_name, DEST_FILE))

    show_ok(
        "%s advancedsettings.xml installed.\n\nRestart Kodi for changes to take effect." % profile_name
    )


if __name__ == "__main__":
    install_advancedsettings()
