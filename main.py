'''
Pääskripti, joka kutsuu muita oleellisia asioita.
Ei tarvitse esim. miettiä, minkä tiedoston alla olikaan __main__
'''
import funktiot_puuvertailu as pver
import funktiot_logifunktiot as logfun
import vakiot_kansiovakiot as kvak

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