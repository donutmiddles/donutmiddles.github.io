#!/usr/bin/env python3
import os
import hashlib

def generate_addons_xml(addons_dir, output_dir):
    addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"

    for addon in os.listdir(addons_dir):
        addon_path = os.path.join(addons_dir, addon)
        if os.path.isdir(addon_path):
            addon_xml_path = os.path.join(addon_path, 'addon.xml')
            if os.path.isfile(addon_xml_path):
                with open(addon_xml_path, 'r', encoding='UTF-8') as xml_file:
                    xml_content = xml_file.read()
                    # Remove the first line (<?xml ...?>)
                    xml_content = ''.join(xml_content.splitlines(True)[1:])
                    addons_xml += xml_content.strip() + "\n\n"

    addons_xml += "</addons>\n"

    # Write the addons.xml file
    addons_xml_path = os.path.join(output_dir, 'addons.xml')
    with open(addons_xml_path, 'w', encoding='UTF-8') as f:
        f.write(addons_xml)

    # Generate the MD5 hash
    md5_hash = hashlib.md5(addons_xml.encode('UTF-8')).hexdigest()

    # Write the addons.xml.md5 file
    md5_path = os.path.join(output_dir, 'addons.xml.md5')
    with open(md5_path, 'w') as f:
        f.write(md5_hash)

if __name__ == "__main__":
    # Paths to your 'addons' directory and 'repo' directory
    ADDONS_DIR = 'addons'  # The directory containing your add-ons' source folders
    OUTPUT_DIR = 'repo'    # The directory where addons.xml and addons.xml.md5 will be generated

    generate_addons_xml(ADDONS_DIR, OUTPUT_DIR)
    print("addons.xml and addons.xml.md5 have been generated in the 'repo' directory.")