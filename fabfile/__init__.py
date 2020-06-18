from . import common
from . import install

from dotenv import load_dotenv
from fabric.decorators import task
from fabric.state import env

import os

load_dotenv()

env.repository = "https://git.codebusters.team"
env.repository_ssh = "https://git.codebusters.team"
env.repo_name = "uniq"
env.user = "ubuntu"
env.key_filename = "~/work/key/uniq.pem"
env.hosts = [""]


@task
def dev():
    env.config = 'Dev'
    env.user = os.getenv('DEV_USER')
    env.password = os.getenv('DEV_PASSWORD')
    env.hosts = [os.getenv('DEV_HOST')]
    env.environ = 'dev'
    env.dotenv_path = '{}/.env'.format(env.repo_name)


@task
def prod():
    env.config = 'Prod'
    env.user = os.getenv('PROD_USER')
    env.password = os.getenv('PROD_PASSWORD')
    env.hosts = [os.getenv('PROD_HOST')]
    env.environ = 'prod'
    env.dotenv_path = '{}/.env'.format(env.repo_name)
