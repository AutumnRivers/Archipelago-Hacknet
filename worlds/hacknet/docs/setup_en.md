# Hacknet: Archipelago Setup
**Hacknet: Archipelago** is compatible with *Windows* and *Linux*, but does not natively support macOS/OSX.

## Installing Hacknet: Archipelago
**Hacknet: Pathfinder** is the mod loader that HacknetAP utilizes for modifying the game to make it compatible with Archipelago.

1. Download the [latest Pathfinder release](https://github.com/Arkhist/Hacknet-Pathfinder/releases/). (If on Windows, .exe installer recommended.)
2. When Pathfinder is successfully installed, [download the mod files](https://github.com/AutumnRivers/HacknetArchipelago/releases).
3. Extract the zip file into the `BepInEx/plugins` folder in your Hacknet root directory.

The final file structure should look like this:
```
└── Hacknet
    └── BepInEx
        └── plugins
            ├── assets
            │   └── aplogo.png
            ├── Archipelago.MultiClient.Net.dll
            ├── HacknetArchipelago.dll
            ├── PathfinderAPI.dll
            └── PathfinderUpdater.dll
```

## Logging into Archipelago
Launch into Hacknet with the mod and its files installed. On the main menu, you should now see a new section on the right with the Archipelago logo.

* `Archipelago Host` - The hostname for your session. For the most part, just leave this as `archipelago.gg`.
* `Archipelago Port` - The port of the session. If generating from the website, it'll be after the colon.
    * For example, the port of `archipelago.gg:38281` would be `38281`.
* `Archipelago Player Name` - The name of your slot, the one you defined in your player YAML.
* `Archipelago Room Pass` - If your room has a password, you'd put it here.

Hacknet's built-in textbox isn't the greatest, so keep in mind:

* Backspace won't do anything when held
* Caps Lock does not capitalize letters

After you've entered all the correct information, click on the "Connect to Archipelago" button.

If successful, you should see the logo change to green and display the text "Successfully connected to Archipelago" beneath.

If it failed to connect, you'll see the text "Failed to connect" and an error message in the terminal that launches with the game.

## Some things to remember
Non-modded saves are incompatible with this mod. If you're starting a new Archipelago session, you should start a new session in-game, too.

You can run `archistatus` in the terminal at any time to check your connection status to Archipelago.
