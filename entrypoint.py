#!/usr/bin/env python3

import os
import json
import sys

confj = '/data/config.json'

stat_confj = os.path.isfile(confj)

cmdparams = ['/root/fiche']

spvdconf = '/data/supervisord.conf'

stat_flag = os.path.isfile(spvdconf)

stat_template = os.path.isfile(spvdconf + '.template')

if stat_template == False:
    raise FileNotFoundError
    sys.exit(7)

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
        confdic = json.loads(open(confj,'r').read())
        procconf(confdic)
        finalcmd = finalcmd.join(cmdparams)
        tempstr = 'command=' + finalcmd
        os.system('cp -f /data/supervisord.conf.template /data/supervisord.conf')
        fspv = open('/data/supervisord.conf', 'a')
        fspv.write(tempstr)
        fspv.close()
    else:
        pass
    # READ CONFIG AND THEN APPEND TO SUPERVISORD
    execcmd = ["/usr/bin/supervisord", "-n", "-c", "/data/supervisord.conf"]
    cmdstr = ' '.join(execcmd)
    os.system(cmdstr)
else:
    raise FileNotFoundError
