# vim-dwimmer

Vim support for [pydwimmer](https://github.com/paulfchristiano/py-dwimmer).
pydwimmer should be in a folder on your PYTHONPATH.

The command ":Run f(x, y, z)" calls the function f(x, y, z) with py-dwimmer.
The scope is the global scope in the file main.py in the current directory.

If you run a command that encounters a novel state,
it should open the appropriate file and generate a stub which you need to fill in.
For now, this will only work if that file is in your current directory,
and the template is defined in the current directory.

The plugin is most likely to work for files in the pydwimmer repository.

## Installation

Use your plugin manager of choice.

- [Pathogen](https://github.com/tpope/vim-pathogen)
  - `git clone https://github.com/paulfchristiano/vim-dwimmer ~/.vim/bundle/vim-dwimmer`
- [Vundle](https://github.com/gmarik/vundle)
  - Add `Bundle 'https://github.com/paulfchristiano/vim-dwimmer'` to .vimrc
  - Run `:BundleInstall`
- [NeoBundle](https://github.com/Shougo/neobundle.vim)
  - Add `NeoBundle 'https://github.com/paulfchristiano/vim-dwimmer'` to .vimrc
  - Run `:NeoBundleInstall`
- [vim-plug](https://github.com/junegunn/vim-plug)
  - Add `Plug 'https://github.com/paulfchristiano/vim-dwimmer'` to .vimrc
  - Run `:PlugInstall`
