

import sublime
import sublime_plugin
#from Tmov.Base import *
from Tmov.Base import *

class TmovCommand(sublime_plugin.TextCommand):
  def run(self, edit, args, new_mode = None):
    view = self.view
    modeName = view.settings().get("tmov-token-mode")
    mode = modes[modeName]
    if new_mode != None and new_mode != modeName:
      newMode = modes[new_mode]
      setTokenMode(view, newMode)
      mode = newMode

    mode.call(args, view, edit)

class ToggleTmovCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.settings().get('tmov_isMoveMode'):
      plugin_unloaded()
    else:
      _plugin_loaded()

def setTokenMode(view, mode):
  view.settings().set('tmov-token-mode', mode.name)
  view.set_status('tmov-token-mode', "(Token " + mode.name + ")")

editModeStr = "Edit"
moveModeStr = "Move"

def setEditMode(view):
  setKeyMode(view, editModeStr)
  view.settings().set('inverse_caret_state', False)
  view.settings().set('tmov_isMoveMode', False)

def setMoveMode(view):
  setKeyMode(view, moveModeStr)
  view.settings().set('inverse_caret_state', True)
  view.settings().set('tmov_isMoveMode', True)

def setKeyMode(view, mode):
  view.settings().set('tmov-key-mode', mode)
  view.set_status('tmov-key-mode', "(Key " + mode + ")")

def _plugin_loaded():
  initMode = Line
  for window in sublime.windows():
    for view in window.views():
      setMoveMode(view)
      setTokenMode(view, initMode)
      initMode.call('switch', view, None)

def plugin_unloaded():
  for w in sublime.windows():
    for v in w.views():
      setEditMode(v)
      # delete settings?







# zererg





class Token():
  name = "**TOKEN**"

  @staticmethod
  def fromStr(cls, str):
    # movement
    if str == "next":
      return cls.next
    if str == "toMiddle":
      return cls.toMiddle
    if str == "toEnd":
      return cls.toEnd 

    if str == "delete":
      return cls.delete
    if str == "change":
      return cls.change

    if str == "fuse":
      return cls.fuse

    if str == "add":
      return cls.add
    if str == "new":
      return cls.new

    if str == "paste":
      return cls.paste
    if str == "copy":
      return cls.copy
    if str == "copyForget":
      return cls.copyForget
      
    if str == "switch":
      return cls.switch



  @classmethod
  def call(cls, argsStr, view, edit):
    handler = cls.foreach
    toEditMode = False
    where = None

    args = argsStr.split(" ")
    if len(args) == 1:
      action = args[0]
      direction = onward
    else:
      (action, _direction) = args
      direction = directions[_direction]
    
    l = action.split(":")
    if len(l) == 2 and l[0] == "paste":
      mstr = l[0]
      where = cls.fromStr(l[1])
    else:
      mstr = action
    method = Token.fromStr(cls, mstr)

    if mstr in ["change", "new", "add"]:
      toEditMode = True

    if where != None: # for pasting
      newSel = handler(cls, method, view, edit, direction, where)
    else:
      newSel = handler(cls, method, view, edit, direction)

    sel = view.sel()
    sel.clear()
    if mstr in ["delete", "cut"]:
      for r in newSel:
        r = cls.next(view, edit, r, onward)
        sel.add(r) 
    else:
      for r in newSel:
        sel.add(r)

    if toEditMode:
      cls.toEditMode(view, edit)
  
  # @staticmethod
  # def do_once(cls, boundMeth, view, edit, direction):
  #   boundMeth(view, edit, direction)

  @staticmethod
  def foreach(cls, boundMeth, view, edit, direction):
    sel = view.sel()
    newSel = []
    for region in sel:
      res = boundMeth(view, edit, region, direction)
      if res != None:
        if not isinstance(res, list):
          res = [res]
        newSel = newSel + res
    return newSel

  @classmethod
  def toEditMode(cls, view, edit):
    setEditMode(view)

  @classmethod
  def switch(cls, view, edit, region, direction):
    return cls.convert(view, region)

  @classmethod
  def change(cls, view, edit, region, direction):
    return region

  @classmethod
  def paste(cls, view, edit, region, direction, where):
    str = cls.toPaste(view)
    if str == "":
      return region # do noth
    r = where(view, edit, region, direction)
    view.replace(edit, r, str)
    p = extremity(r, direction)
    pastedRegion = relativeRegion(p, len(str))
    return cls.convert(view, pastedRegion)
  
  @classmethod
  def new(cls, view, edit, region, direction):
    sep = cls.separator(view, region, direction) # indent of new line depends on previous
    p = extremity(region, direction)
    view.insert(edit, p, sep)
    if direction == onward:
      return zeroRegion(p + direction*len(sep))
    else:
      return zeroRegion(p) # adding the sep to the left moves us to the right location
    
  @classmethod
  def add(cls, view, edit, region, direction):
    p = extremity(region, direction)
    return zeroRegion(p)

  @classmethod
  def fuse(cls, view, edit, region, direction, subsep = None):
    if subsep == None:
      subsep = cls.subseparator
    next = cls.next(view, edit, region, direction, pongIfFails = False)
    if next == None:
      return region # do nothing: nothing to fuse with in that direction
    bwn = betweenRegions(region, next)
    view.replace(edit, bwn, subsep)
    return cls.convert(view, region)

  @classmethod
  def delete(cls, view, edit, region, direction):
    todel = cls.spacesAround(view, region) # clipped if word or line (since line musn eat the next's indent)
    replacement = cls.basicSeparator
    if (cls.isFirst(view, region)
        or cls.isLast(view, region)
        or len(todel) == len(region)):
      replacement = ""
    view.replace(edit, todel, replacement)
  
  @classmethod
  def pongNext(cls, view, edit, direction):
    newDirection = rev(direction)
    r = etherBound(view, newDirection)
    return Word.next(view, edit, r, newDirection, pongIfFails = False)
  # copy
  # paste = paste + "forget"
  # cut = copy + delete
  # copyForget = "forget" + copy


# values:
#   basicSeparator

# methods:
#   spacesAround
#   convert
#   toPaste
#   next
#   isFirst
#   isLast

class Line(Token):
  name = "Line"

  subseparator = " "
  

  @staticmethod
  def convert(view, region):
    return Line.smallLine(view, region.a)

  @staticmethod
  def smallLine(view, point):
    l = Line.line(view, point)
    indent = Line.indent(view, l)
    return mkRegion(indent.b, l.b)

  @staticmethod
  def line(view, point):
    return normalized(view.line(point))

  @staticmethod
  def indent(view, line):
    (blockOne, blockOneType) = block(view, charRegion(line.a), onward)
    if blockOneType == C.space:
      indent = clipped(view, blockOne)
      return indent
    else:
      return zeroRegion(line.a)

  @staticmethod
  def next(view, edit, region, direction, pongIfFails = True):
    p = extremity(region, direction)
    (ix, _) = view.rowcol(p)
    (eof, _) = view.rowcol(view.size())
    nextExists = not ((ix == 0 and direction == backward)
        or (ix == eof and direction == onward))
    
    if nextExists:
      p = view.text_point(ix + direction, 0)
      return Line.smallLine(view, p)

    if not pongIfFails:
      return None
    return Line.smallLine(view, p)

  @staticmethod
  def separator(view, region, direction):
    p = extremity(region, direction)
    indent = Line.indent(view, Line.line(view, p))
    indentStr = view.substr(indent)
    # if direction == onward:        
    return newline + indentStr
    # else:
    #   return indentStr + newline




class Word(Token):
  name = "Word"

  subseparator = ""
  # @staticmethod
  # def convert(view, region):
  #   left = block(view, region, backward).a
  #   leftBorder = borderingRegion(view, left, backward)
  #   return Word.next(view, edit, leftBorder, onward, pongIfFails = True)

  @staticmethod
  def next(view, edit, region, direction, pongIfFails = True):
    (start, typeStart) = block(view, region, direction)
    p = extremity(start, direction)
    r = mkRegion(p, p + direction)
    (here, typeHere) = block(view, r, direction)
    res = Word._next(view, direction, typeStart, typeHere, here)

    if res != None:
        (res, _) = res
        return res

    if pongIfFails:
      #res = Word.next(view, edit, etherBound(view, rev(direction)), rev(direction), pongIfFails = False)
      return Char.pongNext(view, edit, direction)
    else:
      return None

  @staticmethod
  def _next(view, direction, typePrev, typeHere, here):
    p = extremity(here, direction)
    r = mkRegion(p, p + direction)
    (there, typeThere) = block(view, r, direction)

    ans = Word._diagnosis(typePrev, typeHere, typeThere)
    if ans == "pong":
      return None
    if ans == "here":
      return (here, typeHere)
    # else:
    return Word._next(view, direction, typeHere, typeThere, there)

  @staticmethod
  def _diagnosis(typeBef, typeHere, typeAft):
    if typeHere == C.ether:
      return "pong"
    if typeHere in [C.symbol, C.alpha, C.control]:
      return "here"
    if typeHere == C.symbol:
      allowed = [C.control, C.space, C.ether]
      if typeBef in allowed and typeAft in allowed:
        return "here"
    return "cont"

  @staticmethod
  def separator(view, region, direction):
    return " "



class Char(Token):
  name = "Char"

  subseparator = ""

  @staticmethod
  def next(view, edit, region, direction, pongIfFails = True):
    p = extremity(region, direction)
    eof = view.size()
    nextExists = not (p == 0 or p == eof)
    if nextExists:
      return mkRegion(p, p + direction)
    # else
    if pongIfFails:
      return Char.pongNext(view, edit, direction)
    else:
      return None

  @staticmethod
  def separator(view, region, direction):
    return ""




modes = {'Line': Line, 'Word': Word, 'Char': Char}








# betweenRegions

# zeroRegion

# boundary (extremity)

# relativeRegion



