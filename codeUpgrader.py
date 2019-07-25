import sys, os, zipfile, warnings
import github3 as git
from tkinter import *

#hello, this code wasn't upgraded

warnings.simplefilter('ignore', category=ResourceWarning)
warnings.simplefilter('ignore', category=DeprecationWarning)


def setState(state,text):
    state.config(state=NORMAL)
    state.insert(END, '\n' + text)
    state.config(state=DISABLED)


def copyInfo(a, interp_path, path_upgrade, repo):
    filesbase = [name for name in os.listdir(interp_path)]
    filestoolbox = [name for name in os.listdir(os.path.join(interp_path,'toolBox'))]
    interface = [name for name in os.listdir(os.path.join(interp_path,'appInterface'))]
    for name in a.namelist():
        basename = os.path.basename(name)
        extention = basename.split('.')[len(basename.split('.')) - 1]
        if basename in filesbase and extention == 'py':
            with a.open(name, 'r') as f:
                data = f.read()
            f.close()
            with open(os.path.join(interp_path, basename), 'w') as f:
                f.write(data.decode('windows-1252'))
            f.close()
        if basename in filestoolbox and extention == 'py':
            with a.open(name, 'r') as f:
                data = f.read()
            f.close()
            with open(os.path.join(interp_path,'toolBox', basename), 'w') as f:
                f.write(data.decode('windows-1252'))
            f.close()
        if basename in interface and extention == 'py':
            with a.open(name, 'r') as f:
                data = f.read()
            f.close()
            with open(os.path.join(interp_path,'appInterface', basename), 'w') as f:
                f.write(data.decode('windows-1252'))
            f.close()
    with open(path_upgrade, "w") as f:
        f.write(str(repo.updated_at))
    f.close()


def upgradeCode(state):
    try:
        interp_path = sys.executable.replace("python.exe", "textMiner")
        path = os.path.join(interp_path, 'GitHub', 'files.zip')
        path_upgrade = os.path.join(interp_path, 'GitHub', 'upgrated.txt')
        repo = git.GitHub().repository('gamug', 'pdfMiner')
        repo.archive('zipball', path=path)  # download repository content
        a = zipfile.ZipFile(path, 'r')  # This is the zip download Github content loaded
        # here we prepare download version information
        with open(path_upgrade, "r") as f:
            upgrated = f.read()
        f.close()
        if upgrated != str(repo.updated_at):
            copyInfo(a, interp_path, path_upgrade, repo)  # we upload code if there is recent version in my repository
            setState(state,'The code was successfully upgraded, changes will be available next time you restar the program.')
            return True
        else:
            setState(state,"Seems you have code's latest version")
            return False
    except:
        setState(state,"The code wasn't upgraded")
        return False