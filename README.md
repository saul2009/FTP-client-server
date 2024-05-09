# FTP-server-and-FTP-client
implement (simplified) FTP server and FTP client. The client shall connect to the server and support uploading and downloading of files to/from server.
# Names and Email Addresses:
Nathan Bupte - treeman_joe@csu.Fullerton.edu
Saul Andrade - saulandrade124@csu.fullerton.edu
An Dao - andao123@csu.fullerton.edu
Angel Villa - angelvilla7@csu.fullerton.edu
# Language Used:
Python 3.9
# How to execute program:
1) Open 1 terminal window and run the script server.py by the example command: python server.py <PORTNUMBER> (Replace the <PORTNUMBER> with your chosen port number)
2) Open another terminal window to run the client.py with command: python client.py <SERVER_MACHINE> <SERVER_PORT>
3) On the client terminal will show up the prompt ftp. Now you can enter FTP commands such as:
   - ls: to list files in the server's working directory
   - put <FILENAME>: to upload a file to server
   - get <FILENAME>: to download a file from the server
   - quit: to quit the client