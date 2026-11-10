# Dell PowerEdge T320: Official upgrades and accessories

Part of the [Dell PowerEdge T320](Dell_PowerEdge_T320.md) documentation.

## Power supplies

Systems with redundant power supplies come with 495 W or 750 W hot plug units.
In redundant mode the system has 750 W in total, not 1500 W, because a single unit must be able to carry the whole load.

To check which units are installed:

```sh
sudo ipmitool fru print                  # Look for "PWR SPLY,495W,RDNT,..." or "PWR SPLY,750W,RDNT,..."
sudo ipmitool sdr type "Power Supply"    # Presence, "AC lost" and redundancy status
```

The 750 W units are needed to power a [GPU](Dell_PowerEdge_T320_Mods.md#gpu) with power connectors.

If you want to replace your PSUs, replace both power supplies!
Do not mix 495 W and 750 W units!

Compatible part numbers:

| Generation | Power | Dell P/N                                        | Fits |
| ---------- | ----- | ----------------------------------------------- | ---- |
| 12th       | 750 W | 5NF18, 6W2PW, N30P9, 79RDR, 9PXCV, F9F51, W0CTF | Yes  |
| 13th       | 750 W | 5RHVV, 0XW8W, TPJ2X, XTVK2                      | No   |
