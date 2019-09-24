# CS 98 Hack 1: PocketCrypt

PocketCrypt is a file encryption manager that allows you to keep encrypted copies of files you're working on and carry them around with you. They can be kept anywhere, even the cloud \(potentially\)! This page will walk you through everything you need to know to get started using PocketCrypt.

PocketCrypt works by allowing you to create and manage different File Systems. Each File System can 'watch' different files, and all files under a specific file system will be encrypted under the same cryptographic key. No need to worry about the encryption, all that is taken care of behind the scenes!


We'll start by launching the program interface.
```
$ python fileManagerCMD.py
> Initializing metadata file.
> Awaiting command...
```
You can quit this program interface at any time using 'q'. Don't worry, all your data is saved in a metadata file.

### Create a File System
First thing we should do is create a File System.
```
> Awaiting command...
create myfs
> File system 'myfs' created.
```

Remember, you can view all existing File Systems and their metadata with the `show all systems` command.

### Add a File to a File System
Now that we have a File System, we need to tell it which files it will be in charge of. Let's create some files!

```
echo "Hello World!" > myFile.txt
echo "foobar" > anotherFile.txt
```

Now we can add them to our File System we created.

```
> Awaiting command...
add myFile.txt to myfs
File 'myFile.txt' added to system 'myfs'.
> Awaiting command...
add anotherFile.txt to myfs
File 'anotherFile.txt' added to system 'myfs'.
```

If you want to remove a file from your filesystem, use the `remove` command.

### Encrypting the File System
With all the relevent files added to our File System, we can encrypt it for the first time.

```
> Awaiting command...
encrypt myfs
> File 'myFile.txt' encrypted as '859fbe69f3dbd2cf35be8ba9aa047d05' using key 'GEhRTS1WLlPnlw0FgAGRWuHEY7ZWIwTqCzvu6joK7Ec='.
> File 'anotherFile.txt' encrypted as 'acdfa5354379904cfd65b29915fc0c60' using key 'GEhRTS1WLlPnlw0FgAGRWuHEY7ZWIwTqCzvu6joK7Ec='.
```
You'll notice that a folder `crypt` has been created. This is where all the encrypted files live. Open it up! Notice how all the file names are unrecognizable? That's because each file that's encrypted is given a random hash. Don't worry, though, PocketCrypt knows which one it is.

### Update a File System
Let's make a change to `myFile.txt`. Now the new version is out of date with the encrypted version! We have to update the encrypted version too.
```
$ echo "Added this part." >> myFile.txt
$ python fileManagerCMD.py
> Awaiting command...
update myfs
> Change detected in 'myFile.txt', re-encrypting file.
> File 'myFile.txt' encrypted as '859fbe69f3dbd2cf35be8ba9aa047d05' using key 'GEhRTS1WLlPnlw0FgAGRWuHEY7ZWIwTqCzvu6joK7Ec='.
```

Notice how it uses the same key to encrypt and it re-encrypts under the same file name as previously. No wasted space!

### Watch a File System
Who wants to manually use the `update` command?? Nobody! By using the `watch` command, you can edit your files in your File System and they will automatically be backed up into your crypt.
```
> Awaiting command...
watch myfs

```
Now all the files in 'myfs' are being monitored. Make a change to a file and see what happens.
```
> Change detected in 'anotherFile.txt', re-encrypting file.
> File 'anotherFile.txt' encrypted as 'acdfa5354379904cfd65b29915fc0c60' using key 'GEhRTS1WLlPnlw0FgAGRWuHEY7ZWIwTqCzvu6joK7Ec='.

```
Convenient! Conclude the watching process by tapping 'q'.

### Importing an Existing File System
There's a reason this program is called PocketCrypt. It's like a little pocket for your encrypted files! If you carry around with you your crypt and your metadata file \(you should encrypt this with a password\), then you can decrypt all your files on-the-go.

Let's delete the plaintext files.
```
$ rm myFile.txt
$ rm anotherFile.txt
```

Starting back up PocketCrypt, we can use the `import` command to get our files back from the crypt!

```
$ python fileManagerCMD.py 
> Awaiting command...
import myfs
> Creating myFile.txt by decrypting 859fbe69f3dbd2cf35be8ba9aa047d05 with key GEhRTS1WLlPnlw0FgAGRWuHEY7ZWIwTqCzvu6joK7Ec=
> Creating anotherFile.txt by decrypting acdfa5354379904cfd65b29915fc0c60 with key GEhRTS1WLlPnlw0FgAGRWuHEY7ZWIwTqCzvu6joK7Ec=
> Awaiting command...
q
> Safely quit.
$ cat myFile.txt
Hello World!
Added this part.
$ cat anotherFile.txt
foobarz
```

Pretty sweet, huh! If at any time you need help, type `help` or a specific command into the prompt.


## Tutorials Followed
- https://nitratine.net/blog/post/encryption-and-decryption-in-python/

## Other Resources
- https://cryptography.io
- https://stackoverflow.com/questions/2507808/how-to-check-whether-a-file-is-empty-or-not
- https://stackoverflow.com/questions/24072790/detect-key-press-in-python
- https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
- https://stackabuse.com/creating-and-deleting-directories-with-python/

## To Do
- Improve management of how all metadata is loaded into memory each time (use mySQLite)
