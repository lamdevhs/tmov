import sublime
import sublime_plugin
from Tmov.Parse import *

onward = 1
backward = -1

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


def endPoint(r, direction):
  if direction == onward:
    return r.b
  return r.a

def mkRegion(x,y):
  return normalized(sublime.Region(x, y))

def nextBlock(view, region, direction):
  r = normalized(region)
  p = endPoint(r, direction)
  return block(view, mkRegion(p, p + direction), direction)



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