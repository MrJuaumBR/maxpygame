
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# MaxPyGame

*A Engine made in Python, with Python & PyGame for PyGame*

<img src="https://img.shields.io/github/v/release/MrJuaumBR/maxpygame">

<button style="background-color: #232323; color: #C7C1C1; border-radius: 10px">[<i class="bi bi-window"></i> Test PyPi](https://test.pypi.org/project/maxpygame/)</button>

<button style="background-color: #232323; color: #C7C1C1; border-radius: 10px">[<i class="bi bi-window"></i> GitHub](https://github.com/MrJuaumBR/maxpygame)</button>

[<img src="https://raw.githubusercontent.com/MrJuaumBR/maxpygame/main/engine-icon.png" id="icon" width="256px" height="256px" style="margin-left: 50%; margin-right: 50%;" alt="Logo" title="Logo">](https://raw.githubusercontent.com/MrJuaumBR/maxpygame/main/engine-icon.png)

*A bug found? A Tip? A Idea? Please make a issue in this Github page*

# Requirements
*! Versions ≥ 0.1.7 will automatically install dependencies*
```shell
python -m pip install pygame
```

# Installation
```shell
pip install -i https://test.pypi.org/simple/ maxpygame
```
*! Update*
```shell
pip install -U -i https://test.pypi.org/simple/ maxpygame
```

# ToDo
- [x] Slider fill when pass;
- [x] Install Via GitHub;
- [x] LongText Widget;
- [x] [Colors Json](https://mrjuaumbr.github.io/data/colors.json);
- [x] [Spritesheet System(Not tested)](https://www.pygame.org/wiki/Spritesheet);
- [x] [Engine Default Icon](#icon);
- [x] Colors aliases;
- [x] Fix Icon for PyPi users;
- [x] Fix Set Value Widget of Slider;
- [x] Fix Select Widget don't draw buttons;
- [x] FPS Control;
- [x] Readme Fix;
- [x] Change Delay Time of Some Widgets;
- [x] Progress Bar widget;
- [x] Fix Slider Widget Fill(A Little Space beetween Circle & Filled area);
- [x] Removed Longtext Widget print(Forgot to remove in before release);
- [x] Make all Widgets lower case(In case of 2 Words in one, e.g.: LongText → Longtext, ProgressBar → Progressbar)
- [x] Rect Border fix;
- [x] Select Widget Spacement fix;
- [x] Text Border;
- [x] Widgets Fix Custom Id;
- [x] Widgets Delete;
- [x] Time support to FPS Variability;
- [x] Time Settings(Easier to change);
- [x] New logo;
- [x] Engine Apply Default Icon(May be ignored);
- [x] Rework Colors System;
- [x] Text Box Widget;
- [x] New Events System;
- [x] Verify Version Online;
- [x] Auto install dependencies;
- [x] New colors(67 → 76);
- [x] Fixes on Colors System;
- [x] Fix on findWidgetById Function(Now returns the Widget not the Index.);
- [x] Updated [colors example](./examples/colors.py) for work better in newer versions;
- [x] Returns None when not found for some functions;
- [x] Fix Time System(0.1.6 → 0.1.6fix(.1) → 0.1.7)
- [x] Fixed Spritesheet System(How i don't recognize this later?);
- [x] Is Running Variable for detect if the game stills running;
- [x] Threading Example(Really cool for multiplayer games);
- [ ] Opacity on hover widgets;
- [ ] TextArea Widget;
- [ ] Optimization;
- [ ] Dropdown Widget;
- [ ] Music Support;
- [ ] Sounds Support.

# Colors
The engine has 67 Built-in colors!
and some aliases, in capitalized(Starts with ther *first* letter in UPPER, and in Lower, is all in lower case)
```py
# Example
pygameengine.Colors.BLACK
pygameengine.Colors.Black
pygameengine.Colors.black
```
To get color RGB or Hex:

```py
# RGB
pygameengine.Colors.BLACK.rgb # → Tuple[int,int,int] = 0,0,0
pygameengine.Colors.BLACK._rgb.rgb() # → Tuple[int,int,int] = 0,0,0

# Hex
pygameengine.Colors.WHITE.hex # → String = '#fff' or 'fff'
pygameengine.Colors.WHITE._hex.ghex() # → String = '#fff' or 'fff'
```

# Widgets
Currently the engine has some widgets
- Button;
- Checkbox;
- Slider;
- Select;
- LongText;
- ProgressBar;
- TextBox;

# Prompts
*pre-build setup.py*
```shell
py setup.py build
```
*Build Packages*
```shell
py -m build
```
*Local Install*
```shell
pip install .
```
*Send to Test PyPi*
```shell
twine upload --repository testpypi dist/*
```

# Credits
- [PyGame](https://www.pygame.org/news) for developing the base librarie.
- MrJuaumBR for trying to make more easier to create games.

# Contacts
[YouTube](https://www.youtube.com/@mrjuaumbr)

[GitHub](https://github.com/MrJuaumBR)

[TestPyPi](https://test.pypi.org/user/MrJuaumBR/)

[Discord](https://discord.gg/fb84sHDX7R)