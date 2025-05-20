# MYNA

MYNA is a python program that helps you create shortcuts and translation

## Installation

Use [GIT](https://github.com/git-guides/git-clone) clone to install myna.

```bash
git clone https://github.com/itsal3xis/myna.git
```
You can also put the program as a shell script
```bash
sudo nano /usr/local/bin/myna
------------------------------------------------

#!/bin/bash
python3 /home/user/myna/myna/main.py "$@"
-------------------------------------------------

sudo chmod +x /usr/local/bin/myna
```

## Example Usage

```bash
alexis@kali:~/Documents/myna 🐦>lsal
/bin/sh: 1: lsal: not found
❓ Unknown command 'lsal'. Create alias? (y/N): y
📝 Real command for 'lsal': ls -al
✅ Alias saved: lsal → ls -al
total 32
drwxrwxr-x 4 alexis alexis 4096 May 20 18:01 .
drwxr-xr-x 3 alexis alexis 4096 May 20 18:01 ..
drwxrwxr-x 8 alexis alexis 4096 May 20 18:01 .git
-rw-rw-r-- 1 alexis alexis 3443 May 20 18:01 .gitignore
-rw-rw-r-- 1 alexis alexis 1071 May 20 18:01 LICENSE
-rw-rw-r-- 1 alexis alexis   49 May 20 18:01 README.md
drwxrwxr-x 3 alexis alexis 4096 May 20 18:06 myna
-rw-rw-r-- 1 alexis alexis   31 May 20 18:01 requirements.txt
-rw-rw-r-- 1 alexis alexis    0 May 20 18:01 setup.py

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
