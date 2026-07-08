# AdvancedSettings Installer for Kodi

This Kodi script add-on installs a bundled `advancedsettings.xml` file into the active Kodi profile directory.

It includes four bundled profiles:

* `advancedsettings.xml.universal.low`
* `advancedsettings.xml.universal.midrange`
* `advancedsettings.xml.universal.high`
* `advancedsettings.xml.shield.internal`

When run, the add-on allows the user to install an optimized profile, view the current `advancedsettings.xml` file if one exists, or cancel.

## What it does

* Prompts the user to install a selected `advancedsettings.xml` profile
* Provides Universal Low, Universal Midrange, Universal High, and Shield Internal LAN options
* Copies the selected bundled file to `special://profile/advancedsettings.xml`
* Creates a timestamped backup if an existing `advancedsettings.xml` file is found
* Prompts before overwriting an existing file
* Allows the user to view the current `advancedsettings.xml` file if one exists
* Reminds the user to restart Kodi after installation

## Bundled profiles

### Universal Low

The Universal Low profile is intended for lower-powered Kodi clients such as Fire TV devices, budget Onn boxes, older Android TV devices, low-memory streamers, and similar entry-level hardware.

### Universal Midrange

The Universal Midrange profile is intended for common modern Kodi clients such as Google TV devices, Raspberry Pi-class clients, lightweight mini PCs, and other balanced devices.

### Universal High

The Universal High profile is intended for stronger Kodi clients such as HTPCs, NUC-style systems, powerful mini PCs, and devices with more capable CPU, GPU, memory, storage, and network resources.

### Shield Internal LAN

The Shield Internal LAN profile is intended for NVIDIA Shield TV / Shield TV Pro devices used on an internal local network with a local server or NAS.

This profile is especially suited for Shield-based local playback environments using Jellyfin, NFS/SMB, wired LAN, and high-bitrate content, including UHD 4K Blu-ray remux files.

## Installation from ZIP

1. Download the release ZIP.
2. In Kodi, go to **Add-ons > Install from zip file**.
3. Select the ZIP file.
4. After installation, go to **Add-ons > Program add-ons**.
5. Run **AdvancedSettings Installer**.
6. Choose **Install advancedsettings.xml**.
7. Choose the profile that best matches your device.
8. Confirm the overwrite prompt if an existing `advancedsettings.xml` file is found.
9. Restart Kodi.

## Installation from repository

If this add-on is included in an installed Kodi repository:

1. In Kodi, go to **Add-ons > Install from repository**.
2. Open the repository that contains this add-on.
3. Go to **Program add-ons**.
4. Install **AdvancedSettings Installer**.
5. Run **AdvancedSettings Installer**.
6. Choose **Install advancedsettings.xml**.
7. Choose the profile that best matches your device.
8. Restart Kodi.

## Viewing the current file

If an `advancedsettings.xml` file already exists, the add-on can display its contents from within Kodi.

To view it:

1. Run **AdvancedSettings Installer**.
2. Choose **View current advancedsettings.xml**.

If no current file exists, the add-on will show the expected location.

## File locations

Bundled source files:

```text
resources/data/advancedsettings.xml.universal.low
resources/data/advancedsettings.xml.universal.midrange
resources/data/advancedsettings.xml.universal.high
resources/data/advancedsettings.xml.shield.internal
```

Installed destination:

```text
special://profile/advancedsettings.xml
```

Kodi resolves `special://profile/` to the active Kodi profile directory.

## Notes

Kodi only reads `advancedsettings.xml` at startup, so Kodi must be restarted after installation.

For Kodi Omega and newer, video cache size, read factor, chunk size, and related cache behavior should be configured in:

```text
Settings > Services > Caching
```

The legacy cache block in `advancedsettings.xml` is retained only as a reference in the bundled profiles and is deprecated/ignored by Kodi Omega and newer.
