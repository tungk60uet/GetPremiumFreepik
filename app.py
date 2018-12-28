import requests
from flask import Flask, request, json,render_template
# import cv2
# import numpy as np
# import base64
mask=None

def removeMask(src,mask):
    alpha=1-(1-src[:,:,3]/255)/(1-mask[:,:,3]/255)
    src[:,:,0]=(src[:,:,0]-mask[:,:,0]*(mask[:,:,3]/255))/(1-mask[:,:,3]/255)
    src[:,:,1]=(src[:,:,1]-mask[:,:,1]*(mask[:,:,3]/255))/(1-mask[:,:,3]/255)
    src[:,:,2]=(src[:,:,2]-mask[:,:,2]*(mask[:,:,3]/255))/(1-mask[:,:,3]/255)
    src[:,:,3]=alpha*255
# def imUrl(url):
#     res=requests.request("GET", url)
#     img_array = np.array(bytearray(res.content), dtype=np.uint8)
#     return cv2.imdecode(img_array, -1)
headers = {
    'upgrade-insecure-requests': "1",
    'dnt': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'referer': "https://www.freepik.com/premium-vector/city-background-business-book-cover-design-template_1363172.htm",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.9,vi;q=0.8",
    'cookie': "_ga=GA1.2.248191043.1533890339; fbm_102556336476545=base_domain=.freepik.com; __gads=ID=db8a47a8bcd9f80b:T=1533890458:S=ALNI_MZJyZY4pOTPYwXKlQf-Eed9Bo_Pfw; cto_lwid=8b8f1063-c79c-4f05-ab7c-96cacc618976; testab_ranking=A1; testab_se_pos=A1; _gid=GA1.2.888966877.1545788640; _fbp=fb.1.1545788639928.600723792; testab_ad_prem=A1; testab_pay_A=A1; testab_pay_B=B2; _gaexp=GAX1.2.-wZcU3LORcqXdDb7DI7VdA.17961.0; CB_URL=https://profile.freepik.com/preagreement/getstarted/; __zlcmid=q3htRn6xEQGNrY; gr_welcome=%7B%22site%22%3A%22flaticon%22%2C%22date%22%3A%222018-12-26T02%3A51%3A16%2B01%3A00%22%7D; gr_lang=english; ck_items_10628241=%5B%221363172%22%5D; _ga=GA1.2.248191043.1533890339; fbm_102556336476545=base_domain=.freepik.com; __gads=ID=db8a47a8bcd9f80b:T=1533890458:S=ALNI_MZJyZY4pOTPYwXKlQf-Eed9Bo_Pfw; cto_lwid=8b8f1063-c79c-4f05-ab7c-96cacc618976; testab_ranking=A1; testab_se_pos=A1; _gid=GA1.2.888966877.1545788640; _fbp=fb.1.1545788639928.600723792; testab_ad_prem=A1; testab_pay_A=A1; testab_pay_B=B2; _gaexp=GAX1.2.-wZcU3LORcqXdDb7DI7VdA.17961.0; CB_URL=https://profile.freepik.com/preagreement/getstarted/; __zlcmid=q3htRn6xEQGNrY; gr_welcome=%7B%22site%22%3A%22flaticon%22%2C%22date%22%3A%222018-12-26T02%3A51%3A16%2B01%3A00%22%7D; mp_28a22b7cf07cbca77b89d85b685d82f5_mixpanel=%7B%22distinct_id%22%3A%20%2216522fd2146db2-0b89f2d527c2bc-47e1039-1fa400-16522fd2147857%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com.vn%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com.vn%22%2C%22source%22%3A%20%22premium-detail%22%2C%22website%22%3A%20%22freepik%22%2C%22banner%22%3A%20%22fashion%20app%22%2C%22item%22%3A%20%22photo%22%2C%22id_photo%22%3A%20%223361889%22%7D; gr_lang=english; _gat=1; ck_items_10628241=%5B%221363172%22%5D; mp_28a22b7cf07cbca77b89d85b685d82f5_mixpanel=%7B%22distinct_id%22%3A%20%2216522fd2146db2-0b89f2d527c2bc-47e1039-1fa400-16522fd2147857%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com.vn%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com.vn%22%2C%22source%22%3A%20%22premium-detail%22%2C%22website%22%3A%20%22freepik%22%2C%22banner%22%3A%20%22fashion%20app%22%2C%22item%22%3A%20%22photo%22%2C%22id_photo%22%3A%20%223361889%22%7D; fbsr_102556336476545=io1HCUlzJOvce6iDf7onc3vI3Ie9bvdjhxYs_okaeJg.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFWaGRDYUI4em04enRaTUE5WTB2d0NwYWd1Sld6Tkd2dkQ1X2ZvT0p6dVZKRk5TZDNad0ltdTd1MzRHS2hheWtNYkVoSHhLTXVOVVpaelRxUC1WUWR0SGJZMkZHTGhSNEM3UndqTVRiUk81eko4VDY2d213Nk5FSlRMX1Z6X3pZT0h3aWtSUGc2Y29NdU0zUkZPbkNwNHNnYndnRE1VZHRfR1FsVHdtVjFKdDZYTzNvdmdUWHc2X0lYQ1hfaGFBSVRYdjJxb3FsZ25aNHZtODV1eFF0NFpyb1F3cjlfN0laQS1rcm1laVBPcTBpcnp4YlR6QmZZS0p6QUNURG1wVkhWZnBkdVI1a2Z3bVh1THVHQlRDdDFrM2dzOU9iTWZQMWdvVUpGakN2dkVhZjZvNFhIaXYyNzNNYlBXSFBKaFNUTEdEenNwd2hkMUl1clRrdkVjc1JOUSIsImlzc3VlZF9hdCI6MTU0NTc4OTMxMywidXNlcl9pZCI6IjE0NDkzNDY0NDg1MDQyOTQifQ; gr_session=c98e484fe46506a4260316c9a20f416bec8bafa6eedff44a72ee5dc71b8122fb9102285f431d76d63484e4e7a7cf2b772daee804ca97d3eba1beb898c1efb020Q2JQLKWdcboGddta8ek2zgEY7jTgnSWQI9PbzRguTNvG6vt1mMhDVfzf5Y7BJmkl8FeuJBLkHDp7Sbw5d%2BlmBJnjkoNhdqpgXMsg8m897NctRfjKso2lAXEbvpe%2FCdhrd7fRVNQvyuQ5pXE7S4a73RagxiPPjSmt4BPye%2FpX6q6celAd%2B8DQ5QBF3H0te27pMR57FbmXqYBCok7H0unx%2BGyvifq1%2F%2FgyBH%2FWT99JQG9Yfu5EQ7a5vIO%2F72hyofannqTeYcL1A0XwU2z%2BiIchNbbN1JkZtCd1BnOF8PcinwFbJG7bvOqoe9ZDdD2Rl%2B1LsJIInmTX8HWBn5YyMuWLF9dh4A%2FRWkV1UjIrkMiZaUaYgjE8ifoV6dWUPqjpzUuVgS5gCMBO9%2BDDbAhTXZyTgOq0m5FoP2HOCP81jAPkDn8S8ShorKf1RAX7ht%2FHLq28kB%2B4giaj%2BHTtl%2FqSMipCciNsKV7VuwqDSWIvn9S2Wcqw69F1I6Smg3FsSxLL16Fqmb363PEe76rmL%2F27MzDzMfPGfP5wGqeMiw8E%2Fx9xA1VvRHQ2nN2tyj7Smn%2FwjiMjpl5BTns4kAy2iJIwJ1o3EtViZrxGrZM0yRuGA5b0E%2F5VkRXPMpMkiL2c4WKH8DYO; gr_session=e358ea545ab438861240937bec4debd0ab8e5d40103164d8e0dec431a5b2eeffe263be36f4a4146703898d1c1cf9c7bcca8c471e41d9b6ee234edd83641e0b0fItm89tklmcbRXjBCOfhSx%2B%2Bk5xIRJweFNzcuFsRMxrqoywL4TOx77vzk7%2FabGg%2Ftyr2mzyHmrr2CHTxv2bMpju7GS%2FJE1OlkE7vxLc0nidmuJkt1jrbE4S6xMfaQRzq1cDjdXiDiViUVckc4oY7%2BEMKfc54TRJnTOmtuVlUMqfuhzY8re6eMYkfhP2GwM3XiT2PQhVJ%2BbDAFT1LzseWP%2BCCrFC84NeF5KTuItH1qke9ojbq1CrC8ZiU%2FXnMgW8HNZDfr0J%2FC1Qd%2BTCO2%2BQiCKNWfXOu4E4NhvqT2ngjsS%2FACi4AVCl7KFKi2TUb%2Bes3D9U7ukWMbQ%2FAFlQs7H8SWEv2rhvsSaASePQSETDGsGhhyRW7nI9AY69W62rruwuh%2FgkOrzu2f9XQHcndDKD6AronSMe5pGiZA07vaudp1aCMY4D2Y2aWqt8g80rUa%2BbDQwkWt1OtcXCF4gYgygpu79meYqazKqwbThqMFAdr1goNgZDYCJfHRKVK%2BqNa4GdrdTvTisarAQpfkYVg1OzbSO%2Ba6BfDdWzGf7rfhSJQ%2FT%2B9Q9TCUQmS5%2FJJc0XiffQuYQENOqbCkIVGWipjqgaxhSz%2BkWZAyuoeQiwhnie2SyGBnaHm0r19XBZ2QZQGaSlDm; fbsr_102556336476545=io1HCUlzJOvce6iDf7onc3vI3Ie9bvdjhxYs_okaeJg.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFWaGRDYUI4em04enRaTUE5WTB2d0NwYWd1Sld6Tkd2dkQ1X2ZvT0p6dVZKRk5TZDNad0ltdTd1MzRHS2hheWtNYkVoSHhLTXVOVVpaelRxUC1WUWR0SGJZMkZHTGhSNEM3UndqTVRiUk81eko4VDY2d213Nk5FSlRMX1Z6X3pZT0h3aWtSUGc2Y29NdU0zUkZPbkNwNHNnYndnRE1VZHRfR1FsVHdtVjFKdDZYTzNvdmdUWHc2X0lYQ1hfaGFBSVRYdjJxb3FsZ25aNHZtODV1eFF0NFpyb1F3cjlfN0laQS1rcm1laVBPcTBpcnp4YlR6QmZZS0p6QUNURG1wVkhWZnBkdVI1a2Z3bVh1THVHQlRDdDFrM2dzOU9iTWZQMWdvVUpGakN2dkVhZjZvNFhIaXYyNzNNYlBXSFBKaFNUTEdEenNwd2hkMUl1clRrdkVjc1JOUSIsImlzc3VlZF9hdCI6MTU0NTc4OTMxMywidXNlcl9pZCI6IjE0NDkzNDY0NDg1MDQyOTQifQ; gr_session2=a%3A8%3A%7Bs%3A2%3A%22id%22%3Bs%3A8%3A%2210628241%22%3Bs%3A5%3A%22login%22%3Bs%3A5%3A%22punib%22%3Bs%3A5%3A%22email%22%3Bs%3A19%3A%22punib%40providier.com%22%3Bs%3A9%3A%22real_name%22%3BN%3Bs%3A6%3A%22avatar%22%3Bs%3A69%3A%22https%3A%2F%2Fprofile.freepik.com%2Faccounts%2Favatar%2Fdefault_09.png%3F1545789302%22%3Bs%3A7%3A%22premium%22%3Bs%3A1%3A%221%22%3Bs%3A14%3A%22cc_will_expire%22%3Bi%3A0%3Bs%3A2%3A%22ts%22%3Bi%3A1545789314%3B%7D0f862121e552e1c3736bb33bc9d095a89dd1ee28; gr_session2=a%3A8%3A%7Bs%3A2%3A%22id%22%3Bs%3A8%3A%2210628241%22%3Bs%3A5%3A%22login%22%3Bs%3A5%3A%22punib%22%3Bs%3A5%3A%22email%22%3Bs%3A19%3A%22punib%40providier.com%22%3Bs%3A9%3A%22real_name%22%3BN%3Bs%3A6%3A%22avatar%22%3Bs%3A69%3A%22https%3A%2F%2Fprofile.freepik.com%2Faccounts%2Favatar%2Fdefault_09.png%3F1545789302%22%3Bs%3A7%3A%22premium%22%3Bs%3A1%3A%221%22%3Bs%3A14%3A%22cc_will_expire%22%3Bi%3A0%3Bs%3A2%3A%22ts%22%3Bi%3A1545789523%3B%7D260a4f95391e981bb786dd2dad39f00dfe8f046c; _gat=1",
    'cache-control': "no-cache"
}

app = Flask(__name__) 
@app.route('/')
def home():
    return render_template('home.html') 
@app.route('/getlink',methods=['POST'])
def getPremium(): 
    link=request.form['link']
    if link.rfind('flaticon.com')>-1:
        return '<p>Please check your link!!</p>'
        # id=link[link.rfind('_')+1:]
        # mini_id=''
        # if len(id)<=3:
        #     mini_id='0'
        # else: 
        #     mini_id=id[:len(id)-3]
        # img=imUrl("https://image.flaticon.com/icons/png/512/"+mini_id+"/"+id+".png")
        # if img is None:
        #     return '<p>Flaticon Not Found</p>'
        # else:
        #     if link.rfind('premium-icon')>-1:
        #         removeMask(img,mask)
        #     retval, buffer = cv2.imencode('.png', img)
        #     png_as_text = base64.b64encode(buffer)
        #     r = requests.request("POST", "https://api.imgur.com/3/image", headers = {'Authorization': 'Client-ID 61c083c996646da'},data={'image':png_as_text})
        #     linkicon=json.loads(r.text)['data']['link']
        #     print(linkicon)
        #     r2 = requests.request("GET", "https://123link.co/api?api=1153a84fc77a96e31d5971d6e66276e81b60ce66&url="+linkicon)
        #     shortlink=json.loads(r2.text)['shortenedUrl']
        #     return "<p>Flaticon "+id+": <a href='"+shortlink+"' target='_blank'>"+shortlink+"</a></p>"
    elif link.rfind('freepik.com')>-1:        
        id=link[link.rfind('_')+1:link.rfind('.htm')]
        r = requests.request("GET", "https://download.freepik.com/"+id, headers=headers,allow_redirects=True)
        if r.url=='https://www.freepik.com/404':
            return '<p>Freepik Not Found</p>'
        r2 = requests.request("GET", "https://123link.co/api?api=1153a84fc77a96e31d5971d6e66276e81b60ce66&url="+r.url)
        shortlink=json.loads(r2.text)['shortenedUrl']
        return "<p>Freepik "+id+": <a href='"+shortlink+"' target='_blank'>"+shortlink+"</a></p>"
    else:
        return '<p>Please check your link!!</p>'
if __name__ == '__main__':
    #mask=imUrl("https://i.imgur.com/1Ax3jx4.png")
    #mask=cv2.imread("mask.png",-1)
    app.run()