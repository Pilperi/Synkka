import funktiot_kansiofunktiot as kfun

class Tiedostopuu():
	'''
	Tiedostopuun luokka.
	Käytännössä sisältää tiedot kansioista
	ja siitä, mitä biisejä on minkäkin kansion alla,
	jottei tarvitse roikottaa täysiä tiedostopolkuja
	koko aikaa messissä.
	Pääpointti lähinnä siinä, että asiat saadaan
	kirjoitettua tiedostoon fiksusti ja luettua sieltä ulos.
	'''
	def __init__(self, kansio=None, edellinenkansio=None, syvennystaso=0):
		if TULOSTA:
			print(kansio)
		self.edellinentaso  = edellinenkansio	# edellinen kansio (Tiedostopuu tai None)
		self.syvennystaso   = syvennystaso		# int, monesko kerros menossa
		self.kansio         = kansio 			# str, pelkkä kansionimi jollei ylin kansio
		self.tiedostot      = [] 				# Lista Tiedostoja
		self.alikansiot     = [] 				# Lista Tiedostopuita

	def kansoita(self):
		'''
		Lado kansion biisit biisilistaan ja
		alikansiot alikansiolistaan.
		'''
		nykyinen_polku = self.hae_nykyinen_polku()
		tiedostot, alikansiot = kfun.kansion_sisalto(self.hae_nykyinen_polku(), kvak.MUSATIEDOSTOT)
		# Tiedosto tiedostolistaan
		for tiedosto in tiedostot:
			self.biisit.append(Tiedosto(os.path.join(self.hae_nykyinen_polku(), tiedosto)))
		# Alikansiot yhtä tasoa syvemmällä, ole näiden 'edellinenkansio'
		for kansio in alikansiot:
			puu = Tiedostopuu(kansio, self, self.syvennystaso+1)
			puu.kansoita()
			self.alikansiot.append(puu)

	def lue_tiedostosta(self, tiedosto):
		'''
		Lue puurakenne tietokantatiedostosta.
		Huom. 'tiedosto' on tiedostokahva (vai mikälie), ei tiedostopolku str
		'''
		rivi = tiedosto.readline()
		# Jos pääkansio, lue tietokannan pääkansion nimi
		# ekalta riviltä ja siirry seuraavalle
		if self.syvennystaso == 0 and rivi and rivi[1] == "\"":
			kansionimi = ""
			i = 2
			while rivi[i] != "\"":
				kansionimi += rivi[i]
				i += 1
			self.kansio = kansionimi
			rivi = tiedosto.readline()
		# print("\nKansio: {}\nEdellinen: {}\nSyvennystaso: {}".format(self.kansio, self.edellinentaso, self.syvennystaso))
		while rivi:
			# Laske syvennystaso: rivin alussa luvut ilmaisemassa
			syvennys = ""
			i = 0
			while rivi[i].isnumeric():
				syvennys += rivi[i]
				i += 1
			syvennys = int(syvennys)
			# print("Asian taso: {}".format(syvennys))
			if syvennys == self.syvennystaso+1:
				# Tapaus biisi nykyisellä syvennystasolla: lisää biisilistaan
				if rivi[i] == "{":
					# print("Tämän kansion biisi")
					diktibiisi = json.loads(rivi[i:-1])
					self.biisit.append(Biisi(diktibiisi))
					rivi = tiedosto.readline()
				# Tapaus kansio: lisää Tiedostopuu alikansioihin
				elif rivi[i] == "\"":
					# Lue kansion nimi, joka on "" välissä
					i += 1
					kansionimi = ""
					while rivi[i] != "\"":
						kansionimi += rivi[i]
						i += 1
					# print("Kansion {} alikansio {}".format(self.kansio, kansionimi))
					alipuu = Tiedostopuu(kansionimi, self, self.syvennystaso+1)
					rivi = alipuu.lue_tiedostosta(tiedosto)
					self.alikansiot.append(alipuu)
			else:
				# Palauta viimeisin rivi, koska sitä tarvitaan vielä ylemmällä tasolla
				# print("Alemman tason asia.")
				return(rivi)

	def hae_nykyinen_polku(self):
		'''
		Hae nykyisen tason koko polku edeltävistä tasoista latomalla.
		'''
		polku = [self.kansio]
		ylempitaso = self.edellinentaso
		while ylempitaso is not None:
			if type(ylempitaso) is str:
				print(ylempitaso)
			polku.append(ylempitaso.kansio)
			ylempitaso = ylempitaso.edellinentaso
		polku.reverse()
		polkustringi = ""
		for osa in polku:
			polkustringi += osa+"/"
		return(polkustringi)

	def __str__(self):
		'''
		Rekursiivinen str-operaatio, käydään kaikki alikansiotkin läpi.
		Kansiot ja biisit erottaa siitä että biisien tiedot on {} välissä
		ja kansioiden nimet eivät ala "{" ja lopu "}" (...eihän?)
		'''
		st = "{:d}\"{:s}\"\n".format(self.syvennystaso, self.kansio)
		for biisi in self.biisit:
			# print(biisi.biisinimi)
			st += "{:d}{:s}\n".format((self.syvennystaso+1), str(biisi))
		for kansio in self.alikansiot:
			# print(type(kansio))
			st += str(kansio)
		return(st)


