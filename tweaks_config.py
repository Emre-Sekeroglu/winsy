from power_utils import read_powercfg_value, run_powercfg_commands
# -------------------------------
# REGISTRY TWEAKS
# -------------------------------

REGISTRY_TWEAKS = [

    {
    "name": "Show Advanced Power Settings",
    "description": "Show advanced power settings in Control Panel",
    "tooltip": "ON = extra options in advanced power settings",
    "type": "registry",
    "path":  r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings"
             r"\54533251-82be-4824-96c1-47b60b740d00"
             r"\be337238-0d82-4146-a960-4f3749d470c7",
    "value": "Attributes",
    "on":    2,
    "off":   1,
    "root": "HKEY_LOCAL_MACHINE",  # ← critical
    "category": "Power Tweaks"
    },
    {
        "name":        "Remove 'Learn more about this picture' Desktop Icon",
        "description": "Hides the 'Learn more about this picture' desktop icon.",
        "tooltip":     "ON = icon hidden\nOFF = icon shown\nCredit: Shawn Brink (www.elevenforum.com)",
        "path":        r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
        "value":       "{2cc5ca98-6485-489a-920e-b3e88a6ccce3}",
        "on":          1,
        "off":         0,
        "category": "Personalization" 
    },
    {
        "description": "Show Computer Icon",
        "category": "Personalization",
        "type": "registry",
        "path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel",
        "value": "{20D04FE0-3AEA-1069-A2D8-08002B30309D}",
        "on": 0,
        "off": 1,
        "root": "HKEY_CURRENT_USER",
        "tooltip": "Toggle visibility of the 'This PC' (Computer) icon on the desktop.",
        "refresh_desktop": True,
        "is_desktop_icon_toggle": True
    },
    {
        "description": "Show User's Files Icon",
        "category": "Personalization",
        "type": "registry",
        "path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel",
        "value": "{59031a47-3f72-44a7-89c5-5595fe6b30ee}",
        "on": 0,
        "off": 1,
        "root": "HKEY_CURRENT_USER",
        "tooltip": "Toggle visibility of the user's personal folder icon on the desktop.",
        "refresh_desktop": True,
        "is_desktop_icon_toggle": True
    },
    {
        "description": "Show Recycle Bin Icon",
        "category": "Personalization",
        "type": "registry",
        "path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel",
        "value": "{645FF040-5081-101B-9F08-00AA002F954E}",
        "on": 0,
        "off": 1,
        "root": "HKEY_CURRENT_USER",
        "tooltip": "Toggle visibility of the Recycle Bin icon on the desktop.",
        "refresh_desktop": True,
        "is_desktop_icon_toggle": True
    },
    {
        "description": "Show Network Icon",
        "category": "Personalization",
        "type": "registry",
        "path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel",
        "value": "{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}",
        "on": 0,
        "off": 1,
        "root": "HKEY_CURRENT_USER",
        "tooltip": "Toggle visibility of the Network icon on the desktop.",
        "refresh_desktop": True,
        "is_desktop_icon_toggle": True
    },
    {
        "description": "Show Control Panel Icon",
        "category": "Personalization",
        "type": "registry",
        "path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\HideDesktopIcons\\NewStartPanel",
        "value": "{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}",
        "on": 0,
        "off": 1,
        "root": "HKEY_CURRENT_USER",
        "tooltip": "Toggle visibility of the Control Panel icon on the desktop.",
        "refresh_desktop": True,
        "is_desktop_icon_toggle": True
    }
]



# -------------------------------
# POWERCFG TWEAKS
# -------------------------------

POWERCFG_TWEAKS = [
    {
        "description": "Set CPU Min 5% / Max 100% (AC+DC)",
        "category": "Power Tweaks",
        "type": "powercfg",
        "on_cmds": [
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100"
        ],
        "off_cmds": [
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 80",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100"    
        ],
        "tooltip": "Sets min CPU at 5% and max at 100% for both plugged and battery modes. Improves responsiveness without boosting. Default is 80% min and 100% max while plugged in.",
    },
    {
    "description": "CPU Boost Mode",
    "type": "powercfg_dropdown",
    "setting_guid": "be337238-0d82-4146-a960-4f3749d470c7",
    "category": "Power Tweaks",
    "options": {
        "Disabled": "0",
        "Enabled": "1",
        "Aggressive": "2",
        "Efficient Aggressive": "3",
        "Efficient Enabled": "4"
    },
    "setting": "PERFBOOSTMODE",
    "default": "Disabled",
    "tooltip": "Controls processor performance boost policy.",
    "read_current_value": lambda: (
    print("[SYNC DEBUG] Read PERFBOOSTMODE:", read_powercfg_value("ac", "SUB_PROCESSOR", "PERFBOOSTMODE")) or {
        "0": "Disabled",
        "1": "Enabled",
        "2": "Aggressive",
        "3": "Efficient Aggressive",
        "4": "Efficient Enabled"
    }.get(
        str(read_powercfg_value("ac", "SUB_PROCESSOR", "PERFBOOSTMODE")),
        "Disabled"
    )
    ),
    "apply": lambda val: run_powercfg_commands([
        f"powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE {val}",
        f"powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE {val}",
        "powercfg /S SCHEME_CURRENT"
    ])
}

]


# -------------------------------
#  Merge for use in the app
# -------------------------------

TWEAKS = REGISTRY_TWEAKS + POWERCFG_TWEAKS
