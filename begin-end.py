import sys

"""
This is to help diagnose brace and begin/end mismatch errors.
"""

#
# TODO: handle backslash escapes
#

def err(count, msg, context):
    sys.stdout.write("%d: %s\n" % (count,msg))
    sys.stdout.write("context: %s\n" % context)
    sys.exit(1)
    
def index(s, sub):
    try:
        return s.index(sub)
    except:
        return -1

def beginEndMatcher(line):
    while len(line):
        begin = index(line,"\\begin{")
        end = index(line,"\\end{")
        if begin>=0 and (end<0 or end>begin):
            line = line[begin+7:]
            brace = index(line,"}")
            if brace<0:
                err(count, "Missing closing brace", line)
            beginEndStack.append( (count,line[:brace]) )
            line = line[brace+1:]
        elif end>=0 and (begin<0 or begin>end):
            line = line[end+5:]
            brace = index(line,"}")
            if brace < 0:
                err(count, "Missing closing brace", line)
            env = line[:brace]
            if len(beginEndStack) == 0:
                err(count, "\end{%s} without opening" % env, line)
            elif beginEndStack[-1][1] != env:
                err(count, "\begin{%s} in line %d doesn't match \end{%s}" % (beginEndStack[-1][1], beginEndStack[-1][0], env), line)
            beginEndStack.pop()
            line = line[brace+1:]
        else:
            line = ""
        
def braceMatcher(line):
    for i,c in enumerate(line):
        if c == '{' and (i==0 or line[i-1] != '\\'):
            braceStack.append(count)
        elif c == '}' and (i==0 or line[i-1] != '\\'):
            if len(braceStack) == 0:
                err(count, "Closing brace without matching opening", line)
            else:
                braceStack.pop()
        
for file in sys.argv[1:]:
    print(file)
    beginEndStack = []
    braceStack = []
    count = 1
    with open(file) as f:
        for line in f:
            beginEndMatcher(line)
            braceMatcher(line)
            count += 1
        if len(beginEndStack) > 0:
            err(count, "begin-end stack still has %d elements; last one is \begin{%s} started in line %d" % (len(beginEndStack), beginEndStack[-1][1], beginEndStack[-1][0]), "EOF")
        if len(braceStack) > 0:
            err(count, "brace stack still has %d elements; last one was started on line %d" % (len(braceStack), braceStack[-1]), "EOF")
        