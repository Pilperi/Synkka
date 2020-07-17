'''
Musatietokannan vakiot kootussa paikkaa.
Sallitut tiedostotyypit, kielletyt sanat (?),
relevanttien kansioiden sijainnit eri tietokoneilla.
'''
import os

MUSATIEDOSTOT = ["mp3", "flac", "wma"]
KIELLETYT = []

# Tunnista käytettävä kone kotikansion perusteella.
LOKAALI_KONE = None
if os.path.exists("/home/pilperi"):
	LOKAALI_KONE = "Murakumo-linux"
if os.path.exists("C:\\"):
	LOKAALI_KONE = "Murakumo-win"
elif os.path.exists("/home/taira"):
	LOKAALI_KONE = "Pettan"
elif os.path.exists("/home/olkkari"):
	LOKAALI_KONE = "Olkkari"

if LOKAALI_KONE is None:
	print("Käytettävää tietokonetta ei kyetty määrittämään...")
else:
	print(f"Lokaali kone: {LOKAALI_KONE}")

# Musiikkien sijainnit
KANSIOT = {
			  None:		        {[]},
			  "Murakumo-linux": {"Musiikki:":   ["/mnt/Suzuya/Suzuyajako/Musiikki/"],
			                     "INTERNET":    ["/mnt/Norot/Data/INTERNET/"],
			                     "Screenshots": ["/mnt/Suzuya/Suzuyajako/Screenshots/Jaotellut/"]
			                     },
			  "Murakumo-win":   {"Musiikki":    ["S:\\Suzuyajako\\Musiikki\\"],
			                     "INTERNET":    ["C:\\data\\INTERNET\\"],
			                     "Screenshots": ["S:\\Suzuyajako\\Screenshots\\Jaotellut\\"]
			                     },
			  "Pettan":         {"Musiikki":    ["/mnt/data/Jouni/Musiikki/",
			                                     "/mnt/data/Nipa/Musiikki/",
			                                     "/mnt/data/Tursa/Musiikki/",],
			                     "INTERNET":    ["/mnt/data/Jouni/INTERNET/"],
			                     "Screenshots": ["/mnt/data/Jouni/Screenshots/Jaotellut/"]
			                     },
			  "Olkkari":        {"Musiikki":     ["/mnt/Data/Jouni/Musiikki/"],
                                 "INTERNET":     ["/mnt/home/olkkari/Pictures/INTERNET/"],
			                     "Screenshots":  ["/mnt/Data/Jouni/Screenshots/Jaotellut/"]
			                     },
			  }
# Sijainteja vastaavien tietokantatiedostojen sijainnit
TIETOKANNAT = {
			  None:		  [],
			  "Murakumo": {"Musiikki:":   ["/home/pilperi/Tietokannat/Musiikit/musiikit.tietokanta"],
			               "INTERNET":    ["/mnt/Norot/Data/INTERNET/"],
			               "Screenshots": ["/mnt/Suzuya/Suzuyajako/Screenshots/Jaotellut/"]
			              },
			  "Pettan":   ["/home/taira/tietokannat/Musakirjasto/jounimusat.tietokanta",
			  			   "/home/taira/tietokannat/Musakirjasto/nipamusat.tietokanta",
			  			   "/home/taira/tietokannat/Musakirjasto/tursamusat.tietokanta"
			  			  ],
			  "Olkkari":  ["/home/olkkari/Tietokannat/Musiikit/musiikit.tietokanta"]
			  }
LOKAALIT_MUSIIKIT    = MUSAKANSIOT.get(LOKAALI_KONE)
LOKAALIT_TIETOKANNAT = TIETOKANNAT.get(LOKAALI_KONE)
# Jos pituuksissa hämminkiä, täytä nulleilla (ei kyl saisi olla)
if all(type(a) is list for a in [LOKAALIT_MUSIIKIT, LOKAALIT_MUSIIKIT]) and len(LOKAALIT_MUSIIKIT) != len(LOKAALIT_MUSIIKIT):
	while len(LOKAALIT_MUSIIKIT) < len(LOKAALIT_TIETOKANNAT):
		LOKAALIT_MUSIIKIT.append(None)
	while len(LOKAALIT_MUSIIKIT) > len(LOKAALIT_TIETOKANNAT):
		LOKAALIT_TIETOKANNAT.append(None)
