import platform
import subprocess

def _run_powershell(cmd):
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def get_pc_specs():
    specs = {}

    version = platform.win32_ver()[0]
    edition = _run_powershell(
        "(Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').EditionID"
    )
    specs["OS Version"] = f"Windows {version} {edition or ''}".strip()
    specs["Architecture"] = "64-bit" if platform.machine().endswith("64") else "32-bit"
    serial = _run_powershell("(Get-WmiObject Win32_BIOS).SerialNumber")
    specs["Motherboard Serial"] = serial or "Unavailable"
    model = _run_powershell("(Get-WmiObject Win32_BaseBoard).Product")
    specs["Model"] = model or "Unavailable"

    return specs
