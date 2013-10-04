from base import Task
from common import phases

from common.tasks.network import RemoveDNSInfo


class ConfigureNetwork(Task):
	description = 'Configuring network DNS'
	phase = phases.system_modification
	after = [ RemoveDNSInfo ]

	def run(self, info):
		import os.path
		resolv_path = os.path.join(info.root, 'etc/resolv.conf')
		with open(resolv_path, 'w') as resolv_conf:
			resolv_conf.write('nameserver 10.0.2.2\n')
