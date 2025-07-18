import os
import subprocess
from winsy_version import __version__, VERSION_INFO

# Step 1: Generate version.txt
parts = [int(p) for p in __version__.split(".")]
while len(parts) < 4:
    parts.append(0)
filevers = prodvers = tuple(parts)

version_content = f'''\
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={filevers},
    prodvers={prodvers},
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',
          [
''' + ",\n".join([
    f'            StringStruct("{key}", "{value}")' for key, value in VERSION_INFO.items()
]) + '''
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
'''

with open("version.txt", "w", encoding="utf-8") as f:
    f.write(version_content)
print("✅ version.txt generated")

# Step 2: Build with PyInstaller
exe_name = f"Winsy-{__version__}"
cmd = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--icon=winsy_icon.ico",
    "--add-data", "winsy_icon.ico;.",
    f"--name={exe_name}",
    "--version-file=version.txt",
    "main.py"
]

print(f"🚀 Running PyInstaller with name: {exe_name}")
subprocess.run(cmd)
