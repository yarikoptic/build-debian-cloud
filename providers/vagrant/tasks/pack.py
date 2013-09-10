from base import Task
from common import phases
from common.tasks import packages
from common.tasks.host import CheckPackages
import os

class CreateBox(Task):
	description = 'Create Vagrant Box from image'
	phase = phases.image_registration

	def run(self, info):
        print "NOT YET IMPLEMENTED"

class VagrantConfig(Task):
    description = 'Customize image for Vagrant'
    phase = phases.system_modification

    def run(self, info):
        from shutil import copy
        assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), 'assets'))
        ssh_pub = os.path.join(assets_dir, 'ssh/vagrant.pub')
        os.chmod(script_dst, rwxr_xr_x)

        from common.tools import log_check_call
        log_check_call(['/bin/mkdir', '-p',
                        os.path.join(info.root,'root/.ssh')])
        authorized_keys = os.path.join(info.root,
                            'root/.ssh/authorized_keys')
        if "vagrant" in info.manifest and \
           "key.public" in info.manifest['vagrant']:
            f = open(authorized_keys,"a")
            f.write(info.manifest['vagrant']['key.public']+"\n")
            f.close()
        else:
            copy(ssh_pub, authorized_keys)
        log_check_call(['/usr/sbin/chroot', info.root,
                        '/bin/chmod', '600', '/root/.ssh/authorized_keys'])

