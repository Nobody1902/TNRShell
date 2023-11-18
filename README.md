# TNRShell
- A remote control commandline tool, used for controlling multiple devices.

## Installation
- Run `pip install -r requirements.txt`
- Make sure to change the **SERVER INFO** in `client.py` to your server information.


- *Optionally you can change the settings in `.env`*

## Documentation


After starting `server.py` the commands you can use are:
<ln>
- *list* - prints all the connected clients (**ID**, **ip:port**)
- ***select (sel) [ip:port]*** - selects a client to control by hostname
- ***select (sel) .[ID]*** - selects a client to control by connection id
- *exit* - closes the serever
- *clear (cls)* -clears screen

After selecting a client to control the commands are:
<ln>
- *!exit* - exits the selection
- *!close (!stop)* - closes the server connection to the client
- **Any other command will be executed on the client's machine**

## Additional

- Check out this project's  [LICENSE](https://github.com/Nobody1902/TNRShell/blob/main/LICENSE)
- If you encounter any problems [create an issue](https://github.com/Nobody1902/TNRShell/issues/new).
- Or if you want to contribute [open a pull request](https://github.com/Nobody1902/TNRShell/compare).