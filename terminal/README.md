## redplag_terminal
Terminal version of RedPlag.

### Functions :
1. Login
2. Change password
3. Upload
4. Download

### Usage

The server must be active. If you are testing locally, follow the instructions for the backend.

#### For Ubuntu and Mac users

The name of the terminal file is `redplagcli`. The `redplag_support.py` file must be present in the same folder as `redplagcli`.

First make `redplagcli` executable by using the command `chmod a+x redplagcli`

If this fails, you may use `python3 replag_support.py`

#### For Windows Users.

Use the .exe file named `replag.exe`

If this fails, you may use `python3 redplag_support.py`

+ Login:
`.\redplagcli login <email_id> <password>`

+ Change Password:
It is necessary to first login before changing password.
`.\redplagcli change <old_password> <new_password>`

+ Upload:
`.\replagcli upload <zip_file_path> <type_of_plag_check>`

	- Optional arguments : `[-b (short) or --boilerplate (long)] <boilerplate_path>`

	- zip file must have all files to be checked at depth 0 only. It must not contain any other subfolders.

	- types of plag check and the argument to be passed :
		1. C++ : cpp
		2. Python : python
		3. Codes in other languages : moss
		4. English Language Text : text

+ Download:
`.\redplagcli download`

	- Optional arguments : `[-p (short) or --path (long)] <download_path>`
