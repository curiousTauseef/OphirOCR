# styledtextbox.py

# todo: component styles (like e.g. TextBox), if possible
# XXX Lots of work to be done on this one...

import wx
import wxPython.stc as stc
import waxobject

# create a method that calls StyledTextBox.SendMsg with a given code
def _bindcmd(code):
    def cmd(self):
        self.SendMsg(code)
    return cmd

class StyledTextBox(waxobject.WaxObject, stc.wxStyledTextCtrl):

    __events__ = {
        'Char': wx.EVT_CHAR,
        'CharAdded': stc.EVT_STC_CHARADDED, # a character was added
        'Change': stc.EVT_STC_CHANGE,
         # change is made to the text of the document, except for styles
        'DoubleClick': stc.EVT_STC_DOUBLECLICK,
        'MarginClick': stc.EVT_STC_MARGINCLICK,
        'Modified': stc.EVT_STC_MODIFIED,
         # document was modified, including style changes
        'Paint': stc.EVT_STC_PAINTED, # occurs after all painting is complete
        #'PosChanged': stc.EVT_STC_POSCHANGED,  # deprecated
        'StyleNeeded': stc.EVT_STC_STYLENEEDED,
        'UpdateUI': stc.EVT_STC_UPDATEUI,
    }

    def __init__(self, parent, size=(125,-1)):
        # TODO: set lots of options here

        style = 0
        stc.wxStyledTextCtrl.__init__(self, parent, wx.NewId(), size=size,
         style=style)
        self._language = None

        self.BindEvents()
	
    #
    # events

    # this dummy method is necessary, otherwise the StyledTextBox starts
    # complaining... probably because the existing OnPaint method will be
    # hooked up to stc.EVT_STC_PAINTED, which is Wrong.
    def OnPaint(self, event):
        event.Skip()

    def write(self, s):
        # Added so we can use a TextBox as a file-like object and redirect
        # stdout to it.
        self.AddText(s)

    #
    # synchronize part of the APIs of TextBox and StyledTextBox

    def AppendText(self, s):
        self.AddText(s)

    def Clear(self):
        self.ClearAll()

    def GetValue(self):
        return self.GetText()

    def GetStringSelection(self):
        return self.GetSelectedText()

    def Replace(self, start, end, text):
        self.SetTargetStart(start)
	self.SetTargetEnd(end)
	self.ReplaceTarget(text)

    def GetCurrentLineNumber(self):
        return self.LineFromPosition(self.GetCurrentPos())

    def GetLineText(self, lineno):
        return self.GetLine(lineno)

    #
    # cursor

    CursorEnd = _bindcmd(stc.wxSTC_CMD_LINEEND)
    CursorHome = _bindcmd(stc.wxSTC_CMD_HOME)
    CursorRight = _bindcmd(stc.wxSTC_CMD_CHARRIGHT)
    CursorLeft = _bindcmd(stc.wxSTC_CMD_CHARLEFT)
    CursorDocumentStart = _bindcmd(stc.wxSTC_CMD_DOCUMENTSTART)
    CursorDocumentEnd = _bindcmd(stc.wxSTC_CMD_DOCUMENTEND)

    #
    # editing

    DeleteCurrentLine = _bindcmd(stc.wxSTC_CMD_LINEDELETE)

    #
    # line endings

    def GetEOLMode(self):
        """ Return the EOL mode.  This is a string that can be 'mac', 'dos',
            or 'unix'. """
        eolmode = stc.wxStyledTextCtrl.GetEOLMode(self)
        return _eol_to_string[eolmode]

    def SetEOLMode(self, mode):
        """ Set the EOL mode.  <mode> can be a wxSTC flag, or a string 'unix',
            'dos', 'windows' or 'mac'.  ('dos' and 'windows' are the same.) """
        if isinstance(mode, basestring):
            mode = _string_to_eol[mode]
        stc.wxStyledTextCtrl.SetEOLMode(self, mode)

    def ConvertEOLs(self, mode):
        """ Convert the line endings to the given mode.  <mode> can be a wxSTC
            flag, or a string 'unix', 'dos', 'windows', or 'mac'. """
        if isinstance(mode, basestring):
            mode = _string_to_eol[mode]
        stc.wxStyledTextCtrl.ConvertEOLs(self, mode)

    #
    # styles

    def _getstyleconst(self, name):
        try:
            return language_states[self._language][name]
        except KeyError:
            pass

        try:
            return other_styles[name]
        except KeyError:
            raise KeyError, "Unknown style name '%s'" % (name,)

    def SetLanguage(self, language):
        self._language = language
        langconst = languages[language]
        self.SetLexer(langconst)

    def SetStyle(self, state, style):
        #stateconst = language_states[self._language][state]
        const = self._getstyleconst(state)
        self.StyleSetSpec(const, style)

    def StyleSetFont(self, style, font):
        """ If self._language is set, this can be called with a string for
            <state>, e.g. 'default' or 'comment', etc. """
        if isinstance(style, str) or isinstance(style, unicode):
            #style = language_states[self._language][style]
            style = self._getstyleconst(style)
        stc.wxStyledTextCtrl.StyleSetFont(self, style, font)

    def SetFont(self, font):
        if self._language and self._language != 'container':
            for name, value in language_states[self._language].items():
                self.StyleSetFont(value, font)
        else:
            self.StyleSetFont(stc.wxSTC_STYLE_DEFAULT, font)

#
# styles

# XXX maybe a wrapper function can be used to make the style strings

# languages supported by the STC lexer
languages = {
    'container': stc.wxSTC_LEX_CONTAINER,
    'null': stc.wxSTC_LEX_NULL,
    'python': stc.wxSTC_LEX_PYTHON,
    'c++': stc.wxSTC_LEX_CPP,
    'html': stc.wxSTC_LEX_HTML,
    'xml': stc.wxSTC_LEX_XML,
    'lisp': stc.wxSTC_LEX_LISP,
    'scheme': stc.wxSTC_LEX_LISP,
    'ruby': stc.wxSTC_LEX_RUBY,
    'groovy': stc.wxSTC_LEX_RUBY,   # for now, this will have to do
    # XXX more...
}

language_states = {
    'python': {
        'default': stc.wxSTC_P_DEFAULT,
        'comment': stc.wxSTC_P_COMMENTLINE,
        'number': stc.wxSTC_P_NUMBER,
        'string': stc.wxSTC_P_STRING,
        'character': stc.wxSTC_P_CHARACTER,
        'keyword': stc.wxSTC_P_WORD,
        'triple_string': stc.wxSTC_P_TRIPLE,
        'triple_double_string': stc.wxSTC_P_TRIPLEDOUBLE,
        'classname': stc.wxSTC_P_CLASSNAME,
        'defname': stc.wxSTC_P_DEFNAME,
        'operator': stc.wxSTC_P_OPERATOR,
        'identifier': stc.wxSTC_P_IDENTIFIER,
        'comment_block': stc.wxSTC_P_COMMENTBLOCK,
        'string_eol': stc.wxSTC_P_STRINGEOL,
    },

    'lisp': {
        'default': stc.wxSTC_LISP_DEFAULT,
        'comment': stc.wxSTC_LISP_COMMENT,
        'number': stc.wxSTC_LISP_NUMBER,
        'keyword': stc.wxSTC_LISP_KEYWORD,
        'string': stc.wxSTC_LISP_STRING,
        'stringeol': stc.wxSTC_LISP_STRINGEOL,
        'identifier': stc.wxSTC_LISP_IDENTIFIER,
        'operator': stc.wxSTC_LISP_OPERATOR,
    },

    'groovy': {
    },

    # XXX add more languages
}
language_states['scheme'] = language_states['lisp']

other_styles = {
    'line_number': stc.wxSTC_STYLE_LINENUMBER,
    'brace_bad': stc.wxSTC_STYLE_BRACEBAD,
    'brace_match': stc.wxSTC_STYLE_BRACELIGHT,
    'default': stc.wxSTC_STYLE_DEFAULT,
}

_eol_to_string = {
    stc.wxSTC_EOL_CR: 'mac',      # \r
    stc.wxSTC_EOL_CRLF: 'dos',    # \r\n
    stc.wxSTC_EOL_LF: 'unix'      # \n
}

_string_to_eol = {
    'unix': stc.wxSTC_EOL_LF,
    'dos': stc.wxSTC_EOL_CRLF,
    'windows': stc.wxSTC_EOL_CRLF,
    'mac': stc.wxSTC_EOL_CR,
}
