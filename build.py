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

# Step 3: Generate Checksum Files
import hashlib

def generate_checksums(file_path):
    hashes = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha256': hashlib.sha256()
    }

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            for h in hashes.values():
                h.update(chunk)

# Store for markdown
    markdown_lines = ["**Checksums:**", ""]

    for algo, h in hashes.items():
        checksum = h.hexdigest()
        checksum_file = f"{file_path}.{algo}"
        with open(checksum_file, "w") as out_file:
            out_file.write(checksum + "\n")
        print(f"[✓] {algo.upper()} saved to {checksum_file}")
        markdown_lines.append(f"`{algo.upper()}:` `{checksum}`")

    markdown_lines.append("")
    markdown_lines.append("To verify your download, run:")
    markdown_lines.append("")
    markdown_lines.append("```powershell")
    markdown_lines.append(f"Get-FileHash .\\{os.path.basename(file_path)} -Algorithm SHA256")
    markdown_lines.append("```")

    # Write the final .txt file
    markdown_file = file_path.replace(".exe", "-checksums.txt")
    with open(markdown_file, "w") as f:
        f.write("\n".join(markdown_lines))
    print(f"[✓] Markdown summary saved to {markdown_file}")

# Use version from winsy_version.py
exe_path = os.path.join("dist", f"Winsy-{__version__}.exe")

if os.path.exists(exe_path):
    print(f"[✓] Found executable: {exe_path}")
    generate_checksums(exe_path)
else:
    print(f"[!] Executable not found at {exe_path}")
