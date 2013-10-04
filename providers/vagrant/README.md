



Vagrant box creation
====================


For the moment the provider does to create the vagrant box but only the vmdk
file needed to created the vagrant box.
to create the box, one need virtualbox and vagrant installed, then run the
following script:

    #!/bin/bash

    set -e

    # Path to the generated VMDK file
    VMPATH="vagrant"
    VM=`basename "$VMPATH" .vmdk`

    VBoxManage createvm --name $VM --ostype "Debian_64" --register
    VBoxManage storagectl $VM --name "SATA Controller" --add sata \
     --controller IntelAHCI
    VBoxManage storageattach $VM --storagectl "SATA Controller" --port 0 \
      --device 0 --type hdd --medium  $VMPATH

    VBoxManage modifyvm $VM --ioapic on
    VBoxManage modifyvm $VM --boot1 dvd --boot2 disk --boot3 none --boot4 none
    VBoxManage modifyvm $VM --memory 1024 --vram 128
    VBoxManage modifyvm $VM --nic1 nat

    vagrant package --base vagrant --output $VM.box
