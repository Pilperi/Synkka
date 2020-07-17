Skriptit kämpän tietokoneiden väliseen tiedostosynkkailuun.
Vanhassa versiossa kasattiin hashit lokaaleista tiedostoista, puskettiin hashit
Pettanille. Pettanilla olevia [muiden koneiden] hasheja verrattiin sitten omiin,
ja jos hashit erosivat ja isäntätietokone oli verkossa (eli päällä), kiskottiin sieltä
ei-täsmäävät tiedostot paikallisiin kansioihin.

Kyllä, tämä on menettelytapana aikas kömpelö ja siitä seurasi aika usein monen moisia ongelmia.
Lähinnä: meitin huoneen kone on käytännössä aina päällä ennen olkkarin konetta, eli synkkaus
meni oikeastaan aina yhteen suuntaan.

Väännän nyt uuden version, jossa

	1) Asiat pusketaan aina Pettanille ja kiskotaan Pettanilta, koska se on aina päällä
	2) Käytetään JSON-formaatin sijaan biisisynkkauksen myötä väsättyä Tiedostopuu-rakennetta. Yleinen ja laajennettava.
	3) Hashien tarpeellisuus vähän kysymysmerkki. Mitä jos vaan kirjataan ja katsotaan muokkauspäivämääriä?


Tehtäviä asioita:

	[ ] Tiedostotyypin määrittely (vrt. Biisi-luokka musasynkassa)
		[ ] Tiedostonimi
		[ ] Lisäyspäivä
		[ ] Hashi (?)
	[ ] Synkkafunktiot pyörimään Tiedostopuilla
	[ ] Kansiomääritelmät, mitä on missäkin ja mihin tietokantatiedostoon pitäisi tallentaa
		[/] Oman huoneen kone
			[x] Lokaalit tiedostokansiot
			[ ] Pettanin tiedostokansiot
			[ ] Lokaalit tietokannat
			[ ] Pettanin tietokannat
		[/] Olkkarikone
			[x] Lokaalit tiedostokansiot
			[ ] Pettanin tiedostokansiot
			[ ] Lokaalit tietokannat
			[ ] Pettanin tietokannat
		[/] Pettankone
			[x] Lokaalit tiedostokansiot
			[ ] Lokaalit tietokannat


STATUS:
	- Asiat vielä ihan sikin sokin eikä varmaan toimi millään tasolla (outoa jos toimis)