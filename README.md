# OneClickBackup
This is a program that simplifies backing up files. I knew too many people in college who lost at least 1 assignment due to technical problems. While cloud backups are becoming more common, internet access is not always guaranteed and cloud service providers typically charge monthly to lease storage capacity beyond a certain point. This is where my backup program can help.

This program allows end users to either copy or move files from one specified location to another. Amongst a group of files, backups can be limited to a specified file extension only, or all files can be included in the backup - at the user's choice. User preferences are stored in a database, and the backups only occur for files that were created or edited after the last backup date and time.

This project was a fun way for me to think about effective GUI design, learn wx.Python GUI objects as opposed to the more familiar WPF objects, and practice creating/reading/updating/deleting database information.

This project is almost complete, the last feature to be implemented is storing the user's working file location and backup file location preferences in the database. Once complete, I will compile this program for Windows, Mac, and Linux and release as an open source solution.
