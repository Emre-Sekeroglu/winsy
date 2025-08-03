import winreg

ROOT_KEYS = {
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
}
READ_ACCESS = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
WRITE_ACCESS = winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY

def read_value(path, value_name, root):
    try:
        with winreg.OpenKey(ROOT_KEYS[root], path, 0, READ_ACCESS) as key:
            val, _ = winreg.QueryValueEx(key, value_name)
            return val
    except Exception as e:
        print("[READ ERROR]", e)
        return None

def write_value(path, value_name, value, root, create_if_missing=False):
    try:
        if create_if_missing:
            key = winreg.CreateKeyEx(ROOT_KEYS[root], path, 0, WRITE_ACCESS)
        else:
            key = winreg.OpenKey(ROOT_KEYS[root], path, 0, WRITE_ACCESS)

        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        return True
    except PermissionError:
        print("[WRITE ERROR] Run as Administrator.")
    except Exception as e:
        print("[WRITE ERROR]", e)
    return False
