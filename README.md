# meetingScheduler
Proiect de tip A la Python.

Proiectul reprezinta o aplicatie GUI in tkinter pentru managementul unor meetinguri. Aplicatia se conecteaza la o baza de date PostgreSQL pentru a face modificarile necesare. 

Prin intermediul acesteia putem adauga o persoana in baza de date care are un nume, prenume si o adresa de email unica.
De asemenea, putem programa un meeting caruia trebuie sa ii dam un nume, o data de desfasurare si orele de start si stop pentru acesta. De asemenea, putem seta si verifica ce persoane vrem sa participe la acest meeting, selectand adresele de mail ale persoanelor din baza de date.

Un alt feature al aplicatiei este acela de a putea vizualiza meetingurile dintr-un anumit interval de timp, si informatii despre acestea cum ar fi data si orele de desfasurare precum si optional ce participanti are respectivul meeting.

Cu ajutorul aplicatiei putem exporta un calendar atat in formatul .ical cat si in formatul .ics. Exportul se face la toate meetingurile din baza de date impreuna cu participantii si detaliile despre fiecare meeting.
Putem face si import a unui calendar in format .ics sau .ical, moment in care se introduc in baza de date meetingurile din calendrul respectiv, persoanele nu se vo introduce in baza de date.

Pentru a porni proiectul se ruleaza fisierul app.py. In fisierul DB_manager.py sunt implementate actiunile directe cu baza de date.
Dependintele necesare proiectului sunt urmatoarele pachete: psycopg2(conexiunea la baza de date), tkinter(interfata grafica), PIL(imagini), tkcalendar(calendar gui), ics(parsare calendar), datetime(parsare data), re(regex).

In folderul rce se gaseste documentatia proiectului in format html. In folderul programs se gasesc calendare in format .ics si .ical cu care am facut teste pentru import si export.

