# AdvancedSettings Installer for Kodi

This Kodi script add-on installs a bundled `advancedsettings.xml` file into the active Kodi profile directory.

It includes two bundled profiles:

* `advancedsettings.xml.universal`
* `advancedsettings.xml.shield`

When run, the add-on prompts the user to choose whether they are installing for an NVIDIA Shield device or a universal/non-Shield Kodi device.

## What it does

* Prompts the user to choose the **NVIDIA Shield** or **Universal** profile
* Copies the selected bundled file to `special://profile/advancedsettings.xml`
* Creates a timestamped backup if an existing `advancedsettings.xml` file is found
* Prompts before overwriting an existing file
* Reminds the user to restart Kodi after installation

## Bundled profiles

### Universal

The Universal profile is intended for general Kodi clients and conservative compatibility across supported platforms.

### NVIDIA Shield

The Shield profile is intended for NVIDIA Shield TV / Shield TV Pro devices, especially when used with Jellyfin through an NGINX reverse proxy and high-bitrate playback, including UHD 4K Blu-ray remux content.

The Shield profile includes conservative network, SMB, NFS, artwork, Android passthrough, and playback/resume behavior settings.

## Installation from ZIP

1. Download the release ZIP.
2. In Kodi, go to **Add-ons > Install from zip file**.
3. Select the ZIP file.
4. After installation, go to **Add-ons > Program add-ons**.
5. Run **AdvancedSettings Installer**.
6. Choose either **NVIDIA Shield** or **Universal**.
7. Confirm the overwrite prompt if an existing `advancedsettings.xml` file is found.
8. Restart Kodi.

## Installation from repository

If this add-on is included in an installed Kodi repository:

1. In Kodi, go to **Add-ons > Install from repository**.
2. Open the repository that contains this add-on.
3. Go to **Program add-ons**.
4. Install **AdvancedSettings Installer**.
5. Run **AdvancedSettings Installer**.
6. Choose either **NVIDIA Shield** or **Universal**.
7. Restart Kodi.

## File locations

Bundled source files:

```text
resources/data/advancedsettings.xml.universal
resources/data/advancedsettings.xml.shield
```

Installed destination:

```text
special://profile/advancedsettings.xml
```

Kodi resolves `special://profile/` to the active Kodi profile directory.

## Notes

Kodi only reads `advancedsettings.xml` at startup, so Kodi must be restarted after installation.

For Kodi Omega and newer, video cache size, read factor, and related cache behavior should be configured in:

```text
Settings > Services > Caching
```

The legacy cache block in `advancedsettings.xml` is retained only as a reference in the bundled profiles and is deprecated/ignored by Kodi Omega and newer.
