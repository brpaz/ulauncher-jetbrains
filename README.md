# Ulauncher Jetbrains

[![Ulauncher Extension](https://img.shields.io/badge/Ulauncher-Extension-green.svg?style=for-the-badge)](https://ext.ulauncher.io/-/github-brpaz-ulauncher-jetbrains)
[![CI Status](https://img.shields.io/github/workflow/status/brpaz/ulauncher-jetbrains/CI?color=orange&label=actions&logo=github&logoColor=orange&style=for-the-badge)](https://github.com/brpaz/ulauncher-jetbrains)
![License](https://img.shields.io/github/license/brpaz/ulauncher-jetbrains.svg?style=for-the-badge)

> Open your recent projects from Jetbrains based IDEs from [ulauncher](https://ulauncher.io/).

## Demo

![demo](demo.gif)

## Requirements

- Ulauncher 5
- Python >= 3 
- The Jetbrains IDE you want to use.

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```
https://github.com/brpaz/ulauncher-jetbrains
```

## Usage

The following Jetbrains IDEs are supported:

* PHPStorm
* WebStorm
* PyCharm
* IntelliJ Idea
* GoLand
* CLion
* Android Studio
* Rider
* RubyMine

Before using this extension, you must create a command line launcher for your Jetbrains IDE. For that 
you can go to "Tools -> Create Command Line Launcher" in your IDE.
After that, you should configure the path to the created launcher in the plugin settings.

You also need to configure the path of your IDE "recentProjects" file in the plugin settings. The path
is something like "~/.PhpStorm2018.1/config/options/recentProjectDirectories.xml". You will probably
just need to change the ".PhpStorm2018.1/" part to match your IDE version.

## Development

```
git clone https://github.com/brpaz/ulauncher-jetbrains
cd ulauncher-jetbrains
make link
```

The `make link` command will symlink the cloned repo into the appropriate location on the ulauncher
extensions folder.

To see your changes, stop ulauncher and run it from the command line with: `ulauncher -v`.

## Contributing

[pwnyprod](https://github.com/pwnyprod)

All contributions are welcome.

## Show your support

<a href="https://www.buymeacoffee.com/Z1Bu6asGV" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## License 

Copywright @ 2019 [Bruno Paz](https://github.com/brpaz)

This project is [MIT](LICENSE) Licensed.

