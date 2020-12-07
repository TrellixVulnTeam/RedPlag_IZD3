""" \package redplag_terminal
## redplag_terminal
Terminal version of RedPlag.

### Functions :
1. Login
2. Change password
3. Upload
4. Download

### Usage :

First make redplagcli executable by using the command "chmod a+x redplagcli"


+ Login:
`.\redplagcli login <email_id> <password>`

+ Change Password:
It is necessary to first login before changing password.
`.\redplagcli change <old_password> <new_password>`

+ Upload:
`.\replagcli upload <zip_file_path> <type_of_plag_check>`

Optional arguments :
`[-b (short) or --boilerplate (long)] <boilerplate_path>`

zip file must have all files to be checked at depth 0 only. It must not contain any other subfolders.

+ Download:
`.\redplagcli download`

Optional arguments :
`[-p (short) or --path (long)] <download_path>`


"""






import json
import sys
import os
import argparse
import re
import requests




argparser = argparse.ArgumentParser(description = "RedPlag Terminal")
argsubparsers = argparser.add_subparsers(title = "Commands", dest = "command")
argsubparsers.required = True


def main(argv = sys.argv[1:]):
    """!
    \brief Interaction between binary and python
    """
    
    args = argparser.parse_args(argv)

    # Commands
    # 1. Login
    # 2. Change Password
    # 3. Upload
    # 4. Download
    

    if (args.command == "login"):
        cmd_login(args)
    elif (args.command == "change"):
        cmd_change(args)
    elif (args.command == "upload"):
        cmd_upload(args)
    elif (args.command == "download"):
        cmd_download(args)
    else :
        print("Please use a valid command")

URL = "http://127.0.0.1:8000"


def redplag_login(email, password):
    """!
    \brief Login function
    """
    
    details = {'email' : email, 'password' : password}
    API_ENDPOINT = URL + "/api/login/"
    r = requests.post(url = API_ENDPOINT, data = details)
    data = r.json()

    if(r.status_code != 200):
        for e in data['non_field_errors']:
            print(e)
        print("Please login with the correct credentials")
        return
    else:
        print("Login Successful!")
    

    if not os.path.isdir('.redplag'):
        os.mkdir('.redplag')

    with open('.redplag/Authorization','w') as fout:
        fout.write(data['token'])

    #print(r.text)
    #print(data['status code'])

argsp = argsubparsers.add_parser("login", help = "Login using credentials")
argsp.add_argument('email')
argsp.add_argument('password')

def cmd_login(args):
    """!
    \brief Login function
    """
    
    redplag_login(args.email, args.password)





def redplag_change(old_password, new_password):
    """!
    \brief Change password function
    """
    
    details = {'old_password' : old_password, 'new_password' : new_password}
    jwt_token = ''

    if not os.path.isfile('.redplag/Authorization'):
        print("Please login first to change your password")
        return

    with open('.redplag/Authorization', 'r') as fout:
        jwt_token = 'Bearer ' + fout.read()


    
    auth = {'Authorization' : jwt_token}

    API_ENDPOINT = URL + "/api/change_pass/"
    r = requests.put(url = API_ENDPOINT, headers = auth, data = details)

    if(r.status_code != 200):
        print(r.text)
        print("Please enter correct credentials or relogin")
    else:
        print("Password change successful!")


argsp = argsubparsers.add_parser("change", help = "Change password")
argsp.add_argument('old_password')
argsp.add_argument('new_password')

def cmd_change(args):
    """!
    \brief Change password function
    """
    
    redplag_change(args.old_password, args.new_password)



def redplag_upload(upload_path, boilerplate_path, fileType):
    """!
    \brief Upload files function
    """
    
    
    API_ENDPOINT = URL + "/file/upload/"


    jwt_token = ''

    if not os.path.isfile('.redplag/Authorization'):
        print("Please login first to upload files")
        return


    with open('.redplag/Authorization', 'r') as fout:
        jwt_token = 'Bearer ' + fout.read()


    
    auth = {'Authorization' : jwt_token}

    details = {'fileType' : fileType}
    
    file = {'uploaded' : open(upload_path, 'rb')}
    if boilerplate_path != '':
        file[boilerplate] = open(boilerplate_path, 'rb')

    
    r = requests.post(url = API_ENDPOINT, headers = auth, data = details, files = file)
    
    if(r.status_code != 201):
        print(r.text)
        print("Please enter correct credentials or relogin")
    else:
        print("Upload successful!")

argsp = argsubparsers.add_parser("upload", help = "Upload files for plagiarism checking")
argsp.add_argument("zip_path", help = "Path of .zip to be uploaded for checking")
argsp.add_argument('-b','--boilerplate', help = "Path of boilerplate code", dest = 'boilerplate_path', default = '')
argsp.add_argument("type", help = "Type of files in zip")


def cmd_upload(args):
    """!
    \brief Upload files function
    """
    
    
    valid_types = ["cpp", "text"]
    if args.type not in valid_types:
        print("Please select one of the valid types of plagiarism checks")
        print("Valid types = ",valid_types)
    else:
        redplag_upload(args.zip_path, args.boilerplate_path, args.type)




def redplag_download(path):
    """!
    \brief Download files function
    """
    

    jwt_token = ''

    if not os.path.isfile('.redplag/Authorization'):
        print("Please login first to download results")
        return


    with open('.redplag/Authorization', 'r') as fout:
        jwt_token = 'Bearer ' + fout.read()


    
    auth = {'Authorization' : jwt_token}


    API_PROCESS = URL + "/file/upload/"
    API_ENDPOINT = URL + "/file/results/"
    process_files = requests.get(url = API_PROCESS, headers = auth)


    if(process_files.status_code != 200):
        print("Please enter correct credentials or relogin")
        return
    
    name_of_zip = process_files.text[1:-1]
    
    
    r = requests.get(url = API_ENDPOINT, headers = auth)


    if(r.status_code != 200):
        print("Please enter correct credentials or relogin")
        return
    
    
    result_path = path + "/" + name_of_zip
    if path == '':
        result_path = result_path[1:]

    print(result_path)
        

    with open(result_path, 'wb') as fout:
        fout.write(r.content)

    print("Download successful!")

    
    

argsp = argsubparsers.add_parser("download", help = "Download results of plagiarism checker")
argsp.add_argument('-p','--path', help = "Location to store results", default = '', dest = 'path')

def cmd_download(args):
    """!
    \brief Download files function
    """
    redplag_download(args.path)



if __name__ == '__main__':
    main()
