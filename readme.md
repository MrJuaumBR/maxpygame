
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
# MaxPyGame
*A Engine made in Python, with Python & PyGame for PyGame*

<img src="https://img.shields.io/github/v/release/MrJuaumBR/maxpygame">

<button style="background-color: #232323; color: #C7C1C1; border-radius: 10px">[<i class="bi bi-window"></i> Test PyPi](https://test.pypi.org/project/maxpygame/)</button>

[<img src="https://raw.githubusercontent.com/MrJuaumBR/maxpygame/main/engine-icon.png" id="icon" width="256px" height="256px" style="margin-left: 50%; margin-right: 50%;" alt="Logo" title="Logo">](https://raw.githubusercontent.com/MrJuaumBR/maxpygame/main/engine-icon.png)

# Requirements
```shell
python -m pip install pygame
```

# Installation
```shell
pip install -i https://test.pypi.org/simple/ maxpygame
```

# ToDo
- [x] Slider fill when pass;
- [x] Install Via GitHub;
- [x] LongText Widget;
- [x] [Colors Json](https://mrjuaumbr.github.io/data/colors.json);
- [x] [Spritesheet System](https://www.pygame.org/wiki/Spritesheet);
- [x] [Engine Default Icon](#icon);
- [x] Colors aliases;
- [x] Fix Icon for PyPi users;
- [x] Fix Set Value Widget of Slider;
- [x] Fix Select Widget don't draw buttons;
- [x] FPS Control;
- [ ] TextArea Widget;
- [ ] Optimization;
- [ ] Text Border;
- [ ] Dropdown Widget;
- [ ] Music Support;
- [ ] Sounds Support;
- [ ] Engine Apply Default Icon(May be ignored).

# Colors
The engine has 67 Built-in colors!
and some aliases, in capitalized(Starts with ther *first* letter in UPPER, and in Lower, is all in lower case)
```py
# Example
pygameengine.Colors.BLACK
pygameengine.Colors.Black
pygameengine.Colors.black
```

# Widgets
Currently the engine has some widgets
- Button;
- Checkbox;
- Slider;
- Select;
- LongText;

# Prompts
```shell
# pre-build setup.py
py setup.py build

# Build Packages
py -m build

# Src Build
py -m build --sdist

# Local Install
pip install .

# Send to testPyPi
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
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