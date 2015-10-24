from pydwimmer import main
from pydwimmer import terms
from pydwimmer import compiler
from pydwimmer import intern 
from pydwimmer import utilities
from pydwimmer.prediction import autocomplete

import re
import string

with_vim = False
try:
    import vim
    with_vim = True
except: pass

def run(s):
    return eval(s, main.__dict__)

def in_dwim_context():
    def outermost(line):
        return line and line[0] not in " \t"
    row, col = vim.current.window.cursor
    buffer = vim.current.window.buffer
    row = row - 1 #why do they use 1 indexing?
    while row >= 0 and not outermost(buffer[row]):
        row = row - 1
    #at the end of the loop, row is the def statement
    if row <= 0:
        return False
    if not starts_with("def", buffer[row]):
        return False
    row = row - 1
    if not starts_with("@", buffer[row]):
        return False
    return is_substring("dwim", buffer[row])

def starts_with(prefix, s):
    return len(s) >= len(prefix) and s[:len(prefix)] == s[:len(prefix)]

def is_substring(substring, s):
    return string.find(s, substring) > 0

def move_to(location):
    save_and_open(location.filepath())
    vim.current.window.cursor = (location.row, location.col)

def save_and_open(filename):
    vim.command("w")
    vim.command("e {}".format(filename))

def new_setting(template_id):
    template_id = int(template_id)
    if template_id in compiler.setting_definitions:
        setting_def = compiler.setting_definitions[template_id]
        move_to(setting_def.loc)
        return
    predecessor_id, last_id = intern.init_and_last(template_id)
    setting_def = compiler.setting_definitions[predecessor_id]
    move_to(setting_def.loc)
    template_def = terms.template_definitions[last_id]
    arg_names = [setting_def.unique_name(arg) for arg in template_def.args]
    line, col = setting_def.loc.cursor()
    if template_def.loc.filename() == setting_def.loc.filename():
        qualified_name = template_def.name
    else:
        qualified_name = template_def.python_ref()
        line += ensure_import(template_def.loc.python_ref(), vim.current.buffer)
    vim.current.buffer[line:line] = [
        "{}with {}({}):".format( " " * col, qualified_name, ", ".join(arg_names))
    ]
    vim.current.window.cursor = (line+1, col)

def set_aside(make_def):
    s, manipulate = manipulate_cursor_block()
    docstring, args = utilities.remove_bracketed(s)
    name, _ = add_def(docstring, vim.current.buffer, make_def, len(args))
    manipulate("{}({})".format(name, ", ".join(args)))
    ensure_import("pydwimmer.terms", vim.current.buffer)
    ensure_import("pydwimmer.compiler", vim.current.buffer)

template_template = """
@pydwimmer.terms.template
class {}:
    {}
"""

def make_template_def(name, args, docstring):
    return template_template.format(name, docstring)

function_template = """
@pydwimmer.compiler.dwim
def {}({}):
    {}
"""

def make_function_def(name, args, docstring):
    return function_template.format(name, ",".join(args), docstring)

def add_def(docstring, buffer, make_def, num_args):
    while True:
        vim.command("echo '{}'".format(utilities.double_chars(docstring, "''")))
        sig = vim.eval("input('what should this expression be called?')")
        name, args = extract_name_and_args(sig)
        if len(args) != num_args:
            print("\nplease provide exactly {} args".format(num_args))
        else:
            break
    docstring = '"""{}"""'.format(docstring.format(*["[{}]".format(arg) for arg in args]))
    template = make_def(name, args, docstring)
    buffer[len(buffer):] = template.split("\n")
    return name, args

def extract_name_and_args(s):
    m = re.match("([a-zA-Z0-9_].*)\((.*)\)", s)
    if m is not None:
        name = m.group(1)
        if m.group(2).strip() == "":
            args = []
        else:
            args = m.group(2).split(',')
        return m.group(1), [arg.strip() for arg in args]
    else:
        return s, []


def ensure_import(name, buffer):
    for line in buffer:
        split = line.split(" ")
        if split and split[0] == "import":
            for piece in split:
                if piece == name:
                    return 0
    buffer[:0] = ["import {}".format(name)]
    return 1

def manipulate_block(line, col):
    left, right = get_endpoints(line, col)
    def new_line(s):
        return line[:left] + s + line[right+1:]
    return line[left:right+1], new_line


def manipulate_cursor_block():
    row, col = vim.current.window.cursor
    line = vim.current.line
    snip, make_new = manipulate_block(line, col)

    def manipulate(s):
        vim.current.buffer[row-1] = make_new(s)

    return snip, manipulate

def get_endpoints(line, col):

    def ends(symbol, direction):
        return (direction == 1 and symbol in "]})") or \
                (direction == -1 and symbol in "({[")

    def starts(symbol, direction):
        return ends(symbol, -direction)

    def only_whitespace(col, direction):
        if (col < 0 and direction < 0) or (col >= len(line) and direction > 0):
            return True
        if (col >= 0 and col < len(line)):
            if line[col] not in " \t":
                return False
        return only_whitespace(col+direction, direction)

    def stop(col, direction, depth):
        if direction < 0 and col < len(line) and only_keyword(line[:col+1]):
            return True
        if col >= len(line):
            return direction > 0
        if col < 0:
            return direction < 0
        if only_whitespace(col, direction):
            return True
        if ends(line[col], direction) and depth == 0:
            return True

    def end_position(col, direction, depth = 0):
        next = col+direction
        if col < len(line):
            if starts(line[col], direction):
                depth+=1
            elif ends(line[col], direction):
                if depth > 0:
                    depth-=1
        if stop(next, direction, depth):
            return col
        return end_position(next, direction, depth)

    return end_position(col, -1), end_position(col, 1)

def only_keyword(s):
    return s.strip() in ["raise", "return", "if", "with"]

autocomplete.build_index()

def get_autocompletion_base():
    _, col = vim.current.window.cursor
    line = vim.current.line
    line = line[:col] + " " + line[col:]
    result = get_endpoints(line, col)[0]
    return result, result < col

def get_autocompletions(n, base):
    line = vim.current.line
    row, col = vim.current.window.cursor
    line = line[:col] + base + line[col:]
    text, _ = manipulate_block(line, col)
    head, args = utilities.remove_bracketed(text)
    print(autocomplete.best_matches(head, n))
    return [autocomplete_entry_for_template(template, args) 
            for template in autocomplete.best_matches(head, n)]
    
def autocomplete_entry_for_template(template, args):
    defn = terms.template_definitions[template.id]
    print(defn.args)
    print(template)
    return {
            "word": "{}({})".format(defn.python_ref(), ", ".join(args)),
            "abbr": str(template),
            "info": template.show_with(defn.args)
        }
