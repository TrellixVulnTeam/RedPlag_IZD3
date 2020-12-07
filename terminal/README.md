""" ## redplag_terminal
Terminal version of RedPlag.

### Functions :
1. Login
2. Change password
3. Upload
4. Download

### Usage :

First make redplagcli executable by using the command "chmod a+x redplagcli"


+ Login:
.\redplagcli login <email_id> <password>

+ Change Password:
It is necessary to first login before changing password.
.\redplagcli change <old_password> <new_password>

+ Upload:
.\replagcli upload <zip_file_path> <type_of_plag_check>

Optional arguments :
[-b (short) or --boilerplate (long)] <boilerplate_path>

zip file must have all files to be checked at depth 0 only. It must not contain any other subfolders.

+ Download:
.\redplagcli download

Optional arguments :
[-p (short) or --path (long)] <download_path>

"""
