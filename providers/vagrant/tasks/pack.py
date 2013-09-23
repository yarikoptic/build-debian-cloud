from base import Task
from common import phases
from common.tasks import packages
from common.tasks.host import CheckPackages
from providers.virtualbox.tasks.packages import ImagePackages as VirtualBoxImagePackages
import os

class CreateBox(Task):
	description = 'Create Vagrant Box from image'
	phase = phases.image_registration

	def run(self, info):
		print "NOT YET IMPLEMENTED"

class VagrantPackages(Task):
	description = 'Determining required image packages'
	phase = phases.preparation
	after = [ VirtualBoxImagePackages ]

	def run(self, info):
		manifest = info.manifest
		include, exclude = info.img_packages
		include.add('ruby')
		include.add('rubygems')
		include.add('sudo')
		include.add('build-essential')
		include.add('linux-headers-'+manifest.system['architecture'])


class VagrantUser(Task):
	description = 'Create default vagrant user'
	phase = phases.system_modification

	def run(self, info):
		from common.tools import log_check_call
		log_check_call(['/usr/sbin/chroot', info.root,
		                '/usr/sbin/groupadd', 'admin'])
		log_check_call(['/usr/sbin/chroot', info.root,
		                '/usr/sbin/useradd', '-G', 'admin', '-m', 'vagrant'])
		log_check_call(['/usr/sbin/chroot', info.root,
		                '/usr/sbin/chpasswd'],
		                'vagrant:vagrant')
		sudoer = os.path.join(info.root,'etc/sudoers.d/vagrant')
		f = open(sudoer,"w")
		f.write("%admin ALL=(ALL) NOPASSWD: ALL\n")
		f.close()


class VagrantHostname(Task):
	description = 'sets Vagrant image name'
	phase = phases.system_modification

	def run(self, info):
	hostname_file = os.path.join(info.root,'etc/hostname')
	f = open(hostname_file,"w")
	f.write("vagrant-debian")
	f.close()
	from common.tools import sed_i
	hosts_file = os.path.join(info.root,'etc/hosts')
	sed_i(hosts_file, 'localhost', 'localhost vagrant-debian')


class VagrantConfig(Task):
	description = 'Customize image for Vagrant'
	phase = phases.system_modification
	after = [ VagrantUser]

	def run(self, info):
		from shutil import copy
		assets_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '../assets'))
		ssh_pub = os.path.join(assets_dir, 'ssh/vagrant.pub')

		from common.tools import log_check_call
		log_check_call(['/bin/mkdir', '-p',
		               os.path.join(info.root,'home/vagrant/.ssh')])

		authorized_keys = os.path.join(info.root,
		                               'home/vagrant/.ssh/authorized_keys')
		if 'key.public' in info.manifest.vagrant:
			f = open(authorized_keys,"a")
			f.write(info.manifest['vagrant']['key.public']+"\n")
			f.close()
		else:
			copy(ssh_pub, authorized_keys)

		log_check_call(['/usr/sbin/chroot', info.root,
		          '/bin/chmod', '600', '/home/vagrant/.ssh/authorized_keys'])
		log_check_call(['/usr/sbin/chroot', info.root,
		                '/bin/chown', '-R', 'vagrant', '/home/vagrant/.ssh'])

