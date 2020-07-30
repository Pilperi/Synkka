'''
Musatietokannan vakiot kootussa paikkaa.
Sallitut tiedostotyypit, kielletyt sanat (?),
relevanttien kansioiden sijainnit eri tietokoneilla.
'''
import os

# Tulosta komentoriville, älä poistele juttuja
TESTIMOODI = False
LOGITIEDOSTO = "logi"

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
		  None:		        {},
		  "Murakumo-linux": {"Musiikki":   ["/mnt/Suzuya/Suzuyajako/Musiikki/"],
		                     "INTERNET":    ["/mnt/Norot/Data/INTERNET/"],
		                     "Screenshots": ["/mnt/Suzuya/Suzuyajako/Screenshots/Jaotellut/"]
		                     },
		  "Murakumo-win":   {"Musiikki":    ["S:\\Suzuyajako\\Musiikki\\"],
		                     "INTERNET":    ["C:\\data\\INTERNET\\"],
		                     "Screenshots": ["S:\\Suzuyajako\\Screenshots\\Jaotellut\\"],
		                     },
		  "Pettan":         {"Musiikki":    ["/mnt/data/Jouni/Musiikki/",
		                                     "/mnt/data/Nipa/Musiikki/",
		                                     "/mnt/data/Tursa/Musiikki/"],
		                     "INTERNET":    ["/mnt/data/Jouni/INTERNET/"],
		                     "Screenshots": ["/mnt/data/Jouni/Screenshots/Jaotellut/"]
		                     },
		  "Olkkari":        {"Musiikki":     ["/mnt/Data/Jouni/Musiikki/"],
                             "INTERNET":     ["/home/olkkari/Pictures/INTERNET/"],
		                     "Screenshots":  ["/mnt/Data/Jouni/Screenshots/Jaotellut/"]
		                     },
		}
# Sijainteja vastaavien tietokantatiedostojen sijainnit
TIETOKANNAT = {
			  None:		        {},
			  "Murakumo-linux": {"Musiikki":    ["/home/pilperi/Tietokannat/Musiikit/musiikit.tietokanta"],
			                     "INTERNET":    ["/home/pilperi/Tietokannat/Synkka/INTERNET.tietokanta"],
			                     "Screenshots": ["/home/pilperi/Tietokannat/Synkka/Screenshots.tietokanta"]
			                    },
			  "Murakumo-win":   {"Musiikki":    [""],
			                     "INTERNET":    [""],
			                     "Screenshots": [""]
			                    },
			  "Pettan":         {"Musiikki":    ["/home/taira/tietokannat/Musakirjasto/jounimusat.tietokanta",
			  			                         "/home/taira/tietokannat/Musakirjasto/nipamusat.tietokanta",
			  			                         "/home/taira/tietokannat/Musakirjasto/tursamusat.tietokanta"
			  			                        ],
			  			         "INTERNET":    ["/home/taira/tietokannat/Synkka/INTERNET.tietokanta"],
			  			         "Screenshots": ["/home/taira/tietokannat/Synkka/Screenshots.tietokanta"]
			  			        },
			  "Olkkari":        {"Musiikki":    ["/home/olkkari/Tietokannat/Synkka/musiikit.tietokanta"],
			                     "INTERNET":    ["/home/olkkari/Tietokannat/Synkka/INTERNET.tietokanta"],
			                     "Screenshots": ["/home/olkkari/Tietokannat/Synkka/Screenshots.tietokanta"]
			                    }
			  }
LOKAALIT_MUSIIKIT    = None
LOKAALIT_INTERNET    = None
LOKAALIT_SCREENSHOTS = None
LOKAALIT_TIETOKANNAT = None
if KANSIOT.get(LOKAALI_KONE) is not None:
	LOKAALIT_MUSIIKIT    = KANSIOT[LOKAALI_KONE].get("Musiikki")
	LOKAALIT_INTERNET    = KANSIOT[LOKAALI_KONE].get("INTERNET")
	LOKAALIT_SCREENSHOTS = KANSIOT[LOKAALI_KONE].get("Screenshots")
	LOKAALIT_TIETOKANNAT = TIETOKANNAT.get(LOKAALI_KONE)

# Mitkä on voimasuhteet, pusketaanko Pettanille (True) vai kiskotaanko Pettanilta (False)
# ja minkä indeksiseen Pettanin tietokantaan verrataan (esim. jounimusat.tietokanta vai tursamusat.tietokanta)
# Pettan ei kisko eikä puske mitään minnekään.
MASTERIT =  {
            "Murakumo-linux": {"Musiikki":    (True,  0),
                               "INTERNET":    (True,  0),
                               "Screenshots": (False, 0)
                              },
            "Murakumo-win":   {"Musiikki":    (True,  0),
                               "INTERNET":    (True,  0),
                               "Screenshots": (False, 0)
                              },
            "Olkkari":        {"Musiikki":    (False, 0),
                               "INTERNET":    (False, 0),
                               "Screenshots": (True,  0)
                              }
            }
VOIMASUHTEET = None
if LOKAALI_KONE:
	VOIMASUHTEET = MASTERIT.get(LOKAALI_KONE)
