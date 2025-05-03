# Dell PowerEdge T320

Dell Generation 12 tower format server.


## iDRAC Console

This server has iDRAC 7. The console still works via Java and requires a quite obsolete version of it to run. You may not want to install such an obsolete java version in your system so you may want to use one of the following links to get a zipped non-installable distribution:

* [Oracle JDK 8u421 x64 from Adobe](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u421/jdk/jdk-8u421-windows-x64.zip)
* [Oracle JDK 8u421 x86 from Adobe](https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u421/jdk/jdk-8u421-windows-i586.zip)

To launch the viewer you may run the following command:

```pwsh
.\jdk1.8.0_421\bin\javaws.exe -wait '.\viewer.jnlp'
```


## Life cycle updates

One may find updates in the corresponding [Dell support webpage](https://www.dell.com/support/product-details/es-es/product/poweredge-t320/drivers) but they force you to manually download files and upload them to iDRAC one by one.

Alternatively, an awesome guy called Kenneth Finnegan, has setup a mirror server with updates for these obsolete machines at <https://updateyodell.net/>.

The configuration for this model would be as follows:

| Setting       | Value                 |
|---------------|-----------------------|
| File location | FTP                   |
| Address       | ftp.updateyodell.net  |
| Username      | dell                  |
| Password      | calvin                |
| Path          | g12                   |



## Mods

### Additional hard disk bays

One may use the 5.25" bays to install extra hard drive caddies.

Beware that it is not easy to obtain additional power cables for those drives and that we will be loading the existing power rails over their limits if we are not careful enough.

Finally, you may need to acquire some hard drive controllers.

Caddies:
* [OImaster MR-6601](https://aliexpress.com/item/1005005545723632.html)

Cursed power cable adapters:
* [OULLX male SATA to dual Molex](https://aliexpress.com/item/4000138991016.html)

HDD controllers:
* [Dell PERC H200](../raid_controllers/Dell_PERC_H200.md)
