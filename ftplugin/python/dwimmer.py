import vim
import pydwimmer.main as main
import pydwimmer.terms as terms
import pydwimmer.compiler as compiler
import pydwimmer.intern as intern

def run(s):
    return eval(s, main.__dict__)

def new_setting(template_id):
    template_id = int(template_id)
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

def ensure_import(name, buffer):
    for line in buffer:
        split = line.split(" ")
        if split and split[0] == "import":
            for piece in split:
                if piece == name:
                    return 0
    buffer[:0] = ["import {}".format(name)]
    return 1


