import os
import vakiot_kansiovakiot as kvak
import funktiot_kansiofunktiot as kfun
from class_tiedosto import Tiedosto
from class_biisit import Biisi
from class_tiedostopuu import Tiedostopuu

def vertaa_puita(isantapuu=None, isantapalvelin=None, lapsipuu=None, lapsipalvelin=None):
	'''
	Vertaa lapsipuuta isäntäpuuhun.
	Jos lapsipuussa on kansioita tai tiedostoja jotka
	puuttuvat isäntäpuusta, poista ne (puusta ja kovalevyltä)
	Jos lapsipuusta puuttuu tiedostoja tai kansioita joita
	isäntäpuussa on, tai isäntäpuun versiot tiedostoista on uudempia,
	kopioi ne isäntäpuusta lokaaliin tiedostojärjestelmään.

	Käy koko puu rekursiivisesti läpi.
	Tiedostosiirrot käyvät SCP:llä, muodossa scp isantapalvelin:asia lapsipalvelin:asia
	Yleensä näistä toinen on lokaali tiedostojärjestelmä, jolloin sen palvelimeksi laitetaan None.
	'''
	if None in [isantapuu, lapsipuu]:
		return(None)

	# Tiedosto pitäisi olla ja puuttuu tai on vanhentunut: kopioi
	for tiedosto in isantapuu.tiedostot:
		if not any([a.tiedostonimi==tiedosto.tiedostonimi and a.lisayspaiva>=tiedosto.lisayspaiva for a in lapsipuu.tiedostot]):
			lahdetiedosto = os.path.join(isantapuu.hae_nykyinen_polku(), tiedosto.tiedostonimi)
			if type(isantapalvelin) is str:
				lahdetiedosto = "{}:{}".format(isantapalvelin, lahdetiedosto)
			kohdetiedosto = os.path.join(lapsipuu.hae_nykyinen_polku(), tiedosto.tiedostonimi)
			if type(lapsipalvelin) is str:
				kohdetiedosto = "{}:{}".format(lapsipalvelin, tiedosto.tiedostonimi)
			# Siirrä
			siirrettiin = False
			for yritys in range(5):
				siirrettiin = kfun.lataa(True, lahdetiedosto, kohdetiedosto)
				if siirrettiin:
					lapsipuu.tiedostot.append(tiedosto)
					break
	# Tiedostoa ei pitäisi olla: poista
	poistetut_tiedostot = []
	for indeksi,tiedosto in enumerate(lapsipuu.tiedostot):
		if not any([a.tiedostonimi==tiedosto.tiedostonimi for a in isantapuu.tiedostot]):
			lahdetiedosto = os.path.join(lapsipuu.hae_nykyinen_polku(), tiedosto.tiedostonimi)
			# Tiedosto etäpalvelimella
			if type(lapsipalvelin) is str:
				poistettu = False
				for i in range(5):
					poistettu = kfun.etapoisto(True, lapsipalvelin, lahdetiedosto)
					if poistettu:
						poistetut_tiedostot.append(indeksi)
						break
			# Lokaali tiedosto
			else:
				os.remove(lahdetiedosto)
	i = len(poistetut_tiedostot)-1
	while i >= 0:
		p = lapsipuu.tiedostot.pop(i)
		i -= 1

	# Sama alikansioille
	for alikansio in isantapuu.alikansiot:
		# Löytyy molemmista: sukella sisään
		molemmissa = False
		for indeksi,lapsi_alikansio in enumerate(lapsipuu.alikansiot):
			if alikansio.kansio == lapsi_alikansio.kansio:
				lapsi_alikansio = vertaa_puita(alikansio, isantapalvelin, lapsi_alikansio, lapsipalvelin)
				lapsipuu.alikansiot[indeksi] = lapsi_alikansio
				molemmissa = True
		# Ei ole lapsipuussa: kopioi
		if not molemmissa:
			lahdekansio = os.path.join(isantapuu.hae_nykyinen_polku(), alikansio.kansio)
			if type(isantapalvelin) is str:
				lahdekansio = "{}:{}".format(isantapalvelin, lahdekansio)
			kohdekansio = os.path.join(lapsipuu.hae_nykyinen_polku(), alikansio.kansio)
			if type(lapsipalvelin) is str:
				kohdekansio = "{}:{}".format(lapsipalvelin, alikansio.kansio)
			# Siirrä
			siirrettiin = False
			for yritys in range(5):
				siirrettiin = kfun.lataa(False, lahdekansio, kohdekansio)
				if siirrettiin:
					# Luo Tiedostopuu alikansiosta.
					# Voitaisiin vaan ottaa suoraan alikansiosta versio jonka isäntä on lapsipuun
					# kansio, mutta tällöin päiväykset menisivät ihan miten sattuu.
					alikansiopuu = Tiedostopuu(kansio=alikansio.kansio, edellinenkansio=lapsipuu, syvennystaso=alikansio.syvennystaso+1, tiedostotyyppi=alikansio.tiedostotyyppi)
					alikansiopuu.kansoita()
					lapsipuu.alikansiot.append(alikansiopuu)
					break

	# Kansiota ei pitäisi olla: poista
	poistetut_kansiot = []
	for indeksi,alikansio in enumerate(lapsipuu.alikansiot):
		if not any([a.kansio==alikansio.kansio for a in isantapuu.alikansiot]):
			lahdekansio = os.path.join(lapsipuu.hae_nykyinen_polku(), alikansio.kansio)
			# Tiedosto etäpalvelimella
			if type(lapsipalvelin) is str:
				poistettu = False
				for i in range(5):
					poistettu = kfun.etapoisto(False, lapsipalvelin, lahdekansio)
					if poistettu:
						poistetut_kansiot.append(indeksi)
						break
			# Lokaali tiedosto
			else:
				os.remove(lahdekansio)
	i = len(poistetut_kansiot)-1
	while i >= 0:
		p = lapsipuu.alikansiot.pop(i)
		i -= 1

	# Palauta (ehkä) muokattu lapsipuu
	return(lapsipuu)

def kasaa_tietokanta(kansiotyyppi):
	'''
	Alusta annetun tyyppinen tietokanta.
	'''
	tiedostotyyppi = Tiedosto
	if kansiotyyppi == "Musiikki":
		tiedostotyyppi = Biisi
	for k,tietokansio in enumerate(kvak.KANSIOT[kvak.LOKAALI_KONE][kansiotyyppi]):
		puu = Tiedostopuu(kansio=tietokansio, tiedostotyyppi=tiedostotyyppi)
		puu.kansoita()
		kohdetiedosto = kvak.LOKAALIT_TIETOKANNAT[kansiotyyppi][k]
		f = open(kohdetiedosto, "w+")
		f.write(str(puu))
		f.close()

def tarkista_onko_tietokannat():
	'''
	Tarkista kustakin tietokantatyypistä, onko sen tiedot kirjattu
	vai eikö ole. Jos ei, aja 'kasaa_tietokanta()'
	'''
	for kansiotyyppi in kvak.LOKAALIT_TIETOKANNAT:
		if any([a and not os.path.exists(a) for a in kvak.LOKAALIT_TIETOKANNAT[kansiotyyppi]]):
			print(f"Paikallista {kansiotyyppi}-tietokantaa ei oltu määritelty, määritetään...")
			kasaa_tietokanta(kansiotyyppi)
			print("\tMääritetty")

def synkkaa():
	# Ei tehdä mitään jos asioita ei ole määritelty
	if None in [kvak.VOIMASUHTEET, kvak.LOKAALIT_TIETOKANNAT]:
		print("Tietokonetta ei määritelty kansiovakioissa, ei tehdä mitään.")
		return(0)

	# Varmistetaan että tietokannat on olemassa
	tarkista_onko_tietokannat()

	# Kullekin tiedostokansiolle: kopioi Pettanin tietokantatiedosto ja vertaa sitä omaan
	for kansiotyyppi in kvak.LOKAALIT_TIETOKANNAT:
		pettanin_tietokanta = kvak.TIETOKANNAT["Pettan"][kansiotyyppi] # lista tiedostopolkuja, valkkaa oikea
		lokaali_tietokanta  = kvak.LOKAALIT_TIETOKANNAT[kansiotyyppi][0]
		# Yritä siirtää max. viisi kertaa
		siirretty = False
		for yritys in range(5):
			siirretty = kfun.lataa(True, "pettankone", pettanin_tietokanta[kvak.VOIMASUHTEET[kansiotyyppi][1]], "pettan_{kansiotyyppi}.tietokanta")
			if siirretty:
				break
		if siirretty:
			# Lue tietokantatiedostoista
			if kansiotyyppi == "Musiikki":
				puu_lokaali = Tiedostopuu(tiedostotyyppi=Biisi)
				puu_pettan  = Tiedostopuu(tiedostotyyppi=Biisi)
			else:
				puu_lokaali = Tiedostopuu(tiedostotyyppi=Tiedosto)
				puu_pettan  = Tiedostopuu(tiedostotyyppi=Tiedosto)
			f = open(lokaali_tietokanta, "r")
			puu_lokaali.lue_tiedostosta(f)
			f.close()
			f = open(pettanin_tietokanta, "r")
			puu_pettan.lue_tiedostosta(f)
			f.close()

			# Vertaa tietokantatiedostoja
			# Paikallinen kone masteri
			if VOIMASUHTEET[kansiotyyppi][0]:
				puu_pettan = vertaa_puita(isantapuu=puu_lokaali, isantapalvelin=None, lapsipuu=puu_pettan, lapsipalvelin="pettankone")
				f = open(pettanin_tietokanta, "w+")
				f.write(puu_pettan)
				f.close()

			# Pettani masteri
			else:
				puu_lokaali = vertaa_puita(isantapuu=puu_pettan, isantapalvelin="pettankone", lapsipuu=puu_lokaali, lapsipalvelin=None)
				f = open(lokaali_tietokanta, "w+")
				f.write(puu_lokaali)
				f.close()
		else:
			print("Ei saatu kopioitua Pettanilta tiedostotietokantoja")
	return(1)

# onnistuminen = synkkaa()