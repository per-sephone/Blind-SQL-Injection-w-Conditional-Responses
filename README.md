This repository programatically solves [this](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses) Portswigger level which contains a blind SQL vulnerability. 

The program first finds the length of the password using a brute-force approach. It then uses a binary search algorithm to *quickly* brute force the password.

To use this program, download the requirements and pass in your unique URL for this level through the command line.
