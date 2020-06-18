# 0. CSV-Filter
Dieser CSV-Filter wurde entwickelt um aus einer Quell-CSV-Datei Daten zu lesen und nur die freigegebenen Spalten in eine Ziel-CSV-Datei zu übertragen.

Das CLI basierende Skript wurde auf Basis von Flask entwickelt.

## 1. Abhängigkeiten
Die benötigten Abhängigkeiten sind gewohnt in der `requirements.txt` zu finden und lassen sich mit `pip install -r requirements.txt` erfüllen.

## 2. Start des Skripts
Nachdem alle Abhängigkeiten erfüllt wurden muss sichergestellt werden, dass die Umgebugsvariable `FLASK_APP` (siehe 2.1) gesetzt wurde. Danach kann die Anwendung wie folgt gestartet werden: `flask convert input.csv output.csv pattern.json`

Der hier genannte Prozess lässt sich auch in einer Batch oder einem Shellskript zusammenfassen. Siehe 4.

### 2.1 Umgebungsvariablen
Da das Skript auf FLASK basiert, können/müssen über Umgebungsvariablen einige Einstellungen vorgenommen werden:
|Variable|Bedeutung|Optional|Beispiel|
|---------|--------|-|--------|
|`FLASK_APP`|Gibt an, welches Skript von flask gestartet werden soll. Für unseren Fall müssen wir den Pfad zur `convert.py` angeben.|Nein|`FLASK_APP=convert.py`|
|`FLASK_DEBUG`|Gibt an, ob das Skript im Debugmodus gestartet werden soll. Hierbei werden erheblich mehr Log-Meldungen erzeugt.|Ja|`FLASK_DEBUG=TRUE`|

### 2.2 Startparameter
|Parameter|Bedeutung|
|---------|---------|
|convert  | Zur Zeit beherrscht das Skript nur die Funktion die unter 0. beschrieben wurde|

### 2.2.1 Argumente für `convert` 
|Parameter|Bedeutung|Optional|
|---------|---------|--------|
|`INPUT`|Pfad zur Quell-CSV-Datei|Nein|
|`OUTPUT`|Pfad zur Ziel-CSV-Datei. Diese Datei muss nicht vor dem Start des Skripts existieren. Sie wird angelegt oder ggf. überschrieben.|Nein|
|`PATTERN`|Pfad zur Pattern-JSON-Datei|Nein|

Die Argumente werden vom Skript in der Reihenfolge `INPUT OUTPUT PATTERN` erwartet.
 
Ein gültiger Aufruf kann wie folgt aussehen: `flask convert input.csv output.csv pattern.json`




## 3. Konfiguration - pattern.json
Das Verhalten des Konverters lässt sich über die `pattern.json` oder einer beliebigen anderen JSON-Datei (siehe 2.2.1 Startparameter) steuern.

Folgende Parameter müssen in der JSON-Datei zwingend angegeben werdem:
|Parameter|Bedeutung|Beispiel|
|---------|---------|--------|
|`delimiter`|Gibt sowohl für die Quell-, als auch für die Ziel-CSV-Datei an, welche(s) Zeichen zum trennen der Spalten verwendet werden soll.|`","` oder `";"` etc.|
|`quotechar`|Gibt für die Quell-, als auch für die Ziel-CSV-Datei an, welcher Charakter benutzt werden soll, Texte einer Zelle zu Umranden, welche den definierten Delimiter enthalten|`"\""` oder `"^"` etc. |
|`ignore_first_line`|Oft wird bei einer CSV-Datei auch eine Header-Zeile mitgeliefert, welche die Spalten beschreibt. Mit diesem Parameter wird gesteuert, ob diese Zeile mitkopiert werden soll|`true` oder `false`|
|`schema`|Gibt an welche Spalten kopiert werden sollen. Hierzu wird ein Array von Booleans übergeben. Für jede Spalte muss ein Boolean übergeben werden. Die Reihenfolge der Booleans im Array entspricht der Reihenfolge der Spalten in der Quell-CSV-Datei.|`[true, true, true, true, true, true, false, true, true]`|
|`logging.logToFile`|Gibt an ob zusätzlich eine Logdatei angelegt werden soll. Logdateien werden max 5MB groß. Danach bekommt die Logdatei den Suffix .1 / .2 etc. und es wird eine neue Logfile angelegt. Es werden maximal fünf Vorgänger aufgehoben.|`true` oder `false`|
|`logging.logfile`|Gibt den Pfad zur Logdatei an.|`C:/logs/converter.log`|

## 4. Beispiele
Dieses Skript kommt mit exemplarischen Daten für die Quelldatei: `input.csv` bzw. `input_with_header.csv` , der Zieldatei: `output.csv` und der Konfigurationsdatei: `pattern.json`. Ferner findet sich ein möglicher Aufbau einer Batchdatei in `convert.bat`.
