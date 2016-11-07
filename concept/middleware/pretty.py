
import sys


# Pretty-printing #############################################################

class Pretty(object):

    __slots__ = ['file', 'level']

    def __init__(self, file=sys.stdout, level=0):
        self.file = file
        self.level = level

    def indent(self, txt=None):
        return Indent(self, txt)

    def parens(self):
        return Parens(self)

    def write(self, x):
        self.file.write(str(x))

    def writeln(self, x):
        self.newline()
        self.file.write(x)

    def newline(self):
        self.vspace()
        self.file.write(' ' * self.level)

    def vspace(self):
        self.file.write('\n')

    def sep(self, sep, things):
        if len(things) <= 0:
            return

        self.write(things[0])

        for thing in things[1:]:
            self.write(sep)
            self.write(thing)

    def comment(self, txt):
        self.writeln('# ' + txt)

    def define(self, name, *params):
        self.write('\n\n\ndef ' + name)

        with self.parens():
            self.sep(', ', params)

        self.write(':')

        indented = self.indent()

        return indented


class Indent(object):
    __slots__ = ['parent']

    def __init__(self, parent, txt=None):
        self.parent = parent
        if txt is not None:
            parent.newline()
            parent.write(txt)

        parent.level += 4

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.parent.level -= 4


class Parens(object):
    __slots__ = ['parent']

    def __init__(self, parent):
        self.parent = parent

    def __enter__(self):
        self.parent.write('(')
        return self

    def __exit__(self, type, value, traceback):
        self.parent.write(')')
