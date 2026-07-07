# AdvancedSettings Installer for Kodi

This Kodi script add-on installs a bundled `advancedsettings.xml` file into the active Kodi profile directory.

## What it does

- Copies `resources/data/advancedsettings.xml` to `special://profile/advancedsettings.xml`
- Creates a timestamped backup if an existing `advancedsettings.xml` file is found
- Prompts before overwriting an existing file
- Reminds the user to restart Kodi

## Installation

1. Download the release ZIP.
2. In Kodi, go to **Add-ons > Install from zip file**.
3. Select the ZIP file.
4. After installation, go to **Add-ons > Program add-ons**.
5. Run **AdvancedSettings Installer**.
6. Restart Kodi.

## Notes

Kodi only reads `advancedsettings.xml` at startup, so Kodi must be restarted after installation.

For Kodi Omega and newer, cache size and read factor should be configured in:

`Settings > Services > Caching`
