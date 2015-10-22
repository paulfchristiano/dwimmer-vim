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
python import dwimmer

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
python << endOfPython
try:
    if vim.eval("a:findstart") in [1, "1"]:
        result, shouldComplete = dwimmer.get_autocompletion_base()
        if not shouldComplete:
            vim.command("return -3")
        else:
            vim.command("return {}".format(result))
    else:
        base = vim.eval("a:base")
        if base == "":
            vim.command("return []")
        else:
            autocompletions = [base, 'hi', 'hey', {'word': 'test'}]
            autocompletions = [base] + dwimmer.get_autocompletions(5)
            print("return {}".format(autocompletions))
            #vim.command("return {}".format(autocompletions))
            #vim.command("return ['plus']")
            vim.command("return ['plus', {'info': 'two times x plus one', 'word': 'pydwimmer.builtin.ints.double_inc()', 'abbr': 'two times {} plus one'}, {'info': 'what is x plus y?', 'word': 'pydwimmer.builtin.ints.add()', 'abbr': 'what is {} plus {}?'}]")
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! NewSetting(id)
python << endOfPython

try:
    x = dwimmer.new_setting(vim.eval("a:id"))
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction


function! MakeTemplate()
python << endOfPython

try:
    dwimmer.set_aside(dwimmer.make_template_def)
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! MakeFunction()
python << endOfPython

try:
    dwimmer.set_aside(dwimmer.make_function_def)
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

function! TestLine()
python << endOfPython

try:
    dwimmer.manipulate_cursor_block()
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
command! RunLast call RunLast()
command! -nargs=1 NewSetting call NewSetting(<f-args>)
command! MakeFunction call MakeFunction()
command! MakeTemplate call MakeTemplate()
command! Test call Testfunc(0, "plus")
command! IDC call InDwimContext()

" TODO: replace these with plugs so that the user can rebind them
inoremap <C-t> <Esc>:MakeTemplate<CR>
nnoremap <C-t> :MakeTemplate<CR>
inoremap <C-f> <Esc>:MakeFunction<CR>
nnoremap <C-f> :MakeFunction<CR>

inoremap <C-a> <Esc>:RunLast<CR>
nnoremap <C-a> :RunLast<CR>

set completefunc=Testfunc

function! AutoCompleteInDwimContext()
python << endOfPython
try:
    if dwimmer.in_dwim_context():
        vim.command('call feedkeys("\<C-x>\<C-u>")')
except Exception:
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

endOfPython
endfunction

set updatetime=200
au CursorHoldI <buffer> call AutoCompleteInDwimContext()

