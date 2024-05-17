import os
import xml.etree.ElementTree as ET

# extract changelog of latest version
changelog_of_latest_version = ""

with open("ChangeLog.md", "r") as f:
    in_section = False
    for line in f:
        if line.startswith("# "):
            if in_section:
                break
            in_section = True
        else:
            if "###" in line:
                line += "\n"
                line = line.replace("###", "")
            changelog_of_latest_version += line

print(changelog_of_latest_version)
with open("changelog_of_latest_version.md", "w") as f:
    f.write(changelog_of_latest_version)

# convert Markdown to HTML
html_changelog = os.popen("pandoc --from markdown --wrap none --to html5 changelog_of_latest_version.md").read()
print(html_changelog)

# add changelog to release tag of metainfo file
output = ""
with open("/app/share/metainfo/eu.vcmi.VCMI.metainfo.xml") as f:
    latest_release_found = False
    for line in f:
        if "<release " in line and not latest_release_found:
            print("found!")
            print(line)
            latest_release_found = True
            line = line.replace("/>", f"><description>{html_changelog}</description></release>")
        output += line

# format XML
element = ET.XML(output)
ET.indent(element)
xml_string = ET.tostring(element, encoding="unicode")
print(xml_string)

with open("/app/share/metainfo/eu.vcmi.VCMI.metainfo.xml", "w") as f:
    f.write(xml_string)
