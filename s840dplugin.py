import sublime, sublime_plugin
import math
import re
import cProfile, pstats


class S840dTextCommand(sublime_plugin.TextCommand):
  """
  Base class for all S840D text commands.

  This class handles some common operations of all SINUMERIK
  related text operations and is therefore the base class for all
  the other text command classes.

  Basically it is used to show the commands in the command pallet
  only, if an s840d file is open.
  """

  # API method
  def is_visible(self):
    """
    Show the command in command pallet only, if open document is
    a valid SINUMERIK 840D source file.
    """
    return self.is_scope_s840d()

  # private member
  def is_scope_s840d(self):
    return (self.view.scope_name(0).find('source.s840d') >= 0)


class S840dMinifyCommand(S840dTextCommand):
  """
  Shrink code code as small as possible.

  Remove all comments and block numbers as well as all unrequired
  whitespaces to make the code as small as possible.
  """

  # API method
  def run(self, edit):

    # pr = cProfile.Profile()
    # pr.enable()

    # run only for SINUMERIK code
    if (self.is_scope_s840d()):
      view = self.view

      # get a copy of the file content
      region = sublime.Region(0, view.size())
      text = view.substr(region)
      # remove leading line spaces and block numbers
      text = re.sub(r'(?im)^(?:\s*N\d+)?\s*', '', text)
      # remove comments excluding some special header comments
      text = re.sub(r'(?im)\s*;(?!(?:\$PATH\=|DATE|VERSION|CHANGE)).*$', '', text)
      # no whitespaces around operators or seperators
      text = re.sub(r'[\t ]*([-+*/=><,\:\[\(\]\)]+)[\t ]*', r'\1', text)
      # remove multi space
      text = re.sub(r'[\t ]{2,}', ' ', text)
      # replace view's content
      view.replace(edit, region, text)

    # pr.disable()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr).sort_stats(sortby)
    # ps.print_stats()


class S840dBeautifyCommand(S840dTextCommand):
  """
  Make a minified code readable.

  Try to make the code more readable, by indending and inserting
  whitespaces by a fixed rule.
  """

  indents = 0
  tab_size = 2

  # API method
  def run(self, edit):

    # pr = cProfile.Profile()
    # pr.enable()

    # run only for SINUMERIK code
    if (self.is_scope_s840d()):
      view = self.view
      # get a copy of the file content
      view_region = sublime.Region(0, view.size())

      # this is basically what sublime's reindent does
      repl = ''
      for line in re.sub(r'(?im)^[ \t]*N\d+[ \t]*', '', view.substr(view_region)).split('\n'):
        repl += self.__indentdify(line.strip()) + '\n'

      # surround IF condition with parentheses
      # this is not required but looks better
      repl = re.sub(r'(?i)^[ \t]*IF\b[ \t]*([\w\d\$].*?(?=GOTO|;|$))', r'IF (\1) ', repl)
      # one whitespace before and after literal operators
      repl = re.sub(r'(?i)[ \t]*\bNOT\b[ \t]*', r' NOT ', repl)
      # no whitespaces around ( or [
      repl = re.sub(r'[ \t]*([\[\(]+)[ \t]*', r'\1', repl)
      # one whitespace before and after literal operators
      repl = re.sub(r'(?i)[ \t]*\b(AND|OR|XOR|B_AND|B_OR|B_XOR|B_NOT|MOD|DIV)\b[ \t]*', r' \1 ', repl)
      # one whitespace after ) or ]
      repl = re.sub(r'[ \t]*([\]\)\:]+)[ \t]*', r'\1 ', repl)
      # no whitespace around unary operators
      repl = re.sub(r'[ \t]*([-+*/=><,]+)[ \t]*', r'\1', repl)
      # one whitespace after keyword
      repl = re.sub(r'(?i)\b(IF|FOR|LOOP|UNTIL|WHILE)\b[ \t]*', r'\1 ', repl)

      # replace view's content and keep the last empty line only
      view.replace(edit, view_region, repl.strip() + '\n')

    # pr.disable()
    # sortby = 'name' # 'cumulative'
    # ps = pstats.Stats(pr)#.sort_stats(sortby)
    # ps.print_stats()

  def __indentdify(self,text):
    # block start
    if regexp_match(r'^(?i)(?:IF|FOR|LOOP|REPEAT|WHILE)\b', text):
      text = ' ' * self.indents + text
      if (text.find('GOTO') == -1):
        self.indents += self.tab_size
    else:
      # intermediate keyword
      if regexp_match(r'^(?i)ELSE\b', text):
        text = ' ' * (self.indents - self.tab_size) + text
      else:
        # block end
        if regexp_match(r'^(?i)(?:END(?:IF|FOR|LOOP|WHILE)|UNTIL)\b', text):
          self.indents = max(0, self.indents - self.tab_size)

        # don't indent block beginning with a label
        if not regexp_match(r'^\w+:', text):
          text = ' ' * self.indents + text

    return text


class S840dRenumberCommand(S840dTextCommand):
  """
  Add or update block numbers.

  Each CNC block normally starts with a number for identification.
  After editing the numbers may be mixed up. This command helps to
  update the block numbers.
  """

  # API method
  def run(self, edit):

    # run only for SINUMERIK code
    if (self.is_scope_s840d()):
      view = self.view
      # build whole content's region
      view_region = sublime.Region(0, view.size())
      # create a list of rows
      rows = view.substr(view_region).split('\n')
      # determine first block number so that all blocknumbers
      # will have the same amount of digits
      blockno_step = 10
      num_digits = int(math.log10(len(rows) * blockno_step))
      blockno = 10 ** num_digits
      # Add block numbers to each row which is not
      # empty or a comment. Try to keep indented
      # comments in position with blocks
      repl = ''
      for row in rows:
        # not an empty row
        if row:
          # unindented line comment
          if row[0] == ';':
            repl += row

          else:
            i = 0
            # skip leading white space
            while row[i] == ' ':
              i += 1

            # indented line comment
            if row[i] == ';':
              # insert spaces instead of 'Nxxx '
              repl += ' ' * (2 + num_digits) + row

            else:
              # skip existing block number
              if row[i] == 'N':
                i += 1
                while row[i] >= '0' and row[i] <= '9':
                  i += 1
                # skip one whitespace after block number
                # as it will be added anyway in the next step
                if row[i] == ' ':
                  i += 1

              # ordinary block
              repl += 'N' + str(blockno) + ' ' + row[i:]
              blockno += blockno_step

        # finalize the row
        repl += '\n'

      # replace view's content and keep the last empty line only
      view.replace(edit, view_region, repl.strip() + '\n')
