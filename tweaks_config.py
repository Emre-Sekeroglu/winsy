# -------------------------------
# REGISTRY TWEAKS
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
            "powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 0",
            "powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 0"
        ],
        "tooltip": "Sets min CPU at 5% and max at 100% for both plugged and battery modes. Improves responsiveness without boosting."
    },
    {
        "description": "CPU Boost Mode",
        "category": "Power Tweaks",
        "type": "powercfg_dropdown",
        "setting_guid": "be337238-0d82-4146-a960-4f3749d470c7",
        "tooltip": "Controls how aggressively your CPU boosts performance.\n\n0 = Disabled\n1 = Enabled\n2 = Aggressive\n3 = Efficient Aggressive\n4 = Efficient Enabled"
    }
]


# -------------------------------
#  Merge for use in the app
# -------------------------------

TWEAKS = REGISTRY_TWEAKS + POWERCFG_TWEAKS
