from fabric.api import *

env.hosts = ["ec2-35-167-182-249.us-west-2.compute.amazonaws.com"]
env.user = "ubuntu"
env.key_filename = ['/home/cognizac/Downloads/Stevens-key.pem']

def fix_502():
    put('myproject.py')

    with settings(warn_only=True), hide('output'):
        sudo('service myproject stop')
        sudo('service nginx stop')

        run('conda remove --name chatbot --all')

        run('conda create --name chatbot python=2')

        with prefix('source activate chatbot'):
            run('pip install flask uwsgi')
            run('conda install anaconda')

        sudo('service myproject start')
        sudo('service nginx start')

        ip = run('curl icanhazip.com')

        print '\n\n\n\nOPEN THIS IN YOUR BROWSER - {}:41953'.format(ip)
