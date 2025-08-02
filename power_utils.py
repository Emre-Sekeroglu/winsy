import subprocess

def run_powercfg_commands(commands: list[str]) -> bool:
    try:
        for cmd in commands:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(cmd, shell=True, check=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except subprocess.CalledProcessError as e:
        print("Powercfg error:", e)
        return False

def read_powercfg_value(dc_or_ac: str, subgroup: str, setting: str) -> int | None:
    try:
        cmd = f'powercfg /query SCHEME_CURRENT {subgroup} {setting}'
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        output = subprocess.check_output(cmd, shell=True, text=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
        mode = "AC" if dc_or_ac.lower() == "ac" else "DC"
        for line in output.splitlines():
            if f"{mode} Power Setting Index" in line:
                return int(line.strip().split()[-1], 16)
    except subprocess.CalledProcessError as e:
        print(f"[READ ERROR] powercfg failed: {e.output}")
    except Exception as e:
        print(f"[READ ERROR] Unexpected: {e}")
    return None

