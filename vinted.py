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
        time.sleep(5)
        print(f"{Spy.blanc}[{Spy.jaune}RECHERCHE{Spy.blanc}] - Le bot recupere les informations de l'item...")
        reponse = requests.get(str(url))
        if 429 == reponse.status_code:
            print(f"{Spy.blanc}[{Spy.rouge}ERREUR{Spy.blanc}] - Rate Limit !")
            time.sleep(60)
        soup = BeautifulSoup(reponse.text, "html.parser")

        res = soup.findAll('div', {"class": "details-list__item-value"})
        res2 = soup.findAll('script', {"class": "js-react-on-rails-component"})

        description = json.loads(res2[14].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemDescription" data-dom-id="ItemDescription-react-component-3d79657d-a1b5-4f1d-b501-2f470f328c66" type="application/json">',
            "").replace("</script>", ''))
        userinfo = json.loads(res2[17].text.replace(
            '<script class="js-react-on-rails-component" data-component-name="ItemUserInfo" data-dom-id="ItemUserInfo-react-component-2105d904-b161-47d1-bfce-9b897a8c1cc6" type="application/json">',
            '').replace("</script>", ''))

        description = description["content"]["description"]
        positive = userinfo["user"]["positive_feedback_count"]
        negative = userinfo["user"]["negative_feedback_count"]
        username = userinfo["user"]["login"]

        taille = str(res[1]).replace('<div class="details-list__item-value">', "").replace('''<div class="overflow-menu overflow-menu--top-right u-cursor-pointer js-item-info-link" data-url="/help/515?access_channel=product_link" role="button" tabindex="0">
<div aria-label="Size information" class="c-icon--x-small c-icon--cg4 c-icon"><svg height="12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M6 12A6 6 0 1 1 6 0a6 6 0 0 1 0 12zm0-8a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM5 5v5h2V5H5z"></path></svg>
</div>
</div> </div>''', "").replace('''<divclass="overflow-menuoverflow-menu--top-rightu-cursor-pointerjs-item-info-link"data-url="/help/511?access_channel=product_link"role="button"tabindex="0">
<divaria-label="Sizeinformation"class="c-icon--x-smallc-icon--cg4c-icon"><svgheight="12"width="12"xmlns="http://www.w3.org/2000/svg"><pathd="M612A6601160a66001012zm0-8a110100-21100002zM55v5h2V5H5z"></path></svg>
</div>
</div></div>''', "").strip()
        etat = str(res[2]).replace('<div class="details-list__item-value" itemprop="itemCondition">', '').replace('''<div class="overflow-menu overflow-menu--top-right u-cursor-pointer js-item-info-link" data-url="/help/50?access_channel=product_link" role="button" tabindex="0">
<div aria-label="Condition information" class="c-icon--x-small c-icon--cg4 c-icon"><svg height="12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M6 12A6 6 0 1 1 6 0a6 6 0 0 1 0 12zm0-8a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM5 5v5h2V5H5z"></path></svg>
</div>
</div> </div>''', '').strip()
        couleur = str(res[3]).replace('<div class="details-list__item-value" itemprop="color">', '').replace('</div>',
                                                                                                             '').strip()
        emplacement = str(res[4]).replace('<div class="details-list__item-value">', '').replace('</div>', '').strip()
        return taille, etat, couleur, emplacement, description, positive, negative, username

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



        value = res[48].text.replace('<script data-js-react-on-rails-store="MainStore" type="application/json">', "")

        z = json.loads(value)
        del z["intl"]
        del z["session"]
        del z["screen"]
        del z["abTests"]
        del z["auth"]
        del z["savedSearches"]
        del z["consent"]
        del z["catalogFilters"]
        del z["ads"]
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
                with open("test.json",'w+') as testjson:
                    json.dump(z,testjson,indent=4)

                x = z["items"]["catalogItems"]["byId"]
                dictlist = list(x)
                for i in range(8, 0, -1):
                    time.sleep(1)
                    post = dictlist[i - 1]


                    if str(post) in posting:
                        print(f"{Spy.blanc}[{Spy.rouge}{post}{Spy.blanc}] - Item déjà envoyé !")
                        time.sleep(1)
                        continue
                    else:
                        print(f"{Spy.blanc}[{Spy.vert}{post}{Spy.blanc}] - Nouvel item trouvé !")
                        info = get_info_post(x[post]["url"])
                        taille = info[0]
                        etat = info[1]
                        couleur = info[2]
                        emplacement = info[3]
                        description = info[4]
                        positive = info[5]
                        negative = info[6]
                        username = info[7]

                        if "<div" in taille:
                            taille = "Erreur de donnée"
                        if "<div" in etat:
                            etat = "Erreur de donnée"
                        if "<div" in couleur:
                            couleur = "Erreur de donnée"
                        if "<div" in emplacement:
                            emplacement = "Erreur de donnée"


                        data = {"username": "$py",
                                "avatar_url": "https://cdn.discordapp.com/avatars/755734583005282334/158a0c81f5a3bd1f283bedd5f817a524.webp?size=1024",
                                "embeds": [
                                    {
                                        "title": f"``👕`` **__{x[post]['title']}__**",
                                        "description": f"```{configs['embed-color']}\n{description}```",
                                        "color": configs["embed-color"],
                                        "url": x[post]['url'],
                                        "fields": [

                                        ],
                                        "image": {
                                            "url": x[post]["photo"]["thumbnails"][4]["url"]
                                        },
                                        "footer": {
                                            "text": f"つ ◕_◕ ༽つ Merci 2$py !",
                                            "icon_url": "https://cdn.discordapp.com/avatars/828698716332097617/c4cd48b294bb755ec98521cec86f7899.webp?size=1024"
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
                            if taille == "":
                                size_title = "Pas de donnée"
                            else:
                                size_title = x[post]["size_title"]
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
                                "value": f"```{configs['embed-color-text']}\n{str(positive)} - {str(negative)}```",
                                "inline": True
                            })

                        if configs["embed-config"]["localisation"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``📍`` Emplacement **",
                                "value": f"```{configs['embed-color-text']}\n{emplacement}```",
                                "inline": True
                            })


                        if configs["embed-config"]["vendeur"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``👨`` Auteur**",
                                "value": f"```{configs['embed-color-text']}\n{username}```",
                                "inline": True
                            })

                        if configs["embed-config"]["couleur"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``🎨`` Couleur**",
                                "value": f"```{configs['embed-color-text']}\n{couleur}```",
                                "inline": True
                            })

                        if configs["embed-config"]["etat"] == "oui":
                            data["embeds"][0]["fields"].append({
                                "name": "**``🔭`` Etat**",
                                "value": f"```{configs['embed-color-text']}\n{etat}```",
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
