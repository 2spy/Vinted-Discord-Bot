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


class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[2;0;1m"


def get_info_post(url):
    try:
        time.sleep(2)
        print(f"{Spy.blanc}[{Spy.jaune}RECHERCHE{Spy.blanc}] - Le bot recupere les informations de l'item...")
        reponse = requests.get(str(url))
        if 429 == reponse.status_code:
            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
            time.sleep(60)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('script', {"class": "js-react-on-rails-component"})

        description = json.loads(res[15].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemDescription" data-dom-id="ItemDescription-react-component-3d79657d-a1b5-4f1d-b501-2f470f328c66" type="application/json">',
            "").replace("</script>", ''))
        userinfo = json.loads(res[18].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemUserInfo" data-dom-id="ItemUserInfo-react-component-2105d904-b161-47d1-bfce-9b897a8c1cc6" type="application/json">',
            '').replace("</script>", ''))

        titre = description["content"]["title"]
        description = description["content"]["description"]
        positive = userinfo["user"]["positive_feedback_count"]
        negative = userinfo["user"]["negative_feedback_count"]
        username = userinfo["user"]["login"]
        pays = userinfo["user"]["country_title"]
        ville = userinfo["user"]["city"]

        lesinfo = {}

        if titre == "":
            titre = "Pas de donnée"
        if description == "":
            description = "Pas de donnée"
        if positive == "":
            positive = "Pas de donnée"
        if negative == "":
            negative = "Pas de donnée"
        if username == "":
            username = "Pas de donnée"
        if pays == "":
            pays = "Pas de donnée"
        if ville == "":
            ville = "Pas de donnée"

        try:
            lesinfo["titre"] = titre
            lesinfo["description"] = description
            lesinfo["positive"] = positive
            lesinfo["negative"] = negative
            lesinfo["username"] = username
            lesinfo["pays"] = pays
            lesinfo["ville"] = ville
            with open("test.json",'w+') as testjson:
                json.dump(lesinfo,testjson,indent=4)
        except Exception as err:
            print(err)
        return lesinfo
    except:
        pass


def search(url):
    try:
        time.sleep(5)
        print(f"{Spy.blanc}[{Spy.jaune}RECHERCHE{Spy.blanc}] - Le bot cherche des nouveaux items...")
        reponse = requests.get(str(url))
        if 429 == reponse.status_code:
            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
            time.sleep(60)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('script')
        value = res[49].text.replace('<script z-js-react-on-rails-store="MainStore" type="application/json">', "")
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

try:
    os.system('cls')
except:
    os.system('clear')
posting = []


class moniteur:
    def __init__(self, weburl, url):
        while True:
            try:
                z = search(str(url))
                x = z["items"]["catalogItems"]["byId"]
                dictlist = list(x)
                for i in range(9, 0, -1):
                    time.sleep(1)
                    post = dictlist[i - 1]
                    if str(post) in posting:
                        print(f"{Spy.blanc}[{Spy.rouge}{post}{Spy.blanc}] - Item déjà envoyé !")
                        time.sleep(1)
                        continue
                    else:
                        print(f"{Spy.blanc}[{Spy.vert}{post}{Spy.blanc}] - Nouvel item trouvé !")
                        info = get_info_post(x[str(post)]["url"])

                        data = {"username": "$py",
                                "avatar_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024",
                                "embeds": [
                                    {
                                        "description": f"```{configs['embed-color-text']}\n{info['description']}```",
                                        "title": f"``👕`` **__{x[post]['title']}__**",
                                        "color": configs["embed-color"],
                                        "url": x[post]['url'],
                                        "fields": [

                                        ],
                                        "image": {
                                            "url": x[post]["photo"]["thumbnails"][4]["url"]
                                        },
                                        "footer": {
                                            "text": f"つ ◕_◕ ༽つ Merci d'utiliser mes programmes ! <3",
                                            "icon_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024"
                                        }
                                    }]}
                        if configs["embed-config"]["prix"] == "oui":
                            data["embeds"][0]["fields"].append(
                                {
                                    "name": "**``💶`` Prix**",
                                    "value": f"```{configs['embed-color-text']}\n{x[post]['price']}€```",
                                    "inline": True
                                })

                        if configs["embed-config"]["taille"] == "oui":
                            if x[post]['size_title'] == "":
                                size_title = "Pas de donnée"
                            else:
                                size_title = x[post]['size_title']
                            data["embeds"][0]["fields"].append({
                                "name": "**``📏`` Taille**",
                                "value": f"```{configs['embed-color-text']}\n{size_title}```",
                                "inline": True
                            })

                        if configs["embed-config"]["marque"] == "oui":
                            data["embeds"][0]["fields"].append(
                                {
                                    "name": "**``🔖`` Marque**",
                                    "value": f"```{configs['embed-color-text']}\n{x[post]['brand_title']}```",
                                    "inline": True
                                }
                            )

                        if configs["embed-config"]["avis"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "``👍``/``👎`` **Note du vendeur**",
                                "value": f"```{configs['embed-color-text']}\n{str(info['positive'])} - {str(info['negative'])}```",
                                "inline": True
                            })

                        if configs["embed-config"]["localisation"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``📍`` Emplacement **",
                                "value": f"```{configs['embed-color-text']}\n{info['pays']}, {info['ville']}```",
                                "inline": True
                            })

                        if configs["embed-config"]["vendeur"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``👨`` Auteur**",
                                "value": f"```{configs['embed-color-text']}\n{info['username']}```",
                                "inline": True
                            })
                        result = requests.post(weburl, json=data)

                        if 429 == result.status_code:
                            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
                            time.sleep(60)
                        else:
                            posting.append(str(post))
                            print(f"{Spy.blanc}[{Spy.bleu}POSTE{Spy.blanc}] - Poste envoyé !")
            except:
                time.sleep(10)


if len(configs["suburl"]) > 5:
    print(
        f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Trop de salon veuillez en enlever car le bot se fera rate limit !")
else:
    for webhurl in configs["suburl"]:
        print(
            f"{Spy.blanc}[{Spy.violet}LANCEMENT{Spy.blanc}] - Lance de la tâche dans le salon {configs['suburl'][webhurl]['salon']}")

        t = threading.Thread(target=moniteur, args=[webhurl, configs["suburl"][str(webhurl)]["url"]])
        t.start()
