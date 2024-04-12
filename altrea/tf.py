# altrea/tf.py

"""Provides functions to construct a proof in propositional logic.

The module contains the following functions:

- `bicondelim(first, second, comments)` - Given a biconditional and one of the terms return the other term as a
        new statement.
- `bicondintro(blockids, comments)` - Construct a biconditional given two blocks showing
        the implications in both directions.
- `closeblock()` - Closes the current block.
- `conjelim(line, comments)` - Adds a new line in the proof for each conjunct in the statement at line number `line`.
- `conjintro(first, second, comments)` - Joins as conjunctions the states at line numbers `first` and `second`
- `disjelim(line, blockids, comments)` - Check the correctness of a disjunction elimination line before adding it to the proof.
- `disjintro(newdisjunct, line, comments)` - The newdisjunct statement and the statement at the line number 
        become a disjunction.
- `explosion(expr, line, comments)` - An arbitrary statement is entered in the proof given a false statement preceding it.
- `impelim(first, second, comments)` - From an implication and its antecedent derive the consequent.
- `impintro(blockid, comments)` - The command puts an implication as a line in the proof one level below the blockid.
- `negelim(first, second, comments)` - When two statements are contradictory a false line can be derived.
- `negintro(blockid, comments)` - When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
- `openblock(statement)` - Opens a new block.
- `reit(line, comments)` - A statement that already exists which can be accessed can be reused.
"""

from IPython.display import display, Math, Markdown, Latex, display_markdown, HTML
from sympy.logic.boolalg import Xor, And, Or, Not, Implies, Equivalent, eliminate_implications
from sympy.abc import x,y,z,A,B,C,D,E,F
from sympy import latex, S
import sympy
#import sympy.logic.boolalg
import altrea.exception

class Proof:
    """
    This class contains methods to construct, verify, display, save and retrieve proofs in 
    in truth functional logic.
    """

    columns = ['Statement', 'Block ID', 'Rule', 'Lines', 'Blocks', 'Status','Comment']
    statementindex = 0
    blockidindex = 1
    ruleindex = 2
    linesindex = 3
    blocksindex = 4
    statusindex = 5
    complete = 'Complete'
    completemessage = 'The proof is complete.'
    goalname = 'Goal'
    premisename = 'Premise'
    assumptionname = 'Assumption'
    disjintroname = 'DisjIntro'
    disjelimname = 'DisjElim'
    conjintroname = 'ConjIntro'
    conjelimname = 'ConjElim'
    reitname = 'Reit'
    impintroname = 'ImpIntro'
    impelimname = 'ImpElim'
    negintroname = 'NegIntro'
    negelimname = 'NegElim'
    indprfname = 'IndirectProof'
    bicondintroname = 'BiCondIntro'
    bicondelimname = 'BiCondElim'
    explosionname = 'Explosion'
    falsename = S.false
    warningmessage = 'Warning'

    def __init__(self, goal, premises=[], name: str = '', indx: str ='', comments: str = ''):
        """Create a Proof object with optional premises, but a specific goal.
        
        Parameters:
            premises: A list of premises for the proof.
            goal: The goal to be reached by the proof.
            name: The name assigned to the proof.
            comments: Comments that will go on the proof line associated with the goal."""
            
        self.name = name
        self.goal = goal
        self.comments = comments
        self.subproofname = '1'
        self.subproofcounts = [1]
        self.subproofs = []
        self.level = 0
        self.status = ''
        self.premises = premises
        self.lines = [[goal, self.subproofname, self.goalname, '', '', self.status, self.comments]]
        for i in self.premises:
            if i == self.goal:
                self.status = self.complete
                print(self.completemessage)
                self.lines.append([i, self.subproofname, self.premisename, '', '', self.status, ''])
                break
            else:
                self.lines.append([i, self.subproofname, self.premisename, '', '', self.status, '']) 

    def blockstartend(self, blockid: int | str):
        """Return the first and last lines of a named block of proof lines.
        
        Parameter:
            blockid: The name of the block of proof lines.
            
        Yields:
            The first and last statements of the block of proof lines.
            
        Exceptions:
            BlockNotAvailable: The block was not found in thee list of blocks.
            BlockNotClosed: The block was not closed and so is not complete.
        """

        strblockid = self.makestring(blockid)
        found = S.false
        for i in self.subproofs:
            if i[0] == strblockid:
                start = i[1][0]
                try:
                    end = i[1][1]
                except:
                    raise altrea.exception.BlockNotClosed(strblockid)
                found = S.true
                break
        if not found:
            raise altrea.exception.BlockNotAvailable(strblockid)
        return start, end

    def getassumption(self, blockid: int | str):
        """Return the first line of a closed block as the assumption of the block of proof lines.
        
        Parameter:
            blockid: The name of the block of code which the assumption begins.
            
        Yields:
            The assumption of the block of proof lines is returned.

        Exceptions:
            BlockNotAvailable: The block was not found in thee list of blocks.
            BlockNotClosed: The block was not closed and so is not complete.
        """

        assumption, conclusion = self.blockstartend(blockid)
        return assumption
    
    def getconclusion(self, blockid: int | str):
        """Return the last line of a closed block as the conclusion of a block of proof lines.
        
        Parameter:
            blockid: The name of the block of proof lines.
            
        Yields:
            The conclusion of the block of proof lines is returned.

        Exceptions:
            BlockNotAvailable: The block was not found in thee list of blocks.
            BlockNotClosed: The block was not closed and so is not complete.
        """

        assumption, conclusion = self.blockstartend(blockid)
        return conclusion
    
    def makestring(self, s: int | str) -> str:
        """Return a string if an int has been entered.
        
        Parameter:
            s: The string or int that has been entered.
            
        Yield:
            Return a string for s.
        """

        if type(s) == int:
            return str(s)
        else:
            return s
        
    def checkblock(self, line: int):
        """Check that the block of lines is accessible.
        
        Parameter:
            line: The line number of the statement in a specific block of proof lines.
            
        Exception:
            ScopeError: The block is not accessible.
        """

        block = self.lines[line][self.blockidindex]
        if self.subproofname != block and len(block) >= len(self.subproofname):
           raise altrea.exception.ScopeError(line, self.lines[line][self.blockidindex], self.subproofname)

    def checksamelevel(self, first: int, second: int):
        """Check if two statements are at the same level.
        
        Parameters:
            first: The first line number.
            second: The second line number.
        
        Exception:
            NotSameLevel: The two statements are not at the same level of the proof.
        """

        firstblock = self.lines[first][self.blockidindex]
        secondblock = self.lines[second][self.blockidindex]
        if len(firstblock) != len(secondblock):
           raise altrea.exception.NotSameLevel(firstblock, secondblock)

    def checkassumption(self, line):
        """Check if a line represent the assumption that opens a block of proof lines.
        
        Parameter:
            line: The line number of the statement.
            
        Exception:
            NotAssumption: The line number does not point to an assumption.
        """

        if self.lines[line][self.ruleindex] != self.assumptionname:
            raise altrea.exception.NotAssumption(line)

    def checkcomplete(self, statement):
        """Check if a proof is complete by comparing the last statement of the proof at 
            the bottom level with the stated goal of the proof.
        
        Parameter: 
            statement: The last statement at the bottom level of the proof.
        """

        if statement == self.goal and self.subproofname == '1':
            self.status = self.complete
            print(self.completemessage)

    def reftwolines(self, first: int, second: int) -> str:
        """A function to join two line numbers together to place in a proof line.
        
        Parameters:
            first: The first line number to join.
            second: The second line number to join.
            
        Yields:
            A string containing the first line number, a comma, and the second line number."""
        return ''.join([str(first), ', ', str(second)])
    
    def getstatement(self, line: int):
        """Return a statement from lines of a proof.
        
        Parameter:
            line: The line number of the proof.
            
        Yields:
            A statement from the line of the proof is returned.

        Exception:
            NoSuchNumber: The line number is not in the lines of the proof."""
        try:
            statement = self.lines[line][self.statementindex]
        except:
            raise altrea.exception.NoSuchNumber(line)
        return statement

    def addstatement(self, statement, rule: str, lines='', blocks='', status='', comments=''):
        """A a new line to the proof."""

        if self.status == self.complete:
            pass
        else:
            self.checkcomplete(statement)
            self.lines.append([statement, self.subproofname, rule, lines, blocks, status, comments])

    def addpremise(self, premise, comments: str = ''):
        for i in self.lines:
            if i[self.ruleindex] not in [self.goalname, self.premisename]:
                raise altrea.exception.PremiseBeginsProof(premise)
        self.addstatement(statement=premise,
                          rule=self.premisename,
                          comments=comments)
        
    def bicondelim(self, first: int, second: int, comments: str = ''):
        pass
        # """"""
        # test = []
        # firststatement = self.getstatement(first)
        # secondstatement = self.getstatement(second)
        # self.checkblock(first)
        # for c in biconditional.args:
        #     test.append(c)
        # testbiconditional = S.true
        # for t in test:
        #     testbiconditional = And(testbiconditional, t)
        # if testbiconditional != biconditional:
        #     raise altrea.exception.NotSameStatements(biconditional, self.bicondelimname, testbiconditional)
        # for statement in biconditional.args:
        #     self.addstatement(statement=statement, 
        #                       rule=self.bicondelimname, 
        #                       lines=str(first),
        #                       comments=comments
        #                      )

    def bicondintro(self, blockids: list, comments: str = ''):
        pass

    def closeblock(self):
        """Closes the block of statements that the proof is currently in.
        
        Example:
        >>> from altrea.tf import Proof
        >>> ex = Proof([A], C >> A, 'Example using closeblock')
        >>> ex.openblock(C)
        >>> ex.reit(1)
        >>> ex.closeblock()
        >>> ex.impintro('11')
        The proof is complete.  
        """

        end = len(self.lines)-1
        blockid = self.lines[end][self.blockidindex]
        for i in self.subproofs:
            if i[0] == blockid:
                i[1].append(end)
                break
        self.level -= 1
        self.subproofname = self.subproofname[:-1]

    def conjelim(self, line: int, comments: str = ''):
        """A conjunction is split into its individual conjuncts.
        
        Arguments:
            line: The line number of the conjunction to be split.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """

        # Test 1: The statement must exist.
        conjunction = self.getstatement(line)

        # Test 2: The statement must be in a block that can be accessed.
        self.checkblock(line)

        # Test 3: The statement must be a conjunction.
        if type(conjunction) != And:
            raise altrea.exception.NotConjunction(line, conjunction)
            # self.addstatement(statement=conjunction,
            #                   rule=self.conjelimname,
            #                   lines=str(line),
            #                   status=self.warningmessage,
            #                   comments='not a conjunction'
            #                   )
        else:
            conjuncts = sympy.logic.boolalg.conjuncts(conjunction)
            for statement in conjuncts:
                self.addstatement(statement=statement, 
                                  rule=self.conjelimname, 
                                  lines=str(line),
                                  comments=comments
                                 )
            
    def conjintro(self, first: int, second: int, comments: str = ''):
        """The statement at first line number is joined with And to the statement at second
        line number.

        Parameters:
            first: The line number of the first conjunct.
            second: The line number of the second conjunct.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """

        # Test 1: The two statements must exist.
        firstconjunct = self.getstatement(first)
        secondconjunct = self.getstatement(second)

        # Test 2: They must be in blocks which can be accessed.
        self.checkblock(first)
        self.checkblock(second)

        statement = And(firstconjunct, secondconjunct)
        self.addstatement(statement=statement, 
                          rule=self.conjintroname, 
                          lines=self.reftwolines(first, second), 
                          comments=comments
                         )

    def disjelim(self, line: int, blockids: list, comments: str = ''):
        """Check the correctness of a disjunction elimination line before adding it to the proof.
        
        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """

        # Test 1: The statement that is being eliminated has to be a valid statement.
        disj = self.getstatement(line)

        # Test 2: The statement must in a block that can be accessed.
        self.checkblock(line)

        # Test 3: The statement has to be a disjunction.
        if type(disj) != Or:
            raise altrea.exception.NotDisjunction(line, disj)
        
        # Setup for the next tests 4, 5, 6
        assumptions = []
        conclusions = []
        for i in blockids:
            start, end = self.blockstartend(i)
            assumptions.append(self.getstatement(start))
            conclusions.append(self.getstatement(end))

        # Test 4: Each disjunct must be an assumption in a subproof.
        for j in disj.args:
            found = S.false
            for k  in assumptions:
                if k == j:
                    found = S.true
            if not found:
                raise altrea.exception.DisjunctNotFound(j, disj, line)
            
        # Test 5: The assumptions of each subproof must be a disjunct in the disjunction.
        for j in assumptions:
            found = S.false
            for k in disj.args:
                if k == j:
                    found = S.true
            if not found:
                raise altrea.exception.AssumptionNotFound(k, disj)
            
        # Test 6: All of the conclusions of the subproofs must be identical.
        for i in conclusions:
            if i != conclusions[0]:
                raise altrea.exception.ConclusionsNotTheSame(conclusions[0], k)

        self.addstatement(statement=conclusions[0],
                          rule=self.disjelimname,
                          blocks=blockids,
                          comments=comments
                          )
            
    def disjintro(self, newdisjunct, line: int, comments: str = ''):
        """The newdisjunct statement and the statement at the line number become a disjunction.
        
        Parameters:
            newdisjunct: A statement that will be used in the disjunction.
            line: The line number of the statement that will be the other disjunct.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """

        # Test 1: The statment must exist.
        startdisjunct = self.getstatement(line)

        # Test 2: The statement must in a block that can be accessed.
        self.checkblock(line)

        statement = Or(startdisjunct, newdisjunct)
        self.addstatement(statement=statement, 
                          rule=self.disjintroname, 
                          lines=str(line),
                          comments=comments
                         )

    def explosion(self, expr, line: int, comments: str = ''):
        """An arbitrary statement is entered in the proof given a false statement preceding it.
        
        Parameters:
            expr: The statement to add to the proof.
            line: The line number of the proof containing the statement False.
            comments: A optional comment for this line of the proof.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
            """
        statement = self.getstatement(line)
        if statement != self.falsename:
            raise altrea.exception.NotFalse(line, statement)
        else:
            self.addstatement(statement=expr,
                              rule=self.explosionname,
                              lines=line,
                              comments=comments
                              )
            
    def impelim(self, first: int, second: int, comments: str = ''):
        """From an implication and its antecedent derive the consequent.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """

        # Test 1: The statements must exist.
        s1 = self.getstatement(first)
        s2 = self.getstatement(second)

        # Test 2: The statements must be in blocks that can be accessed.
        self.checkblock(first)
        self.checkblock(second)

        # Test 3: Check that the antecedent of the implication equals the other statement.
        if type(s2) == Implies:
            if s1 != s2.args[0]:
                raise altrea.exception.NotAntecedent(s1, s2)
            else:
                self.addstatement(statement=s2.args[1], 
                                  rule=self.impelimname, 
                                  lines=self.reftwolines(first, second),
                                  comments=comments
                                 )
        elif type(s1) == Implies:
            if s2 != s1.args[0]:
                raise altrea.exception.NotAntecedent(s2, s1)
            else:
                self.addstatement(statement=s1.args[1], 
                                  rule=self.impelimname, 
                                  lines=self.reftwolines(first, second),
                                  comments=comments
                                 )

    def impintro(self, blockid: int | str, comments: str = ''):
        """The command puts an implication as a line in the proof one level below the blockid.
        
        Parameters:
            blockid: The block identified by [start, end].
            comments: Comments added to the line.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """
        strblockid = self.makestring(blockid)
        (start, end) = self.blockstartend(strblockid)
        self.checksamelevel(start, end)
        self.checkassumption(start)
        antecedent = self.getstatement(start)
        consequent = self.getstatement(end)
        statement = Implies(antecedent, consequent)
        self.addstatement(statement=statement, 
                          rule=self.impintroname, 
                          blocks=strblockid,
                          comments=comments
                         )

    def openblock(self, statement):
        """Opens a uniquely identified block of statements with an assumption.
        
        Example:
        >>> from altrea.tf import Proof
        >>> ex = Proof([A], C >> A, 'Example using openblock')
        >>> ex.openblock(C)
        >>> ex.reit(1)
        >>> ex.closeblock()
        >>> ex.impintro('11')
        The proof is complete.

        AParameters:
            statement: The assumption that starts the block of derived statements.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """
        self.level += 1
        try:
            self.subproofname += str(self.subproofcounts[self.level] + 1)
            self.subproofcounts[self.level] += 1
        except:
            self.subproofcounts.append(1)
            self.subproofname += str(self.subproofcounts[self.level])
        start = len(self.lines)
        self.subproofs.append([self.subproofname, [start]])
        self.addstatement(statement=statement, 
                          rule=self.assumptionname
                         )
                
    def negelim(self, first: int, second: int, comments: str = ''):
        """When two statements are contradictory a false line can be derived.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.
            comments: An optional comment for this line.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.                       
        """
        
        s1 = self.getstatement(first)
        s2 = self.getstatement(second)
        if Not(s1) == s2:
            self.addstatement(statement=self.falsename, 
                              rule=self.negelimname, 
                              lines=self.reftwolines(first, second),
                              comments=comments
                             )
        else:
            raise altrea.exception.NotContradiction(first, second)
        
    def negintro(self, blockid: int | str, comments: str = ''):
        """When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
        
        Example:
        
        Parameter:
            blockid: The name of the block containing the assumption and contradiction.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """
        strblockid = self.makestring(blockid)

        # Test 1: Check that the block exists, is accessible and is closed.
        start, end = self.blockstartend(strblockid)
        s1 = self.getstatement(start)
        s2 = self.getstatement(end)

        # Test 2: Check that the last line is false: a contradiction
        if s2 != self.falsename:
            raise altrea.exception.NotFalse(end, s2)
        else:
            self.addstatement(statement=Not(s1), 
                              rule=self.negintroname,
                              blocks=strblockid,
                              comments=comments
                              )      

    def reit(self, line: int, comments: str = ''):
        """A statement that already exists which can be accessed can be reused.

        Parameter:
            line: The line number of the statement.

        Example:
            >>> from altrea.tf import Proof
            >>> ex = Proof([A], C >> A, 'Example using openblock')
            >>> ex.openblock(C)
            >>> ex.reit(1)
            >>> ex.closeblock()
            >>> ex.impintro('11')
            The proof is complete.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            DisjunctNotFound: The disjunct from the disjunction on the specified line was not found
                as one of the assumptions starting a block.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotConjunction: The statement is not a conjunction.
            NotContradiction: Two referenced statements are not contradictions.
            NotDisjunction: The statement is not a disjunction.
            NotFalse: The referenced statement is not False.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.

        """
        
        # Test 1: The statement must exist.
        statement = self.getstatement(line)

        # Test 2: The statement must be in a block which can be accessed.
        self.checkblock(line)

        self.addstatement(statement=statement, 
                          rule=self.reitname, 
                          lines=str(line),
                          comments=comments
                         )
        