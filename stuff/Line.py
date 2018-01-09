import sublime
import sublime_plugin
from Tmov.Gen import *
from Tmov.Parse import *

def linear(view, region):
  r = normalized(region)
  (startLine, _) = view.rowcol(r.a)
  (endLine, _) = view.rowcol(r.b)
  i = startLine
  lines = []
  while i <= endLine:
    p = view.text_point(i, 0)
    l = smallLine(view, p)
    lines.append(l)
    i += 1
  return lines

# def smallLine(view, point):
#   l = normalized(view.line(point))
#   (firstBlock, typee) = block(view, sublime.Region(l.a, l.a + 1), direction = 1)
#   (hereLine, _) = view.rowcol(point)
#   (endBlockLine, _) = view.rowcol(firstBlock.b)
#   if endBlockLine != hereLine:
#     # case when the line is full of spaces (or empty): the firstBlock then extends
#     # to the start of the next line, which is not the desired thing
#     # so we return a zero-length region stopping right before the newline
#     return sublime.Region(l.b, l.b)
#   if typee == C.space:
#     return sublime.Region(firstBlock.b, l.b)
#   return l

def nextLine(view, region):
  r = normalized(region)
  (lIndex, _) = view.rowcol(r.b)
  p = view.text_point(lIndex + 1, 0)
  return smallLine(view, p)

def prevLine(view, region):
  r = normalized(region)
  (lIndex, _) = view.rowcol(r.a)
  p = view.text_point(lIndex - 1, 0)
  return smallLine(view, p)



class LineMode():
  # does not work for more than one line at a time
  def delete(view, edit, region):
    r = normalized(region)
    line = view.line(r.a)
    eof = view.size()
    line.a -= 1
    if line.a < 0: # we try to delete the first line
      line.b += 1 # delete the next newline
    if line.b == eof: # if we try to delete the last line
      pass
    else:
      pass
    view.erase(edit, line)
    return smallLine(view, r.a)

# newAfter
# newBefore
# toTheEnd
# toTheStart
# copy
# cut
# paste-add
# paste2
# paste-wipe
# goto start/middle/end of upper level

# section
# character
# subword
# expression: selecting all inside parentheses instead of just the paren
  # character
  # could be default, and the next word could still be inside the parens, eg:
  # aze|(abc, def)| aze
  # aze(|abc|, def) aze
  # aze(abc|,| def) aze
  # aze(abc, |def|) aze
  # aze|(abc, def)| aze
  # aze(abc, def) |aze|
  # there could be a key to erase the parens, or replace them, or to cut all
  # there is in it

  #and maybe i should add " to the alpha characters


# functions like delete shudn take care of creating a new selection after
# the deleting. it shud be the role of a subclass of TextCommand, sth like
# ChangeCommand, versus MotionCommand (currently called SelectionCommand)

# btw, Line.delete is bugging: it doesn't properly select the next line to select
# overall i think we need to extract ourselves from the quirks of sublime text,
# esp we need to directly change lines by their index, same for words

#aka: separate the appearances from the data underneath