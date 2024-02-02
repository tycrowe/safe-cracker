### SafeCracker Description
This is a tiny FTP-backed game where you have to attempt to crack a safe by uploading algorithms to match the possible 
BigO time complexity required to crack the safe. The game is played by uploading a file to the FTP server, and the server
will then run the file and determine if the result is a pass. 

## Hosting
The game is hosted locally by creating a FTP server using the `pyftpdlib` library. The server is hosted on `localhost` and
the port is `2121`. The server is started by running the `safe_cracker.py` file.

Steps to host the game:
1. Create user credentials for all the players that will be playing the game. This can be done in the `safe_cracker.py`.
2. Determine the local network IP address of the host machine, this can be done by running the `ipconfig` command on
Windows or the `ifconfig` command on Unix-based (Linux/Mac) systems. Use this in place of `<your-network-ip>` in the
third step.
3. Run the `safe_cracker.py` file
4. The server will start and the game will be hosted on `<your-network-ip>:2121`
5. The game can be accessed by connecting to the server using an FTP client or by using the `ftp` command in the terminal
if you are on a Unix-based system (All systems should have the `ftp` command installed by default).

## Playing the Game
The game is played by uploading a file to the FTP server. The file should contain an algorithm that can crack the safe
that has some random time complexity. The server will run the file and determine if the result is a pass.

Step to play the game:
1. Connect to the server using an FTP client or by using the `ftp <host-network-ip> 2121` command in the terminal.
2. You will be prompted to enter a username and password. The host should provide you with the credentials.
3. Once connected, you can upload a file to the server. The file should contain an algorithm that can crack the safe. The 
command to upload a file is `put <file-name>.py <username>.py`.