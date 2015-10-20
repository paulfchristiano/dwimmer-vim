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
function! Run(input)
    call Reload()
python << endOfPython

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
python << endOfPython


try:
    import dwimmer
    from pydwimmer.utilities import nostdout
    from IPython.lib import deepreload
    with nostdout():
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

    return ["hi", "hello", "test"]

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




" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! Reload call Reload()
command! -nargs=1  Run call Run(<f-args>)
command! -nargs=1 NewSetting call NewSetting(<f-args>)

"set completeopt=longest,menuone
"set omnifunc=Testfunc
