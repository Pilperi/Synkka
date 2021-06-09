'''
Pääskripti, joka kutsuu muita oleellisia asioita.
Ei tarvitse esim. miettiä, minkä tiedoston alla olikaan __main__
'''
from . import funktiot_puuvertailu as pver
from tiedostohallinta import funktiot_logifunktiot as logfun
from tiedostohallinta import vakiot_kansiovakiot as kvak

def main():
	logi = None
	if kvak.LOGITIEDOSTO:
		logfun.kopsaa_logit()
		logi = open(kvak.LOGITIEDOSTO, "w+")
		logfun.kirjaa(logi, "Aloitetaan.")
	onnistuminen = pver.synkkaa(logitiedosto=logi)
	if onnistuminen:
		logfun.kirjaa(logi, "Synkattu'd.")
		print("Synkattu'd")
	else:
		logfun.kirjaa(logi, "Synkkaaminen ei onnistunut.")
		print("Synkkaaminen ei onnistunut.")
	if kvak.LOGITIEDOSTO:
		logi.close()

if __name__ == "__main__":
	import sys
	kvak.TESTIMOODI = "testimoodi" in sys.argv or "--testi" in sys.argv
	main()
