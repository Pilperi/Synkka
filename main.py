'''
Pääskripti, joka kutsuu muita oleellisia asioita.
Ei tarvitse esim. miettiä, minkä tiedoston alla olikaan __main__
'''
import funktiot_puuvertailu as pver

onnistuminen = pver.synkkaa()
if onnistuminen:
	print("Synkattu'd")
else:
	print("Synkkaaminen ei onnistunut.")
