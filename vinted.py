import os
import json
import threading
import time

try:
    import requests
    from bs4 import BeautifulSoup
except:
    os.system("pip install requests")
    os.system("pip install bs4")



def get_info_post(url):
    try:
        reponse = requests.get(str(url))
        print(reponse)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('script', {"class": "js-react-on-rails-component"})

        description = json.loads(res[14].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemDescription" data-dom-id="ItemDescription-react-component-3d79657d-a1b5-4f1d-b501-2f470f328c66" type="application/json">',
            "").replace("</script>", ''))
        buybutton = json.loads(res[16].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemBuyButton" data-dom-id="ItemBuyButton-react-component-026520bb-78fd-4e8f-9477-541dcafab42d" type="application/json">',
            "").replace("</script>", ''))
        userinfo = json.loads(res[18].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemUserInfo" data-dom-id="ItemUserInfo-react-component-2105d904-b161-47d1-bfce-9b897a8c1cc6" type="application/json">',
            '').replace("</script>", ''))

        titre = description["content"]["title"]
        description = description["content"]["description"]
        buybutton = "https://www.vinted.fr" + buybutton["path"]
        positive = userinfo["user"]["positive_feedback_count"]
        negative = userinfo["user"]["negative_feedback_count"]
        username = userinfo["user"]["login"]
        pays = userinfo["user"]["country_title"]
        ville = userinfo["user"]["city"]

        lesinfo = {}
        lesinfo["titre"] = titre
        lesinfo["description"] = description
        lesinfo["buybutton"] = buybutton
        lesinfo["positive"] = positive
        lesinfo["negative"] = negative
        lesinfo["username"] = username
        lesinfo["pays"] = pays
        lesinfo["ville"] = ville
        return lesinfo
    except:
        pass


def search(url):
    try:
        reponse = requests.get(str(url))
        print(reponse)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('script')
        value = res[47].text.replace('<script z-js-react-on-rails-store="MainStore" type="application/json">', "")
        z = json.loads(value)

        del z["intl"]
        del z["session"]
        del z["screen"]
        del z["abTests"]
        del z["auth"]
        del z["savedSearches"]
        del z["ads"]
        del z["catalogFilters"]
        del z["items"]["catalogItems"]["ids"]
        return z
    except:
        pass


with open("config.json", 'r') as config:
    configs = json.load(config)

os.system('cls')

posting = []

import random

def moniteur(weburl, url):
    time.sleep(random.randint(15,25))
    while True:
        try:
            z = search(str(url))
            x = z["items"]["catalogItems"]["byId"]
            dictlist = list(x)
            for i in range(8, 0, -1):
                post = dictlist[i - 1]
                if str(post) in posting:
                    print("dedans")
                    continue
                else:
                    info = get_info_post(x[str(post)]["url"])

                    data = {"username": "$py",
                            "avatar_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024",
                            "embeds": [
                                {
                                    "description": f"```fix\n{info['description']}```",
                                    "title": f"``👕`` **__{x[post]['title']}__**",
                                    "url": x[post]['url'],
                                    "fields": [
                                        {
                                            "name": "**``💶`` Prix**",
                                            "value": f"```fix\n{x[post]['price']}€```",
                                            "inline": True
                                        },
                                        {
                                            "name": "**``📏`` Taille**",
                                            "value": f"```fix\n{x[post]['size_title']}```",
                                            "inline": True
                                        },
                                        {
                                            "name": "**``🔖`` Marque**",
                                            "value": f"```fix\n{x[post]['brand_title']}```",
                                            "inline": True
                                        },
                                        {
                                            "name": "``👍``/``👎`` **Avis**",
                                            "value": f"```fix\n{str(info['positive'])} - {str(info['negative'])}```",
                                            "inline": True
                                        },
                                        {
                                            "name": "**``📍`` Emplacement **",
                                            "value": f"```fix\n{info['pays']}, {info['ville']}```",
                                            "inline": True
                                        },
                                        {
                                            "name": "**``👨`` Auteur**",
                                            "value": f"```fix\n{info['username']}```",
                                            "inline": True
                                        }
                                    ],
                                    "image": {
                                        "url": x[post]["photo"]["thumbnails"][4]["url"]
                                    },
                                    "footer": {
                                        "text": f"つ ◕_◕ ༽つ Merci d'utiliser mes programmes ! <3",
                                        "icon_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024"
                                    }
                                }]}

                    result = requests.post(weburl, json=data)
                    try:
                        result.raise_for_status()
                    except Exception as err:
                        print(err)
                    posting.append(str(post))
                    time.sleep(6)
            time.sleep(60)
        except:
            pass

waiting = 0
for webhurl in configs["suburl"]:
    t = threading.Thread(target=moniteur, args=[webhurl, configs["suburl"][str(webhurl)]["url"]])
    time.sleep(waiting)
    t.start()
    waiting += 2
