import sys, os, zipfile, warnings, shutil
import github3 as git
from tkinter import *

warnings.simplefilter('ignore', category=ResourceWarning)
warnings.simplefilter('ignore', category=DeprecationWarning)


def setState(state,text):
    state.config(state=NORMAL)
    state.insert(END, '\n' + text)
    state.config(state=DISABLED)


def copyInfo(a, interp_path, path_upgrade, repo):
    workPath=os.path.join(interp_path,'gitHub')
    filesbase = [name for name in os.listdir(interp_path)]
    filestoolbox = [name for name in os.listdir(os.path.join(interp_path,'toolBox'))]
    filesinterface = [name for name in os.listdir(os.path.join(interp_path, 'appInterface'))]
    a.extractall(path=workPath)
    for folder in os.listdir(workPath):
        if len(folder.split(r'.')) == 1:
            for file in os.listdir(os.path.join(workPath, folder)):
                extention = file.split('.')[len(file.split('.')) - 1]
                if file in filesbase and extention == 'py':
                    shutil.copy2(os.path.join(workPath, folder, file), interp_path)
                if file in filestoolbox and extention == 'py':
                    shutil.copy2(os.path.join(workPath, folder, file),
                                 os.path.join(interp_path, 'toolBox'))
                if file in filesinterface and extention == 'py':
                    shutil.copy2(os.path.join(workPath, folder, file),
                                 os.path.join(interp_path, 'appInterface'))


def upgradeCode(state):
    try:
        interp_path = os.path.dirname(sys.executable)
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
            setState(state,'********************************************')
            setState(state,'The code was successfully upgraded, changes will be available next time you restar the program.')
            setState(state,'********************************************')
            return True
        else:
            setState(state,'********************************************')
            setState(state,"Seems you have code's latest version")
            setState(state,'********************************************')
            return False
    except:
        setState(state,'********************************************')
        setState(state,"The code wasn't upgraded")
        setState(state,'********************************************')
        return False