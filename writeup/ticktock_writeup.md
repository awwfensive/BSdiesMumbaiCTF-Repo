The secret is generated as a random uppercase letter string using a pseudo-random number generator seeded with the current time in minutes XORed with a fixed constant.
The attacker is supposed to indetify this behavior and enumerate the secret. 

[exploit attatched. ](https://github.com/awwfensive/BSdiesMumbaiCTF-Repo/blob/main/writeup/tick_tock_exploit.py)

# Instructions for Testing 
visit http://127.0.0.1:5000/?debug=true

Script to automate secret enumeration is provided within. 

once correct secret is prvided the flag is printed. 
