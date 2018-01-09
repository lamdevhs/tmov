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