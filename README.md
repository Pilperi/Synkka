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

	[x] Tiedostotyypin määrittely (vrt. Biisi-luokka musasynkassa)
		[x] Tiedostonimi
		[x] Lisäyspäivä
		[x] Hashi (?)
	[/] Synkkafunktiot pyörimään Tiedostopuilla
		[x] Puiden vertailu toisiinsa
		[/] Lokaalin puun päivittäminen
	[/] Kansiomääritelmät, mitä on missäkin ja mihin tietokantatiedostoon pitäisi tallentaa
		[/] Oman huoneen kone
			[x] Lokaalit tiedostokansiot
			[/] Lokaalit tietokannat (winukkapuoli...?)
			[x] Pettanin tietokannat
		[/] Olkkarikone
			[x] Lokaalit tiedostokansiot
			[x] Lokaalit tietokannat
			[x] Pettanin tietokannat
		[x] Pettankone
			[x] Lokaalit tiedostokansiot
			[x] Lokaalit tietokannat


STATUS:
	- Asiat hyvinkin kunnossa, pitää vielä ihmetellä että miksi ihmeessä asiat näyttää aina siltä että ne on muuttunu viime käynnistyksen yhteydessä... (käyttöpäivä vs. muokkauspäivä? Implementoi hashit nyt sit kuitenkin?)
