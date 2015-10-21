if exists('*Run')
    if @% != "dwimmer.vim"
        finish
    endif
endif

" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! RunLast()
    call Run(w:lastdwim)
endfunction
  
function! Run(input)
    let w:lastdwim = a:input
    call Reload()
python << endOfPython

last_input = vim.eval("a:input")

try:
    import dwimmer
    x = dwimmer.run(vim.eval("a:input"))
    if x is not None:
        print(x.full_repr())
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! Reload()
    write
python << endOfPython


try:
    import dwimmer
    from pydwimmer.utilities import nostdout, noreloads
    from IPython.lib import deepreload
    with noreloads():
        deepreload.reload(dwimmer, exclude=['sys', 'os.path', '__builtin__', '__main__', 'ipdb', 'vim'])
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! Testfunc(findstart, base)

    echom a:base

    if a:findstart == 1
        return 2
    endif
    return [{"word": a:base, "abbr": "(none)"}]
    "return [{"word": a:base, "abbr": "(none)","info": "info1"}, {"word": "hi", "abbr": "the first option","info": "how does info display?"}, "hello", "test"]

endfunction

function! NewSetting(id)
python << endOfPython

try:
    import dwimmer
    x = dwimmer.new_setting(vim.eval("a:id"))
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction


function! MakeTemplate()
python << endOfPython

try:
    import dwimmer
    dwimmer.set_aside(dwimmer.make_template_def)
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! MakeFunction()
python << endOfPython

try:
    import dwimmer
    dwimmer.set_aside(dwimmer.make_function_def)
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! TestLine()
python << endOfPython

try:
    import dwimmer
    dwimmer.manipulate_cursor_block()
exhicept Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! Reload call Reload()
command! -nargs=1  Run call Run(<f-args>)
command! RunLast call RunLast()
command! -nargs=1 NewSetting call NewSetting(<f-args>)
command! MakeFunction call MakeFunction()
command! MakeTemplate call MakeTemplate()

" TODO: replace these with plugs so that the user can rebind them
inoremap <C-t> <Esc>:MakeTemplate<CR>
nnoremap <C-t> <Esc>:MakeTemplate<CR>
nnoremap <C-f> <Esc>:MakeFunctions<CR>

inoremap <C-d> <Esc>:RunLast<CR>
nnoremap <C-d> :RunLast<CR>

" TODO reactivate these and build autocomplete
"set completefunc=Testfunc
"inoremap <C-k> <C-x><C-u>

"set updatetime=200
"au CursorHoldI <buffer> call feedkeys("\<C-k>")
