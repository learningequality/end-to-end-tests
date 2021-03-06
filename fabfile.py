#/usr/bin/env python
import os
import shutil

from fabric.api import *
from fabric.api import shell_env


# GLOCABL SETTINGS
################################################################################

# CHECK-SPECIFIC SETTINGS
################################################################################
env.landscape = 'mvp'


# When using host provisioned using docker-machine
################################################################################
# env.hosts = ['localhost']
# env.user = 'ubuntu'
# env.key_filename = '/Users/ivan/.docker/machine/machines/gcptestshost/id_rsa'
# env.MACHINE_NAME = 'gcptestshost'
# env.MACHINE_PORT = '2376'



# MVP Proof-of-concept only Kolibri
################################################################################

@task
def kolibri_poc_build():
    # Copy over source code files so they will be in build context
    if not os.path.exists('dockerfiles/src'):
        os.mkdir('dockerfiles/src')
    if os.path.exists('dockerfiles/src/studio'):
        shutil.rmtree('dockerfiles/src/studio')
    local('cp -r src/studio dockerfiles/src/')
    with lcd('landscapes/mvp'):
        dcbuild()
        local('rm -rf ../../dockerfiles/src/studio')

@task
def kolibri_poc_up():
    with lcd('landscapes/mvp'):
        dcup()


@task
def kolibri_poc_down():
    with lcd('landscapes/mvp'):
        dcdown(options='-v')



# HIGH-LEVEL CHECKS API
################################################################################



# SOURCE CODE UTILS
################################################################################

STUDIO_GIT_REPO_URL = 'https://github.com/fle-internal/content-curation.git'
STUDIO_GIT_BRANCH = 'master'

@task
def checkout_studio(branch='master'):
    if not os.path.exists('src'):
        os.mkdir('src')
    with lcd('src/'):
        if not os.path.exists('studio'):
            git_clone(STUDIO_GIT_REPO_URL, dirname='studio')
        with lcd('studio'):
            update(branch=branch)



# GIT UTILS
################################################################################

@task
def git_clone(repo_repo_url, branch='master', dirname=''):
    local('git clone ' + repo_repo_url + ' ' + dirname)
    local('git checkout ' + branch)

@task
def git_fetch(branch='master'):
    local('git fetch origin ' + branch)

@task
def update(branch='master'):
    git_fetch(branch=branch)
    local('git checkout ' + branch)
    ###EZ### local('git reset --hard origin/' + branch)
    # update requirements
    # activate_sh = os.path.join(CHEF_DATA_DIR, 'venv/bin/activate')
    # reqs_filepath = os.path.join(CHEF_DATA_DIR, 'requirements.txt')
    # with prefix('export HOME=/data && source ' + activate_sh):
    #     sudo('pip install -U --no-input --quiet -r ' + reqs_filepath)


# DOCKER-COMPOSE API
################################################################################

@task
def dclogs():
    machineenv('docker-compose logs')

@task
def dcbuild(name='', options=''):
    cmd = 'docker-compose build '
    cmd += options
    cmd += '  ' + name
    machineenv(cmd)

@task
def dcup(options='-d'):
    cmd = 'docker-compose up '
    cmd += options
    machineenv(cmd)

@task
def dcdown(options=''):
    cmd = 'docker-compose down '
    cmd += options
    machineenv(cmd)


# via https://github.com/SkygearIO/skygear-server/blob/master/examples/quickstart/fabfile.py
def read_compose_override():
    with settings(abort_exception=Exception):
        try:
            fd = StringIO()
            # get('docker-compose.override.yml', fd)
            get('docker-compose.yml', fd)
            fd.seek(0)
            return yaml.load(fd.read()) or {}
        except Exception:
            return {}

def write_compose_override(data):
    data['version'] = '2'
    fd = StringIO()
    fd.write(yaml.dump(data, default_flow_style=False))
    fd.seek(0)
    put(fd, 'docker-compose.override.yml')




# DOCKER COMMANDS
################################################################################

@task
def dlogs(name, options=''):
    cmd = 'docker logs '
    cmd += options
    cmd += ' {}'.format(name)
    machineenv(cmd)

@task
def dps(options=''):
    cmd = 'docker ps '
    cmd += options
    machineenv(cmd)

@task
def dshell(container):
    cmd = 'docker exec -ti {} /bin/bash'.format(container)
    machineenv(cmd)

@task
def dexec(container, command, options='-ti'):
    cmd = 'docker exec '
    cmd += options
    cmd += ' {} {}'.format(container, command)
    machineenv(cmd)

# def docker_run(image, options=None):
#     '''Run Docker's container'''
#     _options = options or ''
#     local('%s run %s %s' % (env.docker, _options, image))
# run:
# 	docker run --rm --name $(NAME) $(LINKS) $(PORTS) $(VOLUMES) $(ENV) $(REPO):$(VERSION) $(CMD)

# start:
# 	docker run -d --name $(NAME) $(PORTS) $(VOLUMES) $(ENV) $(REPO):$(VERSION)

# stop:
# 	docker stop $(NAME)

# shell:
# 	docker run --rm --name $(NAME) -i -t $(PORTS) $(VOLUMES) $(ENV) $(REPO):$(VERSION) /bin/bash









# DOCKER MACHINE COMMANDS
################################################################################

def machineenv(cmd):
    """
    Execute `cmd` (string) in an ENV that redicrects docker commands to docker
    daemon running on docker-machine-managed cloud instance named `env.MACHINE_NAME`.
    If `env.MACHINE_NAME` is not defined, will execute `cmd` on localhost.
    """
    if 'MACHINE_NAME' in env and env.MACHINE_NAME:
        machine_name = env.MACHINE_NAME
        machine_port = env.MACHINE_PORT
        with hide('running'):  # hide echo of commands we're running 'stdout', 'stderr', 'output'):
            machine_ip = local("docker-machine inspect --format='{{{{.Driver.IPAddress}}}}' {0}".format(machine_name), capture=True)
            machine_cert_path = local("docker-machine inspect --format='{{{{.HostOptions.AuthOptions.StorePath}}}}' {0}".format(machine_name), capture=True)
        with shell_env(DOCKER_TLS_VERIFY='1',
                       DOCKER_HOST='tcp://{0}:{1}'.format(machine_ip, machine_port),
                       DOCKER_CERT_PATH=machine_cert_path,
                       DOCKER_MACHINE_NAME=machine_name):
            # will print containers on the remote machine
            local(cmd)
    else:
        local(cmd)


