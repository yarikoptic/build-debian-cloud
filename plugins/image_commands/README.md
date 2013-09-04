# Image script plugin

This plugin gives the possibility to the user to execute commands or local scripts in the image.

Plugin is defined in the manifest file, plugin section with:

    "image_commands": {
        "enabled": true,
        "cmd": [ [ "echo", "hello" ]],
        "script": [ "/home/myscript.sh" ]
    }

The *cmd* element is an array of commands. Each command is an array describing
the executable and its arguments.

The *script* element will copy the specified files and execute them in the image.
