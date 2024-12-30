# Urzicarius Battle

## Descriere:

Urzicarius Battle este un joc plaformer cu o mica poveste.Vine anul 3,iar un student la Politehnica decide sa aplice in mai multe locuri cu CV-ul,fiind toamna,aplica la toate firmele mari,inclusiv Google.Urzicarius,personajul nostru,s-a atrenat un an pe LeetCode si are 1000 de probleme rezolvate,weekly challenge-uri multe la activ,CV consistent si in final primeste coding challenge.A trecut cu brio de coding challenge,iar acum urmeaza Interviul Tehnic pentru care a avut timp sa se pregateasca o luna jumate.Protagonistul nostru,Urzicarius trebuie sa invinga un Senior SW Engineer la Google de 10 ani.Make Urzicarius a Googler!

## Texturile:

Implementate from scratch,facute intr-o nota usor umoristica asupra protagonistului nostru,imaginea de Win reprezentand viitorul lui Urzicarius la Google,iar imaginea de Game Over,viitorul acestuia dupa 2 ani de aplicat constant.

## Obiectivele proiectului:

1.  Familiarizarea cu pygame si cu limbajul de programare Python
2.  Intelegerea programarii OOP in Python folosind clase pentru implementare
3.  Operarea cu diverse functionale

## Executare comenzi:

Urzicarius are urmatoarele comenzi:

- Miscare stanga: A sau Key Left
- Miscare dreapta: D sau Key Right
- Atac: Space
- Saritura: W

## Implementare:

Am implementat multiple clase in vederea implementarii:

- Clasa Player:
  - functia `draw()` unde se va afisa personajul nostru,health bar-ul animat si arma in diverse pozitii in functie de directia personajului
  - functia `move()` unde se vor implementa miscarile stanga,dreapta,saritura si unde se vor specifica limitele pentru ca personajul nostru sa nu cada de pe harta,cat si imposibilitate de a trece prin pereti
  - functia `get_damage()` unde se va implementa logica atunci cand personajul primeste damage de la enemy
  - functia `get_health()` unde se va implementa logica atunci cand se da pick up la medkit
  - functia `basic_health()`unde se regaseste logica pentru health bar,alaturi de animatie
  - functia `animate_idle()` unde am incercat imitarea unui sprite folosindu-ne de biblioteca math scaland imaginea usor in fata si in spate
- Clasa Enemy:
  - functia `draw()` idem cu cea de la Player
  - functia `update()` unde specificam comportamentul inamicului in functie de pozitia lui Urzicarius
  - functia `attack()` unde exista implementarea pentru atacarea lui Urzicarius
  - functia `get_damage()` idemn cu cea de la Player
  - functia `basic_health()` idem cu cea de la Player
- Clasa Bullet:
  - functia `update()` unde se specifica comportamentul glontului atunci cand loveste zidurile sau cand loveste adversarul
- Clasa Medkit
- Clasa Wall:
  - functia `draw()` de afisare a zidurilor
- Clasa Weapon

## Modul de desfasurare al jocului:

Main Menu principal in care se poate iesi din joc sau incepe jocul cu hover asupra butoanelor.Urzicarius trebuie sa gaseasca cat mai repede arma si sa si infranga adversarul.In caz ca pierde multa viata trebuie sa si ia medkit pentru a infrange cat mai repede si a trece la interviul de HR.Inamicul nostru,intervievatorul,nu ne va lasa in pace si va veni constant dupa noi.

## Probleme intalnite de-a lungul proiectului:

1. Una din principalele probleme aparute,inca de la inceput reprezenta prezenta dreptunghiului care reprezenta inamicul nostru.Chiar daca apelam `.kill()` asupra sprite-ului,dreptunghiul inca a ramas.Ulterior am setat dreptunghiul cu caracteristici nule `self.rect = pygame.Rect(0, 0, 0, 0)`.
2. Atunci cand trageam gloantele nu tineam cont de atributul de flip,mai mult de pozitie,iar de fiecare data tragea din cap,nu din arma,din cauza faptului ca acolo se termina dreptunghiul nostru.In schimb,in urma schimbarii atributului cu flip a functionat.
3. Problema la restart in urma win sau game over asupra animatiei de health bar player.Implementarea in clasa `basic_health()` includea aceasta linie de cod `if not hasattr(self, 'displayed_health'):self.displayed_health = self.health`,ceea ce insemna ca atributul era adaugat,dar doar local,neexistand ca si atribut al clasei,neputand sa l resetam.
