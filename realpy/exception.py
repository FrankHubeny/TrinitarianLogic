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

    line: 
        The line number requested by the call.
    """
    def __init__(self, line: int):
        self.line = line

    def __str__(self):
        return f'The referenced line number {self.line} does not exist in the proof.'

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

class NotSameBlock(Exception):
    """
    This procedure tests the line has the Assumption rule.

    Parameter
    =========

    start:
        The start line number of the subproof.
    startblock:
        The name of the block the start line is in.
    end:
        The last line number of the subproof.
    endblock:
        The name of the block the end line is in.
    """

    def __init__(self, start, startblock, end, endblock):
        self.start = start
        self.startblock = startblock
        self.end = end
        self.endblock = endblock

    def __str__(self):
        return f'The statement at line {self.start} is in block {self.startblock} \
            but the statement in lin {self.end} is in block {self.endblock}.'

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
    
class NotFalse(Exception):
    """
    The line number refers to a statement that was claimed to be False, but was not.

    Parameter
    =========

    line:
        The number of the line claimed to be False.
    statement:
        The startment on the line.
    """

    def __init__(self, line, statement):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The line {self.line} contains {self.statement} not False.'

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

class DisjunctNotFound(Exception):
    """
    The disjunct from the disjunction on the specified line was not found
    as one of the assumptions starting a subproof.
    
    Parameter
    =========
    
    disjunct:
        This is the disjunct that was not found.
    disjunction:
        This is the full disjunction with all disjuncts.
    line:
        This is the line containing the disjunction.
    """

    def __init__(self, disjunct, disjunction, line):
        self.disjunct = disjunct
        self.disjunction = disjunction
        self.line = line

    def __str__(self):
        return f'The disjunct {self.disjunct} from the disjunction {self.disjunction} on lin {self.line}\
            was not found as an assumption of any of the referenced subproofs.'
    
class AssumptionNotFound(Exception):
    """
    The assumptions do not match the disjuncts of the disjunction.
    
    Paramter
    ========
    
    assumption
        The assumption that does not match one of the disjuncts in the disjunction.
    disjunction:
        The disjunction the containing the available disjuncts.
    """

    def __init__(self, assumption, disjunction):
        self.assumption = assumption
        self.disjunction = disjunction

    def __str__(self):
        return f'The assumption {self.assumption} does not match a disjunct in {self.disjunction}.'
    
class ConclusionsNotTheSame(Exception):
    """
    The conclusions of subproofs have to be the same for disjunction elimination.  
    One of the conclusions did not match another.
        
    Parameter
    =========
        
    conclusion:
        The first conclusion to be matched by the others.
    nonmatching:
        The conclusion that did not match.
    """

    def __init__(self, conclusion, nonmatching):
        self.conclusion = conclusion
        self.nonmatching = nonmatching

    def __str__(self):
        return f'The conclusion {self.nonmatching} did not match {self.conclusion}.'
        
class NotDisjunction(Exception):
    """
    The statement is not a disjunction.
    
    Parameter
    =========
    
    line:
        The line number of the statement in the proof.
    statement
        The statement that caused the error.
    """

    def __init__(self, line, statement, constructed):
        self.line = line
        self.statement = statement
        self.constructed = constructed

    def __str__(self):
        return f'The statement {self.statement} on line {self.line} is not the disjunction {self.constructed}.'
    
class NotSameStatements(Exception):
    """
    A logical operator on a statement is being eliminated.  However, the parts of the statement
    are not the same when rejoined with this operator.  Hence the rule for elimination has
    been incorrectly apply.
    
    Parameter
    =========
    
    statement:
        The original statement claimed to be a certain kind.
    rule:
        The rule being invoked.
    rebuilt:
        The rebuilt statement using the operator claimed to be eliminated.
    """

    def __init__(self, statement, rule, rebuilt):
        self.statement = statement
        self.rule = rule
        self.rebuilt = rebuilt

    def __str__(self):
        return f'The statement {self.statement} does not apply to the {self.kind} rule when rebuilt as {self.rebuilt}'
    
