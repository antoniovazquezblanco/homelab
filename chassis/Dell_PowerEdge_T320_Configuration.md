# Dell PowerEdge T320: Configuration

Part of the [Dell PowerEdge T320](Dell_PowerEdge_T320.md) documentation.

## Life cycle updates

One may find updates in the corresponding [Dell support webpage](https://www.dell.com/support/product-details/es-es/product/poweredge-t320/drivers) but they force you to manually download files and upload them to iDRAC one by one.

Alternatively, an awesome guy called Kenneth Finnegan, has setup a mirror server with updates for these obsolete machines at <https://updateyodell.net/>.

The configuration for this model would be as follows:

| Setting       | Value                |
| ------------- | -------------------- |
| File location | FTP                  |
| Address       | ftp.updateyodell.net |
| Username      | dell                 |
| Password      | calvin               |
| Path          | g12                  |

## iDRAC Console

### HTML5

This server has iDRAC 7.
If possible I would recommend using the HTML console.
In iDRAC go to `Server > Virtual Console > Type` and change it from `Java` to `HTML5`.
