# Auto-PokéMeow

Auto-PokéMeow will automatically catch [PokéMeow](https://pokemeow.com/) pokemon for you.

This program requires Python3.x and tested on Windows 10.

## NOTICES

* **USING THIS SCRIPT IS CONSIDERED AS "SELF-BOTS" AND IT'S AGAINST DISCORD TERMS OF SERVICE.** [(ref)](https://support.discord.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-)

* **A CAPTCHA BY POKEMEOW MAY APPEAR AUTOMATICALLY. IN CASE OF THIS HAPPENS, THIS PROGRAM WILL STOP AND YOU NEED TO FILL THE CAPTCHA CORRECTLY UNDER TWO MINUTES OR YOU ACCOUNT WILL BE TEMPORARILY BANNED. THE 5<sup>TH</sup> BAN IS PERMANENT.**

* **WE DON'T RESPONSIBLE TO ANY BAN / LOSS / HARM HAPPENS TO YOU WHILE OR AFTER USING THIS PROGRAM. USE AT YOUR OWN RISK.**

## Quick Start

1. Install required modules using PIP.

```
pip install -r requirements.txt
```

2. Run the program

```
python main.py --run
```

## Arguments

* `--run`
Run the program and start catching pokemons.

* `--preview`
Run the program in simulation environment.

* `--config {path/to/json}`
Determine which configuration json file to use. (default: `config.json`)

* `--output_panels {path/to/save/image}`
Determine where to save preview of input panel, color panel, and ball panels.

* `--output_color_panel {path/to/save/image}`
Determine where to save preview of color panel.

## Configurations

* **Panel**
represented by `[top, left, bottom, right]`

* **Color**
represented by `[red, green, blue]`

* `input_panel`
Area to input commands.

* `color_panel`
Area to detect pokemon color.

* `colors`
Color representations of each pokemon rarity.

* `color_tolerance`
How accurate detected color must be against colors. Higher value mean less strict.

* `balls.panel`
Area to click if would like to use the ball.

* `balls.catch_rarity`
Rarity to cacth using the ball.

* `commands`
Command to be inputted to `input_panel`.

## Modifying Configuration

After modifying configuration JSON, it's recommended to check and test the program on simulation environment. 

The following commands will run the program in simulation environment (without click and mouse movement) and check your panels configuration.

```
python main.py --preview --output_panels panels.png --output_color_panel color_panel.png 
```

While running above commands,

* Check detected color and selected ball on console.

* Check panels positions from `panels.png`

* Check color panel from `color_panel.png`
