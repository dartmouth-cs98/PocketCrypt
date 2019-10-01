# CS 98 Hack 1: PocketCrypt

PocketCrypt is a file encryption manager that allows you to keep encrypted copies of files you're working on and carry them around with you. They can be kept anywhere, even the cloud \(potentially\)! This page will walk you through everything you need to know to get started using PocketCrypt.

PocketCrypt works by allowing you to create and manage different File Systems. Each File System can 'watch' different files, and all files under a specific file system will be encrypted under the same cryptographic key. No need to worry about the encryption, all that is taken care of behind the scenes!

When you're reading to push a filesystem to the cloud, you can do so with the 'push' command, like Git.


### Create a File System
We'll start by creating a File System.
```
$ python fileManagerCMD.py create myfs -e
> Initialized PocketCrypt with metadata file: 'metadata.json'
> File system 'myfs' created.
> Equipped 'myfs'

```

That little `-e` or `--equip` flag we included means the file system will automatically be equipped after creation. If we forget to add it, we can always equip a fileystem using the `equip` command.
Remember, you can view all existing File Systems and their metadata with the `show` command with the `-a` or `--all` flag.

### Add a File to a File System
Now that we have a File System, we need to tell it which files it will be in charge of. Let's create some files!

```
echo "Hello World!" > myFile.txt
echo "foobar" > anotherFile.txt
```

Now we can add them to our File System we created. The `add` command will always add files to the currently equipped system. If you forget what's equipped, just use the `show` command.

```
$ python fileManagerCMD.py add myFile.txt
> File 'myFile.txt' added to system 'myfs'.

$ python fileManagerCMD.py add anotherFile.txt
> File 'anotherFile.txt' added to system 'myfs'.
```

If you want to remove a file from your filesystem, use the `remove` command.

### Encrypting the File System
With all the relevent files added to our File System, we can encrypt it for the first time.

```
$ python fileManagerCMD.py encrypt
> File 'myFile.txt' encrypted as '9908193f63bad15e30df4f32988f0211' using key 'qjpwf4AofCjJBa4exHJTm1V-WBs36F-DUWfhrpqXuwg='.
> File 'anotherFile.txt' encrypted as 'fe5c3abd0924a20fab46b3ccf3ff004e' using key 'qjpwf4AofCjJBa4exHJTm1V-WBs36F-DUWfhrpqXuwg='.
```
You'll notice that a folder `crypt` has been created. This is where all the encrypted files live (locally). Open it up! Notice how all the file names are unrecognizable? That's because each file that's encrypted is given a random hash. Don't worry, though, PocketCrypt knows which is which.

### Update a File System
Let's make a change to `myFile.txt`. Now the new version is out of date with the encrypted version! We have to update the locally encrypted version too.
```
$ echo "Added this part." >> myFile.txt
$ python fileManagerCMD.py update
> Change detected in 'myFile.txt', re-encrypting file.
> File 'myFile.txt' encrypted as '9908193f63bad15e30df4f32988f0211' using key 'qjpwf4AofCjJBa4exHJTm1V-WBs36F-DUWfhrpqXuwg='.
```

Notice how it uses the same key to encrypt and it re-encrypts under the same file name as previously. No wasted space!

### Watch a File System
Who wants to manually use the `update` command?? Nobody! By using the `watch` command, you can edit your files in your File System and they will automatically be backed up into your crypt.
```
$ python fileManagerCMD.py watch
```
Now all the files in 'myfs' are being monitored. Make a change to a file and see what happens.
```
> Change detected in 'myFile.txt', re-encrypting file.
> File 'myFile.txt' encrypted as '9908193f63bad15e30df4f32988f0211' using key 'qjpwf4AofCjJBa4exHJTm1V-WBs36F-DUWfhrpqXuwg='.

```
Convenient! Conclude the watching process by tapping 'q'.

### Pushing an Encrypted File System to the Cloud
Now for the fun part! When you're done editing and encrypting your files, you're gonna want to back them up in the cloud. For now, you can choose from either Dropbox or Google Drive. Let's push our encypted files to Google Drive.

```
$ python fileManagerCMD.py push drive
> Pushing '9908193f63bad15e30df4f32988f0211' (myFile.txt) to drive
> Pushing 'fe5c3abd0924a20fab46b3ccf3ff004e' (anotherFile.txt) to drive
```

Check your Drive. Your encrypted files now live in the "PocketCrypt" folder. They'll just hang out there until they're needed again.

If it happens that you forgot to re-encrypt your files after you made some changes, don't worry, pushing automatically updates your file system too.

### Pulling a File System from the Cloud
There's a reason this program is called PocketCrypt. It's like a little pocket for your encrypted files! If you carry around with you your crypt and your metadata file \(you should encrypt this with a password\), then you can pull and decrypt all your files on-the-go. We'll start with the `pull` command to localize our encrypted files.

```
$ python fileManagerCMD.py pull drive
> Pulling '9908193f63bad15e30df4f32988f0211' (myFile.txt) from drive
> Pulling 'fe5c3abd0924a20fab46b3ccf3ff004e' (anotherFile.txt) from drive
```

The crypt files have been updated! Now we can decrypt the file system and we will have our files.


### Decrypt a File System from the Crypt
Now we have to decrypt the encrypted local files.

First, let's delete the plaintext files.
```
$ rm myFile.txt
$ rm anotherFile.txt
```

Now we can use the `decrypt` command to get our files back from the crypt!

```
$ python fileManagerCMD.py decrypt
> Creating ./myfs//myFile.txt by decrypting 9908193f63bad15e30df4f32988f0211
> Creating ./myfs//anotherFile.txt by decrypting fe5c3abd0924a20fab46b3ccf3ff004e
```

And there, all files in your file system are now decrypted and available for viewing in the 'myfs' folder.

Pretty sweet, huh! If at any time you need help, type `-h` or `--help`.


## Resources
- https://github.com/msiemens/tinydb
- https://nitratine.net/blog/post/encryption-and-decryption-in-python/
- https://cryptography.io
- https://stackoverflow.com/questions/2507808/how-to-check-whether-a-file-is-empty-or-not
- https://stackoverflow.com/questions/24072790/detect-key-press-in-python
- https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
- https://stackabuse.com/creating-and-deleting-directories-with-python/
- https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

## To Do
- Implement a `pocket` command that encrypts the metadata file using a password and sends it into the cloud for future downloading and decryption instead of having to carry it around with you

## What'd I Learn?
- Symmetric encryption in python
- File management
- Python stuff in general
- Local database storage using python-esque JSON databases

## What Didn't Work?
- Coding before coming up with a complete plan made it tough, and also made it take longer than I envisioned. The finished product is completely different than what I first envisioned.
