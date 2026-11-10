# Dell PowerEdge T320: Mods

Part of the [Dell PowerEdge T320](Dell_PowerEdge_T320.md) documentation.

## Additional hard disk bays

One may use the 5.25" bays to install extra hard drive caddies.

Beware that it is not easy to obtain additional power cables for those drives and that we will be loading the existing power rails over their limits if we are not careful enough.

Consult the owner's manual before proceeding. This system does not support more than one internal RAID controller. For this reason, you may need to use expander cards or flash extra cards in IT mode.

Finally, you may need to acquire some hard drive controllers.

Caddies:

- [OImaster MR-6601](https://aliexpress.com/item/1005005545723632.html)

Cursed power cable adapters:

- [OULLX male SATA to dual Molex](https://aliexpress.com/item/4000138991016.html)

HDD controllers:

- [Dell PERC H310](../raid_controllers/Dell_PERC_H310.md)

## GPU

The T320 fits one full height GPU in slot 3, its only PCIe 3.0 x16 slot. Dell only validated the NVIDIA Quadro 4000 and 6000, but other cards work if they stay within the power and cooling limits.

Power:

- Up to 75 W: cards powered only by the slot need no extra parts. Passive datacenter cards (Tesla P4, T4) need extra airflow.
- Up to about 225 W: cards with power connectors need the [750 W power supplies](Dell_PowerEdge_T320_Upgrades.md#power-supplies) and these Dell parts:

| Part             | Dell P/N | Notes                                  |
| ---------------- | -------- | -------------------------------------- |
| GPU power cable  | 3692K    | PDB 8-pin to PCIe 8+6-pin (T620 cable) |
| PCIe card holder | 5HJGD    | Supports a full length card            |

Setup:

- Keep the onboard Matrox video as the primary display. The iDRAC virtual console uses it.
- Datacenter cards (Tesla and similar) may need `Memory Mapped I/O above 4 GB` enabled in the BIOS `Integrated Devices` menu. Consumer and workstation cards need no BIOS changes.
