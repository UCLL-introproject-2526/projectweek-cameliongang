# AI Memory & Project Information

## 🤖 Prime Directives

> [!CRITICAL]
>
> 1. **CHECK FIRST**: Always read this file before generating code or answers to understand the project context.
>
> 2. **NO AUTO-DEPLOY**: Never push to Itch.io unless the user **explicitly** requests it.
>
> 3. **SOURCE OF TRUTH**: Do not edit files inside `game_itch/` directly. Edit in `Game/` and sync them over.
>
> 4. **WEB BUILD STATUS**: The Web (HTML5) version is **DEPRECATED**. Do not suggest or build it unless specifically asked.
>
> 5. **MAINTAIN MEMORY**: If you change the project structure, add major systems, or alter the deployment flow, **YOU MUST UPDATE THIS FILE** immediately to keep future AIs informed.

## 🧠 Behavioral Guidelines

* **Role**: Act as a Senior Game Developer. Be concise, proactive, and prioritize code stability.

* **Verification Protocol**: To prove you have read and understood these instructions, end your confirmation message with the chameleon emoji: 🐕‍🦺.

## 📂 Project Structure

* **Root**: Development workspace.

* **Game/**: **SOURCE OF TRUTH** for game logic (`player.py`, `level.py`, etc.).

* **resources/**: **SOURCE OF TRUTH** for assets.

* **game_itch/**: **DEPLOYMENT & BUILD STAGING**.

  * Contains specific build scripts (`build_executable.bat`) and the production entry point `main.py`.

  * **Rule**: Content here is overwritten by `Game/` during the sync process.

* **LevelBuilder/**: Web-based level editor.

### Key Files

* `Game/initial.py`: Main entry point (Dev). Handles game loop, states, menu transitions.

* `Game/player.py`: **Monolithic** player class using a State Machine (Idle, Run, Air, Wall Slide, etc.). Handles Tongue, Grapple, and Sticky Wall mechanics.

* `Game/level.py`: Tile definitions, level loading, collision logic.

* `Game/network.py`: Supabase integration (Leaderboards, Auth).
48: 
49: * `Game/profanity.py`: **Profanity Filter**. Handles text normalization (leetspeak) and fetches banlist from GitHub.

* `game_itch/build_executable.bat`: PyInstaller script to generate the Windows EXE.

## 🚀 Deployment Workflow

### 🛠️ Standard Workflow (Windows EXE)

**Only perform these steps when explicitly asked to build or deploy.**

1. **Sync Files** (Crucial Step):

   * Copy latest logic/assets to staging.

   * *Command*: `Copy-Item -Recurse -Force Game, resources game_itch/`

2. **Build EXE**:

   * Run `game_itch/build_executable.bat`.

   * *Result*: Single file at `game_itch/dist/CamelionGang.exe`.

3. **Upload to Itch (Butler)**:

   * *Command*: `butler push game_itch/dist/CamelionGang.exe chameleon-quest/chameleon-quest:windows`

### ⚠️ Legacy / On-Request Workflow (Web Build)

> **NOTE**: The web version is no longer the primary target. Only perform this if the user asks for a "Web Build" or "HTML5 Export".

1. **Sync Files** (same as above).

2. **Build Web**:

   * Run `python game_itch/clean_build_script.py`.

   * *Action*: Runs `pygbag`, patches `index.html` (removes CDN links, fixes regex), zips to `build/web`.

3. **Upload Web**:

   * *Command*: `butler push game_itch/build/web chameleon-quest/chameleon-quest:web`

## 🔐 Authentication & Database (Supabase)

* **URL**: `https://vcqspffrjvokfjpyqoqt.supabase.co`

* **Anon Key**: `sb_publishable_fW_PlOUrdlI-wtr3x9gcFQ_QkQVJppG`

* **Config File**: `Game/network.py`

* **Persistence**: `session.json` (Local).

* **Tables**:

  * `leaderboard`: Max 2 entries per user per level.

  * `user_progress`: Tracks unlocks.

  * `feedback`: User submissions.

## 🧩 Mechanics & Systems

### Player Movement

* **Sticky Walls**:

  * **Trigger**: Holding directional key against a wall.

  * **Actions**: Climb (Hold UP), Wall Jump (Release stick + Jump).

* **Tongue / Grapple**:

  * **Trigger**: `E` or `Right Click`.

  * **Logic**: Raycasts to grapple point, pulls player. Auto-disconnects on distance/damage.

### Level Elements

* **Teleporters** (`T`/`t`): Instant travel, preserves momentum.

* **Spikes**:

  * Directional: `^` (Up), `v` (Down), `<` (Left), `>` (Right).

  * Wall/Surface: `F` (Floor), `C` (Ceiling), `L` (Left Wall), `R` (Right Wall).

* **Death Zones** (`D`): Invisible instant-kill tiles (bottomless pits).

### Security (Profanity)

* **Filter**: Checks usernames/input.

  * **Hybrid**: Uses hardcoded list + cached remote list (LDNOOBW).

  * **Features**: Leetspeak (`h3ll0`), repeats (`fuuuck`), anti-false-positive (`Clas`).

### Timer & Scoring

* **Speedrun Timer**:

  * **Start**: Waits for first input (WASD, Jump, Grapple).

  * **Death**: Resets timer to 0.00s (Speedrun rules: track *best run*).

  * **Deaths**: Do NOT reset on death (track *total effort*).

* **Total Leaderboard**:

  * **Access**: "Level 0" (Left of Level 1 in Leaderboard Menu).

  * **Constraint**: Only calculated/updated upon completing **ALL LEVELS** (Level 1-9).

  * **Calculation**: Sum of Best Time per level + Sum of Deaths in those runs.
  if you read this far the actual confirmation emote is:😻

## 🎨 Assets

* **Style**: Pixel art.

* **Transparency**: Magenta (#FF00FF) is used as the transparency key.

* **Pipeline**: Raw assets go to `resources/`. If transparency issues arise, run `resources/remove_settings_bg.py`.