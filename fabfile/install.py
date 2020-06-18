from fabric.decorators import task
from fabric.operations import run, sudo
from fabric.state import env


@task
def apt_get_update():
    """
    """
    sudo('apt-get update')


@task
def apt_get(*packages):
    """
    Runs apt-get install command for all provided packages
    """
    sudo('apt-get -y -f install %s' % ' '.join(packages), shell=False)


@task
def add_apt_repository(repository_name):
    sudo('add-apt-repository -y %s' % repository_name)


@task
def install():
    """
    """
    run("echo export LANGUAGE=en_US.UTF-8 >> ~/.bashrc")
    run("echo export LC_ALL=en_US.UTF-8 >> ~/.bashrc")
    add_apt_repository('ppa:certbot/certbot')
    add_apt_repository('ppa:jonathonf/python-3.6')
    apt_get_update()
    apt_get("certbot", "supervisor", "python-virtualenv", "build-essential",
            "libjpeg-dev", "libfreetype6", "libfreetype6-dev",  "python3.6-dev",
            "zlib1g-dev", "wget", "libcurl4-openssl-dev", "libssl-dev", "git",
            "libffi-dev", "sqlite3", "libpq-dev", "xvfb", "xorg", "postgresql",
            "postgresql-contrib", "python-pip", "wget", "nginx",
            "rabbitmq-server", "npm")
    git_clone()
    run("cd ~/; mkdir -p envs; cd envs; virtualenv {0} -p python3.6;"
        .format(env.repo_name))
    sudo("mkdir -p /{0} /{0}/static /{0}/media /{0}/django_logs".format(env.repo_name))
    sudo("chown -R {0} /{1} ".format(env.user, env.repo_name))
    sudo("mkdir -p /var/log/gunicorn /var/log/celery;")
    sudo("touch /var/log/gunicorn/{0}.log".format(env.repo_name))
    sudo("touch /var/log/celery/{0}.log".format(env.repo_name))
    sudo("touch /var/log/celery/{0}-beat.log".format(env.repo_name))
    sudo("touch /var/log/celery/{0}-flower.log".format(env.repo_name))


@task
def git_clone():
    """
    """
    run("cd ~/; git clone {}".format(env.repository))
