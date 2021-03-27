# PHP Logger

Výpis je na adrese: http://covid.martinpolacek.eu

- Řazen od nejnovějších
- Čas je stanoven podle data zapsání do DB

Zápis dat pomocí adresy: http://covid.martinpolacek.eu/writeLog.php

Přijímá dva parametry:

- <strong>type</strong> - důležitost logu
    - 0 - informační log
    - 1 - varovný log
    - 2 - error log
- <strong>text</strong> - popis o co se jedná

Dotaz se musí poslat jako <strong>POST</strong> nikoliv jako GET.

