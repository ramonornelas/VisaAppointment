import requests
from bs4 import BeautifulSoup

def process_cookies_and_token():
	cookie, csfrToken = get_cookie_and_token()
	cookie = get_sign_in_cookie(cookie, csfrToken)
	return cookie

# Define a function to call a post endpoint
def get_sign_in_cookie(cookie, csrfToken):
  login_url = "https://ais.usvisa-info.com/es-mx/niv/users/sign_in"
  email = "ornelas.carlos@gmail.com"
  password = "stdes#1Visa"

  login_request_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "DNT": "1",
    "Cookie": cookie,
    "Origin": "https://ais.usvisa-info.com",
    "Pragma": "no-cache",
    "Referer": login_url,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-CSRF-Token": csrfToken,
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
  }

  body = {
      "user[email]": email,
      "user[password]": password,
      "policy_confirmed": "1",
      "commit": "Sign In"
  }

  response = requests.post(
      login_url,
      headers=login_request_headers,
      data=body
  )

  # Check the response status code
  if response.status_code == 200:
    # Get the 'Set-Cookie' header
    set_cookie_header = response.headers.get('Set-Cookie')
    return set_cookie_header
  else:
    return "Error"

def get_cookie_and_token():
  # Get data from the API
  url = "https://ais.usvisa-info.com/es-mx/niv/users/sign_in"

  headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
  }

  # Send a GET request to the endpoint
  response = requests.get(url, headers=headers)

  # Check the response status code
  if response.status_code == 200:
    # Parse the response content as HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # Find all meta tags
    meta_tags = soup.find_all('meta')

    csrfToken = "no csrfToken found"
    # Iterate over the meta tags
    for meta in meta_tags:
      # Check if the meta tag has a 'content' attribute
      if 'content' in meta.attrs:
        csrfToken = meta['content']
    
    # Get the 'Set-Cookie' header
    set_cookie_header = response.headers.get('Set-Cookie')
    
    return set_cookie_header, csrfToken
      
  else:
    return "Error"
  
# Call the function
# cookie, csfrToken = get_cookie_and_token()
# print("Cookie:", cookie)
# print("Token:", csfrToken)

# print(sign_in_cookie(cookie, csfrToken))

    
      