# altrea/tf.py

"""Provides functions to construct a proof in propositional logic.

The module contains the following functions:

- `equivalent_elim(first, second, comments)` - Given a biconditional and one of the terms return the other term as a
        new statement.
- `equivalent_intro(blockids, comments)` - Construct a biconditional given two blocks showing
        the implications in both directions.
- `closeblock()` - Closes the current block.
- `and_elim(line, comments)` - Adds a new line in the proof for each conjunct in the statement at line number `line`.
- `and_intro(first, second, comments)` - Joins as conjunctions the states at line numbers `first` and `second`
- `or_elim(line, blockids, comments)` - Check the correctness of a disjunction elimination line before adding it to the proof.
- `or_intro(newdisjunct, line, comments)` - The newdisjunct statement and the statement at the line number 
        become a disjunction.
- `explosion(expr, line, comments)` - An arbitrary statement is entered in the proof given a false statement preceding it.
- `implies_elim(first, second, comments)` - From an implication and its antecedent derive the consequent.
- `implies_intro(blockid, comments)` - The command puts an implication as a line in the proof one level below the blockid.
- `not_elim(first, second, comments)` - When two statements are contradictory a false line can be derived.
- `not_intro(blockid, comments)` - When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
- `openblock(statement)` - Opens a new block.
- `reit(line, comments)` - A statement that already exists which can be accessed can be reused.
"""

from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, Xor, Nand, Nor, Xnor
from sympy.core.symbol import Symbol
import sympy

import altrea.exception


class Proof:
    """
    This class contains methods to construct, verify, display, save and retrieve proofs in 
    in truth functional logic.
    """

    columns = ['Statement', 'Level', 'Block', 'Rule', 'Lines', 'Blocks', 'Comment']
    statementindex = 0
    levelindex = 1
    blockidindex = 2
    ruleindex = 3
    linesindex = 4
    blocksindex = 5
    commentindex = 6
    lowestlevel = 0
    complete = 'COMPLETE     '
    completemessage = 'The proof is complete.'
    goalname = 'Goal'
    premisename = 'Premise'
    assumptionname = 'Assumption'
    or_introname = '$\\vee$ Intro'
    or_elimname = '$\\vee$ Elim'
    and_introname = '$\\wedge$ Intro'
    and_elimname = '$\\wedge$ Elim'
    reitname = 'Reiteration'
    implies_introname = '$\\implies$ Intro'
    implies_elimname = '$\\implies$ Elim'
    not_introname = '$\\neg$ Intro'
    not_elimname = '$\\neg$ Elim'
    indprfname = 'Indirect Proof'
    equivalent_introname = '$\\Leftrightarrow$ Intro'
    equivalent_elimname = '$\\Leftrightarrow$ Elim'
    xor_introname = 'Xor Intro'
    xor_elimname = 'Xor Elim'
    nand_introname = 'Nand Intro'
    nand_elimname = 'Nand Elim'
    nor_introname = 'Nor Intro'
    nor_elimname = 'Nor Elim'
    xnor_introname = 'Xnor Intro'
    xnor_elimname = 'Xnor Elim'
    lem_name ='LEM'
    explosionname = 'Explosion'
    falsename = sympy.S.false
    warningmessage = 'Warning'

    def __init__(self, 
                 goal: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                 name: str = '', 
                 comments: str = ''):
        """Create a Proof object with optional premises, but a specific goal.
        
        Parameters:
            goal: The goal to be reached by the proof.
            name: The name assigned to the proof.
            comments: Comments that will go on the proof line associated with the goal.
        """
            
        self.name = name
        self.goal = goal
        self.comments = comments
        self.blockname = '1'
        self.blockcounts = [1]
        self.currentblock = [1]
        self.currentblockid = 0
        self.blocklist = [[self.lowestlevel, self.currentblock]]
        self.blocks = []
        self.level = self.lowestlevel
        self.status = ''
        self.premises = []
        self.lines = [[goal, 0, 0, self.goalname, '', '', self.comments]]

    def getlevelblock(self, blockid: int | str) -> list:
        """Return the first and last lines of a named block of proof lines.
        
        Parameter:
            blockid: The id of the block of proof lines.
            
        Yields:
            A list containing the level and another list contining the first and last lines of the block.
            
        Exceptions:
            BlockNotFound: The block id entered does not correspond to an existing block.
        """

        try:
            levelblock = self.blocklist[blockid]
        except:
            raise altrea.exception.BlockNotFound(blockid)

        return levelblock

    def getassumption(self, blockid: int | str) -> Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol:
        """Return the first line of a closed block as the assumption of the block of proof lines.
        
        Parameter:
            blockid: The name of the block of code which the assumption begins.
            
        Yields:
            The assumption of the block of proof lines is returned.

        Exceptions:
            BlockNotAvailable: The block was not found in thee list of blocks.
            BlockNotClosed: The block was not closed and so is not complete.
        """

        s = self.getlevelblock(blockid)
        return s[0]
    
    def getconclusion(self, blockid: int | str) -> Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol:
        """Return the last line of a closed block as the conclusion of a block of proof lines.
        
        Parameter:
            blockid: The name of the block of proof lines.
            
        Yields:
            The conclusion of the block of proof lines is returned.

        Exceptions:
            BlockNotAvailable: The block was not found in thee list of blocks.
            BlockNotClosed: The block was not closed and so is not complete.
        """

        s = self.getlevelblock(blockid)
        return s[1]
    
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

       # block = self.lines[line][self.blockidindex]
        #if self.blockname != block and len(block) >= len(self.blockname):
        #   raise altrea.exception.ScopeError(line, self.lines[line][self.blockidindex], self.blockname)

    def checksamelevel(self, first: int, second: int):
        """Check if two statements are at the same level.
        
        Parameters:
            first: The first line number.
            second: The second line number.
        
        Exception:
            NotSameLevel: The two statements are not at the same level of the proof.
        """

        #block1 = self.lines[first][self.blockidindex]
        #block2 = self.lines[second][self.blockidindex]
        #if len(block1) != len(block2):
        #   raise altrea.exception.NotSameLevel(block1, block2)

    def checkassumption(self, line: int):
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

        if statement == self.goal and self.level == self.lowestlevel:
            self.status = self.complete
            #print(self.completemessage)

    def reftwolines(self, first: int, second: int) -> str:
        """A function to join two line numbers together to place in a proof line.
        
        Parameters:
            first: The first line number to join.
            second: The second line number to join.
            
        Yields:
            A string containing the first line number, a comma, and the second line number.
        """

        return ''.join([str(first), ', ', str(second)])
    
    def getstatement(self, line: int) -> Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol:
        """Return a statement from lines of a proof.
        
        Parameter:
            line: The line number of the proof.
            
        Yields:
            A statement from the line of the proof is returned.

        Exception:
            NoSuchNumber: The line number is not in the lines of the proof.
        """

        try:
            statement = self.lines[line][self.statementindex]
        except:
            raise altrea.exception.NoSuchNumber(line)
        return statement
    
    def getstatementlevelblock(self, line: int) -> list:
        """Return a statement from lines of a proof.
        
        Parameter:
            line: The line number of the proof.
            
        Yields:
            A list containing the statement, the level and the blockid
            of the proof line.

        Exception:
            NoSuchNumber: The line number is not in the lines of the proof.
        """

        try:
            statement = self.lines[line][self.statementindex]
        except:
            raise altrea.exception.NoSuchNumber(line)
        level = self.lines[line][self.levelindex]
        blockid = self.lines[line][self.blockidindex]
        return [statement, level, blockid]  

    def addstatement(self, 
                     statement: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                     rule: str, 
                     lines: list = '', 
                     blocks: list = '', 
                     comments: str =''):
        """A a new line to the proof.
        
        Parameters:
            statement: The statement to add to the proof.
            rule: The rule justifying the inclusion of the statement.
            lines: The lines justifying the rule.
            blocks: The blocks justifying the rule.
            comments: Comments added to this line of the proof.

        Exceptions:
            StringType: The expression is a string not a sympy boolean type.
        """

        if self.status == self.complete:
            pass
        else:
            if type(statement) == str:
                raise altrea.exception.StringType(statement)
            else:
                self.checkcomplete(statement)
                newcomment = comments
                if self.status == self.complete:
                    newcomment = ''.join([self.complete, " ", comments])
                self.lines.append([statement, 
                                   self.level, 
                                   self.currentblockid, 
                                   rule, 
                                   lines, 
                                   blocks, 
                                   newcomment]
                                   )

    def addpremise(self, 
                   premise: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                   comments: str = ''):
        """Add a premise to the proof.
        
        Parameters:
            premise: The premise to add to the proof.
            comments: Comments for this line of the proof.

        Exceptions:
            PremiseAtLowestLevel: A premise can only be added at the lowest level of the proof.
        """

        # for i in self.lines:
        #     if i[self.ruleindex] not in [self.goalname, self.premisename]:
        #         raise altrea.exception.PremiseBeginsProof(premise)
        if self.level > 0:
            raise altrea.exception.PremiseAtLowestLevel(premise)
        self.premises.append(premise)
        self.addstatement(statement=premise,
                          rule=self.premisename,
                          comments=comments)
        
    def equivalent_elim(self, first: int, second: int, comments: str = ''):
        pass

    def equivalent_intro(self, blockids: list, comments: str = ''):
        pass

    def closeblock(self):
        """Closes the block of statements that the proof is currently in.
        
        Examples:
            >>> from altrea.tf import Proof
            >>> ex = Proof([A], C >> A, 'Example using closeblock')
            >>> ex.openblock(C)
            >>> ex.reit(1)
            >>> ex.closeblock()
            >>> ex.implies_intro('11')
            The proof is complete.  
        """

        end = len(self.lines)-1
        blockid = self.lines[end][self.blockidindex]
        if blockid == 0:
            raise altrea.exception.CannotCloseStartingBlock()
        else:
            self.currentblock.append(end)
            self.level -= 1
            for i in range(len(self.blocklist)):
                if self.blocklist[i][0] == self.level and len(self.blocklist[i][1]) == 1:
                    self.currentblock = self.blocklist[i][1]
                    self.currentblockid = i
                    break

    def and_elim(self, line: int, comments: str = ''):
        """A conjunction is split into its individual conjuncts.
        
        Arguments:
            line: The line number of the conjunction to be split.

        Exceptions:
            NoSuchNumber: The referenced line does not exist in the proof.
            NotConjunction: The statement is not a conjunction.
            ScopeError: The referenced statement is not accessible.
        """

        s1 = self.getstatement(line)
        self.checkblock(line)
        if type(s1) != And:
            raise altrea.exception.NotConjunction(line, s1)
        else:
            conjuncts = sympy.logic.boolalg.conjuncts(s1)
            for statement in conjuncts:
                self.addstatement(statement=statement, 
                                  rule=self.and_elimname, 
                                  lines=str(line),
                                  comments=comments
                                 )
            
    def and_intro(self, first: int, second: int, comments: str = ''):
        """The statement at first line number is joined with And to the statement at second
        line number.

        Parameters:
            first: The line number of the first conjunct.
            second: The line number of the second conjunct.

        Exceptions:
            ScopeError: The lines must be in a level less than or equal to the current level.
        """

        s1 = self.getstatementlevelblock(first)
        s2 = self.getstatementlevelblock(second)
        if self.level < s1[1]:
            raise altrea.exception.ScopeError(first)
        elif self.level < s2[1]:
            raise altrea.exception.ScopeError(second)
        else:
            expr = And(s1[0], s2[0])
            self.addstatement(statement=expr, 
                              rule=self.and_introname, 
                              lines=self.reftwolines(first, second), 
                              comments=comments
                             )

    def or_elim(self, line: int, blockids: list, comments: str = ''):
        """Check the correctness of a disjunction elimination line before adding it to the proof.
        
        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            ConclusionsNotTheSame: The conclusions of blocks are not the same.
            NoSuchNumber: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
        """

        s1 = self.getstatementlevelblock(line)
        #self.checkblock(line)
        if type(s1[0]) != Or:
            raise altrea.exception.NotDisjunction(line, s1[0])
        assumptions = []
        conclusions = []
        firstlevel = blockids[0]
        if firstlevel < s1[1] + 1:
            raise altrea.exception.ScopeError(line, firstlevel, s1[1])
        for i in blockids:
            b = self.getlevelblock(i)
            if b[0] != firstlevel:
                raise altrea.exception.NotSameLevel(firstlevel, b[0])
            assumptions.append(self.getstatement(b[1][0]))
            conclusions.append(self.getstatement(b[1][1]))
        for j in s1[0].args:
            found = sympy.S.false
            for k  in assumptions:
                if k == j:
                    found = sympy.S.true
            if not found:
                raise altrea.exception.DisjunctNotFound(j, s1, line)
        for j in assumptions:
            found = sympy.S.false
            for k in s1[0].args:
                if k == j:
                    found = sympy.S.true
            if not found:
                raise altrea.exception.AssumptionNotFound(k, s1)
        for i in conclusions:
            if i != conclusions[0]:
                raise altrea.exception.ConclusionsNotTheSame(conclusions[0], k)
        self.addstatement(statement=conclusions[0],
                          rule=self.or_elimname,
                          #blocks=blockids,
                          blocks=self.reftwolines(blockids[0], blockids[1]), 
                          comments=comments
                          )
            
    def or_intro(self, 
                  disjunct: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                  line: int, 
                  comments: str = ''):
        """The newdisjunct statement and the statement at the line number become a disjunction.
        
        Parameters:
            disjunct: A statement that will be used in the disjunction.
            line: The line number of the statement that will be the other disjunct.

        Exceptions:
            NoSuchNumber: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
        """

        s1 = self.getstatement(line)
        self.checkblock(line)
        expr = Or(s1, disjunct)
        self.addstatement(statement=expr, 
                          rule=self.or_introname, 
                          lines=str(line),
                          comments=comments
                         )

    def explosion(self, 
                  expr: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol, 
                  comments: str = ''):
        """An arbitrary statement is entered in the proof given a false statement preceding it.
        
        Parameters:
            expr: The statement to add to the proof.
            line: The line number of the proof containing the statement False.
            comments: A optional comment for this line of the proof.

        Exceptions:
            NoSuchNumber: The referenced line does not exist in the proof.
            NotFalse: The referenced statement is not False.
            BlockClose: A line cannot be added to a closed block.
        """
        
        line = len(self.lines) - 1
        blockid = self.lines[line][self.blockidindex]
        if len(self.blocklist[blockid][1]) == 2:
            raise altrea.exception.BlockClosed(blockid)
        else:
            s1 = self.getstatement(line)
            if s1 != self.falsename:
                raise altrea.exception.NotFalse(line, s1)
            else:
                self.addstatement(statement=expr,
                                  rule=self.explosionname,
                                  lines=line,
                                  comments=comments
                                 )
            
    def implies_elim(self, first: int, second: int, comments: str = ''):
        """From an implication and its antecedent derive the consequent.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.

        Exceptions:
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAntecedent: The statement is not the antecedent of the implication.
            ScopeError: The referenced statement is not accessible.
        """

        s1 = self.getstatement(first)
        s2 = self.getstatement(second)
        #self.checkblock(first)
        #self.checkblock(second)
        if type(s2) == Implies:
            if s1 != s2.args[0]:
                raise altrea.exception.NotAntecedent(s1, s2)
            else:
                self.addstatement(statement=s2.args[1], 
                                  rule=self.implies_elimname, 
                                  lines=self.reftwolines(first, second),
                                  comments=comments
                                 )
        elif type(s1) == Implies:
            if s2 != s1.args[0]:
                raise altrea.exception.NotAntecedent(s2, s1)
            else:
                self.addstatement(statement=s1.args[1], 
                                  rule=self.implies_elimname, 
                                  lines=self.reftwolines(first, second),
                                  comments=comments
                                 )

    def implies_intro(self, blockid: int | str, comments: str = ''):
        """The command puts an implication as a line in the proof one level below the blockid.
        
        Parameters:
            blockid: The block identified by [start, end].
            comments: Comments added to the line.

        Exceptions:
            AssumptionNotFound: The assumption from a block does not match a disjunct of the disjunction.
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            NoSuchNumber: The referenced line does not exist in the proof.
            NotAssumption: The referenced statement is not an assumption, the first line of a block.
            NotSameBlock: Two referenced statements are not from the same block.
            NotSameLevel: The two blocks are not at the same level.
            ScopeError: The referenced statement is not accessible.
        """

        levelblock = self.getlevelblock(blockid)
        if levelblock[0] != self.level + 1:
            raise altrea.exception.ScopeError(blockid)
        else:
            antecedent = self.getstatement(levelblock[1][0])
            consequent = self.getstatement(levelblock[1][1])
            expr= Implies(antecedent, consequent)
            self.addstatement(statement=expr, 
                              rule=self.implies_introname, 
                              blocks=blockid,
                              comments=comments
                             )

    def nand_elim(self, line: int, comments: str = ''):
        pass

    def nand_intro(self, line: int, comments: str = ''):
        pass

    def nor_elim(self, line: int, comments: str = ''):
        pass

    def nor_intro(self, line: int, comments: str = ''):
        pass

    def not_elim(self, first: int, second: int, comments: str = ''):
        """When two statements are contradictory a false line can be derived.
        
        Parameters:
            first: The line number of the first statement.
            second: The line number of the second statement.
            comments: An optional comment for this line.

        Exceptions:
            NoSuchNumber: The referenced line does not exist in the proof.
            NotContradiction: Two referenced statements are not contradictions.
            ScopeError: The referenced statement is not accessible.                       
        """
        s1 = self.getstatement(first)
        s2 = self.getstatement(second)
        if Not(s1) == s2:
            self.addstatement(statement=self.falsename, 
                              rule=self.not_elimname, 
                              lines=self.reftwolines(first, second),
                              comments=comments
                             )
        else:
            raise altrea.exception.NotContradiction(first, second)
        
    def not_intro(self, blockid: int | str, comments: str = ''):
        """When an assumption generates a contradiction, the negation of the assumption
        can be used as a line of the proof in the next lower block.
        
        Example:
        
        Parameter:
            blockid: The name of the block containing the assumption and contradiction.

        Exceptions:
            BlockNotAvailable: The block is outside the scope of the current block.
            BlockNotClosed: The block cannot be accessed until it is closed.
            NoSuchNumber: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.
        """
        
        levelblock = self.getlevelblock(blockid)
        s1 = self.getstatement(levelblock[1][0])
        s2 = self.getstatement(levelblock[1][1])
        if s2 != self.falsename:
            raise altrea.exception.NotFalse(blockid, s2)
        else:
            self.addstatement(statement=Not(s1), 
                              rule=self.not_introname,
                              blocks=strblockid,
                              comments=comments
                              )      

    def openblock(self, 
                  statement: Not | And | Or | Implies | Equivalent | Xor | Nand | Nor | Xnor | Symbol,
                  comments: str = ''):
        """Opens a uniquely identified block of statements with an assumption.
        
        Example:
            >>> from altrea.tf import Proof
            >>> ex = Proof([A], C >> A, 'Example using openblock')
            >>> ex.openblock(C)
            >>> ex.reit(1)
            >>> ex.closeblock()
            >>> ex.implies_intro('11')
            The proof is complete.

        Parameters:
            statement: The assumption that starts the block of derived statements.
        """
        if self.status != self.complete:
            self.level += 1
            nextline = len(self.lines)
            self.currentblock = [nextline]
            self.blocklist.append([self.level, self.currentblock])
            self.currentblockid = len(self.blocklist) - 1

            try:
                self.blockname += str(self.blockcounts[self.level] + 1)
                self.blockcounts[self.level] += 1
            except:
                self.blockcounts.append(1)
                self.blockname += str(self.blockcounts[self.level])
            start = len(self.lines)
            self.blocks.append([self.blockname, [start]])

            self.addstatement(statement=statement, 
                              rule=self.assumptionname,
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
            >>> ex.implies_intro('11')
            The proof is complete.

        Exceptions:
            NoSuchNumber: The referenced line does not exist in the proof.
            ScopeError: The referenced statement is not accessible.

        """
        
        statement = self.getstatement(line)
        self.addstatement(statement=statement, 
                          rule=self.reitname, 
                          lines=str(line),
                          comments=comments
                         )
        
    def xnor_elim(self, line: int, comments: str = ''):
        pass

    def xnor_intro(self, line: int, comments: str = ''):
        pass

    def xor_elim(self, line: int, comments: str = ''):
        pass

    def xor_intro(self, line: int, comments: str = ''):
        pass

    