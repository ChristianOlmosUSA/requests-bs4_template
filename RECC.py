# example of login and download website, including bypass the challenge/response which aims to stop scrapers
# the login form was taking the md5 has of the password, then adding the username and password to it and hashing it again
# https://www.youtube.com/c/RedEyedCoderClub/videos
from config import username, password
import hashlib
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def get_md5(s):
    return hashlib.md5(bytes(s, encoding='utf8')).hexdigest()

def main():
    url= 'https://sevashoes.com/en/login'

    with requests.session() as session:
        response = session.post(url,auth=(username,password))

        md5_pass = get_md5(password)+':'
        email = username + ':'

        soup = BeautifulSoup(response.text, 'lxml')
        challenge = soup.find('input', id='challenge').get('value')

        response = get_md5(email+md5_pass+challenge)

        data = {'username':username,
                'password': '',             # the form after hashing never actually sends the password, it makes it blank and sends the MD5
                'challenge': '',
                'response':response}

        r_post = session.post(url, data=data)

        pprint(response.text)

        with open('index.html', 'w') as f:
            f.write(r_post.text)

   #  print(get_md5('red')) .... this was just to check the md5 function was giving the right answer





if __name__ == '__main__':
    main()