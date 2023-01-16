Zapojenie ako v navode na LED-y
https://dordnung.de/raspberrypi-ledstrip/

Rozdiel je, ze nedavas Drain(odvod) z MOSFET-u do farby LED-pasiku, ale na ventilator.
t.j.

odvod z MOSFET (stredny) na SIGNAL pin (ked sa pozeras kablom k sebe, tak v pravo) ventilatora
\+ (plus) z 12V zdroja na +12V ventilatora (ked sa pozeras kablom k sebe, tak v strede)
https://landing.coolermaster.com/faq/3-pin-and-4-pin-fan-wire-diagrams/
zdroj z MOSFET (pravy) na - (minus) 12V zdroja
Brana/Gate z MOSFET (lavy) na ovladatelne GPIO na RPi (napriklad 17)
Akykolvek volny Ground z RPi na -12V zdroja.
To je fyzicke zapojenie.

Co sa tyka konfiguracie programu, nastavuje sa (zatial), cez konfiguracny subor.
Mozes si ho nazvat ako-kolvek, ale pri spustani budes musiet zadat prepinac -c a cestu k suboru.
Ma to strukturu INI suboru, t.j. do spravnej sekcie musis dat spravny parameter.
Zatial su len 3 sekcie TEMPERATURE, SENSOR a FAN.
Takto to v podstate vyzera:

	[TEMPERATURE]
	#mandatory
	limit_temperature =
	#optional
	#interval =
	#retention =
	[SENSOR]
	#mandatory
	sensor_id =
	[FAN]
	#optional
	#gpio_pin =

**Popis premennych**

`[TEMPERATURE]`

`limit_temperature` -> **povinny** parameter. Cislo s desatinnou ciarkou (alebo bodkou). Hodnota v stupnoch celzia, na ktoru bude program reagovat a pustat/vypinat ventilator(y)
`interval` -> nepovinny parameter. Cele cislo. Hodnota v sekundach, casovy rozostup medzi jednotlivymi meraniami. Defaultna hodnota je 60 sekund
`retention` -> nepovinny parameter. Cele cislo. Mnozstvo merani, z ktorich sa bude robit priemer teplot, aby sme nespinali ventilator v pripade oscilacie okolo limitnej teploty

`[SENSOR]`
`sensor_id` -> povinny parameter. Retazec. Seriove cislo senzora, ktory bude zdrojom teploty.
`sensor_id = 28-011316cda976`

`[FAN]`
`gpio_pin` -> (ne)povinny parameter. Cele cislo. Defaultny je cislo 17. Cislo GPIO pinu, na ktory je pripojena Brana/Gate z MOSFET-u.

**Spustanie**


Nutna prerekvizita (ako pri LED-kach), **musi** bezat **PiGPIO** (sudo pigpiod)
Mozes ist na to dvoma sposobmi.
1. Bud si nainstalujes python packages z requirements.txt (pip install -r requirements.txt) - odporucam cez virtual environmentsa budes to spustat cez nastavenie **venv** a `python cooler_control.py -c config.txt`
priklad:

		meego@raspberrypi:~/python_projects/rpi_temp $ source .venv/bin/activate
		(.venv) meego@raspberrypi:~/python_projects/rpi_temp $
		(.venv) meego@raspberrypi:~/python_projects/rpi_temp $ python cooler_control.py -c config.ini
		Reading configuration file config.ini
		Key [FAN][gpio_pin] not present in config file
		Key [FAN][gpio_pin] is optional, setting value to default (17)
		Configuration parsed. Using:
		
		Sensor: 28-011316cda976
		Number of measurements: 3
		Interval between measurements: 3
		Limit temperature: 23.85
		
		[23.812]
		Nothing to delete
		28-011316cda976 23.812[23.437, 23.875, 26.437]
		28-011316cda976 24.583000000000002
		2023-01-16 20:40:32.957774: Temeperature rose above limit 23.85. Current temperature is 24.583000000000002. Starting FAN.
		...
		...
		[23.875, 23.812, 23.812]
		28-011316cda976 23.833000000000002
		2023-01-16 20:46:46.141581: Temperature fell under limit 23.85. Current temperature is 23.833000000000002. Shutting down FAN.
		...
		...

*alebo*

2. pouzijes binarku, ktora sa nachadza v dist - binarka ***nie je*** otestovana na inom RPi ako mojom.
`./cooler_control -c config.txt`
(alebo si cestu na binarku das do $PATH a potom bez ./cooler_control)

Priklad:

	meego@raspberrypi:~/python_projects/rpi_temp $ ./cooler_control -c config.ini
	Reading configuration file config.ini
	Key [FAN][gpio_pin] not present in config file
	Key [FAN][gpio_pin] is optional, setting value to default (17)
	Configuration parsed. Using:
	Sensor: 28-011316cda976
	Number of measurements: 3
	Interval between measurements: 3
	Limit temperature: 23.85
	[23.437]
	Nothing to delete
	28-011316cda976 23.437
	[23.437, 23.437]
	Nothing to delete
	28-011316cda976 23.437
	[23.437, 23.437, 23.875]
	28-011316cda976 23.583000000000002
	[23.437, 23.875, 26.437]
	28-011316cda976 24.583000000000002
	2023-01-16 20:40:32.957774: Temeperature rose above limit 23.85. Current temperature is 24.583000000000002. Starting FAN.
	...
	...
	...
	[23.875, 23.812, 23.812]
	28-011316cda976 23.833000000000002
	2023-01-16 20:46:46.141581: Temperature fell under limit 23.85. Current temperature is 23.833000000000002. Shutting down FAN.
	[23.812, 23.812, 23.812]

To by malo byt vsetko. Keby nieco, pis volaj, posielaj postove holuby, alebo skrecky.