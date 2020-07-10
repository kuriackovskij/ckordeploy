'''
ck0's user defined environment auto-redeployment
Securizza. 2020
'''

from shutil import copyfile
import os
import subprocess

def changePS(bashrc):

    copyfile(bashrc,bashrc+'_backup')    #Making a backup of the original .bashrc

    i = 0
    linesToUpdate = []
    with open(bashrc, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'PS1=' in line:
                linesToUpdate.append(i)  #Getting a list of lines where PS1 string is found
            i += 1

    PS1 = r'''    PS1="\[\033[0;96m\]\342\224\214\342\224\200\$([[ \$? != 0 ]] && echo \"[\[\033[0;91m\]\342\234\227\[\033[0;96m\]]\342\224\200\" || echo \"[\[\033[0;92m\]\342\234\223\[\033[0;96m\]]\342\224\200\")[$(if [[ ${EUID} == 0 ]]; then echo '\[\033[01;91m\]root\[\033[01;33m\]@\[\033[01;34m\]\h'; else echo '\[\033[0;97m\]\u\[\033[01;33m\]@\[\033[01;34m\]\h'; fi)\[\033[0;96m\]]\342\224\200[\[\033[0;32m\]\w\[\033[0;96m\]]\342\224\200[\[\033[0;90m\]\t\[\033[0;96m\]]\n\[\033[0;96m\]\342\224\224\342\224\200\342\224\200\342\225\274 \[\033[0m\]\[\e[01;33m\]\\$\[\e[\]0m" ''' + "\n"

    for linenum in linesToUpdate:
        lines[linenum] = PS1

    #Writing changes back to a file
    with open(bashrc, 'w') as fw:
        fw.writelines(lines)


#Getting location of .bashrc for current user
userhome = os.environ['HOME']
bashrc = userhome + '/.bashrc'

if os.getuid() != 0:
    print('This is required, but limited deployment though.')
    print('Dont forget to do the same with root privs!')
else:
    print('Changing PS1 for root...')
    print('To update PS1 for low priv account run it from within that low priv account')
    os.system('sudo apt-get update && apt-get upgrade -y')

changePS(bashrc)
