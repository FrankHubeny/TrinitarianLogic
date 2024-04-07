import pandas as pd
from IPython.display import display, Math, Markdown, Latex, display_markdown, HTML
from sympy.logic.boolalg import Xor, And, Or, Not, Implies, Equivalent, eliminate_implications
from sympy.abc import x,y,z,A,B,C,D,E,F
from sympy import latex, S

class Proof:
    """
    This class contains methods and exceptions to construct, verify, display, save and retrieve proofs in 
    in truth functional logic and first order logic.
    """

    columns = ['Statement', 'Level', 'Rule', 'Ref 1', 'Ref 2', 'Status']
    statementindex = 0
    levelindex = 1
    ruleindex = 2
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

    def __init__(self, premises, goal, name: str = 'Proof'):
        self.name = name
        self.goal = goal
        self.level = 0
        self.status = ''
        self.premises = premises
        self.lines = [[goal, self.level, self.goalname, 0, 0, self.status]]
        for i in self.premises:
            if i == self.goal:
                self.status = self.complete
                print(self.completemessage)
            self.lines.append([i, self.level, self.premisename, 0, 0, self.status])

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

        beginline:
            The first linenumber of the subproof.
        endline:
            The last linenumber of the subproof.
        """

        def __init__(self, beginline, endline):
            self.beginline = beginline
            self.endline = endline

        def __str__(self):
            return f'The statements at lines {self.beginline} and {self.endline} are not at the same level.'

    class NotContradiction(Exception):
        """
        If two statements are not contradictions when they should be raise this exception.

        Parameter
        =========

        beginline:
            The first linenumber of the alleged contradiction.
        endline:
            The last linenumber of the alleged contradiction.
        """

        def __init__(self, beginline, endline):
            self.beginline = beginline
            self.endline = endline

        def __str__(self):
            return f'The statements at lines {self.beginline} and {self.endline} are not contradictions.'
    
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

    def display(self):
        indx = [self.name]
        for i in range(len(self.lines)-1):
            indx.append(i + 1)
        df = pd.DataFrame(self.lines, index=indx, columns=self.columns)
        return df

    def checklevel(self, linenumber: int):
        if self.lines[linenumber][self.levelindex] < 0:
            raise ScopeError(linenumber, self.lines[linenumber][self.levelindex], self.level)

    def checksamelevel(self, beginline: int, endline: int):
        if self.lines[beginline][self.levelindex] != self.lines[endline][self.levelindex]:
            raise NotSameLevel(beginline, endline)

    def checkassumption(self, line):
        if self.lines[line][self.ruleindex] != self.assumptionname:
            raise NotAssumption(line)

    def checkcomplete(self, statement):
        if statement == self.goal and self.level == 0:
            self.status = self.complete
            print(self.completemessage)

    def getstatement(self, linenumber):
        try:
            statement = self.lines[linenumber][self.statementindex]
        except:
            raise NoSuchNumber(first)
        return statement

    def addstatement(self, statement, rule: str, first: int = 0, second: int = 0):
        self.lines.append([statement, self.level, rule, first, second, self.status])

    def opensubproof(self):
        self.level += 1

    def closesubproof(self, beginline: int, endline: int):
        for i in range(beginline, endline+1):
            self.lines[i][self.levelindex] = -self.lines[i][self.levelindex]
        self.level -= 1

    def reit(self, linenumber: int):
        self.checklevel(linenumber)
        statement = self.getstatement(linenumber)
        self.checkcomplete(statement)
        self.addstatement(statement, self.reitname, linenumber)

    def conjintro(self, first: int, second: int):
        firstconjunct = self.getstatement(first)
        secondconjunct = self.getstatement(second)
        self.checklevel(first)
        self.checklevel(second)
        statement = And(firstconjunct, secondconjunct)
        self.checkcomplete(statement)
        self.addstatement(statement, self.conjintroname, first, second)

    def conjelim(self, linenumber: int):
        test = []
        conjunction = self.getstatement(linenumber)
        self.checklevel(linenumber)
        for c in conjunction.args:
            test.append(c)
        testconjunction = S.true
        for t in test:
            testconjunction = And(testconjunction, t)
        if testconjunction != conjunction:
            raise UncategorizedError(f'The original statement {conjunction} is not the same as the rebuilt statements {testconjunction}.')
        for statement in conjunction.args:
            self.checkcomplete(statement)
            self.addstatement(statement, self.conjelimname, linenumber)

    def disjintro(self, seconddisjunct, linenumber: int):
        firstdisjunct = self.getstatement(linenumber)
        self.checklevel(linenumber)
        statement = Or(firstdisjunct, seconddisjunct)
        self.checkcomplete(statement)
        self.addstatement(statement, self.disjintroname, linenumber)

    def assumption(self, statement):
        self.opensubproof()
        self.addstatement(statement, self.assumptionname)

    def impintro(self, beginline: int, endline: int):
        self.checksamelevel(beginline, endline)
        self.checkassumption(beginline)
        statement = Implies(self.lines[beginline][self.statementindex], self.lines[endline][self.statementindex])
        self.closesubproof(beginline, endline)
        self.addstatement(statement, self.impintroname, beginline, endline)

    def impelim(self, beginline: int, endline: int):
        self.checklevel(beginline)
        self.checklevel(endline)
        s1 = self.getstatement(beginline)
        s2 = self.getstatement(endline)
        if s1 == s2.args[0]:
            self.addstatement(s2.args[1], self.impelimname, beginline, endline)
        elif s2 == s1.args[0]:
            self.addstatement(s1.args[1], self.impelimname, beginline, endline)
        else:
            raise UncategorizedError('Did not succeed with implication elimination.')

    def negintro(self, first: int, second: int):
        s1 = self.getstatement(first)
        s2 = self.getstatement(second)
        if Not(s1) == s2:
            self.addstatement(S.false, self.negintroname, first, second)
        else:
            raise NotContradiction(first, second)