from worlds.generic.Rules import set_rule, add_rule, forbid_item, forbid_items, add_item_rule
from BaseClasses import MultiWorld

from .LocationList import location_table
from .Locations import HacknetLocation
from .Options import get_option_value, hacknet_options

# --------------------------------------------------- Rules ---------------------------------------------------
# Rules do not need to be repeated - if a user is in Entropy, it's assumed they already have FTP and SSHCrack
# (because the connection rule requires those), so there's no need to require FTP and SSH on *every* node that
# needs it in-game.
#
# Alternatively, missions should can_reach check against the earliest required mission. For example, "Smash n' Grab"
# in Entropy requires the eOS intro mission, so we require that. The eOS intro mission requires the user to be in
# Entropy, so we require the Entropy introduction missions instead of, say, PointClicker.
#
# This line of requiring previous nodes starts with Maiden Flight and ends with Bit -- Termination. If Labyrinths is
# enabled, it ends with Altitude Loss. The player will be plopped back into Entropy or CSEC and will return to the
# original questline with its original rules.

def set_rules(multiworld: MultiWorld, player: int) -> None:
    # Options
    shuffle_achievements = get_option_value(multiworld, player, "shuffle_achievements")
    include_labs = get_option_value(multiworld, player, "include_labyrinths")
    shuffle_postgame = get_option_value(multiworld, player, "shuffle_postgame")
    shuffle_nodes = get_option_value(multiworld, player, "shuffle_nodes")
    win_condition = get_option_value(multiworld, player, "victory_condition")

    # ----- Intro Rules -----
    # Tutorial -> Maiden Flight
    # First Contact & Getting Tools Together are skipped since they don't require any executables
    set_rule(multiworld.get_location("INTRO Maiden Flight", player),
        lambda state: state.has("SSHCrack", player) or state.has("FTPBounce", player)
        or state.has("FTPSprint", player) or state.has("SMTPOverflow", player)
        or state.has("WebServerWorm", player))

    # Maiden Flight -> Something In Return
    # No additional executables needed here, so we just link it to Maiden Flight
    set_rule(multiworld.get_location("INTRO Something In Return", player),
    lambda state: multiworld.get_location("INTRO Maiden Flight", player).can_reach(state))

    # Something In Return -> Where To From Here (Entropy Intro)
    set_rule(multiworld.get_location("INTRO Complete Introduction", player),
    lambda state: multiworld.get_location("INTRO Something In Return", player).can_reach(state))

    # ----- Entropy Rules -----
    # Assumed Current Executables: SSHCrack, FTPBounce/FTPSprint
    # Introduction Complete -> Intro / Confirmation
    set_rule(multiworld.get_location("ENT Intro / Confirmation", player),
    lambda state: multiworld.get_location("INTRO Complete Introduction", player).can_reach(state))

    # Intro / Confirmation -> Entropy Mission Sets
    # We skip Intro / Welcome since it's a freebie and only requires the user to log in with an admin account
    # (One that is given to them)
    set_rule(multiworld.get_location("ENT PointClicker", player),
    lambda state: multiworld.get_location("ENT Intro / Confirmation", player).can_reach(state))

    set_rule(multiworld.get_location("ENT The Famous Counter-Hack", player),
    lambda state: multiworld.get_location("ENT Intro / Confirmation", player).can_reach(state))

    set_rule(multiworld.get_location("ENT Back to School", player),
    lambda state: multiworld.get_location("ENT Intro / Confirmation", player).can_reach(state))

    set_rule(multiworld.get_location("ENT X-C Project", player),
    lambda state: multiworld.get_location("ENT Intro / Confirmation", player).can_reach(state))

    # Intro / Confirmation -> Entropy eOS Intro
    # Required Executables: eosDeviceScan
    set_rule(multiworld.get_location("ENT eOS Intro", player),
    lambda state: multiworld.get_location("ENT Intro / Confirmation", player).can_reach(state)
    and state.has("eosDeviceScan", player))

    # Entropy eOS Intro -> Smash N' Grab
    set_rule(multiworld.get_location("ENT Smash N' Grab", player),
    lambda state: multiworld.get_location("ENT eOS Intro", player).can_reach(state))

    # Entropy eOS Intro -> Naix (Entropy End)
    # Required Executables: SMTPOverflow
    set_rule(multiworld.get_location("ENT Naix", player),
    lambda state: multiworld.get_location("ENT eOS Intro", player).can_reach(state)
    and state.has("SMTPOverflow", player) and 
    (state.has("FTPBounce", player) or state.has("FTPSprint", player)))

    # Naix -> Naix Recovery
    # (Technically any time the player loses their x-server, reboots, then gains another one)
    set_rule(multiworld.get_location("NAIX Recover", player),
    lambda state: multiworld.get_location("ENT Naix", player).can_reach(state))

    # Naix -> CSEC Intro
    # Required Executables: WebServerWorm, SQL_MemCorrupt
    set_rule(multiworld.get_location("CSEC Invitation OR /el Sec Completion", player),
    lambda state: multiworld.get_location("ENT Naix", player).can_reach(state)
    and state.has("WebServerWorm", player) and state.has("SQL_MemCorrupt", player))

    # ----- CSEC Rules -----
    # CSEC Intro -> CSEC Set
    # No extra executables... yet.
    set_rule(multiworld.get_location("CSEC Rod of Asclepius", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Binary University", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Imposters on Death Row", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Red Line", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Wipe Clean An Academic Record", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Unjust Absence", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Compromise an eOS Device", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

    # CSEC Intro -> Through The Spyglass
    # Required Executables: Decypher, DECHead
    set_rule(multiworld.get_location("CSEC Through the Spyglass", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state)
    and state.has("Decypher", player) and state.has("DECHead", player))

    # CSEC Start Bit Path
    # Technically this can happen *before* Through the Spyglass...
    # But this is just to be safe.
    set_rule(multiworld.get_location("CSEC Start Bit Path", player),
    lambda state: multiworld.get_location("CSEC Through the Spyglass", player).can_reach(state))

    # CSEC Intro -> Ghosting The Vault
    # Required Executables: Decypher
    set_rule(multiworld.get_location("CSEC Ghosting The Vault", player),
    lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state)
    and state.has("Decypher", player))

    # CSEC Intro -> CSEC Encryption Set
    # Earliest Required Mission: Through the Spyglass
    set_rule(multiworld.get_location("CSEC A Convincing Application", player),
    lambda state: multiworld.get_location("CSEC Through the Spyglass", player).can_reach(state))

    set_rule(multiworld.get_location("CSEC Decrypt A Secure Transmission", player),
    lambda state: multiworld.get_location("CSEC Through the Spyglass", player).can_reach(state))

    # Through The Spyglass -> Project Junebug
    # Required Executables: KBTPortTest
    set_rule(multiworld.get_location("CSEC Project Junebug", player),
    lambda state: multiworld.get_location("CSEC Through the Spyglass", player).can_reach(state)
    and state.has("KBTPortTest", player))

    # Project Junebug can be denied by the player if they are uncomfortable with the mission.
    # It is assumed, in this case, that the player would add Project Junebug to their Excluded Locations

    # Through the Spyglass -> Bit -- Foundation
    # Starting the Bit Path - this is linear.
    # Required Executables: None (KBT isn't needed until Termination) but we'll add KBT anyway
    set_rule(multiworld.get_location("VBIT Foundation", player),
    lambda state: multiworld.get_location("CSEC Start Bit Path", player).can_reach(state)
    and state.has("KBTPortTest", player))

    # ----- V/Bit Rules -----
    # Foundation -> Substantiation
    set_rule(multiworld.get_location("VBIT Substantiation", player),
    lambda state: multiworld.get_location("VBIT Foundation", player).can_reach(state))

    # Substantiation -> Investigation
    set_rule(multiworld.get_location("VBIT Investigation", player),
    lambda state: multiworld.get_location("VBIT Substantiation", player).can_reach(state))

    # Investigation -> Propogation
    set_rule(multiworld.get_location("VBIT Propagation", player),
    lambda state: multiworld.get_location("VBIT Investigation", player).can_reach(state))

    # Propogation -> Vindication
    set_rule(multiworld.get_location("VBIT Vindication", player),
    lambda state: multiworld.get_location("VBIT Propagation", player).can_reach(state))

    # Vindication -> Termination
    set_rule(multiworld.get_location("VBIT Termination / Sequencer", player),
    lambda state: multiworld.get_location("VBIT Vindication", player).can_reach(state))

    # Termination -> Finish Sequencer
    if win_condition == 1 or win_condition == 4:
        set_rule(multiworld.get_location("VBIT Finish Sequencer", player),
        lambda state: multiworld.get_location("VBIT Termination / Sequencer", player).can_reach(state))

    # Post-Game Rules
    if shuffle_postgame is True:
        # Reunion
        set_rule(multiworld.get_location("VBIT Reunion", player),
        lambda state: multiworld.get_location("VBIT Termination / Sequencer", player).can_reach(state))

    # Node Rules
    if shuffle_nodes is True:
        # Intro
        set_rule(multiworld.get_location("NODE Entropy Asset Cache", player),
        lambda state: state.has("SSHCrack", player) or state.has("FTPBounce", player)
        or state.has("FTPSprint", player) or state.has("SMTPOverflow", player)
        or state.has("WebServerWorm", player))

        # CSEC
        set_rule(multiworld.get_location("NODE CCC Hacksquad Dump", player),
        lambda state: multiworld.get_location("CSEC Invitation OR /el Sec Completion", player).can_reach(state))

        # Timekeeper
        set_rule(multiworld.get_location("NODE Timekeeper's Vault", player),
        lambda state: (state.has("FTPBounce", player) or state.has("FTPSprint", player))
        and state.has("SSHCrack", player) and state.has("SMTPOverflow", player)
        and state.has("WebServerWorm", player))

        # Polar Stars - /el Sec
        set_rule(multiworld.get_location("NODE Polar Star / Trial of Patience", player),
        lambda state: multiworld.get_location("ENT Naix", player).can_reach(state)
        and state.has("WebServerWorm", player))

        set_rule(multiworld.get_location("NODE Polar Star / Trial of Haste", player),
        lambda state: multiworld.get_location("ENT Naix", player).can_reach(state)
        and state.has("WebServerWorm", player))

        set_rule(multiworld.get_location("NODE Polar Star / Trial of Focus", player),
        lambda state: multiworld.get_location("ENT Naix", player).can_reach(state)
        and state.has("WebServerWorm", player))

        set_rule(multiworld.get_location("NODE Polar Star / Trial of Dilligence", player),
        lambda state: multiworld.get_location("ENT Naix", player).can_reach(state)
        and state.has("WebServerWorm", player))

    # Item Rules (Traps, mostly)
    for locat in multiworld.get_region("Entropy", player).locations:
        forbid_item(locat, "ETASTrap", player)

    for locat in multiworld.get_region("Menu", player).locations:
        forbid_item(locat, "ETASTrap", player)

def set_labs_rules(multiworld: MultiWorld, player: int) -> None:
    # Options
    shuffle_achievements = get_option_value(multiworld, player, "shuffle_achievements")
    include_labs = get_option_value(multiworld, player, "include_labyrinths")
    shuffle_postgame = get_option_value(multiworld, player, "shuffle_postgame")
    shuffle_nodes = get_option_value(multiworld, player, "shuffle_nodes")
    win_condition = get_option_value(multiworld, player, "victory_condition")

    # ----- Labyrinths Rules -----
    # Entropy eOS Intro OR CSEC -> Kaguya Trials
    # Required Executables: TorrentStreamInjector (it is assumed the player already has an FTP cracker)
    set_rule(multiworld.get_location("LABS Finish Kaguya Trials", player),
    lambda state: (multiworld.get_location("ENT eOS Intro", player).can_reach(state)
    or multiworld.get_location("CSEC Rod of Asclepius", player).can_reach(state))
    and state.has("TorrentStreamInjector", player))

    # Kaguya Trials -> The Ricer
    # Required Executables: None
    set_rule(multiworld.get_location("LABS The Ricer", player),
    lambda state: multiworld.get_location("LABS Finish Kaguya Trials", player).can_reach(state))

    # The Ricer -> DDoS
    # Required Executables: SSLTrojan
    set_rule(multiworld.get_location("LABS DDOSer On Critical Servers", player),
    lambda state: multiworld.get_location("LABS The Ricer", player).can_reach(state)
    and state.has("SSLTrojan", player))

    # DDoS -> Alchemists
    # Required Executables: None
    set_rule(multiworld.get_location("LABS Hermetic Alchemists", player),
    lambda state: multiworld.get_location("LABS DDOSer On Critical Servers", player).can_reach(state))

    # Alchemists -> Memory Forensics
    # Required Executables: MemForensics, MemDumpGenerator
    set_rule(multiworld.get_location("LABS Memory Forensics", player),
    lambda state: multiworld.get_location("LABS Hermetic Alchemists", player).can_reach(state)
    and state.has("MemForensics", player) and state.has("MemDumpGenerator", player))

    # Memory Forensics -> Striker
    # Required Executables: SignalScrambler
    set_rule(multiworld.get_location("LABS Striker's Stash", player),
    lambda state: multiworld.get_location("LABS Memory Forensics", player).can_reach(state)
    and state.has("SignalScrambler", player))

    # Striker -> CoelTrain Recovery
    set_rule(multiworld.get_location("STRK CoelTrain Recovery", player),
    lambda state: multiworld.get_location("LABS Striker's Stash", player).can_reach(state))

    # Striker -> Set 3 (/Content/DLC/Set/3)
    # Required Executables: None! And there won't be any until Take Flight
    set_rule(multiworld.get_location("LABS Set 3", player),
    lambda state: multiworld.get_location("LABS Striker's Stash", player).can_reach(state))

    # Set 3 -> Neopals
    set_rule(multiworld.get_location("LABS Neopals", player),
    lambda state: multiworld.get_location("LABS Set 3", player).can_reach(state))

    # Neopals -> Set 4
    set_rule(multiworld.get_location("LABS Set 4", player),
    lambda state: multiworld.get_location("LABS Neopals", player).can_reach(state))

    # Set 4 -> Take Flight
    # Required Executables: PacificPortcrusher
    set_rule(multiworld.get_location("LABS Take Flight", player),
    lambda state: multiworld.get_location("LABS Set 4", player).can_reach(state)
    and state.has("PacificPortcrusher", player))

    # Take Flight -> Take Flight Contd.
    set_rule(multiworld.get_location("LABS Take Flight Cont.", player),
    lambda state: multiworld.get_location("LABS Take Flight", player).can_reach(state))

    # Take Flight Contd. -> Altitude Loss (Finale Sequence)
    set_rule(multiworld.get_location("LABS Altitude Loss", player),
    lambda state: multiworld.get_location("LABS Take Flight Cont.", player).can_reach(state))

    # Altitude Loss -> Labyrinths Credits
    if win_condition == 2 or win_condition == 4:
        set_rule(multiworld.get_location("LABS Remote Shutdown", player),
        lambda state: multiworld.get_location("LABS Altitude Loss", player).can_reach(state))
    
    # ----- Labyrinths Post-Game Rules -----
    if shuffle_postgame:
        # CSEC Post-Labs
        set_rule(multiworld.get_location("CSEC Subvert Psylance Investigation", player),
        lambda state: multiworld.get_location("LABS Altitude Loss", player).can_reach(state)
        and multiworld.get_location("CSEC Through the Spyglass", player).can_reach(state))

        # The Gibson
        # Required Executables: Literally all of the port crackers
        # It is assumed the player already has:
        # FTP, SSH, Torrent, SSL, and Pacific.
        # So the player needs:
        # Web, SQL, KBT
        # That's actually not as many as I thought...
        set_rule(multiworld.get_location("LABS Break Into Gibson", player),
        lambda state: multiworld.get_location("LABS Altitude Loss", player).can_reach(state)
        and multiworld.get_location("CSEC Start Bit Path", player).can_reach(state)
        and state.has("WebServerWorm", player) and state.has("SQL_MemCorrupt", player)
        and state.has("KBTPortTest", player))

        if(win_condition >= 3):
            set_rule(multiworld.get_location("LABS Broke Into Gibson", player),
            lambda state: multiworld.get_location("LABS Break Into Gibson", player).can_reach(state))

    # ----- Labyrinths-related Node Rules -----
    if shuffle_nodes is True:
        set_rule(multiworld.get_location("NODE Coel_Gateway", player),
        lambda state: multiworld.get_location("LABS Altitude Loss", player).can_reach(state))

        set_rule(multiworld.get_location("NODE Pellium Box", player),
        lambda state: multiworld.get_location("ENT Naix", player).can_reach(state)
        and state.has("MemDumpGenerator", player) and state.has("MemForensics", player))

    # ----- Don't place Labyrinths programs in CSEC/VBIT -----
    labs_programs = [
        "TorrentStreamInjector", "SSLTrojan", "SignalScrambler", "PacificPortcrusher",
        "MemDumpGenerator", "MemForensics"
    ]

    for locat in multiworld.get_region("CSEC", player).locations:
        forbid_items(locat, labs_programs)

    for locat in multiworld.get_region("VBit", player).locations:
        forbid_items(locat, labs_programs)

def set_achv_rules(multiworld: MultiWorld, player: int) -> None:
    # Options
    shuffle_executables = get_option_value(multiworld, player, "shuffle_executables")

    # Makeover
    set_rule(multiworld.get_location("ACHV Makeover", player),
    lambda state: (state.has("ThemeChanger", player) or shuffle_executables >= 2)
    and multiworld.get_location("ENT Intro / Welcome", player).can_reach(state))

    # PointClicker-related achievements
    set_rule(multiworld.get_location("ACHV PointClicker", player),
    lambda state: multiworld.get_location("ENT PointClicker", player).can_reach(state))

    set_rule(multiworld.get_location("ACHV You better not have clicked for those...", player),
    lambda state: multiworld.get_location("ENT PointClicker", player).can_reach(state))

    # Rude
    set_rule(multiworld.get_location("ACHV Rude", player),
    lambda state: multiworld.get_location("NAIX Recover", player).can_reach(state))