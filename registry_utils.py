import winreg

ROOT_KEY = winreg.HKEY_LOCAL_MACHINE
READ_ACCESS = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
WRITE_ACCESS = winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY

def read_value(path, value_name):
    try:
        with winreg.OpenKey(ROOT_KEY, path, 0, READ_ACCESS) as key:
            val, _ = winreg.QueryValueEx(key, value_name)
            return val
    except Exception as e:
        print("[READ ERROR]", e)
        return None

def write_value(path, value_name, value):
    try:
        with winreg.OpenKey(ROOT_KEY, path, 0, WRITE_ACCESS) as key:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
            return True
    except PermissionError:
        print("[WRITE ERROR] Run as Administrator.")
    except Exception as e:
        print("[WRITE ERROR]", e)
    return False
