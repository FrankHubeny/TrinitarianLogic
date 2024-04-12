# altrea/exception

"""This module contains the following exceptions:

- AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
- BlockNotAvailable: The block is outside the scope of the current block.
- BlockNotClosed: The block cannot be accessed until it is closed.
- ConclusionsNotTheSame: The conclusions of blocks are not the same.
- DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
    as one of the assumptions starting a block.
- NoSuchNumber: The referenced line does not exist in the proof.
- NotAntecedent: The statement is not the antecedent of the implication.
- NotAssumption: The referenced statement is not an assumption, the first line of a block.
- NotConjunction: The statement is not a conjunction.
- NotContradiction: Two referenced statements are not contradictions.
- NotDisjunction: The statement is not a disjunction.
- NotFalse: The referenced statement is not False.
- NotSameBlock: Two referenced statements are not from the same block.
- NotSameLevel: The two blocks are not at the same level.
- PremiseBeginsProof: A premise was added after other proof lines besides Premise or Goal.
- ScopeError: The referenced statement is not accessible.
"""

class AssumptionNotFound(Exception):
    """The assumption from a block does not match a disjunct of the disjunction.
    
    Parameters:
        assumption: The assumption that does not match one of the disjuncts in the disjunction.
        disjunction: The disjunction the containing the available disjuncts.
    """

    def __init__(self, assumption, disjunction):
        self.assumption = assumption
        self.disjunction = disjunction

    def __str__(self):
        return f'The assumption {self.assumption} does not match a disjunct in {self.disjunction}.'

class BlockNotAvailable(Exception):
    """The block is outside the scope of the current block.
    
    Parameter:
        blockid: The name of the block that is not available.
    """

    def __init__(self, blockid: str):
        self.blockid = blockid
    
    def __str__(self):
        return f'The block {self.blockid} is not available.'
    
class BlockNotClosed(Exception):
    """The block cannot be accessed until it is closed.
    
    Parameter:
        blockid: The name of the block that is not closed.
    """

    def __init__(self, blockid: str):
        self.blockid = blockid

    def __str__(self):
        return f'The block {self.block} is unavailable because it has not been closed.'
    
class ConclusionsNotTheSame(Exception):
    """The conclusions of blocks are not the same.  
        
    Parameters:
        conclusion: The first conclusion to be matched by the others.
        nonmatching: The conclusion that did not match.
    """

    def __init__(self, conclusion, nonmatching):
        self.conclusion = conclusion
        self.nonmatching = nonmatching

    def __str__(self):
        return f'The conclusion {self.nonmatching} did not match {self.conclusion}.'
    
class DisjunctNotFound(Exception):
    """The disjunct from the disjunction on the specified line was not found
    as one of the assumptions starting a block.
    
    Parameters:
        disjunct: This is the disjunct that was not found.
        disjunction: This is the full disjunction with all disjuncts.
        line: This is the line containing the disjunction.
    """

    def __init__(self, disjunct, disjunction, line: int):
        self.disjunct = disjunct
        self.disjunction = disjunction
        self.line = line

    def __str__(self):
        return f'The disjunct {self.disjunct} from the disjunction {self.disjunction} on lin {self.line}\
            was not found as an assumption of any of the referenced subproofs.'
    
class NoSuchNumber(Exception):
    """The referenced line does not exist in the proof.

    Parameter:
        line: The line number requested by the call.
    """
    def __init__(self, line: int):
        self.line = line

    def __str__(self):
        return f'The referenced line number {self.line} does not exist in the proof.'

class NotAntecedent(Exception):
    """The statement is not the antecedent of the implication.
    
    Parameters:
        antecedent: The statement offered as the antecedent.
        implication: The statement offered as the implication.
    """

    def __init__(self, antecedent, implication):
        self.antecedent = antecedent
        self.implication = implication

    def __str__(self):
        return f'The statement {self.antecedent} is not the antecedent of the implication {self.implication}.'
    
class NotAssumption(Exception):
    """The statement is not an assumption.

    Parameter:
        line: The line of the statement that is not an assumption.
    """

    def __init__(self, line):
        self.line = line

    def __str__(self):
        return f'The original statement {self.statement} does not match the rebuilt one: {self.rebuiltstatement}.'

class NotConjunction(Exception):
    """The statement is not a conjunction.
    
    Parameter:
        line: The line number of the statement in the proof.
        statement: The statement that caused the error.
    """

    def __init__(self, line, statement):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The statement {self.statement} on line {self.line} is not a conjunction.'
    
class NotContradiction(Exception):
    """Two referenced statements are not contradictions.

    Parameters:
        start: The start line of the alleged contradiction.
        end: The last line of the alleged contradiction.
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f'The statements at lines {self.start} and {self.end} are not contradictions.'
    
class NotDisjunction(Exception):
    """The statement is not a disjunction.
    
    Parameter:
        line: The line number of the statement in the proof.
        statement: The statement that caused the error.
    """

    def __init__(self, line, statement):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The statement {self.statement} on line {self.line} is not a disjunction.'

class NotFalse(Exception):
    """The referenced statement is not False.

    Parameters:
        line: The number of the line claimed to be False.
        statement: The startment on the line.
    """

    def __init__(self, line, statement):
        self.line = line
        self.statement = statement

    def __str__(self):
        return f'The line {self.line} contains {self.statement} which is not False.'


class NotSameBlock(Exception):
    """Two referenced statements are not from the same block.

    Parameter:
        start: The start line number of the subproof.
        startblock: The name of the block the start line is in.
        end: The last line number of the subproof.
        endblock: The name of the block the end line is in.
    """

    def __init__(self, start, startblock, end, endblock):
        self.start = start
        self.startblock = startblock
        self.end = end
        self.endblock = endblock

    def __str__(self):
        return f'The statement at line {self.start} is in block {self.startblock} \
            but the statement in lin {self.end} is in block {self.endblock}.'
    
class NotSameLevel(Exception):
    """The two blocks are not at the same level.
    
    Parameter:
        firstblock(list): The first block.
        secondblock(list): The second block. 
    """
    
    def __init__(self, firstblock: list, secondblock: list):
        self.firstblock = firstblock
        self.secondblock = secondblock

    def __str__(self):
        return f'The block {self.firstblock} is not at the same level as the second block {self.secondblock}.'

class PremiseBeginsProof(Exception):
    """Premises are added only at the beginning of the proof.
    
    Parameter:
        premise: The premise that was added after other statements besides Premise were added.
    """

    def __init__(self, premise):
        self.premise = premise
    
    def __str__(self):
        return f'The premise {self.premise} was added after proof lines besides Premise or Goal were added.'
    
class ScopeError(Exception):
    """The referenced statement is not accessible.

    Parameters:
        line: The line number requested by the call.
        linelevel: The level of the line based upon how many open subproofs there are.
        currentlevel: The current level of the proof.
    """

    def __init__(self, line: int, linelevel: int, currentlevel: int):
        self.line = line
        self.linelevel = linelevel
        self.currentlevel = currentlevel

    def __str__(self):
        return f'Line {self.line} at level {self.linelevel} is outside the current level {self.currentlevel}.'
