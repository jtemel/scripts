
import os
import subprocess
import git

class tcolors:
    # For git status
    MERGE = '\033[1m\033[34m'
    IGNORED = '\033[1m\033[38;5;241m'
    UNTRACKED = '\033[1m\033[38;5;241m'
    STAGED = '\033[1m\033[32m'
    STAGED_CHANGED = '\033[1m\033[38;5;178m'
    NOT_STAGED = '\033[1m\033[91m'
    IN_DIR = '\033[1m\033[38;5;252m'

    # For file names 
    DIR = '\033[1m\033[34m'
    LNK = '\033[1m\033[36m'
    EXC = '\033[1m\033[32m'

    ENC = '\033[0m'

status_symbols = [
    [['DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'], tcolors.MERGE + '%' + tcolors.ENC],
    [['??'], tcolors.UNTRACKED + '?' + tcolors.ENC],
    [['!!'], tcolors.IGNORED + '!' + tcolors.ENC],
    [['>>'], tcolors.IN_DIR + '>' + tcolors.ENC]
]

def get_symbol(ls, rs):
    for symbols in status_symbols:
        if ls + rs in symbols[0]:
            return symbols[1]
    if ls != ' ' and rs == ' ':
        return tcolors.STAGED + '+' + tcolors.ENC
    elif ls != ' ' and rs != ' ':
        return tcolors.STAGED_CHANGED + '+' + tcolors.ENC
    elif ls == ' ' and rs != ' ':
        return tcolors.NOT_STAGED + '-' + tcolors.ENC
    return tcolors.ENC + ' ' + tcolors.ENC


try:
    git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
except:
    # If we're not in a repo, just perform the normal ls
    subprocess.run('ls -la --color', shell=True)
    os._exit(1)

# Get some information from git
git_root = git_repo.git.rev_parse('--show-toplevel')
git_status = git_repo.git.status(['--porcelain', '--ignored']).split('\n')

# Perform the normal ls -la
result = subprocess.run(['ls', '-la'], stdout=subprocess.PIPE)
files = result.stdout.decode('utf-8').split('\n')[1:-1]

print(result.stdout.decode('utf-8').split('\n')[0])
for file in files:
    color = tcolors.ENC
    fname = file.split()[-1]
    if len(file.split()) > 9:
        fname = ' '.join(file.split(' ')[-3:])

    if fname in ('.', '..'):
        print(file.replace(fname, '- ' + tcolors.DIR + fname + tcolors.ENC))
        continue

    nfname = '{}/{}'.format(os.getcwd().replace(git_root, ''), fname)[1:]
    if file[0] == 'd':
        nfname += '/'
        color = tcolors.DIR
    if file[0] == 'l':
        color = tcolors.LNK

    printed = False
    for gfiles in git_status:
        if printed:
            break

        gfile = gfiles[3:]
        if nfname == gfile:
            print(file.replace(fname, get_symbol(gfiles[0], gfiles[1]) + ' ' + color + fname + tcolors.ENC))
            printed = True
        elif nfname in gfile and nfname[-1] == '/':
            print(file.replace(fname, get_symbol('>', '>') + ' ' + color + fname + tcolors.ENC))
            printed = True

    if not printed:
        print(file.replace(fname, '- ' + color + fname + tcolors.ENC))
