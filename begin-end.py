import sys

def err(count, msg, context):
    sys.stdout.write("%d: %s\n" % (count,msg))
    sys.stdout.write("context: %s\n" % context)
    sys.exit(1)
    
def index(s, sub):
    try:
        return s.index(sub)
    except:
        return -1

for file in sys.argv[1:]:
    print(file)
    stack = []
    count = 0
    with open(file) as f:
        for line in f:
            while len(line):
                begin = index(line,"\\begin{")
                end = index(line,"\\end{")
                if begin>=0 and (end<0 or end>begin):
                    line = line[begin+7:]
                    brace = index(line,"}")
                    if brace<0:
                        err(count, "Missing closing brace", line)
                    stack.append( (count,line[:brace]) )
                    line = line[brace+1:]
                elif end>=0 and (begin<0 or begin>end):
                    line = line[end+5:]
                    brace = index(line,"}")
                    if brace < 0:
                        err(count, "Missing closing brace", line)
                    env = line[:brace]
                    if len(stack) == 0:
                        err(count, "\end{%s} without opening" % env, line)
                    elif stack[-1][1] != env:
                        err(count, "\begin{%s} in line %d doesn't match \end{%s}" % (stack[-1][1], stack[-1][0], env), line)
                    stack.pop()
                    line = line[brace+1:]
                else:
                    line = ""
            count += 1
        if len(stack) > 0:
            err(count, "Stack still has %d elements; last one is \begin{%s} started in line %d" % (len(stack), stack[-1][1], stack[-1][0]), "EOF")