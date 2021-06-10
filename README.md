# robo-init

robo-init is an extension to `cloud-init` from Canonical and adds some robot/hardware-specific functionality. If you have a robot which needs "hardware"-configuration, you can use `robo-init` to consistently set up things like:

- wifi and other network connections
- install packages
- create udev rules for serial or USB communications
- set up users and user groups
- configure RaspberryPi and RaspberryPi overlays

robo-init is an open source project and licensed under the BSD3 license. We're happy to collaborate!

## How to use

You will have to write a YAML file that describes your desired configuration. An
example yaml file is in the `example/niryo.yml` folder. After installing this 
program using `pip install -e .` you will be able to run `robo-initgen myfile.yml`.

To run the example: `robo-initgen example/niryo.yml`

This will create a new folder: `generated_boot_config`. Inside of this folder, you'll
find three files:

- network-config
- user-data
- usercfg.txt

The usercfg.txt file contains the additional configuration for a RaspberryPi.
The network-config file contains the network configuration for the wifi and ethernet 
connections. The user-data contains the information on what users you want to 
set up initially and more. All of this is derived from the initial "niryo.yml" file.

If you're running a Ubuntu RaspberryPi image, you can just drop these files in the 
boot partition and replace the ones that are there by default.