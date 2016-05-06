# [SyntaxSinumerik840D](https://github.com/deathaxe/SyntaxSinumerik840D)

This package adds syntax highlighting support for the
SINUMERIK 840D CNC control system to the SublimeText 3 Editor.

### Features:
* Syntax highlighting support for SINUMERIK 840D
	* G-Code
	* known NC cycles, functions and commands
	* known NC variables and machine data for nc software version (04.07.02.01)
* code-snippets for most common control functions

### Installation
To install this plugin, clone source code to Sublime Text packages folder.

If you use the portable version of Sublime Text, the **packages folder**
is located in the \Data\Packages subdirectory by default.

### Setup

The package contains a **s84d.sublime-settings** file, which is recommended
to be copied to the Data/User folder to enable the follwing language specific
settings.

- "ensure_newline_at_eof_on_save": true
- "translate_tabs_to_spaces": true
- "use_tab_stops": false

They are all required to ensure NC will read the resulting file correctly.

### License
Copyright &copy; 2016 DeathAxe
