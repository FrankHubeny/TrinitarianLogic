
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
    closesubproof = 'Close Subproof'

    def __init__(self, premises, goal, name: str = 'Proof'):
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
        return (start, end)

    def checklevel(self, linenumber: int):
        pass
        #if self.lines[linenumber][self.levelindex] < 0:
        #    raise ScopeError(linenumber, self.lines[linenumber][self.levelindex], self.level)

    def checksamelevel(self, start: int, end: int):
        pass
        #if self.lines[start][self.levelindex] != self.lines[end][self.levelindex]:
        #    raise NotSameLevel(start, end)

    def checkassumption(self, line):
        if self.lines[line][self.ruleindex] != self.assumptionname:
            raise realpy.exception.NotAssumption(line)

    def checkcomplete(self, statement):
        if statement == self.goal and self.subproofname == '1':
            self.status = self.complete
            print(self.completemessage)

    def getstatement(self, linenumber):
        try:
            statement = self.lines[linenumber][self.statementindex]
        except:
            raise realpy.exception.NoSuchNumber(linenumber)
        return statement

    def addstatement(self, statement, rule: str, lines='', blocks=''):
        if self.status == self.complete:
            print(self.completemessage)
        else:
            self.checkcomplete(statement)
            self.lines.append([statement, self.subproofname, rule, lines, blocks, self.status])

    def opensubproof(self, statement):
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

    def closesubproof(self):
        end = len(self.lines)-1
        blockid = self.lines[end][self.blockidindex]
        for i in self.subproofs:
            if i[0] == blockid:
                i[1].append(end)
                break
        self.level -= 1
        self.subproofname = self.subproofname[:-1]

    def reit(self, linenumber: int):
        self.checklevel(linenumber)
        statement = self.getstatement(linenumber)
        self.addstatement(statement=statement, 
                          rule=self.reitname, 
                          lines=str(linenumber) 
                         )

    def conjintro(self, start: int, end: int):
        startconjunct = self.getstatement(start)
        endconjunct = self.getstatement(end)
        self.checklevel(start)
        self.checklevel(end)
        statement = And(startconjunct, endconjunct)
        self.addstatement(statement=statement, 
                          rule=self.conjintroname, 
                          lines=str(start) + ", " + str(end)
                         )

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
            raise realpy.exception.UncategorizedError(
                f'The original statement {conjunction} is not the same \
                as the rebuilt statements {testconjunction}.')
        for statement in conjunction.args:
            self.checkcomplete(statement)
            self.addstatement(statement=statement, 
                              rule=self.conjelimname, 
                              lines=str(linenumber)
                             )

    def disjintro(self, enddisjunct, linenumber: int):
        startdisjunct = self.getstatement(linenumber)
        self.checklevel(linenumber)
        statement = Or(startdisjunct, enddisjunct)
        self.addstatement(statement=statement, 
                          rule=self.disjintroname, 
                          lines=str(linenumber)
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
        self.checklevel(start)
        self.checklevel(end)
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

    def negintro(self, start: int, end: int):
        s1 = self.getstatement(start)
        s2 = self.getstatement(end)
        if Not(s1) == s2:
            self.addstatement(statement=S.false, 
                              rule=self.negintroname, 
                              lines=str(start) + ", " + str(end)
                             )

        else:
            raise realpy.exception.NotContradiction(start, end)