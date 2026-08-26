# Urzicarius Battle

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=for-the-badge&logo=pygame)

<div align="center">
  <h3>Make Urzicarius a Googler!</h3>
  <p><i>Un joc platformer despre interviul de vis la Google</i></p>
</div>

---

## Povestea

Vine anul 3, iar un student la Politehnica decide să aplice în mai multe locuri cu CV-ul. Fiind toamnă, aplică la toate firmele mari, inclusiv **Google**.

**Urzicarius**, personajul nostru, s-a antrenat un an pe **LeetCode**: are **1000 de probleme rezolvate**, multe weekly challenge-uri la activ și un CV consistent. Primește coding challenge-ul și trece cu brio de el.

Acum urmează **Interviul Tehnic**, pentru care a avut timp să se pregătească o lună și jumătate. Protagonistul nostru trebuie să învingă un **Senior SW Engineer la Google de 10 ani**.

**Make Urzicarius a Googler!**

---

## Texturile

> Toate texturile sunt create **from scratch**, făcute într-o notă ușor umoristică:
> - **Imagine Win**: Reprezintă viitorul lui Urzicarius la Google
> - **Imagine Game Over**: Viitorul acestuia după 2 ani de aplicat constant

---

## Obiectivele Proiectului

| # | Obiectiv |
|---|----------|
| 1 | Familiarizarea cu **pygame** și cu limbajul de programare **Python** |
| 2 | Înțelegerea programării **OOP** în Python folosind clase pentru implementare |
| 3 | Operarea cu diverse funcționalități și concepte avansate |

---

## Instalare Rapidă

```bash
# 1. Clonează repository-ul
git clone https://github.com/deniz2104/Stickman-Battle.git
cd Stickman-Battle

# 2. Creează un virtual environment
python -m venv venv

# 3. Activează virtual environment
# Pe macOS/Linux:
source venv/bin/activate
# Pe Windows:
# venv\Scripts\activate

# 4. Instalează dependențele
pip install -r requirements.txt

# 5. Pornește jocul
python -m src.main
```

---

## Controale

| Acțiune | Taste |
|---|---|
| Mișcare Stânga | `A` sau `←` |
| Mișcare Dreapta | `D` sau `→` |
| Atac | `Space` |
| Pauză | `Esc` |

---

## Cum se joacă

```
                        MAIN MENU
                     [START]  [QUIT]
                          |
                          v
                       GAMEPLAY
        Urzicarius  <-------------->  Senior Engineer
                          |
                +---------+---------+
                v                   v
           GAME OVER               WIN
        [RESTART] [QUIT]     [RESTART] [QUIT]
```

Obiective:
1. **Găsește arma**: spawn-uri random când nu ai gloanțe.
2. **Colectează medkit-uri**: apar când ai viață scăzută.
3. **Învinge Senior Engineer-ul**: evită să te prindă.
4. **Supraviețuiește**: health bar animat care te ține la curent.

---

## Arhitectura Proiectului

Proiectul e organizat pe straturi: `core` (motor de joc), `entities` (obiecte din joc, ierarhie OOP) și `ui` (interfață), toate sub un singur pachet `src`.

```
Stickman-Battle/
└── src/
    ├── main.py                  # bucla principală (orchestrator)
    ├── core/
    │   ├── config.py            # constante globale, fereastra pygame, load_texture()
    │   ├── game_init.py         # construiește starea inițială a jocului
    │   ├── handlers.py          # event handling pentru fiecare stare a jocului
    │   └── spawn.py             # logica de spawn pentru armă și medkit
    ├── entities/
    │   ├── base_classes.py      # ierarhia OOP de bază (GameObject, HealthEntity, MovableEntity, CollectibleItem)
    │   ├── player.py            # Urzicarius: mișcare, animație, armă
    │   ├── enemy.py             # Senior Engineer: urmărire și atac
    │   ├── bullet.py            # traiectorie și coliziuni ale gloanțelor
    │   ├── medkit.py            # item colectabil, vindecă jucătorul
    │   ├── weapon.py            # item colectabil, echipează arma
    │   └── wall.py              # limitele orizontale ale hărții
    ├── ui/
    │   ├── button.py            # butoane interactive (hover, click)
    │   └── render.py            # desenarea fundalului și a HUD-ului
    └── textures/                # toate asset-urile grafice
```

---

## Detalii de Implementare

### Ierarhia entităților (OOP)

`base_classes.py` definește lanțul de moștenire folosit de toate obiectele din joc:

- `GameObject(pygame.sprite.Sprite, ABC)`: încarcă imaginea/masca de coliziune, poziționează sprite-ul;
- `HealthEntity(GameObject)`: adaugă viață, damage/heal și desenarea barii de viață (cu efect de „delay” la damage).
- `MovableEntity(HealthEntity)`: adaugă viteză, direcție și flip; `update()` e abstractă și implementată de `Player`/`Enemy`.
- `CollectibleItem(GameObject)`: bază pentru `Weapon` și `Medkit`; `use(player)` metodă abstractă și aplică efectul la coliziune.

### Gameplay

- **`player.py`**: `Player(MovableEntity)` gestionează mișcarea orizontală cu coliziune asupra zidului, animația idle  și desenarea armei în funcție de orientare.
- **`enemy.py`**: `Enemy(MovableEntity)` urmărește jucătorul pe axa X și aplică damage continuu la contact.
- **`bullet.py`**: `Bullet` se deplasează pe direcția de tragere, verifică coliziunea cu inamicul (mask collision) și cu pereții, apoi dispare.
- **`weapon.py`** / **`medkit.py`**: la coliziune cu jucătorul, echipează arma respectiv vindecă, apoi dispar de pe hartă.
- **`wall.py`**: delimitează harta pe orizontală și blochează mișcarea jucătorului.

### Motorul de joc (`core/`)

- **`config.py`**: constante globale (`SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`), fereastra și fontul pygame, `load_texture()` cu fallback pe un placeholder magenta dacă imaginea lipsește.
- **`game_init.py`**: `create_context()` construiește un dicționar cu toată starea jocului: player, enemy, grupuri de sprite-uri, UI, evenimente de spawn programate.
- **`handlers.py`**: o funcție de handling per stare a jocului (`menu`/`running`/`paused`/`game_over`), procesează input-ul de la tastatură și mouse.
- **`spawn.py`**: spawnează arma random cât timp jucătorul nu are gloanțe, respectiv medkit-ul când viața scade sub un prag.

### `main.py`

`main()` rulează bucla principală: creează contextul, comută între desenare/update în funcție de `game_state`, delegă la `spawn`/`handlers`/`render`, verifică condițiile de win/lose și apelează `pygame.display.update()` la fiecare cadru. La fiecare foc de armă, `make_screen_dynamic()` generează un mic efect de shake pentru ecran.

---

## Probleme Întâlnate și Soluții

<details>
<summary><b>1. Dreptunghiul Inamicului Persista După <code>.kill()</code></b></summary>

**Problema:** Chiar dacă apelam `.kill()` asupra sprite-ului, dreptunghiul inamicului rămânea vizibil.

**Soluție:** Am setat manual dimensiunile dreptunghiului la valori nule:
```python
self.rect = pygame.Rect(0, 0, 0, 0)
```

</details>

<details>
<summary><b>2. Gloanțele Trăgeau Din Cap, Nu Din Armă</b></summary>

**Problema:** Nu țineam cont de atributul `flip`, iar gloanțele se spawnau mereu în același loc (capul personajului).

**Soluție:** Am implementat logică condițională bazată pe `player.flip`:
```python
if player.flip:
    bullet = Bullet(player.rect.left, player.rect.centery + 15, ...)
else:
    bullet = Bullet(player.rect.right, player.rect.centery + 15, ...)
```

</details>

<details>
<summary><b>3. Health Bar Nu Se Reseta La Restart</b></summary>

**Problema:** Atributul `displayed_health` era adăugat local în funcție și nu ca atribut al clasei.

**Soluție:** Am mutat inițializarea în `__init__()` pentru a fi accesibil global:
```python
def __init__(self, ...):
    # ... alte atribute ...
    self.displayed_health = self.health
```

</details>

<details>
<summary><b>4. Inamicul Nu Se Spawna După Win</b></summary>

**Problema:** După ce câștigai, la restart inamicul nu mai apărea pentru că obiectul mort era reutilizat.

**Soluție:** Creăm o instanță nouă de `Enemy` la fiecare restart:
```python
enemy = Enemy(680, 340, 1, 'big_boss.png')
context['enemy_group'].add(enemy)
context['enemy'] = enemy
```

</details>

---

## Tehnologii Utilizate

- **Python 3.12+**
- **Pygame 2.6.1**
- **ABC (Abstract Base Classes)**: pentru ierarhia OOP a entităților
- **Math**: pentru animații și mișcare
- **Random**: pentru spawn-uri
