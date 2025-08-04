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
# Start change what power buttons do
{
    "description": "Power Button Action (On Battery)",
    "type": "powercfg_dropdown",
    "category": "Power Tweaks",
    "group": "Power Buttons",
    "setting_guid": "7648efa3-dd9c-4e3e-b566-50f929386280",
    "setting": "PBUTTONACTION",
    "mode": "dc",
    "options": {
        "Do nothing": "0",
        "Sleep": "1",
        "Hibernate": "2",
        "Shut down": "3"
    },
    "default": "Sleep",
    "tooltip": "What happens when you press the power button on battery.",
    "read_current_value": lambda: {
        0: "Do nothing",
        1: "Sleep",
        2: "Hibernate",
        3: "Shut down"
    }.get(read_powercfg_value("dc", "SUB_BUTTONS", "PBUTTONACTION"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        "powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION " + val,
        "powercfg /S SCHEME_CURRENT"
    ])
},
{
    "description": "Power Button Action (Plugged In)",
    "type": "powercfg_dropdown",
    "category": "Power Tweaks",
    "group": "Power Buttons",
    "setting_guid": "7648efa3-dd9c-4e3e-b566-50f929386280",
    "setting": "PBUTTONACTION",
    "mode": "ac",
    "options": {
        "Do nothing": "0",
        "Sleep": "1",
        "Hibernate": "2",
        "Shut down": "3"
    },
    "default": "Sleep",
    "tooltip": "What happens when you press the power button while plugged in.",
    "read_current_value": lambda: {
        0: "Do nothing",
        1: "Sleep",
        2: "Hibernate",
        3: "Shut down"
    }.get(read_powercfg_value("ac", "SUB_BUTTONS", "PBUTTONACTION"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        "powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION " + val,
        "powercfg /S SCHEME_CURRENT"
    ])
},
{
    "description": "Sleep Button Action (On Battery)",
    "type": "powercfg_dropdown",
    "category": "Power Tweaks",
    "group": "Power Buttons",
    "setting_guid": "96996bc0-ad50-47ec-923b-6f41874dd9eb",
    "setting": "SBUTTONACTION",
    "mode": "dc",
    "options": {
        "Do nothing": "0",
        "Sleep": "1",
        "Hibernate": "2",
        "Shut down": "3"
    },
    "default": "Sleep",
    "tooltip": "What happens when you press the sleep button on battery.",
    "read_current_value": lambda: {
        0: "Do nothing",
        1: "Sleep",
        2: "Hibernate",
        3: "Shut down"
    }.get(read_powercfg_value("dc", "SUB_BUTTONS", "SBUTTONACTION"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        "powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS SBUTTONACTION " + val,
        "powercfg /S SCHEME_CURRENT"
    ])
},
{
    "description": "Sleep Button Action (Plugged In)",
    "type": "powercfg_dropdown",
    "category": "Power Tweaks",
    "group": "Power Buttons",
    "setting_guid": "96996bc0-ad50-47ec-923b-6f41874dd9eb",
    "setting": "SBUTTONACTION",
    "mode": "ac",
    "options": {
        "Do nothing": "0",
        "Sleep": "1",
        "Hibernate": "2",
        "Shut down": "3"
    },
    "default": "Sleep",
    "tooltip": "What happens when you press the sleep button while plugged in.",
    "read_current_value": lambda: {
        0: "Do nothing",
        1: "Sleep",
        2: "Hibernate",
        3: "Shut down"
    }.get(read_powercfg_value("ac", "SUB_BUTTONS", "SBUTTONACTION"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        "powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS SBUTTONACTION " + val,
        "powercfg /S SCHEME_CURRENT"
    ])
},
{
    "description": "Lid Close Action (On Battery)",
    "type": "powercfg_dropdown",
    "category": "Power Tweaks",
    "group": "Power Buttons",
    "setting_guid": "5ca83367-6e45-459f-a27b-476b1d01c936",
    "setting": "LIDACTION",
    "mode": "dc",
    "options": {
        "Do nothing": "0",
        "Sleep": "1",
        "Hibernate": "2",
        "Shut down": "3"
    },
    "default": "Do nothing",
    "tooltip": "What happens when you close the laptop lid on battery.",
    "read_current_value": lambda: {
        0: "Do nothing",
        1: "Sleep",
        2: "Hibernate",
        3: "Shut down"
    }.get(read_powercfg_value("dc", "SUB_BUTTONS", "LIDACTION"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        "powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION " + val,
        "powercfg /S SCHEME_CURRENT"
    ])
},
{
    "description": "Lid Close Action (Plugged In)",
    "type": "powercfg_dropdown",
    "category": "Power Tweaks",
    "group": "Power Buttons",
    "setting_guid": "5ca83367-6e45-459f-a27b-476b1d01c936",
    "setting": "LIDACTION",
    "mode": "ac",
    "options": {
        "Do nothing": "0",
        "Sleep": "1",
        "Hibernate": "2",
        "Shut down": "3"
    },
    "default": "Do nothing",
    "tooltip": "What happens when you close the laptop lid while plugged in.",
    "read_current_value": lambda: {
        0: "Do nothing",
        1: "Sleep",
        2: "Hibernate",
        3: "Shut down"
    }.get(read_powercfg_value("ac", "SUB_BUTTONS", "LIDACTION"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        "powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION " + val,
        "powercfg /S SCHEME_CURRENT"
    ])
    },
# End change what power buttons do
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
    "read_current_value": lambda: {
    0: "Disabled",
    1: "Enabled",
    2: "Aggressive",
    3: "Efficient Aggressive",
    4: "Efficient Enabled"
    }.get(read_powercfg_value("ac", "SUB_PROCESSOR", "PERFBOOSTMODE"), "[UNKNOWN]"),
    "apply": lambda val: run_powercfg_commands([
        f"powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE {val}",
        f"powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE {val}",
        "powercfg /S SCHEME_CURRENT"
    ])
    },
    {
    "name": "Enable Hibernate Option",
    "description": "Show Hibernate in Power Menu",
    "tooltip": "ON = Hibernate option will be visible in Start > Power menu.\nOFF = Hibernate will be hidden.",
    "type": "registry",
    "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FlyoutMenuSettings",
    "value": "ShowHibernateOption",
    "on": 1,
    "off": 0,
    "root": "HKEY_LOCAL_MACHINE",
    "default": 0,
    "create_if_missing": True,
    "category": "Power Tweaks"
    }
]


# -------------------------------
#  Merge for use in the app
# -------------------------------

TWEAKS = REGISTRY_TWEAKS + POWERCFG_TWEAKS
