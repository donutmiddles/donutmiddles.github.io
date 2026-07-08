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

DEST_FILE = xbmcvfs.translatePath("special://profile/advancedsettings.xml")


PROFILE_OPTIONS = [
    {
        "label": "NVIDIA Shield TV / Shield TV Pro",
        "file": "advancedsettings.xml.shield"
    },
    {
        "label": "Fire TV Stick / Budget Android TV",
        "file": "advancedsettings.xml.firetv.low"
    },
    {
        "label": "Google TV / Midrange Android TV",
        "file": "advancedsettings.xml.android.midrange"
    },
    {
        "label": "Raspberry Pi / LibreELEC / CoreELEC",
        "file": "advancedsettings.xml.pi.libreelec"
    },
    {
        "label": "Windows HTPC / Mini PC",
        "file": "advancedsettings.xml.windows.htpc"
    },
    {
        "label": "Linux HTPC / Mini PC",
        "file": "advancedsettings.xml.linux.htpc"
    },
    {
        "label": "macOS HTPC",
        "file": "advancedsettings.xml.macos.htpc"
    },
    {
        "label": "Universal - Low-end",
        "file": "advancedsettings.xml.universal.low"
    },
    {
        "label": "Universal - Midrange",
        "file": "advancedsettings.xml.universal.midrange"
    },
    {
        "label": "Universal - High-end",
        "file": "advancedsettings.xml.universal.high"
    }
]


def notify(message, level=xbmcgui.NOTIFICATION_INFO, seconds=5000):
    xbmcgui.Dialog().notification(ADDON_NAME, message, level, seconds)


def log(message, level=xbmc.LOGINFO):
    xbmc.log("[%s] %s" % (ADDON_ID, message), level)


def show_ok(message):
    xbmcgui.Dialog().ok(ADDON_NAME, message)


def source_path(filename):
    return xbmcvfs.translatePath(
        os.path.join(
            DATA_DIR,
            filename
        )
    )


def choose_source_file():
    labels = [profile["label"] for profile in PROFILE_OPTIONS]
    labels.append("Cancel")

    choice = xbmcgui.Dialog().select(
        ADDON_NAME,
        labels
    )

    if choice == -1 or choice == len(labels) - 1:
        return None, None

    profile = PROFILE_OPTIONS[choice]

    return source_path(profile["file"]), profile["label"]


def backup_existing_file():
    if not xbmcvfs.exists(DEST_FILE):
        return True

    backup_file = DEST_FILE + ".bak-" + time.strftime("%Y%m%d-%H%M%S")

    if not xbmcvfs.copy(DEST_FILE, backup_file):
        msg = "Could not back up the existing advancedsettings.xml file."
        log(msg, xbmc.LOGERROR)
        show_ok(msg)
        return False

    log("Existing advancedsettings.xml backed up to %s" % backup_file)

    overwrite = xbmcgui.Dialog().yesno(
        ADDON_NAME,
        "Backup created.\n\nOverwrite existing advancedsettings.xml?",
        "Cancel",
        "Install"
    )

    if not overwrite:
        notify("Install cancelled.")
        log("Install cancelled by user after backup.")
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
