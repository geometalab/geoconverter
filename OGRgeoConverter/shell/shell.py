import shlex
from subprocess import Popen, PIPE
from shellresult import ShellResult

def execute(shell_call):
    command = shell_call.get_shell_command()
    try:
        args = shlex.split(command)
        # p = Popen(args, stdout=PIPE, stderr=PIPE)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Vor Release shell=True entfernen!
        p = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        stdout, stderr = p.communicate()
    except Exception, e:
        stdout = ""
        stderr = e
    
    return ShellResult(stdout, stderr)
