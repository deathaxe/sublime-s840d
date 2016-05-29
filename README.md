# [CNC Sinumerik840D](https://github.com/deathaxe/sublime-s840d)

This package provides syntax highlighting support for the
SINUMERIK 840D Computerized Numerical Control to the SublimeText 3 Editor.

### Features:

* Syntax highlighting support for NC programs including
	* ISO G-Code
	* SINUMERIK highlevel commands
	* known NC cycles, functions and commands
	* known NC variables and machine data (NC-Version 04.07.02.01)
	* code-snippets for most common control functions

* Syntax highlighting for (EasyScreen/RunMyHmi) sources

### Installing

**With the Package Control plugin:** The easiest way to install SublimeCodeIntel is through Package Control, which can be found at this site: http://wbond.net/sublime_packages/package_control

Once you install Package Control, restart Sublime Text and bring up the Command Palette (``Command+Shift+P`` on OS X, ``Control+Shift+P`` on Linux/Windows). Select "Package Control: Install Package", wait while Package Control fetches the latest package list, then select ``CNC Sinumerik840D`` when the list appears. The advantage of using this method is that Package Control will automatically keep ``CNC Sinumerik840D`` up to date with the latest version.

**Without Git:** Download the latest source from `GitHub <https://github.com/deathaxe/sublime-s840d>`_ and copy the whole directory into the Packages directory.

**With Git:** Clone the repository in your Sublime Text Packages directory, located somewhere in user's "Home" directory::

    git clone git://github.com/deathaxe/sublime-s840d.git


The "Packages" packages directory is located differently in different platforms. To access the directory use:

* OS X::

    Sublime Text -> Preferences -> Browse Packages...

* Linux::

    Preferences -> Browse Packages...

* Windows::

    Preferences -> Browse Packages...

### Setup

The package contains a **s840d.sublime-settings** file, which is recommended
to be copied to the Data/User folder to enable the follwing language specific
settings.

- "ensure_newline_at_eof_on_save": true
- "translate_tabs_to_spaces": true
- "use_tab_stops": false

They are all required to ensure NC will read the resulting file correctly.

### License
[Copyright &copy; 2016 DeathAxe](https://github.com/deathaxe/sublime-s840d/blob/master/LICENSE.md)
