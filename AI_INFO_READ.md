# AI Memory & Project Information

## 🤖 Directives for Future AIs
> [!IMPORTANT]
> **ALWAYS** check this file before starting work to understand the project context.
> **ALWAYS** update this file if you change architecture, add new systems, or change publication workflows.
> **MAINTAIN** the database credentials and Itch.io information accurately.

---

## 📂 Project Structure
- **Root**: Development workspace.
- **Game/**: **SOURCE OF TRUTH** for game logic (`player.py`, `level.py`, etc.).
- **resources/**: **SOURCE OF TRUTH** for assets.
- **game_itch/**: **DEPLOYMENT & BUILD STAGING**.
    - **Do NOT edit code here directly**.
    - Always **SYNC** from `Game/` -> `game_itch/Game` before building.
    - Contains specific build scripts (`clean_build_script.py`, `build_executable.bat`) and the production entry point `main.py`.
- **LevelBuilder/**: Web-based level editor.

### Key Files
- `Game/initial.py`: Main entry point (Dev). Handles game loop, states, menu transitions.
- `Game/player.py`: **Monolithic** player class using a State Machine structure (Idle, Run, Air, Wall Slide, etc.). Handles Tongue, Grapple, and Sticky Wall mechanics.
- `Game/level.py`: Tile definitions, level loading, collision logic (Spikes, Death Zones).
- `Game/camera.py`: Camera system (Follows player, clamps to level bounds).
- `Game/network.py`: Supabase integration (Leaderboards, Auth).
- `game_itch/clean_build_script.py`: **CRITICAL** for Web Builds. Handles `pygbag` build + `index.html` patching for Itch.io.

---

## 🔐 Authentication & Security
**Supabase Auth** (Email/Password + "Username"):
- **Config**: `Game/network.py`
- **Session**: `session.json` (Local persistence).
- **Guest Mode**: Supported.

---

## 🚀 Publication (Itch.io)
**Game URL**: [https://chameleon-quest.itch.io/chameleon-quest](https://chameleon-quest.itch.io/chameleon-quest)
**Channels**: `windows` (EXE), `web` (HTML5).

### 🛠️ Deployment Workflow (The "Golden Path")
1.  **Develop & Test** in Root/Game.
2.  **Sync**: Copy `Game/` and `resources/` to `game_itch/`.
    - *Command*: `Copy-Item -Recurse -Force Game, resources game_itch/`
3.  **Build Web**:
    - Run `python game_itch/clean_build_script.py`.
    - *What it does*: Run `pygbag` -> Patches `index.html` (removes CDN links, fixes `data-os` regex) -> Zips to `build/web`.
4.  **Build EXE**:
    - Run `game_itch/build_executable.bat`.
    - *What it does*: `PyInstaller` -> Single file `dist/CamelionGang.exe`.
5.  **Upload (Butler)**:
    - **Web**: `butler push game_itch/build/web chameleon-quest/chameleon-quest:web`
    - **Windows**: `butler push game_itch/dist/CamelionGang.exe chameleon-quest/chameleon-quest:windows`

---

## 🧩 Mechanics & Systems

### Player Movement
- **Sticky Walls**:
    - **Mechanic**: Player "sticks" to walls if holding directional key against it.
    - **Climb**: Hold `UP` while sticking.
    - **Wall Jump**: Release stick + Jump away.
- **Tongue / Grapple**:
    - **Trigger**: `E` or `Right Click`.
    - **Logic**: Raycasts to find grapple point. Pulls player towards point.
    - **Safety**: Auto-disconnects if distance > max + buffer. Resets on damage/teleport.

### Level Elements
- **Teleporters** (`T`/`t`): Instant travel, preserves momentum.
- **Spikes**:
    - `^` (Up), `v` (Down), `<` (Left), `>` (Right).
    - `F` (Floor), `C` (Ceiling), `L` (Left Wall), `R` (Right Wall) - * refined hitboxes*.
- **Death Zones** (`D`): Invisible tiles that trigger instant death (for pits).

---

## 💾 Database (Supabase)
- **URL**: `https://vcqspffrjvokfjpyqoqt.supabase.co`
- **Key**: `sb_publishable_fW_PlOUrdlI-wtr3x9gcFQ_QkQVJppG`
- **Tables**: `leaderboard` (Max 2 entries/user/level), `user_progress`, `feedback`.

---

## 🎨 Assets
- **Standard**: pixel art.
- **Transparency**: Use Magenta (#FF00FF) background for raw assets, then run `resources/remove_settings_bg.py` (or similar) if needed.
