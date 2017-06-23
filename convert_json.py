#!/usr/bin/python

import json
import sys

if len(sys.argv)!=2:
    print >>sys.sdterr,sys.argv[0]," file.json"
    sys.exit(1)

with open(sys.argv[1]) as f:
    datas=json.loads(f.read())


if type(datas)==dict:
    # from motor based to time based
    times={}
    for m in datas.keys():
        for t,v in datas[m]:
            if times.has_key(t)==False:
                times[t]={}
            times[t][m]=v
    k=times.keys()
    k.sort()
    print "["
    for x in k:
        print "    {"
        print '        "time":',x,
        for m in times[x]:
            print ',\n        "%s"'%(m.strip()),':',times[x][m],
        print '\n    },'
    print "]"
        
else:
    # from time based to motor based
    motors={}
    for v in datas:
        for m in v.keys():
            if m!='time':
                if motors.has_key(m)==False:
                    motors[m]=[]
                motors[m].append((v['time'],v[m]))
    mnames=motors.keys()
    mnames.sort(key= lambda x: x[2:]+x[0:2])
    print '{'
    for i in range(len(mnames)):
        m=mnames[i]
        print '    "%s": ['%(m)        
        motors[m].sort()
        first=True
        for t,v in motors[m]:
            if first:
                first=False
            else:
                print ',\n',
            print '        [',t,',',v,']',
        print '\n'                
        if i==len(mnames)-1:
            print '    ]'
        else:
            print '    ],'
    print '}'
                
