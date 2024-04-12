"""This module contains procedures to forat a display of data.

- `metadata(p)` - Print a list of a proof's metadata.
- `show(p)` - Print a proof line by line.
- `truthtable(p)` - Print a truth table of the proofs premises implying its goal.
"""

import pandas
# import sympy.logic.boolalg 
import sympy

def metadata(p):
    print('Name: {}'.format(p.name))
    print('Goal: {}'.format(p.goal))
    print('Premises')
    for i in p.premises:
        print('   {}'.format(i))
    if p.status == p.complete:
        print('Completed: Yes')
    else:
        print('Completed: No')
    print('Lines: {}'.format(len(p.lines)-1))
    subproofs = -1
    for i in p.subproofcounts:
        subproofs += i
    print('Subproofs: {}'.format(subproofs))

def show(p):
    newp = []
    for i in range(len(p.lines)):
        if p.lines[i][0] == sympy.S.false:
            statement = '$\\bot$'
        else:
            statement = ''.join(['$',sympy.latex(p.lines[i][0]),'$'])
        newp.append([statement,
                     p.lines[i][1],
                     p.lines[i][2],
                     p.lines[i][3],
                     p.lines[i][4],
                     p.lines[i][5],
                     p.lines[i][6]
                     ]
                    )
    indx = ['Line']
    for i in range(len(p.lines)-1):
        indx.append(i + 1)
    df = pandas.DataFrame(newp, index=indx, columns=p.columns)
    print('Proof Name: {}'.format(p.name))
    return df

def truthtable(p):
    premises = sympy.S.true
    for i in p.premises:
        premises = sympy.logic.boolalg.And(premises, i)
    expr = sympy.logic.boolalg.Implies(premises, p.goal)
    vars = list(expr.free_symbols)
    table = sympy.logic.boolalg.truth_table(expr, vars)
    letters = '['
    for s in vars:
        letters += ''.join([str(s), ', '])
    letters = letters[:-2] + ']'
    idx = []
    for i in range(2**len(vars)):
        idx.append(i)
    expr = ''.join(['$',sympy.latex(expr),'$'])
    df = pandas.DataFrame(table, index=idx, columns=[letters, expr], caption=p.name)
    #df.style.set_caption(p.name)
    return df