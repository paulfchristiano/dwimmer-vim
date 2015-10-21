import pydwimmer.main as main
import pydwimmer.terms as terms
import pydwimmer.compiler as compiler
import pydwimmer.intern as intern
import pydwimmer.utilities as utilities
import re

with_vim = False
try:
    import vim
    with_vim = True
except: pass

def run(s):
    return eval(s, main.__dict__)

def new_setting(template_id):
    template_id = int(template_id)
    if template_id in compiler.locations:
        filename, lineno, col, taken_names = compiler.locations[template_id]
        vim.command("w")
        vim.command("e {}".format(filename))
        vim.current.window.cursor = (lineno, col)
        return
    predecessor_id, last_id = intern.init_and_last(template_id)
    filename, lineno, col, taken_names = compiler.locations[predecessor_id]
    vim.command("w")
    vim.command("e {}".format(filename))
    template_name, template_path, arg_names, _ = terms.templates[last_id]
    for i in range(len(arg_names)):
        arg = arg_names[i]
        if arg in taken_names:
            j = 2
            while arg in taken_names:
                arg = arg_names[i] + str(j)
                j+=1
        arg_names[i] = arg
    template_file = template_path.split(".")[-1]
    if template_file != filename:
        lineno += ensure_import(template_path, vim.current.buffer)
    vim.current.buffer[lineno:lineno] = [
        "{}with {}({}):".format( " " * col, 
            template_name 
            if template_file == filename 
            else "{}.{}".format(template_path, template_name),
            ", ".join(arg_names)
        )
    ]
    vim.current.window.cursor = (lineno+1, col)

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

def manipulate_cursor_block():
    row, col = vim.current.window.cursor
    line = vim.current.line
    left, right = get_endpoints(line, col)

    def make_new_line(s):
        vim.current.buffer[row-1] = line[:left] + s + line[right+1:]

    return line[left:right+1], make_new_line

def get_endpoints(line, col):

    def ends(symbol, direction):
        return (direction == 1 and symbol in "]})") or \
                (direction == -1 and symbol in "({[")

    def starts(symbol, direction):
        return ends(symbol, -direction)

    def only_whitespace(col, direction):
        if col < 0 or col >= len(line):
            return True
        if line[col] != " ":
            return False
        return only_whitespace(col+direction, direction)

    def stop(col, direction, depth):
        if only_whitespace(col, direction):
            return True
        if ends(line[col], direction) and depth == 0:
            return True

    def end_position(col, direction, depth = 0):
        next = col+direction
        if starts(line[col], direction):
            depth+=1
        elif ends(line[col], direction):
            if depth > 0:
                depth-=1
        if stop(next, direction, depth):
            return col
        return end_position(next, direction, depth)

    return end_position(col, -1), end_position(col, 1)
