from gitlab import Gitlab
import subprocess
from distutils.spawn import find_executable

def get_user(gl, username):
    try:
        return gl.users.list(username=username)[0]
    except:
        return None

def get_namespace(gl, namespace):
    try:
        return gl.groups.search(namespace)[0]
    except:
        return None

def create(gl, namespace, name):
    user = get_user(gl, namespace)
    if user:
        try:
            user.projects.create({'name': name})
        except:
            pass
        return get_repo(gl, namespace, name)
    
    namespace = get_namespace(gl, namespace)
    if namespace:
        try:
            gl.projects.create({name: name, namespace_id: namespace.id})
        except:
            pass
        return get_repo(gl, namespace, name)
    
    return None


def get_repo(gl, namespace, name):
    repo = "{}/{}".format(namespace, name)
    try:
        return gl.projects.get(repo)
    except:
        return None

def get_or_create(gl, namespace, name):
    repo = get_repo(gl, namespace, name)
    if repo:
        return repo
    
    print('in create')
    return create(gl, namespace, name)


def prepare_repository(gl, namespace, name):
    
    # Create repo or get it
    repo = get_or_create(gl, namespace, name)
    if repo is None:
        return None
    
    # If we have no default branch yet, we will be able to push it later on
    if repo.default_branch is None:
        return repo
    
    # get the default branch
    try:
        dflt = repo.branches.get(repo.default_branch)
    except:
        return None
    
    # and unprotect it
    try:
        dflt.unprotect()
    except:
        pass
    
    # and return the repo
    return repo

def run(pwd, cmd, *args):
    subprocess.run([find_executable(cmd)]+list(args), cwd=pwd, check=True)


def force_upload_folder(gl, folder, namespace, name, message='Initial commit'):
    repo = prepare_repository(gl, namespace, name)
    if repo is None:
        return False
    
    run(folder, 'rm', '-rf', '.git')
    run(folder, 'git', 'init', '.')
    run(folder, 'git', 'add', '-A', '.')
    run(folder, 'git', 'commit', '-m', message)
    run(folder, 'git', 'remote', 'add', 'origin', repo.ssh_url_to_repo)
    run(folder, 'git', 'push', '--force', '--set-upstream', 'origin', 'master')
    

if __name__ == "__main__":
    gl = Gitlab('https://gl.kwarc.info', private_token=input('Enter your private token'))
    force_upload_folder(gl, 'example/test', 'twiesing', 'test3')