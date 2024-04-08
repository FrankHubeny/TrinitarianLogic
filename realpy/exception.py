class ScopeError(Exception):
    """
    This exception occurs when an attempt is made to use a line in a subproof that had already been closed.

    Parameter
    =========

    linenumber: 
        The line number requested by the call.
    linelevel:
        The level of the line based upon how many open subproofs there are.
    currentlevel:
        The current level of the proof.
    """

    def __init__(self, linenumber: int, linelevel: int, currentlevel: int):
        self.linenumber = linenumber
        self.linelevel = linelevel
        self.currentlevel = currentlevel

    def __str__(self):
        return f'Line {self.linenumber} at level {self.linelevel} is outside the current level {self.currentlevel}.'

class NoSuchNumber(Exception):
    """
    This exception occurs when an attempt is made to use a line in a proof that does not yet exist.

    Parameter
    =========

    linenumber: 
    The line number requested by the call.
    """
    def __init__(self, linenumber: int):
        self.linenumber = linenumber

    def __str__(self):
        return f'The referenced line number {self.linenumber} does not exist in the proof.'

class RebuildFailed(Exception):
    """
    This procedure tests whether the user did an elimination of the correct statement. 
    For example, if the statement is an Or statment rather than the And he thought it was
    he would be able to split it into args, but it would not the the correct statement.
    This error message looks for such situations.

    Parameter
    =========

    statement:
        The original statement that was split into its args.
    rebuiltstatement:
        This is the result of building the arguments using the intended And.
    """

    def __init__(self, statement, rebuiltstatement):
        self.statement = statement
        self.rebuiltstatement

    def __str__(self):
        return f'The original statement {self.statement} does not match the rebuilt one: {self.rebuiltstatement}.'

class NotAssumption(Exception):
    """
    This procedure tests the line has the Assumption rule.

    Parameter
    =========

    linenumber:
        The linenumber of the statement that is not an assumption.
    """

    def __init__(self, linenumber):
        self.linenumber = linenumber

    def __str__(self):
        return f'The original statement {self.statement} does not match the rebuilt one: {self.rebuiltstatement}.'

class NotSameLevel(Exception):
    """
    This procedure tests the line has the Assumption rule.

    Parameter
    =========

    start:
        The start linenumber of the subproof.
    end:
        The last linenumber of the subproof.
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f'The statements at lines {self.start} and {self.end} are not at the same level.'

class NotContradiction(Exception):
    """
    If two statements are not contradictions when they should be raise this exception.

    Parameter
    =========

    start:
        The start linenumber of the alleged contradiction.
    end:
        The last linenumber of the alleged contradiction.
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f'The statements at lines {self.start} and {self.end} are not contradictions.'

class UnclassifiedError(Exception):
    """
    This unclassified error should never be executed.  It is available in case some situation
    has not been covered by other error checking.

    Parameter
    =========

    notes:
        This is a string explaining what the calling procedure was doing at the time.
    """

    def __init__(self, notes: str):
        self.notes = notes

    def __str__(self):
        return f'An unknown error occurred: {self.notes}' 
