import typing

from BaseClasses import Location, LocationProgressType

junebug_mission_id = 32
junebug_node_ids = (
    200, 201,
    202, 202
)

class HacknetLocData(typing.NamedTuple):
    id: int | None
    region: str
    display_name: str
    is_dlc: bool
    is_ptc: typing.Optional[bool] = False # ptc = PointClicker, default to false

class HacknetLocation(Location):
    game: str = "Hacknet"

    def __init__(self, player, name, data, region):
        self.player = player
        self.name = name
        self.address = data[0]
        self.raw_region = region

        self.parent_region = None

mission_table = [
    HacknetLocData(300, "Menu", "Intro -- First Contact", False, False),
    HacknetLocData(1, "Intro", "Intro -- Maiden Flight", False, False),
    HacknetLocData(2, "Intro", "Intro -- Something in return", False, False),
    HacknetLocData(3, "Intro", "Intro -- Where to from here", False, False),
    HacknetLocData(4, "Menu", "Intro -- Getting some tools together", False, False),
    HacknetLocData(5, "Intro", "Entropy -- Confirmation Mission", False, False),
    HacknetLocData(6, "Intro", "Entropy -- Welcome", False, False),

    # Entropy
    HacknetLocData(10, "Entropy", "Entropy -- PointClicker (Mission)", False, False),
    HacknetLocData(11, "Entropy", "Entropy -- The famous counter-hack", False, False),
    HacknetLocData(12, "Entropy", "Entropy -- Back to School", False, False),
    HacknetLocData(13, "Entropy", "Entropy -- X-C Project", False, False),
    HacknetLocData(14, "Entropy", "Entropy -- Smash N' Grab", False, False),
    HacknetLocData(15, "Entropy", "Entropy -- eOS Device Scanning", False, False),
    HacknetLocData(16, "Entropy - Naix", "Entropy -- Naix", False, False),
    HacknetLocData(None, "Entropy", "Complete Every Entropy Mission", False, False),

    # /el
    HacknetLocData(301, "/el Sec - Naix", "Naix -- Deface Nortron Website", False, False),
    HacknetLocData(302, "/el Sec - Naix", "Naix -- Nortron Security Mainframe", False, False),
    HacknetLocData(303, "/el Sec - Polar Star", "/el -- Head of Polar Star (Download Files)", False,
                   False),

    # CSEC
    HacknetLocData(20, "CSEC - Intro", "CSEC -- CFC Herbs & Spices", False, False),
    HacknetLocData(21, "CSEC", "CSEC -- Investigate a medical record", False, False),
    HacknetLocData(22, "CSEC", "CSEC -- Teach an old dog new tricks", False, False),
    HacknetLocData(23, "CSEC - DEC", "CSEC -- Locate or Create Decryption Software", False, False),
    HacknetLocData(24, "CSEC", "CSEC -- Remove a Fabricated Death Row Record", False, False),
    HacknetLocData(25, "CSEC - DEC", "CSEC -- Track an Encrypted File", False, False),
    HacknetLocData(26, "CSEC", "CSEC -- Check out a suspicious server", False, False),
    HacknetLocData(27, "CSEC", "CSEC -- Wipe clean an academic record", False, False),
    HacknetLocData(28, "CSEC", "CSEC -- Help an aspiring writer", False, False),
    HacknetLocData(29, "CSEC", "CSEC -- Add a Death Row record for a family member", False, False),
    HacknetLocData(30, "CSEC - DEC", "CSEC -- Decrypt a secure transmission", False, False),
    HacknetLocData(31, "CSEC", "CSEC -- Compromise an eOS Device", False, False),
    HacknetLocData(32, "CSEC - Project Junebug", "CSEC -- Project Junebug", False, False),
    HacknetLocData(33, "CSEC - Bit", "CSEC -- Investigate a CSEC member's disappearance", False, False),
    HacknetLocData(None, "CSEC", "Complete Every CSEC Mission", False, False),
    HacknetLocData(None, "CSEC", "Join CSEC", False, False),

    # V/Bit/Finale
    HacknetLocData(40, "Finale", "Bit -- Foundation", False, False),
    HacknetLocData(41, "Finale", "Bit -- Substantiation", False, False),
    HacknetLocData(42, "Finale", "Bit -- Investigation", False, False),
    HacknetLocData(43, "Finale", "Bit -- Propagation", False, False),
    HacknetLocData(44, "Finale", "Bit -- Termination", False, False),
    HacknetLocData(None, "Finale", "Stop PortHack.Heart", False, False),

    # Labyrinths
    # These are each given their own regions for purpose of grouping them with admin access checks
    HacknetLocData(50, "Labyrinths - Kaguya Trials", "Labyrinths -- Kaguya Trials", True, False),
    HacknetLocData(51, "Labyrinths - Set 1", "Labyrinths -- The Ricer", True, False),
    HacknetLocData(52, "Labyrinths - Set 2", "Labyrinths -- DDOSer on some critical servers", True,
                   False),
    HacknetLocData(53, "Labyrinths - Set 3", "Labyrinths -- Cleanup/It Follows", True, False),
    HacknetLocData(54, "Labyrinths - Set 4", "Labyrinths -- Bean Stalk/Expo Grave/The Keyboard Life",
                   True, False),
    HacknetLocData(55, "Labyrinths - Neopals", "Labyrinths -- Neopals", True, False),
    HacknetLocData(56, "Labyrinths - Memory Forensics", "Labyrinths -- Memory Forensics", True, False),
    HacknetLocData(57, "Labyrinths - Striker", "Labyrinths -- Striker's Stash", True, False),
    HacknetLocData(58, "Labyrinths - Hermetic Alchemists", "Labyrinths -- Hermetic Alchemists", True,
                   False),
    HacknetLocData(59, "Labyrinths - Take Flight", "Labyrinths -- Take Flight", True, False),
    HacknetLocData(60, "Labyrinths - Altitude Loss", "Labyrinths -- Take Flight Cont.", True, False),
    HacknetLocData(61, "Labyrinths - Altitude Loss", "Labyrinths -- Altitude Loss", True, False),
    HacknetLocData(62, "Post-Labyrinths", "CSEC -- Subvert Psylance Investigation", True, False),

    HacknetLocData(None, "Labyrinths - Altitude Loss", "Watched Labyrinths Credits", True, False),
    HacknetLocData(None, "Post-Labyrinths", "Broke Into The Gibson", True, False)
]

pointclicker_table = [
    # Upgrades
    HacknetLocData(70, "PointClicker", "PointClicker -- Click Me!", False, True),
    HacknetLocData(71, "PointClicker", "PointClicker -- Autoclicker v1", False, True),
    HacknetLocData(72, "PointClicker", "PointClicker -- Autoclicker v2", False, True),
    HacknetLocData(73, "PointClicker", "PointClicker -- Pointereiellion", False, True),
    HacknetLocData(74, "PointClicker", "PointClicker -- Upgrade 4", False, True),
    HacknetLocData(75, "PointClicker", "PointClicker -- Upgrade 5", False, True),
    HacknetLocData(76, "PointClicker", "PointClicker -- Upgrade 6", False, True),
    HacknetLocData(77, "PointClicker", "PointClicker -- Upgrade 7", False, True),
    HacknetLocData(78, "PointClicker", "PointClicker -- Upgrade 8", False, True),
    HacknetLocData(79, "PointClicker", "PointClicker -- Upgrade 9", False, True),
    HacknetLocData(80, "PointClicker", "PointClicker -- Upgrade 10", False, True),
    HacknetLocData(81, "PointClicker", "PointClicker -- Upgrade 11", False, True),
    HacknetLocData(82, "PointClicker", "PointClicker -- Upgrade 12", False, True),
    HacknetLocData(83, "PointClicker", "PointClicker -- Upgrade 13", False, True),
    HacknetLocData(84, "PointClicker", "PointClicker -- Upgrade 14", False, True),
    HacknetLocData(85, "PointClicker", "PointClicker -- Upgrade 15", False, True),
    HacknetLocData(86, "PointClicker", "PointClicker -- Upgrade 16", False, True),
    HacknetLocData(87, "PointClicker", "PointClicker -- Upgrade 17", False, True),
    HacknetLocData(88, "PointClicker", "PointClicker -- Upgrade 18", False, True),
    HacknetLocData(89, "PointClicker", "PointClicker -- Upgrade 19", False, True),
    HacknetLocData(90, "PointClicker", "PointClicker -- Upgrade 20", False, True),
    HacknetLocData(91, "PointClicker", "PointClicker -- Upgrade 21", False, True),
    HacknetLocData(92, "PointClicker", "PointClicker -- Upgrade 22", False, True),
    HacknetLocData(93, "PointClicker", "PointClicker -- Upgrade 23", False, True),
    HacknetLocData(94, "PointClicker", "PointClicker -- Upgrade 24", False, True),
    HacknetLocData(95, "PointClicker", "PointClicker -- Upgrade 25", False, True),
    HacknetLocData(96, "PointClicker", "PointClicker -- Upgrade 26", False, True),
    HacknetLocData(97, "PointClicker", "PointClicker -- Upgrade 27", False, True),
    HacknetLocData(98, "PointClicker", "PointClicker -- Upgrade 28", False, True),
    HacknetLocData(99, "PointClicker", "PointClicker -- Upgrade 29", False, True),
    HacknetLocData(100, "PointClicker", "PointClicker -- Upgrade 30", False, True),
    HacknetLocData(101, "PointClicker", "PointClicker -- Upgrade 31", False, True),
    HacknetLocData(102, "PointClicker", "PointClicker -- Upgrade 32", False, True),
    HacknetLocData(103, "PointClicker", "PointClicker -- Upgrade 33", False, True),
    HacknetLocData(104, "PointClicker", "PointClicker -- Upgrade 34", False, True),
    HacknetLocData(105, "PointClicker", "PointClicker -- Upgrade 35", False, True),
    HacknetLocData(106, "PointClicker", "PointClicker -- Upgrade 36", False, True),
    HacknetLocData(107, "PointClicker", "PointClicker -- Upgrade 37", False, True),
    HacknetLocData(108, "PointClicker", "PointClicker -- Upgrade 38", False, True),
    HacknetLocData(109, "PointClicker", "PointClicker -- Upgrade 39", False, True),
    HacknetLocData(110, "PointClicker", "PointClicker -- Upgrade 40", False, True),
    HacknetLocData(111, "PointClicker", "PointClicker -- Upgrade 41", False, True),
    HacknetLocData(112, "PointClicker", "PointClicker -- Upgrade 42", False, True),
    HacknetLocData(113, "PointClicker", "PointClicker -- Upgrade 43", False, True),
    HacknetLocData(114, "PointClicker", "PointClicker -- Upgrade 44", False, True),
    HacknetLocData(115, "PointClicker", "PointClicker -- Upgrade 45", False, True),
    HacknetLocData(116, "PointClicker", "PointClicker -- Upgrade 46", False, True),
    HacknetLocData(117, "PointClicker", "PointClicker -- Upgrade 47", False, True),
    HacknetLocData(118, "PointClicker", "PointClicker -- Upgrade 48", False, True),
    HacknetLocData(119, "PointClicker", "PointClicker -- Upgrade 49", False, True),
    HacknetLocData(120, "PointClicker", "PointClicker -- Upgrade 50", False, True)
]

achievements_table = [
    HacknetLocData(130, "Menu", "Achievement -- Quickdraw", False, False),
    HacknetLocData(131, "Entropy", "Achievement -- To the Wire", False, False),
    HacknetLocData(132, "CSEC", "Achievement -- Makeover!", False, False),
    HacknetLocData(133, "Entropy", "Achievement -- Join Entropy", False, False),
    HacknetLocData(134, "CSEC", "Achievement -- Join CSEC", False, False),
    HacknetLocData(135, "/el Sec - Polar Star", "Achievement -- TRUE ULTIMATE POWER!", False, False),
    HacknetLocData(136, "/el Sec - Polar Star", "Achievement -- Rude//el Sec Champion", False, False),
    HacknetLocData(137, "Entropy", "Achievement -- PointClicker", False, False),
    HacknetLocData(138, "Entropy", "Achievement -- You better not have clicked for those...",
                   False, False)
]

node_admin_table = [
    # oh boy here we go
    HacknetLocData(140, "Menu", "Intro -- Player's PC", False), # basically a freebie, fires after tutorial is finished
    HacknetLocData(157, "Menu", "Intro -- Archipelago IRC", False),
    HacknetLocData(141, "Intro", "Intro -- Bitwise Test PC", False),
    HacknetLocData(142, "Intro", "Intro -- P. Anderson's Bedroom PC", False),
    HacknetLocData(143, "Intro", "Intro -- Entropy test Server", False), # Not a typo
    HacknetLocData(144, "Intro", "Intro -- Viper-Battlestation", False),
    HacknetLocData(284, "Intro", "Intro -- Entropy Asset Cache", False),
    HacknetLocData(145, "Intro", "Entropy -- Slash-Bot News Network", False),

    # Entropy
    HacknetLocData(146, "Entropy", "Entropy -- Entropy Asset Server", False),
    HacknetLocData(147, "Entropy", "Entropy -- Milburg High IT Office", False),
    HacknetLocData(148, "Entropy", "Entropy -- PointClicker (Admin Access)", False),
    HacknetLocData(149, "Entropy", "Entropy -- PP Marketing Inc.", False),
    HacknetLocData(150, "Entropy", "Entropy -- X-C Project Tablet#001//RESEARCH", False),
    HacknetLocData(151, "Entropy", "Entropy -- Jason's PowerBook Plus", False),
    HacknetLocData(152, "Entropy", "Entropy -- JDel Home PC", False),
    HacknetLocData(153, "Entropy", "Entropy -- Jacob's ePhone 4", False),
    HacknetLocData(154, "Entropy - Naix", "Entropy -- Naix Root Gateway", False),
    HacknetLocData(155, "Entropy - Naix", "Entropy -- Proxy_Node-X22", False),
    HacknetLocData(156, "Entropy - Naix", "Entropy -- Proxy_Node-X04", False),

    # Naix/el
    HacknetLocData(160, "/el Sec - Naix", "Naix -- Nortron Security Web Server", False),
    HacknetLocData(161, "/el Sec - Naix", "Naix -- Nortron Internal Services Server", False),
    HacknetLocData(162, "/el Sec - Naix", "Naix -- Nortron Mainframe", False),
    # Nortron Mail is skipped since you're not meant to get into it...

    # This has its region set to Finale since it needs finale portcrackers
    HacknetLocData(163, "Finale", "/el -- /el Message Board", False),
    HacknetLocData(164, "/el Sec - SecuLock", "/el -- COME AT ME /EL's Secure SecuLock Drive", False),
    HacknetLocData(165, "/el Sec - SecuLock", "/el -- Stormrider", False),

    # Polar Star
    HacknetLocData(166, "/el Sec - Polar Star", "/el -- Shrine of the Polar Star", False),
    HacknetLocData(167, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Patience", False),
    HacknetLocData(168, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Haste", False),
    HacknetLocData(169, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Diligence", False),
    HacknetLocData(170, "/el Sec - Polar Star", "/el -- Tail of Diligence", False),
    HacknetLocData(171, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Focus", False),
    HacknetLocData(172, "/el Sec - Polar Star", "/el -- Head of the Polar Star (Admin Access)", False),
    # This has its region set to CSEC since it needs SQL_MemCorrupt
    # Logically, the player could also get it before this via Labyrinths, but, eh...
    HacknetLocData(173, "CSEC", "/el -- Timekeeper's Vault", False),

    # CSEC
    HacknetLocData(180, "CSEC", "CSEC -- www.cfc.com", False),
    HacknetLocData(181, "CSEC", "CSEC -- CFC Corporate Mainframe", False),
    HacknetLocData(182, "CSEC", "CSEC -- CFC Records Repository", False),
    HacknetLocData(183, "CSEC", "CSEC -- CSEC Crossroads Server", False),
    HacknetLocData(184, "CSEC", "CSEC -- CSEC Public Drop Server", False),
    HacknetLocData(185, "CSEC", "CSEC -- Sal_Home_Workstation", False),
    HacknetLocData(186, "CSEC", "CSEC -- CCC Hacksquad Filedump", False),
    HacknetLocData(187, "CSEC", "CSEC -- Jason's LackBook Pro", False),
    HacknetLocData(188, "CSEC", "CSEC -- Death Row Records Database", False),
    HacknetLocData(189, "CSEC", "CSEC -- International Academic Database", False),
    HacknetLocData(190, "CSEC", "CSEC -- Universal Medical", False),
    HacknetLocData(191, "CSEC - DEC", "CSEC -- DEC Solutions Mainframe", False),
    HacknetLocData(192, "CSEC - DEC", "CSEC -- DEC Solutions Web Server", False),
    HacknetLocData(193, "CSEC - DEC", "CSEC -- Joseph Scott's Battlestation", False),
    HacknetLocData(194, "CSEC - DEC", "CSEC -- Macrosoft Workhorse Server 04", False),
    HacknetLocData(195, "CSEC", "CSEC -- CSEC (Contracts Server)", False),

    # CSEC/Project Junebug
    HacknetLocData(200, "CSEC - Project Junebug", "CSEC -- Eidolon Soft Production Server", False),
    HacknetLocData(201, "CSEC - Project Junebug", "CSEC -- KBT-PM 2.44 REG#10811", False),
    HacknetLocData(202, "CSEC - Project Junebug", "CSEC -- Kellis Biotech Client Services", False),
    HacknetLocData(203, "CSEC - Project Junebug", "CSEC -- Kellis Biotech Production Asset Server",
                   False),

    # CSEC/Bit
    HacknetLocData(204, "CSEC - Bit", "CSEC -- Bitwise Drop Server", False),
    HacknetLocData(205, "CSEC - Bit", "CSEC -- Bitwise Relay 01", False),

    # Bit/Finale
    HacknetLocData(210, "Finale", "Bit -- Bitwise Repo Base", False),
    HacknetLocData(211, "Finale", "Bit -- EnTech External Contractor Relay Server", False),
    HacknetLocData(212, "Finale", "Bit -- EnTech Web Server", False),
    HacknetLocData(213, "Finale", "Bit -- En_Prometheus", False),
    HacknetLocData(214, "Finale", "Bit -- En_Romulus", False),
    HacknetLocData(215, "Finale", "Bit -- EnWorkstationCore", False),
    HacknetLocData(216, "Finale", "Bit -- EnTech Workstation _008", False),
    HacknetLocData(217, "Finale", "Bit -- EnTech_Zeus", False),
    HacknetLocData(218, "Finale", "Bit -- EnTech_Offline_Cycling_Backup", False),
    HacknetLocData(219, "Post-Game", "Post-Game -- Credits Server", False),

    # Labyrinths
    HacknetLocData(230, "Labyrinths", "Kaguya Trials -- Kaguya Sprint Trial", True),
    HacknetLocData(231, "Labyrinths", "Kaguya Trials -- Kaguya Push Trial", True),
    HacknetLocData(232, "Labyrinths", "Kaguya Trials -- Kaguya Source", True),
    HacknetLocData(233, "Labyrinths - Core", "Labyrinths -- Bibliotheque DropServer", True),
    HacknetLocData(234, "Labyrinths - Core", "Labyrinths -- Bibliotheque Ghost Storage", True),
    HacknetLocData(235, "Labyrinths - Set 1", "Labyrinths -- Ricer PC", True),
    HacknetLocData(236, "Labyrinths - Set 2", "Labyrinths -- r00t_Tek Battlestation", True),
    HacknetLocData(237, "Labyrinths - Set 2", "Labyrinths -- L. Shaffer's NetBook", True),
    # Sets 3 & 4 are ignored since they aren't linear and are, therefore, missable
    HacknetLocData(238, "Labyrinths - Memory Forensics", "Labyrinths -- Petunia Verres' Powerbook +",
                   True),
    HacknetLocData(239, "Labyrinths - Memory Forensics", "Labyrinths -- iodependency~Atlas", True),
    HacknetLocData(240, "Labyrinths - Memory Forensics", "Labyrinths -- Snackintosh_PASSTHRU", True),
    HacknetLocData(241, "Labyrinths - Memory Forensics", "Labyrinths -- Snackintosh_Proxy", True),
    HacknetLocData(242, "Labyrinths - Memory Forensics", "Labyrinths -- Lihota Productions", True),
    HacknetLocData(243, "Labyrinths - Memory Forensics", "Labyrinths -- Raven Dataworks", True),

    HacknetLocData(244, "Labyrinths - Hermetic Alchemists",
                   "Labyrinths -- School of the Hermetic Alchemists", True),
    HacknetLocData(245, "Labyrinths - Hermetic Alchemists", "Labyrinths -- HA_Solve", True),
    HacknetLocData(246, "Labyrinths - Hermetic Alchemists", "Labyrinths -- HA_Rebis", True),
    HacknetLocData(247, "Labyrinths - Hermetic Alchemists", "Labyrinths -- Nate's ePhone 4S", True),
    HacknetLocData(248, "Labyrinths - Hermetic Alchemists", "Labyrinths -- Nate Wesson Home", True),
    HacknetLocData(249, "Labyrinths - Hermetic Alchemists",
                   "Labyrinths -- Nate Wesson_STOR-DRIVE(tm)", True),
    HacknetLocData(250, "Labyrinths - Hermetic Alchemists", "Labyrinths -- HA_Coagula", True),

    HacknetLocData(251, "Labyrinths - Striker", "Labyrinths -- Striker Cache", True),
    HacknetLocData(252, "Labyrinths - Striker", "Labyrinths -- Striker Proxy", True),
    HacknetLocData(253, "Labyrinths - Striker", "Labyrinths -- Striker_Battlestation", True),

    HacknetLocData(254, "Labyrinths - Neopals", "Labyrinths -- Neopals Homepage", True),
    HacknetLocData(255, "Labyrinths - Neopals", "Labyrinths -- Neopals_Mainframe", True),
    HacknetLocData(256, "Labyrinths - Neopals", "Labyrinths -- Neopals_Authentication", True),
    HacknetLocData(257, "Labyrinths - Neopals", "Labyrinths -- Neopals_VersionControl", True),
    HacknetLocData(258, "Labyrinths - Neopals", "Labyrinths -- Thomas_Office", True),
    HacknetLocData(259, "Labyrinths - Neopals", "Labyrinths -- Ash-ALIENGEAR13", True),
    HacknetLocData(260, "Labyrinths - Neopals", "Labyrinths -- Tiff Doehan_PersonalPowerbook", True),

    HacknetLocData(261, "Labyrinths - Take Flight", "Labyrinths -- LAX_Pacific_Server", True),
    HacknetLocData(262, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_Network_Hub", True),
    HacknetLocData(263, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_Whitelist_Authenticator",
                   True),
    HacknetLocData(265, "Labyrinths - Take Flight", "Labyrinths -- Faith Morello's Laptop", True),
    HacknetLocData(266, "Labyrinths - Take Flight", "Labyrinths -- Vito McMichael's Laptop", True),
    HacknetLocData(267, "Labyrinths - Take Flight", "Labyrinths -- Mark Robertson's Office Computer",
                   True),
    HacknetLocData(268, "Labyrinths - Take Flight", "Labyrinths -- Kim Burnaby's Office Computer",
                   True),
    HacknetLocData(269, "Labyrinths - Take Flight", "Labyrinths -- Yasu Arai's eBook Touch", True),
    HacknetLocData(270, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_BookingsMainframe",
                   True),

    HacknetLocData(271, "Labyrinths - Altitude Loss", "Labyrinths -- Pacific_ATC_RoutingHub", True),
    HacknetLocData(272, "Labyrinths - Altitude Loss",
                   "Labyrinths -- Pacific_ATC_WhitelistAuthenticator", True),
    HacknetLocData(273, "Labyrinths - Altitude Loss", "Labyrinths -- Pacific_ATC_Skylink", True),
    HacknetLocData(274, "Labyrinths - Altitude Loss", "Labyrinths -- PA_747_0022 Flight Computer",
                   True),
    HacknetLocData(275, "Labyrinths - Altitude Loss", "Labyrinths -- PA_747_0018 Flight Computer",
                   True),

    HacknetLocData(276, "Labyrinths - Credits", "Labyrinths -- Kaguya_Projects", True),
    HacknetLocData(277, "Labyrinths - Credits", "Labyrinths -- Kaguya_Gateway", True),
    HacknetLocData(278, "Labyrinths - Credits", "Labyrinths -- Labyrinths_DevChat", True),

    # Post-Labyrinths
    HacknetLocData(279, "Post-Labyrinths", "Labyrinths -- Coel__Gateway", True),
    HacknetLocData(280, "Post-Labyrinths", "Naix -- Pellium Box", True),
    HacknetLocData(281, "Post-Labyrinths", "CSEC -- Psylance Internal Archives", True),
    HacknetLocData(282, "Post-Labyrinths", "CSEC -- Psylance Internal Services", True),
    # Gibson gets its own region that requires EVERY executable, and follows after both,
    # "Labyrinths - Altitude Loss" AND "CSEC - Bit"
    HacknetLocData(283, "Gibson", "Labyrinths -- The Gibson (Veteran)", True)

    # ok. i THINK that's all... around 140 new locations, jesus
]