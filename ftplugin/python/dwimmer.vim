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
    import pydwimmer.plugin as dwimmer
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
    import pydwimmer.plugin as dwimmer
    from pydwimmer.utilities import nostdout
    from IPython.lib import deepreload
    with nostdout():
        deepreload.reload(dwimmer, exclude=['sys', 'os.path', '__builtin__', '__main__', 'ipdb', 'vim'])
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
