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
        "label": "Universal Low (Fire TV, Onn, budget boxes)",
        "file": "advancedsettings.xml.universal.low"
    },
    {
        "label": "Universal Midrange (Google TV, Pi, mini PCs)",
        "file": "advancedsettings.xml.universal.midrange"
    },
    {
        "label": "Universal High (HTPC, NUC, powerful clients)",
        "file": "advancedsettings.xml.universal.high"
    },
    {
        "label": "Shield Internal LAN (Shield + local server/NAS)",
        "file": "advancedsettings.xml.shield.internal"
    }
]

MAIN_MENU_OPTIONS = [
    "Install advancedsettings.xml",
    "View current advancedsettings.xml",
    "Cancel"
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


def choose_main_action():
    choice = xbmcgui.Dialog().select(
        ADDON_NAME,
        MAIN_MENU_OPTIONS
    )

    if choice == -1 or choice == 2:
        return "cancel"

    if choice == 1:
        return "view"

    return "install"


def read_text_file(path):
    file_handle = None

    try:
        file_handle = xbmcvfs.File(path)
        contents = file_handle.read()
    except Exception as error:
        log("Could not read file %s: %s" % (path, error), xbmc.LOGERROR)
        return None
    finally:
        try:
            if file_handle:
                file_handle.close()
        except Exception:
            pass

    if isinstance(contents, bytes):
        contents = contents.decode("utf-8", "replace")

    return contents


def view_current_advancedsettings():
    if not xbmcvfs.exists(DEST_FILE):
        show_ok(
            "No current advancedsettings.xml file was found.\n\n"
            "Expected location:\n%s" % DEST_FILE
        )
        return

    contents = read_text_file(DEST_FILE)

    if contents is None:
        show_ok("Could not open the current advancedsettings.xml file.")
        return

    if not contents.strip():
        contents = "[advancedsettings.xml exists, but it appears to be empty.]"

    xbmcgui.Dialog().textviewer(
        "Current advancedsettings.xml",
        contents,
        True
    )
    log("Viewed current advancedsettings.xml at %s" % DEST_FILE)


def choose_source_file():
    labels = [profile["label"] for profile in PROFILE_OPTIONS]
    labels.append("Cancel")

    choice = xbmcgui.Dialog().select(
        "Choose your device",
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


def main():
    action = choose_main_action()

    if action == "view":
        view_current_advancedsettings()
        return

    if action == "install":
        install_advancedsettings()
        return

    notify("AdvancedSettings cancelled.")
    log("Cancelled from main menu.")


if __name__ == "__main__":
    main()
