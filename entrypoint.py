#!/usr/bin/env python3

import os
import json
import sys

confj = '/data/config.json'

stat_confj = os.path.isfile(confj)

flagfile = '/data/configured1'

stat_flag = os.path.isfile(confj)

cmdparams = ['/root/fiche']

spvdconf = "/data/supervisord.conf"

finalcmd = ' '

def procconf(confdict):
    if isinstance(confdict,dict):
        try:
            cmdparams.append('-o')
            cmdparams.append(confdict['codepath'])
            cmdparams.append('-d')
            cmdparams.append(confdict['baseurl'])
            if confdict['https_enabled'] == True:
                cmdparams.append('-S')
            cmdparams.append('-s')
            cmdparams.append(str(confdict['shorturl']))
            cmdparams.append('-l')
            cmdparams.append(confdict['logfile'])
            cmdparams.append('-p')
            cmdparams.append(str(confdict['port']))
        except IndexError:
            sys.exit(2)
    else:
        raise TypeError


if stat_confj == True:
    if stat_flag == False:
        flf = open(flagfile,'w')
        flf.write('configured')
        flf.close()
        confdic = json.loads(open(confj,'r').read())
        procconf(confdic)
        finalcmd = finalcmd.join(cmdparams)
        tempstr = 'command=' + finalcmd
        fspv = open(spvdconf, 'a')
        fspv.write(tempstr)
        fspv.close()
    else:
        pass
    # READ CONFIG AND THEN APPEND TO SUPERVISORD
    execcmd = ["bash", "-c", "/usr/bin/supervisord", "-n", "-c", spvdconf]
    cmdstr = ' '.join(execcmd)
    os.system(cmdstr)
else:
    raise FileNotFoundError
