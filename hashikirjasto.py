import os
import shutil
import json
import hashlib
import apufunktio_kansiofunktiot as kfun
import apufunktio_kansiovakiot as kvak

TESTISTRINGI = ""

BUFFERI			= 65536 # tiedostoja RAM:iin 64kb paloissa
MERKKIBUFFERI	= 4000	# jsoneita RAM:iin 4000 merkin paloissa

# Plot jotka riippuvat käytettävästä tietokoneesta: lue kansiovakiotiedostosta
HASHIT			= kvak.HASHIT
TIEDOSTOPOLUT	= kvak.TIEDOSTOPOLUT

NULL = kvak.NULL

def hanki_hash(tiedosto, binmode=True):
	'''
	Laskee annetun tiedoston md5-summan heksana,
	lukemalla sitä sopivan kokoinen palanen kerrallaan.
	Parametri 'binmode' määrittää, luetaanko tiedostoa
	binäärimuodossa (metadatoineen kaikkineen) vai
	tiedoston varsinaista sisältöä utf8-merkkeinä.
	Oletuksena 64kb binääripaloina,
	binmode=False -> 4000 merkkiä kerrallaan.
	'''
	md5 = hashlib.md5()
	if os.path.exists(tiedosto):
		if binmode:
			with open(tiedosto, 'rb') as filu:
				while True:
					data = filu.read(BUFFERI)
					if not data:
						break
					md5.update(data)
		else:
			with open(tiedosto, 'r') as filu:
				while True:
					data = filu.read(MERKKIBUFFERI)
					if not data:
						break
					md5.update(data.encode("utf-8"))
	return(md5.hexdigest())

def kasaa_dikti(kansio, printtaa=False):
	'''
	Kasaa diktin, jossa kuvattu puurakenne
 	annetulle hakemistolle 'kansio'
	'''
	if printtaa:
		print(kansio)
	dikti = {
		"tiedostot":{},
		"kansiot":{}
		}
	tiedostot, kansiot = kfun.kansion_sisalto(kansio)
	# 'tiedostot' dikti, jossa avaimina
	# kansion juuressa olevien tiedostojen
	# tiedostonimet ja arvoina tiedostoja
	# vastaavat hashiarvot heksamuodossa
	for tiedosto in tiedostot:
		dikti["tiedostot"][tiedosto] = hanki_hash(os.path.join(kansio, tiedosto))
	# Rekursiivisesti alikansioille:
	# 'kansiot' lista diktejä mallia 'dikti'
	for alikansio in kansiot:
		dikti["kansiot"][alikansio] = kasaa_dikti(os.path.join(kansio,alikansio),printtaa)
	return(dikti)

def kirjoita_dikti(dikti, kohdetiedosto, sisennys=0):
	'''
	Muodostaa annetusta hashidiktistä
	tiedostoon kirjoitettavan
	stringiversion,
	niin että tiedostot ja alikansiot on
	sisennetty selvästi kansion alle
	'''

	sistxt = sisennys*"\t"
	kohdetiedosto.write(f"{sistxt}\"tiedostot\":{{\n")
	avaimia = len(dikti["tiedostot"].keys())
	avaimet = dikti["tiedostot"].keys()
	sortatutavaimet = [a for _,a in sorted(zip([b.encode("utf8") for b in avaimet],avaimet))]
	for indeksi,tiedosto in enumerate(sortatutavaimet):
		hashi = dikti["tiedostot"][tiedosto]
		pilkku = (indeksi < avaimia-1)*"," # Pilkku kaikissa paitsi viimeisessä
		kohdetiedosto.write("{:s}\t\"{:s}\": \"{:s}\"{:s}\n".format(sistxt,tiedosto, str(hashi), pilkku))

	kohdetiedosto.write(f"{sistxt}\t}},\n")
	kohdetiedosto.write(f"{sistxt}\"kansiot\":{{\n")
	avaimia = len(dikti["kansiot"].keys())
	avaimet = dikti["kansiot"].keys()
	sortatutavaimet = [a for _,a in sorted(zip([b.encode("utf8") for b in avaimet],avaimet))]
	for indeksi,kansio in enumerate(sortatutavaimet):
		pilkku = (indeksi < avaimia-1)*"," # Pilkku kaikissa paitsi viimeisessä
		kohdetiedosto.write(f"{sistxt}\"{kansio}\":{{\n")
		kirjoita_dikti(dikti["kansiot"][kansio], kohdetiedosto, sisennys+1)
		kohdetiedosto.write(f"{sistxt}}}{pilkku}\n")
	kohdetiedosto.write(f"{sistxt}}}")

def vertaile_alikansiodikteja(lokaali_dikti, vertailu_dikti, lokaalipolku="", etapolku="", testimoodi=False, logi=NULL):
	'''
	Vertailee kahta diktiä keskenään, ja korjaa tiedostojen
	tilanteen vertailu_diktiä vastaavaksi. Toisin sanottuna:

	Tiedosto vertailu_diktissä muttei lokaali_diktissä:
		-> Kopioi tiedosto lokaaliin kansioon
	
	Tiedosto lokaali_diktissä muttei vertailu_diktissä:
		-> Poista lokaali tiedosto

	Tiedosto molemmissa dikteissä mutta hashit eroavat:
		-> Korvaa lokaali tiedosto
	
	Ja diktien rakenne on puumainen
	"tiedostot": {
					tiedosto: hashi,
					tiedosto: hashi,
					...
					}
	"kansiot":	{
				kansio: {
						"tiedostot": {...}
						  "kansiot": {...}
						}
				kansio: {...}
				}

	eli rekursio_sets kutsuu ja parametri "polku"
	pitää kirjaa siitä, missä päin tiedostorakennetta mennään.
	'''

	# Tiedostot jotka lokaalisti muttei vertailussa: poista
	global TESTISTRINGI

	for tiedosto in lokaali_dikti["tiedostot"].keys():
		if tiedosto not in vertailu_dikti["tiedostot"].keys() and os.path.exists(os.path.join(lokaalipolku,tiedosto)):
			print("\t\t\tPOISTA {}\n".format(os.path.join(lokaalipolku, tiedosto)))
			if logi is not NULL:
				logi.write(f"\tPOISTA {tiedosto}\n")
			if testimoodi:
				TESTISTRINGI += f"\t\t\tPOISTA {tiedosto}\n"
			elif kfun.joinittuonko(lokaalipolku, tiedosto):
				os.remove(os.path.join(lokaalipolku, tiedosto))
			else:
				if logi is not NULL:
					logi.write(f"\tOn jo poistettu {tiedosto}, gut gut\n")
				print("On jo poistettu.")

	# Tiedostot jotka vertailudiktissä muttei lokaalissa
	# tai tiedostojen hashit eroavat: kopio
	for tiedosto in vertailu_dikti["tiedostot"].keys():
		puuttuu = False
		eroaa = False
		if tiedosto not in lokaali_dikti["tiedostot"].keys():
			puuttuu = True
		elif vertailu_dikti["tiedostot"][tiedosto] != lokaali_dikti["tiedostot"][tiedosto]:
			eroaa =  True
		if (eroaa or puuttuu) and os.path.exists(os.path.join(etapolku,tiedosto)):
			print("\t\t\tKOPIOI {}".format(os.path.join(etapolku,tiedosto)))
			if logi is not NULL:
				logi.write("\tKOPIOI {}\n".format(os.path.join(etapolku,tiedosto)))
			if testimoodi:
				TESTISTRINGI += f"\t\t\tKOPIOI {tiedosto}\n"
			else:
				shutil.copy(os.path.join(etapolku, tiedosto), os.path.join(lokaalipolku, tiedosto))
				if kvak.LOKAALI_KONE != "Murakumo":
					shutil.chown(os.path.join(lokaalipolku, tiedosto),1000,1000)

	# Sama kansioille, poista puuttuvat
	# ja kopioi vain vertailusta löytyvät.
	# Kutsu rekursiivisesti alikansioille
	for kansio in lokaali_dikti["kansiot"].keys():
		# Referenssistä puuttuva kansio: poista
		if kansio not in vertailu_dikti["kansiot"].keys() and os.path.exists(os.path.join(lokaalipolku, kansio)):
			print("\t\t\tPOISTAKANSIO {}".format(os.path.exists(os.path.join(lokaalipolku, kansio))))
			if logi is not NULL:
				logi.write("\tPOISTAKANSIO {}".format(os.path.join(lokaalipolku, kansio)))
			if testimoodi:
				TESTISTRINGI += f"\t\t\tPOISTAKANSIO {kansio}\n"
			elif kfun.joinittuonko(lokaalipolku, kansio):
				shutil.rmtree(os.path.join(lokaalipolku, kansio))
			else:
				if logi is not NULL:
					logi.write("\tKansio {} on jo poistettu, gut gut".format(os.path.join(lokaalipolku, kansio)))
				print("On jo poistettu.")
	for kansio in vertailu_dikti["kansiot"].keys():
		# Puuttuva kansio: kopsaa
		if kansio not in lokaali_dikti["kansiot"].keys():
			if os.path.exists(os.path.join(etapolku,kansio)):
				print(f"\t\t\tKOPIOIKANSIO {os.path.join(etapolku,kansio)}")
				if logi is not NULL:
					logi.write(f"\tKOPIOIKANSIO {os.path.join(etapolku,kansio)}\n")
				if testimoodi:
					TESTISTRINGI += f"\t\t\tKOPIOIKANSIO {kansio}\n"
				else:
					shutil.copytree(os.path.join(etapolku,kansio), os.path.join(lokaalipolku,kansio), dirs_exist_ok=True)
		# Muut kansiot: rekursiivisesti pohjalle asti
		else:
			vertaile_alikansiodikteja(lokaali_dikti["kansiot"][kansio], vertailu_dikti["kansiot"][kansio], os.path.join(lokaalipolku, kansio), os.path.join(etapolku, kansio), testimoodi, logi=logi)

def vertaile_hashikirjastoja(hashit=HASHIT, testimoodi=False, logi=NULL):
	'''
	Vertailee annettuja hashikirjastoja laskemalla
	hashiarvot näistä löytyville kirjastotiedostoille
	(joissa lista kohdekansioiden tiedostoista ja näiden
	md5-hashien arvoista). Lokaalia dataa korjataan niin että
	se mätsää vertailtavan datan kanssa.

	Perusrakenne on niin että data on tyypeittäin kansioissa,
	joiden alla kansion nimen mukainen .json ja sen kaverina
	alakansiokohtaiset pienemmät jsonit.
	Jos yläkansion .jsonit täsmäävät keskenään, tiedetään suoraan
	että datat alakansioissakin mätsäävät. Muutoin pitää käydä
	alakansiokohtaiset jsonit yksi kerralaan läpi ja korjata.
	Toisin sanottuna:

	Musiikki (kansio)
		Musiikki.json
		alakansio_1.json
		alakansio_2.json
		...
	Kuvat (kansio)
		Kuvat.json
		...

	ja näistä rullataan kansio kerrallaan

		lokaali/Musiikki/Musiikki.json
	?= 	vertailtava/Musiikki/Musiikki.json
	'''

	global TESTISTRINGI
	lokaali = hashit["HASHIT_LOKAALIT"] # Paikallisen hashikirjaston sijainti
	muuttuneet = {} # paluuarvo, johon listattu mikä kaikki on muuttunut (eli täytyy päivittää)

	tiedostot, kansiot = kfun.kansion_sisalto(lokaali)
	# Pääkirjastot läpi (Musiikki/Kuvat/Screenshots),
	# mutta vain jos kyseinen kansiotyyppi on määritelty vertailtavaksi
	# esim. hashit["Musiikki"] = False tai "polku/isäntä/kansioon/"
	for kansio in [a for a in kansiot if a in hashit.keys() and hashit[a]]:
		# Kansion nimeä vastaava hashi (esim. Musiikki/Musiikki.json)
		vertailtava = hashit[kansio]
		# Lue paikallinen hashi ja vertailtava hashi
		lokaalihashi = hanki_hash(os.path.join(lokaali,f"{kansio}.json"), False)
		toispuolhashi= hanki_hash(os.path.join(vertailtava, f"{kansio}.json"), False)
		if testimoodi:
			TESTISTRINGI += f"{kansio}\n"
			print(f"{kansio}")
			print(f"{lokaalihashi}\t{toispuolhashi}")
		# Jos hashit eroavat, katsotaan millä tavalla
		if lokaalihashi != toispuolhashi:
			muuttuneet[kansio] = []
			if testimoodi:
				TESTISTRINGI += "\t-> eroaa\n"
				print("\t-> eroaa\n")
			# Käydään alakansio-jsonit läpi
			lok_alit = kfun.kansion_sisalto(os.path.join(lokaali,kansio))[0]
			for kansiodikti in lok_alit:
				print(kansiodikti)
				print(os.path.join(lokaali, kansio, kansiodikti))
				print(os.path.join(vertailtava, kansiodikti))
				# Jos diktit eroavat, korjataan niin että lokaali laitetaan mätsäämään vertailtavaan.
				lokhash = hanki_hash(os.path.join(lokaali, kansio, kansiodikti), False)
				verthash = hanki_hash(os.path.join(vertailtava, kansiodikti), False)
				if lokhash != verthash:
					# lisää alikansio muuttuneiden listalle
					muuttuneet[kansio].append(kansiodikti)
					print(f"\t\talikansio \"{kansiodikti}\" eroaa\n")
					if testimoodi:
						TESTISTRINGI += f"\t\talikansio \"{kansiodikti}\" eroaa\n\t\t({lokhash}\t{verthash})\n"
					dikti_lok = json.load(open(os.path.join(lokaali, kansio, kansiodikti), "r"))
					dikti_vert = {}
					# Kansion kuuluukin olla olemanssa, mutta sisältö eroaa: vertaile sisältöä tarkemmin
					if os.path.exists(os.path.join(vertailtava, kansiodikti)):
						dikti_vert = json.load(open(os.path.join(vertailtava, kansiodikti), "r"))
						lk = os.path.join(TIEDOSTOPOLUT["Lokaalit"][kansio], kansiodikti.replace(".json", ""))
						et = os.path.join(TIEDOSTOPOLUT["Etät"][kansio], kansiodikti.replace(".json", ""))
						vertaile_alikansiodikteja(dikti_lok, dikti_vert, lk, et, testimoodi, logi=logi)
					# Koko kansiota ei kuuluisi olla edes olemassa: poista
					else:
						print("\t\tEIKUULUOLLA {}".format(os.path.join(TIEDOSTOPOLUT["Lokaalit"][kansio], kansiodikti.replace(".json", ""))))
						if logi is not NULL:
							logi.write("EIKUULUOLLA {}\n".format(os.path.join(TIEDOSTOPOLUT["Lokaalit"][kansio], kansiodikti.replace(".json", ""))))
						if testimoodi:
							TESTISTRINGI += "\t\tEIKUULUOLLA {}\n".format(os.path.join(TIEDOSTOPOLUT["Lokaalit"][kansio], kansiodikti.replace(".json", "")))
							TESTISTRINGI += "\t\tPOISTAJSON {}\n".format(os.path.join(lokaali, kansio, kansiodikti))
						else:
							print("POISTAJSON {}".format(os.path.join(lokaali, kansio, kansiodikti)))
							os.remove(os.path.join(lokaali, kansio, kansiodikti))
							if kfun.joinittuonko(lokaali, kansio, kansiodikti):
								print("POISTAKANSIO {}".format(os.path.join(lokaali, kansio, kansiodikti)))
								if logi is not NULL:
									logi.write("POISTAKANSIO {}\n".format(os.path.join(lokaali, kansio, kansiodikti)))
								shutil.rmtree(os.path.join(TIEDOSTOPOLUT["Lokaalit"][kansio], kansiodikti.replace(".json", "")))
							else:
								print("Kansio on jo poistettu.")
								if logi is not NULL:
									logi.write("Kansio {} on jo poistettu, gut gut\n".format(os.path.join(lokaali, kansio, kansiodikti)))
				else:
					print(f"\t\talikansio \"{kansiodikti}\" mätsää\n")
					if logi is not NULL:
						logi.write(f"kansio {kansiodikti} ok\n")
					if testimoodi:
						TESTISTRINGI += f"\t\talikansio \"{kansiodikti}\" mätsää\n"
	return(muuttuneet)

def kirjaa_diktit_kansioista():
	hashit_lokaalit = HASHIT["HASHIT_LOKAALIT"]
	for kansio in [a for a in os.listdir(hashit_lokaalit) if os.path.isdir(os.path.join(hashit_lokaalit, a))]:
		libitiedosto = open(os.path.join(hashit_lokaalit, f"{kansio}.json"), "w+", encoding="utf8")
		# Päädikti (kaikki tiedostot) {kansionnimi}.json esim. 'Musiikki.json'
		dikti = kasaa_dikti(TIEDOSTOPOLUT["Lokaalit"][kansio], True)
		libitiedosto.write("{\n")
		kirjoita_dikti(dikti,libitiedosto)
		libitiedosto.write("\n}\n")
		libitiedosto.close()
		# Alakansiot omiin tiedostoihinsa
		for alikansio in dikti["kansiot"].keys():
			libitiedosto = open(os.path.join(hashit_lokaalit, kansio, f"{alikansio}.json"), "w+", encoding="utf8")
			libitiedosto.write("{\n")
			kirjoita_dikti(dikti["kansiot"][alikansio], libitiedosto)
			libitiedosto.write("\n}\n")
			libitiedosto.close()

#kirjaa_diktit_kansioista()

# vertaile_hashikirjastoja(testimoodi=True)
# TESTI = open("/home/olkkari/Scripts/testilogi.txt", "w+", encoding="utf8")
# TESTI.write(TESTISTRINGI)
# TESTI.close()
# print(TESTISTRINGI)
