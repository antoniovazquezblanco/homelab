# Dell PERC H310

This is a very common controller among 12th generation Dell servers. Expect good integration with Rx20 and Tx20 models.

[PERC H310 Spec Sheet](https://i.dell.com/sites/doccontent/shared-content/data-sheets/Documents/dell-perc-h310-spec-sheet.pdf)
[PERC H310 User's Guide](https://dl.dell.com/manuals/common/rc_h310_h710_h710p_h810_ug_en-us.pdf)


## Modes

The card can operate in either in IR or IT modes.

By default, the card seems to ship an IR mode and although there are plenty tutorials on how to flash IT firmwares, the support for direct mode in IR firmwares makes this practice less common when compared to the [PERC H200](Dell_PERC_H200.md).

I would advise to stick to official Dell IR mode firmwares.


## Frimware flashing

In case you decide to flash IT mode firmware:
* [Updated: SAS HBA crossflashing or flashing to IT mode, Dell Perc H200 and H310](https://techmattr.wordpress.com/2016/04/11/updated-sas-hba-crossflashing-or-flashing-to-it-mode-dell-perc-h200-and-h310/)

In case you realize you want to go back to the stock firmware:
* [Revert your Perc H310 back to it’s Dell firmware](https://techmattr.wordpress.com/2014/06/13/revert-your-perc-h310-back-to-its-dell-firmware/)

In case things go very badly, some general documentation:
* [Broadcom Sas2Flash Utility Quick Reference Ghide](https://docs.broadcom.com/doc/12353205)


## Chassis not POSTing with the H310

For those that are unable to POST when an H310 is inserted into a PCI slot:
* [Modding a Dell Perc 6 / Dell H310 / Dell H710 (other LSI 1078 or 9223-8i based) SAS Raidcontroller](https://yannickdekoeijer.blogspot.com/2012/04/modding-dell-perc-6-sas-raidcontroller.html)
