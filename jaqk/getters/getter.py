import requests


def getter(url, timeout=10, proxies=None, retry=True, error=True):
    # main get function for all the website getter
    # it would support proxies, multiple user agent
    # it should raise errors when failure
    # Potential problems
    UA = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 \
        Safari/537.36']
    headers = {
        'User-Agent': UA[0]  # Select user agent
    }
    try:
        html = requests.get(url, headers=headers, proxies=proxies, timeout=timeout).text
        error = False
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        print("Connection Error, read time out")
        error = True
    if retry:
        if error == False:
            return html
        else:
            getter(url, timeout, error)
    else:
        return False
