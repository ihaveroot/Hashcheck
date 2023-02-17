# Hashcheck
A simple hash verifier for files.

I had made this a while back while tinkering with python, forgotten about it and have now updated it to release it (trying to use github more). 

I've always disliked having to open another term to verify hashsums when downloading important files. Generally speaking, any organization that creates Paas, Saas or any of the types, usually have hash checksums beside the download of their binaries. I found it a bit tedious to copy the hashsum, open a term in the directory and then run 'hashutil', 'md5sum', 'sha256sum', etc. to verify the two hashes, I'm sure there's other tools that do this, though this was fun lil project to make.


## Examples
If a match is found:

![Match_found](/img/valid_hash_input_match.gif)

No match:

![No_Match_found](/img/valid_hash_input_no_match.gif)


## Info
This program was written in:
- `python 3.10.4`

**\* I'm sure it can run on previous python versions, though I have not tested this.**

The releases built with:
- `pyinstaller 5.7.0`

The arguments with pyinstaller:
```
pyinstaller --onefile hashcheck.py
```

Since it was built with the flag `--onefile`, the load time will be slower when invoking Hashcheck. I recommend building the binary yourself: [pyinstaller manual](https://pyinstaller.org/en/stable/)


## Dependancies
All of the dependancies are in the `requirements.txt` file.

Hashcheck uses the following libraries:
- `colorama 0.4.6`
- `pyperclip 1.8.2`
- `termcolor 1.1.0`
- `tqdm 4.64.1`

You can install these with `pip3`:

```
pip3 install -r requirements.txt
```

If you do not have pip3 installed then you can run:
```
sudo apt install python3-pip
```


## Running
I wrote this with the intent of having the hash already in my system clipboard. You can copy the hash of whatever program you're checking against, and run the program to the target file.

invoking through python3:
```
python3 Hashcheck.py <file>
```

If you are using the prebuilt binary:
```
Hashcheck.exe <file>
```

You may pass a directory to a target file such as:
```
Linux:   python3 Hashcheck.py /bin/ping
windows: Hashcheck.exe C:\Users\ihr\Desktop\passwords.txt
```

If there are whitespaces in the directory then pass it with double quotes:
```
Linux:   python3 Hashcheck.py "~/Coding/CPP/ihaveroots sketchycode.cpp"
Windows: Hashcheck.exe "C:\Users\ihr rules\Desktop\domain_admin.txt"
```


## Linux
I initally wrote this for windows, it will execute, though, if you're running it from the command line, omit line 280 else it will yield the error of:
```
sh: 1: pause: Permission denied
```


## Windows
I made this with the intent on adding it to windows' context menu for a quick run. I didn't want to mess around with opening terminals. I also wanted to avoid fondling around with the registry so I've found adding it to the `sendto` context much easier. If you're running it from the command line then see Running.

![Right_click_context](/img/sendto.gif)

You may do the same by:
- Opening run: `Windows Key+R`
- Typing in: `shell:sendto`
- Adding the most recent release to the folder location

![Sendto](/img/run.png)