# dwimmer-vim

Vim support for [dwimmer-py](https://github.com/paulfchristiano/py-dwimmer).
That repository should be in a folder on your PYTHONPATH.

The command ":Run f(x, y, z)" calls the function f(x, y, z) with py-dwimmer.
The scope is the global scope in the file main.py in the current directory.

If you run a command that encounters a novel state,
it should open the appropriate file and generate a stub which you need to fill in.
(This will probably only work if the file in question is in your current directory,
and if the template is define somewhere on your vim path.)

This is most likely to work for files in the dwimmer-py repository.

## Installation

Use your plugin manager of choice.

- [Pathogen](https://github.com/tpope/vim-pathogen)
  - `git clone https://github.com/paulfchristiano/dwimmer-vim ~/.vim/bundle/dwimmer-vim`
- [Vundle](https://github.com/gmarik/vundle)
  - Add `Bundle 'https://github.com/paulfchristiano/dwimmer-vim'` to .vimrc
  - Run `:BundleInstall`
- [NeoBundle](https://github.com/Shougo/neobundle.vim)
  - Add `NeoBundle 'https://github.com/paulfchristiano/dwimmer-vim'` to .vimrc
  - Run `:NeoBundleInstall`
- [vim-plug](https://github.com/junegunn/vim-plug)
  - Add `Plug 'https://github.com/paulfchristiano/dwimmer-vim'` to .vimrc
  - Run `:PlugInstall`
