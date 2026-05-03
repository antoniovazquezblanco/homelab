# Sophos XG230

Sophos XG Series rack format firewall. This series hardware reaches its EOL on March 31, 2025 so it is becoming cheap and a good chasis for certain applications.

[Sophos XG 230 Operating Instructions](https://docs.sophos.com/nsg/hardware/operatinginstructions/xg/sophos-operating-instructions-xg-210-rev3-230-rev2-oina.pdf)

![Sophos XG 230](Sophos_XG230.jpg)

## Mods

### Lower noise

For those of us that do not have a dedicated room for noisy devices and that do not expose them to huge amounts of heat, fan speed profile can be tuned to prevent noise on the lowest levels of fan speeds.

To do this, enter the BIOS setup by pressing `DEL` or `TAB` repeatedly after powering on the Sophos.

In the BIOS menu navigate to `Advanced`, `HW Monitor Status`, `Smart Fan Mode Configuration` and tweak the table to lower PWM output on the lowest temperature profiles.

### OpnSense

With Sophos reaching EOL support for this devices, it may not make sense to keep the original Sophos software running.
A good alternative candidate is OPNsense.

The latest OPNsense installer can be downloaded from <https://opnsense.org/download/>. A getting started guide is available at <https://opnsense.org/get-started/>.

Plug in the USB stick one of the USB ports.

Enter the BIOS setup by pressing `DEL` or `TAB` repeatedly after powering on the Sophos.

In the BIOS menu navigate to `Advanced`, `CSM Configuration`, `Boot option filter` and select `UEFI only` to enable UEFI boot mode.
Go to `Boot` and place `USB Key` to boot before `Hard Disk`.
Go to `Save & Exit` and press `Save Changes and Reset`.

The Sophos should boot from USB and you may proceed with the OpnSense installer.

### OpnSense LCD

To get the LCD working we need to install LCDproc in OPNsense.
Unfortunatelly, it is not yet officially supported ([See the Pull Request](https://github.com/opnsense/plugins/issues/5374)), but you can install it from [lcdproc-opnsense](https://github.com/ulyssedu45/lcdproc-opnsense). It can be downloaded from the repo releases at <https://github.com/ulyssedu45/lcdproc-opnsense/releases>.

To install LCDproc, download the latest pkg, upload it to the machine and install via `pkg add file.pkg`.

Once installation is complete, go to `Services`, `LCDproc` to configure the service.

Remember to check the `Enable LCDproc service` and select the following parameters for LCD configuration:

| Parameter       | Value                                    |
| --------------- | ---------------------------------------- |
| COM port        | Serial COM port 2 alternate (/dev/cuau1) |
| Display Size    | 2 rows 16 columns                        |
| Driver          | HD44780 and compatible                   |
| Connection type | Portwell EZIO-100 and EZIO-300           |
| Port speed      | Default                                  |

Press the save button and the LCD should be updated.
You may configure other settings following your preferences.

### Coreboot BIOS

Experimental Coreboot may be found at <https://github.com/ulyssedu45/sg230>. Untested, run at your own risk.
