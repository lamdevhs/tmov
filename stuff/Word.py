import sublime
import sublime_plugin
from Tmov.Gen import *
from Tmov.Parse import *
from Tmov.Line import *

def etherBound(view, direction):
  if direction == onward:
    return sublime.Region(-1,0)
  
  eof = view.size()
  return sublime.Region(eof, eof + 1)






def nextWord(view, direction, region, pong = False):
  (start, typeStart) = block(view, region, direction)
  # eof = view.size()
  # if start.b >= eof: # ping pong
    # return prevWord(view, sublime.Region(eof, eof + 1))
  p = endPoint(start, direction)
  r = mkRegion(p, p + direction)
  (here, typeHere) = block(view, r, direction)
  res = _nextWord(view, direction, typeStart, typeHere, here)
  if res != None or pong:
    return res
  return nextWord(view, - direction, etherBound(view, - direction), pong = True)


def _nextWord(view, direction, typePrev, typeHere, here):
  p = endPoint(here, direction)
  r = mkRegion(p, p + direction)
  (there, typeThere) = block(view, r, direction)

  ans = diagnosis(typePrev, typeHere, typeThere)
  if ans == "pong":
    return None
  if ans == "here":
    return (here, typeHere)
  # else:
  return _nextWord(view, direction, typeHere, typeThere, there)

def diagnosis(typeBef, typeHere, typeAft):
  if typeHere == C.ether:
    return "pong"
  if typeHere in [C.symbol, C.alpha, C.control]:
    return "here"
  if typeHere == C.symbol:
    allowed = [C.control, C.space, C.ether]
    if typeBef in allowed and typeAft in allowed:
      return "here"
  return "cont"
  

# def prevWord(view, region, pong = False):
#   (start, typeStart) = block(view, region, direction = -1)
#   # if start.a == 0:
#     # return nextWord(view, sublime.Region(-1, 0))
#   p = start.a
#   (here, typeHere) = block(view, sublime.Region(p - 1, p), direction = -1)
#   res = pWord(view, typeStart, typeHere, here)
#   if res != None or pong:
#     return res
#   return nextWord(view, etherInf, pong = True)

# def pWord(view, typeAfter, typeHere, here):
  
#   ans = diagnosis(typeAfter, typeHere, typeThere)

#   if ans == "pong":
#     return None
#   if ans == "here":
#     return (here, typeHere)
#   # else:
#   return pWord(view, typeHere, typeThere, there)

def lineOf(view, point):
  return view.rowcol(point)[0]

def isFirstWord(view, word):
  shortL = smallLine(view, word.a)
  return word.a == shortL.a

def isLastWord(view, word):
  (next, _) = nextWord(view, onward, word)
    # ^ if it returns none, the doc is empty
    # if so, then word can only be zero-length
    # and then this function makes no sense

  return next.a == word.a or lineOf(view, next.a) > lineOf(view, word.a)
         # ^ ping pong
         

  # a priori, expected to be normalized
def regionLen(region):
  return region.b - region.a

class WordMode():
  # assuming region is a word
  def delete(view, edit, word):

    # contains error:
    # space shud be deleted only it will be trailing
    # or if two space areas will end up side by side
    # maybe i could just use smallLine to trim
    # the area to delete

    # if first/last word on line
    #   flag for not replacing by a space
    # if aft and bef are spaces:
    #   add them to todel, intersect with smallLine
    # replace with space or nothing

    if word.a == word.b:
      return word

    replacement = " "
    yesIsLastWord = isLastWord(view, word)
    yesIsFirstWord = isFirstWord(view, word)
    if yesIsFirstWord or yesIsLastWord:
      replacement = ""

    shortL = smallLine(view, word.a)
    todel = spacesAround(view, word)
    if regionLen(word) == regionLen(todel):
      # regions are identical, aka no spaces around the word
      replacement = ""
    else:
      print("not equal")
    todel = intersect(shortL, todel)

    view.replace(edit, todel, replacement)
    if yesIsLastWord and not yesIsFirstWord:
      res = nextWord(view, backward, sublime.Region(todel.a, todel.a + 1))
    else:
      res = nextWord(view, onward, sublime.Region(todel.a - 1, todel.a))
    if res != None:
      return res[0]

    return None # todo: handle that case, when we delete the last word


              # r = normalized(region)
              # if region.a == region.b: # case of when the whole buffer is empty
              #   return region

              # a_r = sublime.Region(r.b, r.b +1)
              # (aft, typeAft) = block(view, a_r, onward)

              # if not typeAft in [C.space, C.ether]:
              #   where = r.a
              #   view.erase(edit, r)
              #   return nextWord(view, onward, mkRegion(where - 1, where))[0]

              # line = view.line(region.a) # line without the newline
              # isLastNonSpaceOfLine = \
              #     typeAft == C.ether or \
              #     (typeAft == C.space and aft.b >= line.b) 

              # todel = r
              # if typeAft == C.space:
              #   if isLastNonSpaceOfLine:
              #     aft.b = line.b
              #   todel = todel.cover(aft)
              
              # if isLastNonSpaceOfLine:
              #   b_r = sublime.Region(r.a - 1, r.a)
              #   (bef, typeBef) = block(view, b_r, backward)

              #   if typeBef == C.space:
              #     (befLine, befCol) = view.rowcol(bef.a)
              #     (hereLine, _) = view.rowcol(r.a)
              #     if befLine == hereLine and \
              #        befCol != 0: ## bef isn't spanning over the line's indentation
              #        # note; we could also use smallLine to check that
              #       todel = todel.cover(bef)

              # where = todel.a
              # view.erase(edit, todel)
              # return nextWord(view, onward, mkRegion(where - 1, where))[0]

    # delete prev space iff
      # prev is space and not indent and word is last word
    # delete next space iff
      # exists, to end of line only