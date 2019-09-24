# CS 98 Hack 1: MyCrypt

MyCrypt is a file encryption manager that allows you to keep encrypted copies of files you're working on. They can be kept anywhere, even the cloud \(potentially\)! This page will walk you through everything you need to know to get started using MyCrypt.

MyCrypt works by allowing you to create and manage different File Systems. Each File System can 'watch' different files, and all files under a specific file system will be encrypted under the same cryptographic key. No need to worry about the encryption, all that is taken care of behind the scenes!

Let's start by creating a file system.

## Create a File System



### Tutorials Followed
- https://nitratine.net/blog/post/encryption-and-decryption-in-python/

### Other Resources
- https://cryptography.io
- https://stackoverflow.com/questions/2507808/how-to-check-whether-a-file-is-empty-or-not
- https://stackoverflow.com/questions/24072790/detect-key-press-in-python
- https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python

### To Do
- Add "checkout" functionality for a filesystem
- Throw errors instead of printing messages
- Maybe encrypt specific files instead of entire file system when changes are made
- Improve management of how all metadata is loaded into memory each time (use mySQLite)
