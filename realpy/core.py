import pandas as pd

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

def display(p):
    indx = ['Line']
    for i in range(len(p.lines)-1):
        indx.append(i + 1)
    df = pd.DataFrame(p.lines, index=indx, columns=p.columns)
    return df