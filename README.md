# Network Programming Course 2020

## DataBases

### USERS
| Key | Property |
| --- | ----------- | 
|UID| INTEGER PRIMARY KEY AUTOINCREMENT | 
|Username| TEXT NOT NULL UNIQUE | 
|Email| TEXT NOT NULL | 
|Password| TEXT NOT NULL | 

### BOARDS
| Key | Property |
| --- | ----------- | 
|BID| INTEGER PRIMARY KEY AUTOINCREMENT | 
|BName| TEXT NOT NULL UNIQUE | 
|UID| INTEGER | 

### POSTS
| Key | Property |
| --- | ----------- | 
|PID| INTEGER PRIMARY KEY AUTOINCREMENT | 
|TITLE| TEXT NOT NULL | 
|BName| TEXT | 
|UID| INTEGER | 
|DT| TEXT | 

~~HappyCoding~~ ~
