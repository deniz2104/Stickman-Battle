# 🎮 Urzicarius Battle

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=for-the-badge&logo=pygame)

<div align="center">
  <h3>🚀 Make Urzicarius a Googler! 🚀</h3>
  <p><i>Un joc platformer despre interviul de vis la Google</i></p>
</div>

---

## 📖 Povestea

Vine anul 3, iar un student la Politehnica decide să aplice în mai multe locuri cu CV-ul. Fiind toamnă, aplică la toate firmele mari, inclusiv **Google**. 

**Urzicarius**, personajul nostru, s-a antrenat un an pe **LeetCode** și are **1000 de probleme rezolvate**, weekly challenge-uri multe la activ, CV consistent și în final primește coding challenge-ul. 

✅ A trecut cu brio de coding challenge!  
🎯 Acum urmează **Interviul Tehnic** pentru care a avut timp să se pregătească o lună jumătate.  
⚔️ Protagonistul nostru trebuie să învingă un **Senior SW Engineer la Google de 10 ani**.

**Make Urzicarius a Googler!** 🏆

---

## 🎨 Texturile

> 🖼️ Toate texturile sunt create **from scratch**, făcute într-o notă ușor umoristică:
> - **🏆 Imagine Win**: Reprezintă viitorul lui Urzicarius la Google
> - **💔 Imagine Game Over**: Viitorul acestuia după 2 ani de aplicat constant

---

## 🎯 Obiectivele Proiectului

| # | Obiectiv |
|---|----------|
| 1️⃣ | Familiarizarea cu **pygame** și cu limbajul de programare **Python** |
| 2️⃣ | Înțelegerea programării **OOP** în Python folosind clase pentru implementare |
| 3️⃣ | Operarea cu diverse funcționalități și concepte avansate |

---

## 🚀 Instalare Rapidă

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

# 5. Pornește jocul! 🎮
python Scripts/project.py
```

---

## 🎮 Controale

<table>
  <tr>
    <th>⌨️ Acțiune</th>
    <th>🕹️ Taste</th>
  </tr>
  <tr>
    <td>⬅️ Mișcare Stânga</td>
    <td><kbd>A</kbd> sau <kbd>←</kbd></td>
  </tr>
  <tr>
    <td>➡️ Mișcare Dreapta</td>
    <td><kbd>D</kbd> sau <kbd>→</kbd></td>
  </tr>
  <tr>
    <td>🔫 Atac</td>
    <td><kbd>Space</kbd></td>
  </tr>
</table>

---

## 🏗️ Arhitectura Proiectului

Proiectul a fost refactorizat pentru o mai bună organizare a codului.

### 📁 Structura Fișierelor

```
Stickman-Battle/
├── 📄 Scripts/
│   ├── 🎯 project.py          #  main game loop
│   ├── ⚙️ config.py            # Configurări globale și constante
│   ├── 🧬 base_classes.py      # Clase abstracte de bază (OOP)
│   ├── 👤 player.py            # Logica jucătorului (Urzicarius)
│   ├── 👹 enemy.py             # Logica inamicului (Senior Engineer)
│   ├── 🔫 bullet.py            # Logica gloantelor
│   ├── 💊 medkit.py            # Logica pentru medkit
│   ├── 🗡️ weapon.py            # Logica pentru pistol
│   ├── 🧱 wall.py              # Logica pentru ziduri
│   ├── 🎨 button.py            # UI și butoane interactive
│   ├── 🎬 game_init.py         # Inițializare context joc
│   ├── 📦 spawn.py             # Logica de spawn pentru obiecte
│   ├── 🎛️ handlers.py          # Event handling pentru toate stările
│   └── 🖼️ render.py            # Funcții de desenare și HUD
└── 📄 Textures/                # Toate asset-urile grafice
```

---

## 🔧 Implementare Detaliată

Mai jos găsești, pentru fiecare fișier din `Scripts/`, toate clasele, metodele și funcțiile, cu o scurtă descriere a rolului lor. Listele sunt exhaustive pentru codul actual.

<details>
<summary><b>⚙️ `config.py` — Config și Asset Loader</b></summary>

- Constante globale: `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`
- Obiecte globale: `screen` , `font`
- `load_texture(filename)`
  - Încarcă o imagine încercând mai multe căi posibile (relative și absolute).

</details>

<details>
<summary><b>🧬 `base_classes.py` — Ierarhia de bază (ABC)</b></summary>

- Clasa `GameObject(pygame.sprite.Sprite)`
  - `__init__(x, y, image_path=None)` — setează imaginea (opțional) și poziția.
  - `_load_image(image_path)` — încarcă imaginea și masca de coliziune; fallback pe placeholder.
  - `_setup_position(x, y)` — creează obiectul de tipul respectiv și poziționează centrul la (x, y).
  - `draw(surface=None)` — metoda abstractă; fiecare subclasă va avea o metoda specifica

- Clasa `HealthEntity(GameObject)`
  - `__init__(x, y, image_path, max_health, health_bar_length=100)` — inițializează viața.
  - `_setup_health(max_health, health_bar_length)` — setează atributele de viață și bara.
  - `get_damage(amount)` — scade viața
  - `get_health(amount)` — adauga viata până la `max_health`.
  - `_draw_health_bar(x, y, height=5, surface=None)` — desenează bara de viață cu efect de „delay” pe damage.

- Clasa `MovableEntity(HealthEntity)`
  - `__init__(x, y, image_path, max_health, speed, health_bar_length=100)` — extinde cu mișcare.
  - `_setup_movement(speed)` — setează `speed`, `direction` și `flip`.
  - `update(*args, **kwargs)` — metoda abstractă; actualizează miscarea entitatilor.

- Clasa `CollectibleItem(GameObject)`
  - `__init__(x, y, image_path)` — item colectabil de bază.
  - `draw(surface=None)` — desenează sprite-ul.
  - `use(player)` — metoda abstractă; aplică efect pe `player` și dispare daca a intrat in collide.

</details>

<details>
<summary><b>👤 `player.py` — Jucătorul</b></summary>

- Pereți de limită: `wall_left`, `wall_right` — instanțe `Wall` pentru delimitare orizontală.
- Clasa `Player(MovableEntity)`
  - `__init__(x, y, speed)` — creează jucătorul cu sprite implicit și bară de viață.
  - `_load_additional_images()` — încarcă varianta sprite-ului orientată la stânga.
  - `_setup_physics()` — setează atribute de mișcare verticală (jump/in_air/velocity_y).
  - `_setup_animation()` — inițializează starea pentru arma/medkit și frame timing.
  - `draw(surface=None)` — desenează sprite-ul (cu flip), arma și health bar-ul în HUD.
  - `_draw_weapon(surface)` — poziționează arma în funcție de orientare (`flip`).
  - `update(*args, **kwargs)` — functie care updateaza pozitia ajuntandu se de functia move.
  - `move(moving_left, moving_right)` — deplasare orizontală + coliziuni cu `wall_left/right`.
  - `animate_idle()` — animație facuta sa imite efectul de sprite.

</details>

<details>
<summary><b>👹 `enemy.py` — Inamicul</b></summary>

- Clasa `Enemy(MovableEntity)`
  - `__init__(x, y, speed, image_path)` — setează inamicul cu viață proprie.
  - `_on_death()` — elimină sprite-ul din grupuri și „golește” imaginea ocupata.
  - `draw(surface=None)` — desenează sprite-ul și bara de viață cu poziționare offset în funcție de direcție.
  - `update(*args, **kwargs)` — așteaptă `player` ca prim argument; urmărește poziția lui pe axa X.
  - `attack(player)` — aplică damage continuu dacă cei doi se intersectează.

</details>

<details>
<summary><b>🔫 `bullet.py` — Glont</b></summary>

- Clasa `Bullet(pygame.sprite.Sprite)`
  - `__init__(x, y, direction, image_path, damage=40)` — setează sprite-ul, masca și viteza (semn din `direction`).
  - `update(walls=None, enemies=None)` —
    - translatează pe X; verifică coliziuni cu inamicul și cu pereții;
    - aplică `enemy.get_damage(damage)`; dispare la impact sau când iese din ecran.

</details>

<details> 
<summary><b>💊 `medkit.py` — Medkit</b></summary>

- Clasa `Medkit(CollectibleItem)`
  - `use(player)` — dacă se suprapune cu jucătorul: aplică `player.get_health(heal_amount)`, apoi se va sterge.

</details>

<details>
<summary><b>🗡️ `weapon.py` — Armă</b></summary>

- Clasa `Weapon(CollectibleItem)`
  - `use(player)` — dacă se suprapune: setează `player.weapon_image` (copie a imaginii), apoi se va sterge de pe ecran

</details>

<details>
<summary><b>🧱 `wall.py` — Pereți</b></summary>

- Clasa `Wall(pygame.sprite.Sprite)`
  - `__init__(x, y, width, height, texture_path='wall_texture.png')` — definește dreptunghiul și textura scalată la dimensiuni.
  - `draw(surface=None)` — desenează conturul și textura peretelui.

</details>

<details>
<summary><b>🎨 `button.py` — Buton UI</b></summary>

- Clasa `Button`
  - `__init__(text, x, y, width, height, normal_color, hover_color, text_color, border_radius)` — definește cum va arata butonul.
  - `draw(surface=None)` — actualizează starea de hover și desenează butonul + conturul + textul.
  - `is_clicked(mouse_pos=None)` — testează dacă un click (sau poziție dată) cade se intampla.
  - `_update_hover_state()` — intern: schimbă culoarea curentă în funcție de poziția mouse-ului.

</details>

<details>
<summary><b>🎬 `game_init.py` — Creator de Context</b></summary>

- `create_context()` — pregătește întreaga stare a jocului și returnează un dicționar cu:
  - obiecte: `player`, `enemy`, grupuri `weapon_group`, `bullet_group`, `enemy_group`, `medkit_group`;
  - background: `bg`, `bg_width`, `bg_rect`, `scroll`, `tiles`;
  - evenimente: `WEAPON_SPAWN_EVENT`, `MEDkit_SPAWN_EVENT` (+ timers);
  - UI: `start_button`, `restart_button`, `quit_button`, `resume_button`;
  - imagini ecran: `menu_background`, `game_over_image`, `win_image`;
  - variabile joc: `bullets`, `enemies_killed` (nefolosit în gameplay curent), `game_state`, `moving_left/right`, `weapon_collected`, `medkit_collected`;
  - resurse/constante: `screen`, `font`, `FPS`, `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `wall_left`, `wall_right`.

</details>

<details>
<summary><b>📦 `spawn.py` — Spawn logic</b></summary>

- `spawn_weapon_if_needed(event, context)` — dacă nu există armă pe hartă, jucătorul nu are gloanțe și expira timpul, spawnează `Weapon` la o poziție random.
- `spawn_medkit_if_needed(event, context)` — dacă jucătorul e in viata,dar are viață sub un anumit prag, spawnează `Medkit` random.

</details>

<details>
<summary><b>🎛️ `handlers.py` — Gestionare evenimente</b></summary>

- `handle_menu_events(event, context)` — gestionează Quit/Start în meniu.
- `handle_running_events(event, context)` — procesează evenimente de la tastatura (A/D/←/→, Space, ESC).
- `handle_paused_events(event, context)` — click pe `Resume`/`Quit`.
- `handle_game_over_events(event, context)`.

</details>

<details>
<summary><b>🖼️ `render.py` — Desenare</b></summary>

- `draw_background(context)` — desenează tiles de background cu scroll orizontal.
- `draw_hud(context)` — afișează textul pentru gloanțe în HUD.

</details>

<details>
<summary><b>🧠 `project.py` — Orchestratorul jocului</b></summary>

- `make_screen_dynamic()` — generator de offset-uri pentru efecte de „shake” (în codul actual nu este folosit de `main`).
- `main()` — bucla principală a jocului:
  - creează `context` prin `create_context()`;
  - rulează bucla de randare și update în funcție de `game_state` (`menu`/`running`/`paused`/`game_over`/`win`);
  - delegă spawn/handlers/render; verifică condiții de win/lose; face `pygame.display.update()` pe fiecare cadru.

</details>

<details>
<summary><b>📦 `Scripts/__init__.py` — Marker de pachet</b></summary>

- Marchează folderul `Scripts/` ca pachet Python pentru importuri tip `from Scripts.module import Class`.

</details>

---

## 🎮 Modul de Desfășurare al Jocului

```
┌─────────────────────────────────────────────────────────────┐
│                    🏠 MAIN MENU                             │
│                                                             │
│                   [START]  [QUIT]                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      🎮 GAMEPLAY                               │                                                      
│  👤 Urzicarius ←──────────────────────→ 👹 Senior Engineer  │
│                                                             │
│  🔫 Găsește arma și învinge adversarul!                     │
│  💊 Colectează medkit-uri pentru viață                      │
│  ⚔️ Inamicul te urmărește constant                          │
│                                                             │
│  [ESC] pentru pauză                                         │
└─────────────────────────────────────────────────────────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
    ┌─────────────────┐ ┌─────────────────┐
    │   💀 LOSE.      │      🏆 WIN        │
    │                 │ │                 │
    │  [RESTART]      │ │  [RESTART]      │
    │  [QUIT]         │ │  [QUIT]         │
    └─────────────────┘ └─────────────────┘
```

### 🎯 Obiective:
1. **Găsește arma** 🗡️ - Spawn-uri random când nu ai gloanțe.
2. **Colectează medkit-uri** 💊 - Apar când ai viață scăzută.
3. **Învinge Senior Engineer-ul** 👹 - Evită să te prindă!
4. **Supraviețuiește** ❤️ - Health bar animat care te ține la curent.

---

## 🐛 Probleme Întâlnate și Soluții

<details>
<summary><b>1️⃣ Dreptunghiul Inamicului Persista După `.kill()`</b></summary>

**Problema:** Chiar dacă apelam `.kill()` asupra sprite-ului, dreptunghiul inamicului rămânea vizibil.

**Soluție:** Am setat manual dimensiunile dreptunghiului la valori nule:
```python
self.rect = pygame.Rect(0, 0, 0, 0)
```

</details>

<details>
<summary><b>2️⃣ Gloanțele Trăgeau Din Cap, Nu Din Armă</b></summary>

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
<summary><b>3️⃣ Health Bar Nu Se Reseta La Restart</b></summary>

**Problema:** Atributul `displayed_health` era adăugat local în funcție și nu ca atribut al clasei.

**Soluție:** Am mutat inițializarea în `__init__()` pentru a fi accesibil global:
```python
def __init__(self, ...):
    # ... alte atribute ...
    self.displayed_health = self.health
```

</details>

<details>
<summary><b>4️⃣ Inamicul Nu Se Spawna După Win</b></summary>

**Problema:** După ce câștigai, la restart inamicul nu mai apărea pentru că obiectul mort era reutilizat.

**Soluție:** Creăm o instanță nouă de `Enemy` la fiecare restart:
```python
enemy = Enemy(680, 340, 1, 'big_boss.png')
context['enemy_group'].add(enemy)
context['enemy'] = enemy
```

</details>

---

## 📊 Avantajele Structurii Modulare

| ✅ Avantaj | 📝 Descriere |
|-----------|-------------|
| **Mentenanță Ușoară** | Bug-fixing și updates per modul neafectand prea mult celelalte clase.|
| **Reutilizare Cod** | Base classes care reduc duplicarea codului. |
| **Testare Simplificată** | Fiecare componentă poate fi testată independent. |
| **Scalabilitate** | Ușor de adăugat noi features fără a modifica codul existent. |
---

## 🛠️ Tehnologii Utilizate

- **Python 3.12+** 🐍
- **Pygame 2.6.1** 🎮
- **ABC (Abstract Base Classes)** 🧬 - pentru OOP
- **Math Library** 📐 - pentru animații
- **Random Library** 🎲 - pentru spawn-uri

---