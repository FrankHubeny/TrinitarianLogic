
from IPython.display import display, Math, Markdown, Latex, display_markdown, HTML
from sympy.logic.boolalg import Xor, And, Or, Not, Implies, Equivalent, eliminate_implications
from sympy.abc import x,y,z,A,B,C,D,E,F
from sympy import latex, S
import realpy.exception

class Proof:
    """
    This class contains methods and exceptions to construct, verify, display, save and retrieve proofs in 
    in truth functional logic and start order logic.
    """

    columns = ['Statement', 'Block ID', 'Rule', 'Lines', 'Blocks', 'Status']
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

    def __init__(self, premises, goal, name: str = '', indx: str =''):
        self.name = name
        self.goal = goal
        self.subproofname = '1'
        self.subproofcounts = [1]
        self.subproofs = []
        self.level = 0
        self.status = ''
        self.premises = premises
        self.lines = [[goal, self.subproofname, self.goalname, '', '', self.status]]
        for i in self.premises:
            if i == self.goal:
                self.status = self.complete
                print(self.completemessage)
                self.lines.append([i, self.subproofname, self.premisename, '', '', self.status])
                break
            else:
                self.lines.append([i, self.subproofname, self.premisename, '', '', self.status]) 

    def blockstartend(self, blockid: str):
        for i in self.subproofs:
            if i[0] == blockid:
                start = i[1][0]
                end = i[1][1]
                break
        return start, end

    def checkblock(self, line: int):
        block = self.lines[line][self.blockidindex]
        if self.subproofname != block and len(block) >= len(self.subproofname):
           raise realpy.exception.ScopeError(line, self.lines[line][self.blockidindex], self.subproofname)

    def checksamelevel(self, start: int, end: int):
        startblock = self.lines[start][self.blockidindex]
        endblock = self.lines[end][self.blockidindex]
        if startblock != endblock:
           raise NotSameBlock(start, startblock, end, endblock)

    def checkassumption(self, line):
        if self.lines[line][self.ruleindex] != self.assumptionname:
            raise realpy.exception.NotAssumption(line)

    def checkcomplete(self, statement):
        if statement == self.goal and self.subproofname == '1':
            self.status = self.complete
            print(self.completemessage)

    def getstatement(self, line: int):
        try:
            statement = self.lines[line][self.statementindex]
        except:
            raise realpy.exception.NoSuchNumber(line)
        return statement

    def addstatement(self, statement, rule: str, lines='', blocks=''):
        if self.status == self.complete:
            pass
        else:
            self.checkcomplete(statement)
            self.lines.append([statement, self.subproofname, rule, lines, blocks, self.status])

    def openblock(self, statement):
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

    def closeblock(self):
        end = len(self.lines)-1
        blockid = self.lines[end][self.blockidindex]
        for i in self.subproofs:
            if i[0] == blockid:
                i[1].append(end)
                break
        self.level -= 1
        self.subproofname = self.subproofname[:-1]

    def reit(self, line: int):
        """
        A statement that already exists which can be accessed can be reused.
        
        The following tests are performed to ensure the operation is correct:

        1. The statement must exist.
        2. The statement must be in a block which can be accessed.

        Parameter
        =========

        line:
            The line number of the statement.
        """
        
        # Test 1: The statement must exist.
        statement = self.getstatement(line)

        # Test 2: The statement must be in a block which can be accessed.
        self.checkblock(line)

        self.addstatement(statement=statement, 
                          rule=self.reitname, 
                          lines=str(line) 
                         )

    def conjintro(self, first: int, second: int):
        """
        The statement at first line number is joined with And to the statement at second
        line number.
        
        The following tests are performed to ensure the operation is correct:
        
        1. The two statements must exist.
        2. They must be in blocks which can be accessed.

        Parameter
        =========

        first:
            The line number of the first conjunct.
        second:
            The line number of the second conjunct.
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
                          lines=''.join([str(first), ', ', str(second)])
                         )

    def conjelim(self, line: int):
        """
        A conjunction is split into its individual conjuncts.
        
        The following tests are performed to ensure the operation is correct.
        
        1. The statement must exist.
        2. The statement must be in a block that can be accessed.
        3. The statement must be a conjunction.
        """

        # Test 1: The statement must exist.
        conjunction = self.getstatement(line)

        # Test 2: The statement must be in a block that can be accessed.
        self.checkblock(line)

        # Test 3: The statement must be a conjunction.
        rebuilt = S.true
        for t in conjunction.args:
            rebuilt = And(rebuilt, t)
        if rebuilt != conjunction:
            raise realpy.exception.NotSameStatements(conjunction, self.conjelimname, rebuilt)
        
        for statement in conjunction.args:
            self.addstatement(statement=statement, 
                              rule=self.conjelimname, 
                              lines=str(line)
                             )

    def disjintro(self, newdisjunct, line: int):
        """
        The newdisjunct statement and the statement at the line number become a disjunction.
        
        The following tests are performed to ensure the operation is correct.
        
        1. The statment at the line number must exist.
        2. The statement must in a block that can be accessed.
        
        Parameter
        =========

        newdisjunct:
            A statement that will be used in the disjunction.
        line:
            The line number of the statement that will be the other disjunct.
        """

        # Test 1: The statment must exist.
        startdisjunct = self.getstatement(line)

        # Test 2: The statement must in a block that can be accessed.
        self.checkblock(line)
        
        statement = Or(startdisjunct, enddisjunct)
        self.addstatement(statement=statement, 
                          rule=self.disjintroname, 
                          lines=str(line)
                         )

    def impintro(self, blockid: str):
        (start, end) = self.blockstartend(blockid)
        self.checksamelevel(start, end)
        self.checkassumption(start)
        antecedent = self.getstatement(start)
        consequent = self.getstatement(end)
        statement = Implies(antecedent, consequent)
        self.addstatement(statement=statement, 
                          rule=self.impintroname, 
                          blocks=blockid
                         )

    def impelim(self, start: int, end: int):
        self.checkblock(start)
        self.checkblock(end)
        s1 = self.getstatement(start)
        s2 = self.getstatement(end)
        if s1 == s2.args[0]:
            self.addstatement(statement=s2.args[1], 
                              rule=self.impelimname, 
                              lines=str(start) + ", " + str(end)
                             )
        elif s2 == s1.args[0]:
            self.addstatement(statement=s1.args[1], 
                              rule=self.impelimname, 
                              lines=str(start) + ", " + str(end)
                             )
        else:
            raise realpy.exception.UncategorizedError('Did not succeed with implication elimination.')

    def negelim(self, start: int, end: int):
        s1 = self.getstatement(start)
        s2 = self.getstatement(end)
        if Not(s1) == s2:
            self.addstatement(statement=S.false, 
                              rule=self.negelimname, 
                              lines=str(start) + ", " + str(end)
                             )
        else:
            raise realpy.exception.NotContradiction(start, end)
        
    def negintro(self, blockid: str):
        start, end = self.blockstartend(blockid)
        s1 = self.getstatement(start)
        s2 = self.getstatement(end)
        if s2 != S.false:
            raise realpy.exception.NotFalse(end, s2)
        else:
            self.addstatement(statement=Not(s1), 
                              rule=self.negintroname,
                              blocks=blockid
                              )
            
    def disjelim(self, line, blockids):
        """
        This procedure checks the correctness of a disjunction eliminat line.
        There are various things to check.
        
        1. The statement that is being eliminated has to be a valid statement.
        2. The statement has to be a disjunction.
        3. Each disjunct must be an assumption in a subproof.
        4. The assumptions of each subproof must be a disjunct in the disjunction.
        5. All of the conclusions of the subproofs must be identical.
        
        If those conditions hold then one can add the common conclusion as a
        new line in the proof.
        """

        # Test 1: The statement that is being eliminated has to be a valid statement.
        disj = self.getstatement(line)
        # Test 2: The statement has to be a disjunction.
        disjunct = []
        orstatement = S.false
        for i in disj.args:
            disjunct.append(i)
        for i in disjunct:
            orstatement = Or(orstatement, i)
        if orstatement != disj:
            raise realpy.exception.NotDisjunction(line, disj, orstatement)
        # Setup for the next tests 3, 4, 5
        assumptions = []
        conclusions = []
        for i in blockids:
            start, end = self.blockstartend(i)
            assumptions.append(self.getstatement(start))
            conclusions.append(self.getstatement(end))
        # Test 3: Each disjunct must be an assumption in a subproof.
        for j in disj.args:
            found = S.false
            for k  in assumptions:
                if k == j:
                    found = S.true
            if not found:
                raise realpy.exception.DisjunctNotFound(j, disj, line)
        # Test 4: The assumptions of each subproof must be a disjunct in the disjunction.
        for j in assumptions:
            found = S.false
            for k in disj.args:
                if k == j:
                    found = S.true
            if not found:
                raise realpy.exception.AssumptionNotFound(k, disj)
        # Test 5: All of the conclusions of the subproofs must be identical.
        for i in conclusions:
            if i != conclusions[0]:
                raise realpy.exception.ConclusionsNotTheSame(conclusions[0], k)
        self.addstatement(statement=conclusions[0],
                          rule=self.disjelimname,
                          blocks=blockids
                          )
    def bicondelim(self, line: int):
        test = []
        biconditional = self.getstatement(line)
        self.checkblock(line)
        for c in biconditional.args:
            test.append(c)
        testbiconditional = S.true
        for t in test:
            testbiconditional = And(testbiconditional, t)
        if testbiconditional != biconditional:
            raise realpy.exception.NotSameStatements(biconditional, self.bicondname, testbiconditional)
        for statement in biconditional.args:
            self.addstatement(statement=statement, 
                              rule=self.bicondelimname, 
                              lines=str(line)
                             )

        