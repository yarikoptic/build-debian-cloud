from base import Task
from common import phases
import os
from common.tasks.packages import ImagePackages
from common.tasks.host import CheckPackages
from common.tasks.filesystem import MountVolume


class ImageExecuteCommand(Task):
    description = 'Execute command in the image'
    phase = phases.system_modification

    def run(self, info):
        if 'cmd' not in info.manifest.plugins['image_commands']:
            return
        from common.tools import log_check_call

        for user_cmd in info.manifest.plugins['image_commands']['cmd']:
            chroot_cmd = ['/usr/sbin/chroot', info.root]
	    chroot_cmd.extend(user_cmd)
            log_check_call(chroot_cmd)



class ImageExecuteScript(Task):
    description = 'execute script in the image'
    phase = phases.system_modification

    def run(self, info):
        if 'script' not in info.manifest.plugins['image_commands']:
            return

        import stat
        rwxr_xr_x = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                     stat.S_IRGRP                | stat.S_IXGRP |
                     stat.S_IROTH                | stat.S_IXOTH)

        from shutil import copy
        from common.tools import log_check_call

        for script in info.manifest.plugins['image_commands']['script']:
            script_src = os.path.normpath(script)
            script_dst = os.path.join(info.root, 'tmp/'+os.path.basename(script_src))
            copy(script_src, script_dst)
            os.chmod(script_dst, rwxr_xr_x)

            log_check_call(['/usr/sbin/chroot', info.root,
                            'tmp/'+os.path.basename(script_src)])
            log_check_call(['/usr/sbin/chroot', info.root, 
                            'rm', '-f', 'tmp/'+os.path.basename(script_src)])
