from collections import OrderedDict

# --- Legend ---
# 
# -- Missions --
# ENT - Entropy Mission
# CSEC - CSEC Mission
# LABS - Labyrinths/Bibliotheque Mission
# VBIT - V/Bit Investigation Mission
# 
# -- Events --
# NAIX - Events relating to Naix
# STRK - Events relating to Striker
#
# -- Achievements --
# Achievements are marked with ACHV

# Locations:
# (Name, (Category (Entropy, CSEC, etc.), ID, is exclusive to Labyrinths, is an achievement, is unavoidable))
location_table = OrderedDict([

    # Entropy Missions
    ("ENT Intro / Confirmation", ("Entropy", 1, False, False, True)),
    ("ENT Intro / Welcome", ("Entropy", 2, False, False, True)),
    ("ENT PointClicker", ("Entropy", 3, False, False, False)),
    ("ENT The Famous Counter-Hack", ("Entropy", 4, False, False, False)),
    ("ENT Back to School", ("Entropy", 5, False, False, False)),
    ("ENT X-C Project", ("Entropy", 6, False, False, False)),
    ("ENT eOS Intro", ("Entropy", 7, False, False, True)),
    ("ENT Smash N' Grab", ("Entropy", 8, False, False, False)),
    ("ENT Naix", ("Entropy", 9, False, False, True)),

    # CSEC Missions
    ("CSEC Invitation OR /el Sec Completion", ("CSEC", 10, False, False, False)),
    ("CSEC CFC Herbs and Spices", ("CSEC", 11, False, False, True)),
    ("CSEC Rod of Asclepius", ("CSEC", 12, False, False, False)),
    ("CSEC Binary University", ("CSEC", 13, False, False, False)),
    ("CSEC Ghosting The Vault", ("CSEC", 14, False, False, False)),
    ("CSEC Imposters on Death Row", ("CSEC", 15, False, False, False)),
    ("CSEC Through the Spyglass", ("CSEC", 16, False, False, True)),
    ("CSEC Red Line", ("CSEC", 17, False, False, False)),
    ("CSEC Wipe Clean An Academic Record", ("CSEC", 18, False, False, False)),
    ("CSEC A Convincing Application", ("CSEC", 19, False, False, False)),
    ("CSEC Unjust Absence", ("CSEC", 20, False, False, False)),
    ("CSEC Decrypt A Secure Transmission", ("CSEC", 21, False, False, False)),
    ("CSEC Compromise an eOS Device", ("CSEC", 22, False, False, False)),
    ("CSEC Project Junebug", ("CSEC", 23, False, False, False)), # Players can exclude this location manually
    ("CSEC Start Bit Path", ("CSEC", 24, False, False, True)),

    # V/Bit Missions
    ("VBIT Foundation", ("VBit", 25, False, False, True)),
    ("VBIT Substantiation", ("VBit", 26, False, False, True)),
    ("VBIT Investigation", ("VBit", 27, False, False, True)),
    ("VBIT Propagation", ("VBit", 28, False, False, True)),
    ("VBIT Vindication", ("VBit", 29, False, False, True)),
    ("VBIT Termination / Sequencer", ("VBit", 30, False, False, True)),
    ("VBIT Reunion", ("VBit", 31, False, False, False)),

    ("VBIT Finish Sequencer", ("VBit", None, False, False, False)),

    # Labyrinths Missions
    ("LABS Finish Kaguya Trials", ("Labyrinths", 32, True, False, True)),
    ("LABS The Ricer", ("Labyrinths", 33, True, False, True)),
    ("LABS DDOSer On Critical Servers", ("Labyrinths", 34, True, False, True)),
    ("LABS It Follows", ("Labyrinths", 35, True, False, True)),
    ("LABS Bean Stalk", ("Labyrinths", 36, True, False, False)),
    ("LABS Expo Grave", ("Labyrinths", 37, True, False, False)),
    ("LABS The Keyboard Life", ("Labyrinths", 38, True, False, False)),
    ("LABS Hermetic Alchemists", ("Labyrinths", 39, True, False, True)),
    ("LABS Memory Forensics", ("Labyrinths", 40, True, False, True)),
    ("LABS Neopals", ("Labyrinths", 41, True, False, True)),
    ("LABS Striker's Stash", ("Labyrinths", 42, True, False, True)),
    ("LABS Take Flight", ("Labyrinths", 43, True, False, True)),
    ("LABS Take Flight Cont.", ("Labyrinths", 44, True, False, True)),
    ("LABS Altitude Loss", ("Labyrinths", 45, True, False, True)),

    # Post-Story Labs
    ("LABS Break Into Gibson", ("Labyrinths", 46, True, False, False)),
    ("CSEC Subvert Psylance Investigation", ("CSEC", 47, True, False, False)),

    # One-Off Events
    ("NAIX Recover", ("Entropy", 48, False, False, False)),
    ("STRK CoelTrain Recovery", ("Labyrinths", 49, True, False, True)),

    # Achievements
    ("ACHV Quickdraw", ("Achievements", 50, False, True, False)),
    ("ACHV To the Wire", ("Achievements", 51, False, True, False)),
    ("ACHV Makeover", ("Achievements", 52, False, True, False)),
    ("ACHV PointClicker", ("Achievements", 53, False, True, True)),
    ("ACHV You better not have clicked for those...", ("Achievements", 54, False, True, False)),
    ("ACHV Rude", ("Achievements", 55, False, True, False)),

    ("INTRO Complete Introduction", ("Intro", 56, False, False, True))

])