import sublime
import sublime_plugin
from Tmov.Word import *
from Tmov.Line import *

class Position():
  line = 0
  char = 0
  word = 0

def pulgin_loaded():
  print("wawa")

class SelectionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.makeNewSel(edit)

  def makeNewSel(self, edit):
    sel = self.view.sel()
    newSel = []
    for r in sel:
      rs = self.todo(self.view, edit, r)
      if rs != None:
        newSel = newSel + rs
    sel.clear()
    for r in newSel:
      sel.add(r)

class NextWordCommand(SelectionCommand):
  def todo(self, view, edit, region):
      # (r, _) = blockAround(self.view, r)
      res = nextWord(view, onward, region)
      if res == None:
        return [region]
        # i think we'll want to change `nextWord`
        # to work line by line:
        # and when hitting an empty line,
        # setting a zero-wide selection at the lineEnd
      (r, _) = res
      return [r]

class PrevWordCommand(SelectionCommand):
  def todo(self, view, edit, region):
      res = nextWord(view, backward, region)
      if res == None:
        return [region]
        # i think we'll want to change `nextWord`
        # to work line by line:
        # and when hitting an empty line,
        # setting a zero-wide selection at the lineEnd
      (r, _) = res
      return [r]

class PrevLineCommand(SelectionCommand):
  def todo(self, view, edit, r):
      return [prevLine(view, r)]

class NextLineCommand(SelectionCommand):
  def todo(self, view, edit, r):
      return [nextLine(view, r)]

class EraseLineCommand(SelectionCommand):
  def todo(self, view, edit, r):
    # print(view.rowcol(self.view.size()))
    return [LineMode.delete(view, edit, r)]

class EraseWord(SelectionCommand):
  def todo(self, view, edit, r):
    return [WordMode.delete(view, edit, r)]

class LinearizeCommand(SelectionCommand):
  def todo(self, view, edit, r):
    # print(view.rowcol(self.view.size()))
    return linear(view, r)
# ----------------
# ----------------
# ----------------
# ----------------
# ----------------

class MycmdCommand3(sublime_plugin.TextCommand):
  def run(self, edit, a):
    sel = self.view.sel()[0]
    r = sel
    v = self.view
    print(v.substr(r.a-1) == "\n")
    print(v.rowcol(r.a))

    print(v.rowcol(r.b))
    print(r.b)
    print(v.substr(r))
    v.set_status("koo", "taaaaa")
    #self.view.insert(edit, 0, "\177")


def editMode(view):
  pass

def moveMode(view):
  pass

class FooCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print(polyFoo(Word, 4))
    print(polyFoo(Line, 4))
    print(AClass.call("aaa")(5))
    print(BClass.call("aaa")(5))
    return 
    view = self.view
    sel = view.sel()
    cpy = []
    for r in sel:
      cpy.append(r)
    for r in sel:
      print(r)
      view.erase(edit, r)
    for r in cpy:
      print(r)
    


def methodByStr(c, str):
  if str == "g":
    return c.g
  if str == "a":
    return c.a
  if str == "h":
    return c.h

class Z():
  a = 5
  def g(b, c):
    return c + 45

class B(Z):
  def h(self, foo):
    return self.g(foo) - 45


def polyFoo(dict, a):
  return dict["g"](a)

def w_g(a):
  return 100+a
def l_g(a):
  return 1000+a

Word = {"g":w_g}
Line = {"g":l_g}

class Poly():
  @classmethod
  def call(cls, name):
    if name == "aaa":
      return cls.aaa
  @classmethod
  def aaa(cls, a):
    return cls.g(a) + 42

class AClass(Poly):
  @staticmethod
  def g(a):
    return a + 10000000

class BClass(Poly):
  @staticmethod
  def g(a):
    return a + 100

A = AClass()
B = BClass()

class Action():
  @classmethod
  def mode(C, mode):
    if mode == "word":
      return C.word


class Next(Action):
  def word(view, a):
    return a + 15
  def line(view, a):
    return a + 1000

class NewAfter(Action):
  def mode(C, mode):
    return C.poly(mode)
  def poly(mode):
    return Next.mode(mode)


class Word():


  @staticmethod
  def move(view, direction):
    pass
