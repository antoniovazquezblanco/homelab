# Dell PowerEdge T320: Diagnostics and repairs

Part of the [Dell PowerEdge T320](Dell_PowerEdge_T320.md) documentation.

## iDRAC

### Description

The iDRAC 7 is a small computer of its own on the motherboard.

It runs from standby power, so it is alive whenever the server is plugged in, even when the server is off.

### Hardware

| Component | Part                   | Details                                                                                                                     |
| --------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| SoC       | Renesas SH7757 (SH-4A) | Processor with 256 MB RAM                                                                                                   |
| SPI flash | Macronix MX25L3206E    | Size of 4 MB. Holds two U-Boot copies, its environment and the iDRAC MAC addresses                                          |
| eMMC      | SanDisk SDIN7DR2-4G    | iNAND. 4 GB. 153-ball BGA. Holds the firmware (linux) and the data partitions                                               |
| Host link |                        | IPMI KCS interface at I/O port `0xca8`, which `ipmitool` and the BIOS use                                                   |
| Network   |                        | Shared with LOM1, or a dedicated port with the optional iDRAC ports card (2827M / 81RK6), which also has the vFlash SD slot |

### Boot sequence

1. SoC receives power on as soon as the server is plugged (even when the server is off)
2. U-Boot starts from the SPI flash, checks the eMMC and verifies the firmware images with CRC32.
3. The eMMC holds two firmware copies, the current one (`N`) and the previous one (`N-1`), each with a kernel, a root filesystem and a data image. U-Boot boots `N` and falls back to `N-1`.
4. Linux (3.4) starts the iDRAC services. They store configuration, Lifecycle Controller data and licences on ext3 partitions of the same eMMC.
5. A 180 second watchdog resets the iDRAC if the services never come up.
6. Meanwhile the BIOS waits for the iDRAC during POST. The iDRAC also controls the fans. When iDRAC is not running, the fans go to full speed as a failsafe.
