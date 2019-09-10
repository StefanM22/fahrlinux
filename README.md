 
Script zum auslesen der Fahrerkarte von DigitalenTachographen


Copyright 2009 / 2014 Stefan Manteuffel linux@sm-recycling.de
Die Software habe ich 2009 geschrieben, läuft aber bei mir unter Opensuse Tumbleweed (2019) noch immer.


pyscard wir benötigt http://sourceforge.net/projects/pyscard/

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

zum Starten der Anwendung fahrlinux.py aufrufen.

Im linken Teil der Anwendung erscheint eine Auswahl der Card Reader und der SmartCard.
Durch doppelklick. Die Karte wählen und dann auf Start drücken.

Die datei wird im aktuellen Verzeichniss gespeichert. Das Downloaddatum wird noch nicht zurückgesetzt.


Die Karte kann ausgelesen werden und die DDD datei kann mittels des Tools auf :

http://webdemo.opendtacho.org/
in eine XML Datei konvertiert werden.

Als Daemon muss openct und pcscd laufen.
chipcardd3 DARF NICHT laufen.

Sollten die Rechte für den Reader nicht richtig gesetzt sein, so kann das mit der 
udev regel in 

/etc/udev/rules.d pcscd_ccid.rules and insert your Card Reader like this:
# SCR3311.txt
SUBSYSTEMS=="usb", ATTRS{idVendor}=="04e6", ATTRS{idProduct}=="511d", MODE="0666"
geändert werden.

01/2014

Da es bei mir unter Opensuse 12.3. nicht mehr laufen wollte, hab 
ich eine Fehlerbehandlung für die Kartenabfrage eingebaut.
Es lag nicht an Opensuse sondern an einer defekten Karte.

In fahrlinux define DEBUG ein/ausschalten.

Es wird ein Verzeichnss Download angelegt und die Auswertung dortin verschoben.

Es gibt immer wieder Probleme mit dem cardreader.
Wichtig ist natürlich das dieser richtig eingerichtet ist.
Ich verwende immer noch den SCR3311

Um dem Card reader auf die Spur zu kommen, empfihlt es sich den pcscd in der Konsole mit "pcscd -fd" zu starten, dann hat man die Debugging ausgaben um
zu sehen ob es am dem card Reader liegt.

Um die Daten Auszuwerten eignet sich http://sourceforge.net/projects/readesm/ sehr gut.

Vieleicht hat ja mal jemand lust die beiden Programme zusammenzu bauen.

Die Lesefunktion hab ich im Code Dokumentiert.

viel Spass
Stefan
