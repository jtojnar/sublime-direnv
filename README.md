# Sublime-direnv

**Warning: Sublime Text 4 and recent enough `direnv` (the version in Ubuntu is too old).**

This package allows your Sublime Text to import environment variables from [`direnv`](https://direnv.net/).

## Installation

### Package Control
If you have [PackageControl](https://packagecontrol.io/) installed, you can use it to install the package.

### Manual
You can clone the repository in your `/Packages` folder.

```
git clone git@github.com:zchee/sublime-direnv.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/sublime-direnv
```

## Usage
When there is `.envrc` file to open project, choose “Load direnv” from the command palette.


### .envrc example
You can use any bash code that can be interpreted by `direnv` – set environment variables manually:

```bash
export VAGRANT_IP=192.168.33.10
export THEME_DIR=_theme
export CSS_DIR=$THEME_DIR/css
export JS_DIR=$THEME_DIR/js
export SASS_DIR=$THEME_DIR/sass
export IMG_DIR=$THEME_DIR/img
```

or use functions `direnv`’s [standard library](https://github.com/direnv/direnv/blob/master/stdlib.sh):

```bash
use_nix
```

This is useful for getting environment variables from [Nix](https://nixos.org/) shell or any other supported toolchain.

## To do
Some tasks that remain:

- [ ] `direnv allow` and `direnv deny` support.
- [ ] Avoid running multiple direnv instances.
- [ ] Handle multiple windows and project directories. How would that even work?
