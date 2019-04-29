import requests
# establishing session
s = requests.Session() 
s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

def load_user_data(page, session):
    url = 'http://www.mfc-chita.ru/filial/chita/vopros-otvet?&&&page=%d' % (page)
    request = session.get(url)
    return request.text


# loading files
page = 0
while True:
    data = load_user_data(page, s)
    if page <=25:
        with open('./user_data/page_%d.html' % (page), 'wb') as output_file:
            output_file.write(data.encode('utf-8'))
            page += 1
    else:
            break