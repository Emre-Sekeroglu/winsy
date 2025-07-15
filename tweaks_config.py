# -------------------------------
# 💾 REGISTRY TWEAKS
# -------------------------------

REGISTRY_TWEAKS = [

    {
        "name":        "Show Advanced Power Settings",
        "description": "Show advanced power settings in Control Panel",
        "tooltip":     "ON = extra options in advanced power settings",
        "path":  r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings"
                 r"\54533251-82be-4824-96c1-47b60b740d00"
                 r"\be337238-0d82-4146-a960-4f3749d470c7",
        "value": "Attributes",
        "on":    2,
        "off":   1,
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
    }

]

# -------------------------------
# ⚡ POWERCFG TWEAKS
# -------------------------------

POWERCFG_TWEAKS = [

    {
        "name":        "Optimal Minimum & Maximum Power",
        "type":        "powercfg",
        "description": "Sets CPU min 5% on AC+DC, max 100 %, and disables boost.",
        "tooltip":     "Enabling this tweak will set the CPU minimum to 5% on both AC and DC power, maximum to 100%, and disable the hidden overclock feature which is set 'aggresive' in your settings on windows by default!. Trust me, enable this. It doesn't help FPS by any means, It makes your PC run loud when idle, It just makes your CPU go crazy even if it doesn't need to all the time.",
        "category":    "Power Tweaks",

        # >>> START OF FIXED COMMANDS
        "on_cmds": [
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 0",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 0",
            "powercfg /S SCHEME_CURRENT"
        ],

        "off_cmds": [
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 80",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 2",
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR be337238-0d82-4146-a960-4f3749d470c7 2",
            "powercfg /S SCHEME_CURRENT"
        ]
        # <<< END OF FIXED COMMANDS
    }

]

# -------------------------------
# 🔗 Merge for use in the app
# -------------------------------

TWEAKS = REGISTRY_TWEAKS + POWERCFG_TWEAKS
