## IT Terminvergabesystem Impfzentrum
# Datenschutzfolgeabschätzung
Durch den Betrieb eines IT gestützten System für die Buchung und Vergabe von Impfterminen an Personen und die damit zusammenhängende Verarbeitung personenbezogener Daten der impfwilligen Personen kann der Verlust der personenbezogenen Daten bzw. der Zugriff von Unberechtigten nicht vollständig ausgeschlossen werden. In der hier vorliegenden Datenschutzfolgeabschätzung nach §67 Bundesdatenschutzgesetz werden daher die mit Hilfe der Software durchgeführten Vorgänge erläutert und nach datenschutzrechtlichen Gesichtspunkten bewertet.
Das IT Terminvergabesystem des Impfzentrums wird für die Verwaltung von Impfungen, sowie dem Versand von Terminbestätigungen verwendet. Im Folgenden werden erläutert:
1. Zweck der Datenverarbeitung
2. Erhobene Daten
3. Beschreibung der Vorgänge
4. Zugriffsrechte in der Webapp und Speicherdauer der erhobenen Daten
5. Bewertung der Gefahren für die Rechtsgüter betroffener Personen
6. Sicherheitsmaßnahmen
7. Bewertung von Notwendigkeit und Verhältnismäßigkeit der Vorgänge

## 1. Zweck der Datenverarbeitung
Zweck der Verarbeitung ist die Schaffung einer Onlineplattform für die Terminvergabe im Impfzentrum des DRK KV Odenwaldkreis e.V.

## 2. Erhobene Daten
Mit Hilfe einer Webapplikation werden die Daten der Person in einer zentralen Datenbank auf einem Webserver erfasst.
### Anmeldedaten
Die in dieser Datenbank gespeicherten personenbezogenen Daten bestehen aus der Kombination von laufender Nummer, zufälligem Registrierungstoken, Anmeldezeitpunkt, Vorname, Nachname, Telefonnummer, Adresse, Geburtsdatum, Emailadresse, Impfstoff sowie Impftermin. 

## 3. Beschreibung der Vorgänge
### Anmeldung zu einer Covid Impfung
Personen, die sich für einen Impfung interessieren, können sich online, mit Angabe ihrer Daten inklusive Emailadresse, für eine Impfung anmelden.
Die zu impfenden Personen können sich für einen freien Termin im Impfzentrum anmelden und bekommen zur Verifizierung eine E-Mail zugeschickt, die sie bestätigen müssen. Mit Hilfe einer Webapplikation werden die Daten der Person in der zentralen Anmelde-Datenbank auf einem Webserver erfasst. Mit der Registrierung bekommen die zu impfenden Personen eine Terminbestätigung ausgestellt. 
Bei der Registrierung über die Website werden die zu impfenden Personen über die Erfassung der personenbezogenen Daten aufgeklärt. Die Buchung eines Impftermins ist nur möglich wenn der Erfassung der personenbezogenen Daten explizit zugestimmt wird.
### Ablauf im Impfzentrum
Mit Hilfe der Terminbestätigung können die Personen beim Impfzentrum die Buchung eines Termins für eine Impfung gegen SARS Cov2 nachweisen. Dazu gleicht der Mitarbeiter an der Anmeldung die Daten der Person mit einer Liste aller Termine an diesem Tag in der Webapplikation ab.
Hier endet der Einsatz des hier beschriebenen Systems. Alle weiteren Daten, die für die Impfung erfasst werden, werden in auf einem gesonderten Weg, nicht in dem hier beschriebenen System, erfasst.
## 4. Zugriffsrechte in der Webapp und Speicherdauer der erhobenen Daten
### Zugriffsrechte in der Webapp
In der Webapp des Impfzentrums gibt es einen öffentlichen und einen internen Bereich. Aus dem öffentlichen Bereit sind einzig die online Buchung von Terminen für die Impfung und Abruf von generellen Informationen möglich.
Die Nutzung des internen Bereichs der Webapp ist nur Mitarbeitern des Impfzentrums möglich. Der Zugang ist Passwort geschützt. Im internen Bereich der Webapp existieren folgende Rollen mit unterschiedlichen Berechtigungen:
* Mitarbeiter des Impfzentrum: Mitarbeiter des Impfzentrum können alle Termine im Impfzentrum einsehen und bestätigen, dass der Termin wahrgenommen wurde.
* Backoffice: Kann alle Vorgänge in der Datenbank einsehen, Kann Datensätze korrigieren, Anlegen von Impfstationen und Terminen, 
* Administrator: Vollständiger Zugriff auf die Datenbank.

### Speicherdauer für Anmeldungen
Die Anmeldedaten werden bis zum Ablauf des nächsten Tages nach dem gebuchten Termin gespeichert (Termine können max. 14 vorher möglich, d.h. die maximale Speicherdauer beträgt 15 Tage. In der Regel wird die reelle Speicherdauer jedoch deutlich unter 15 liegen.). Die Kunden können weiterhin eine Voranmeldung auch selbstständig stornieren, ihr Datensatz wird dann nach spätestens 30min aus der Datenbank gelöscht und der Termin wieder freigegeben.

## 5. Bewertung der Gefahren für die Rechtsgüter betroffener Personen
Als wesentliche Gefahren beim Einsatz des hier beschriebenen Terminbuchungssystem lassen sich der Verlust der gespeicherten Daten, unautorisierter Abruf der personenbezogenen Daten sowie unautorisierte Veränderungen der personenbezogenen Daten feststellen. Verfahren zur Gefahrenvermeidung und Sicherheitsvorkehrungen werden im nächsten Abschnitt erläutert.

## 6. Sicherheitsmaßnahmen
Die zentrale Datenbank wird auf einem virtuellen Server in einem kommerziellen Rechenzentrum vorgehalten und ist daher durch den Betreiber des Rechenzentrums vor Datenverlust geschützt.
Die zentrale Datenbank, und alle Komponenten der Webapplikation liegen auf Servern der Firma Contabo GmbH. Die Server befinden sich in Deutschland und mit der Firma Contabo wurde eine Vereinbarung zur Auftragsdatenverarbeitung geschlossen. Zum Server haben nur die Administratoren der Webapp Zugang, auch Mitarbeiter der Firma Contabo haben keinen Zugriff. Alle Kommunikation mit der Webapp und der zentralen Datenbank sind TSL verschlüsselt. Alle internen Komponenten der Webapplikation sind passwortgeschützt (Nach 6 fehlgeschlagenen Loginversuchen wird der betreffende Account bis auf weiteres gesperrt.) und können nur von autorisierten Mitarbeitern aufgerufen werden. Passwörter werden nicht im Klartext sondern nur als Hashwert gespeichert. Die verwendete Software zum Betrieb von Server, Datenbank und Webapp wird von den Administratoren auf dem neuesten Stand gehalten. Somit ist ein ausreichender Schutz gegen unautorisierte Zugriffe gewährleistet. Der Emailserver wird von der Firma domainfactory GmbH betrieben. Auch zu diesem Server haben nur die Administratoren der Webapp Zugang. Eine Vereinbarung zur Auftragsdatenverarbeitung wurde geschlossen. Nur authentifizierte Mitarbeiter des Impfzentrum können Terminbuchungen eintragen oder bestehende Datensätze ändern. 
Es besteht immer ein Backup der aktuellen Datenbank auf einem unabhängigen Server. 
Weiter setzten wir auf das Prinzip der Datensparsamkeit. Wir erheben für die Anmeldung nur absolut notwendige Daten: Name und Vorname sowie zufälliger Token für die Authentifizierung der Person, Telefonnummer und Email-Adresse zur eventuellen Kontaktaufnahme, beispielsweise bei Ausfall des Termins sowie Datum und gewählte Impfstation des Termins. Ansonsten erheben wir nur den Zeitstempel der Anmeldung und evtl. Zeitstempel einer Änderung des Datensatzes da dies, falls irgendwann ein technisches Problem mit der Datenbank bestehen sollte, zum debugging hilfreich sein kann.

## 7. Bewertung von Notwendigkeit und Verhältnismäßigkeit der Vorgänge
Die Rechtsgrundlage zur Erfassung und Verarbeitung der personenbezogenen Daten sind Art. 6 Abs. Lit a sowie 1 Art. 9 Abs. 2 lit. a und i DSGVO. Durch die elektronische Verarbeitung der Daten ergeben sich entscheidende Vorteile:
* Eine generelle Erfassung von Terminen ist notwendig, da genug Fachpersonal und Impfstoffe und Zeit für die Impfung vorhanden sein müssen.
* Durch den Einsatz der Online-Plattform mit angeschlossener Datenbank ist die Anmeldung schnell und problemlos für die impfwilligen Personen selbst durchführbar.
* Durch den Einsatz der Webapp haben sowohl Impfwillige einen immer aktuellen Überblick über die freien Termine als auch Mitarbeiter im Impfzentrum immer einen aktuellen Überblick über die gebuchten Termine.

Nach Abwägung der oben genannten Vorteile gegen die von uns als minimal angesehenen Gefahren für Rechtsgüter der betroffenen Personen bewerten wir den Einsatz einer IT gestützten Lösung zur Erfassung von Impfterminen als verhältnismäßig.

