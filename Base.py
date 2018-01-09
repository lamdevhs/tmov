import sublime
import sublime_plugin


class CLang():
  def __init__(self,
      symbolValues = None,
      spaceValues = None,
      controlValues = None):
    if symbolValues == None:
      self.symbol = C.symbols.replace("_", "")
    if controlValues == None:
      self.control = C.controls
    if spaceValues == None:
      self.space = C.spacing

  def charType(self, char):
    if char in self.control:
      return C.control
    if char in self.space:
      return C.space
    # if self.alpha != None:
    #   if char in self.alpha:
    #     if char in self.symbol:
    #       return C.alphaSymbol # is either one of them
    #     return C.alpha
    #   return C.symbol
    if char in self.symbol:
      return C.symbol
    return C.alpha # by negative definition


class Sym():
  def __init__(self, repr):
    self.repr = repr
  def __repr__(self):
    return self.repr

class C():
  # i defined \r = \15 to be a control
  # no idea what it'll do on windows-made
  # files
  controls = ("\0\1\2\3\4\5\6\7"
           + "\10" +  "\13\14\15\16\17"
           + "\20\21\22\23\24\25\26\27"
           + "\30\31\32\33\34\35\36\37"
           + "\177")
  spacing = "\t\n "
  symbols = "!\"#$%&'()*+,-./"
  numbers = "0123456789"
  symbols += ":;<=>?@"
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  symbols += "[\\]^_`"
  letters += letters.lower()
  symbols += "{|}~"

  alpha = "Alpha"
  symbol = "Symbol"
  alphaSymbol = "AlphaSymbol"
  control = "Control"
  space = "Space"
  ether = "Ether" # represents the type of out-of-file regions

    # control: C.controls
    # space: C.spacing
    # symbol: C.symbols \ "_"
    # alpha: everything else

dftLang = CLang()



# -----------------------------
onward = 1
backward = -1
directions = {'onward': onward, 'backward': backward}

def rev(direction):
  return (- direction)


def normalized(region):
  a, b = region.a, region.b
  if region.a > region.b:
    return sublime.Region(b, a)
  return sublime.Region(a, b)



def blockAround(view, region):
  (right, t) = block(view, region, 1)
  (left, t2)  = block(view, region, -1)
  return (right.cover(left), t2, t)
  
def block(view, region, direction = 1):
  region = normalized(region)

    # empty region is akin to the character to the right
    # even if region.a == eof
  if region.a == region.b: 
    region.b += 1

  if direction == 1:
    return blockRight(view, region)
  return blockLeft(view, region)

def blockRight(view, region):
  t = charType(view, region.b - 1)
  ix = region.b
  eof = view.size()
  while ix < eof and charType(view, ix) == t:
    ix += 1
  # we reached ix == eof or we reached a character with
  # a different type: this position is the end of the region
  return (sublime.Region(region.a, ix), t)

def blockLeft(view, region):
  t = charType(view, region.a)
  ix = region.a - 1
  # eof = view.size()
  while ix >= 0 and charType(view, ix) == t:
    ix -= 1
  # we reached ix == eof or we reached a character with
  # a different type: this position is the end of the region
  return (sublime.Region(ix + 1, region.b), t) 

def charType(view, point):
  if point >= view.size() or point < 0:
    return C.ether
  c = view.substr(point)
  return dftLang.charType(c)


def mkRegion(x,y):
  return normalized(sublime.Region(x, y))

def nextBlock(view, region, direction):
  r = normalized(region)
  p = endPoint(r, direction)
  return block(view, mkRegion(p, p + direction), direction)

def charRegion(p):
  return sublime.Region(p, p+1)

def clipped(view, region): # to line, assuming normalized
  l = view.line(region.a)
  return intersect(region, l)

def spacesAround(view, region):
  (aft, aType) = nextBlock(view, region, onward)
  (bef, bType) = nextBlock(view, region, backward)
  out = region
  if aType == C.space:
    out = aft.cover(out)
  if bType == C.space:
    out = bef.cover(out)
  return out

def intersect(r1, r2):
  b = min(r1.b, r2.b)
  a = max(r1.a, r2.a)
  if a > b:
    return None
  return sublime.Region(a, b)

def betweenRegions(r1, r2):
  a = min(r1.b, r2.b)
  b = max(r1.a, r2.a)
  if a > b:
    return None
  return sublime.Region(a, b)

def extremity(region, direction):
  if direction == onward:
    return region.b
  return region.a

def borderingRegion(view, region, direction):
  p = extremity(region, direction)
  return mkRegion(p, p + direction)

def universe(view):
  return sublime.Region(0, view.size())

def etherBound(view, direction):
  return borderingRegion(view, universe(view), rev(direction))

def zeroRegion(point):
  return sublime.Region(point, point)


newline = '\n'