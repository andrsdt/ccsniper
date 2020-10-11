
from ccbot import fetchProduct
from messages import CreateMessage, SendMessage
from gmail import gmailAPIsetup

keywords = ['p45', 'p125', 'cdps100', 'casio', 'korg b2', 'es110', 'px160']
min_price = 70
max_price = 400
mail_sender = 'mail_sender_gmail'
mail_receiver = 'mail_receiver_mail'
urls = [f"https://www.cashconverters.es/es/es/comprar/informatica/tablet/pc/?pmin={min_price}&pmax={max_price}&srule=new&view=all",
        f"https://www.cashconverters.es/es/es/comprar/instrumentos-musicales/pianos-y-organos/piano/?pmin={min_price}&pmax={max_price}&srule=new&view=all"]

def main():
    for url in urls: # urls == lista
        if (x := fetchProduct(url, keywords)):  # Walrus operator is available since Python 3.8
            found, name, price, final_url, matching_keyword = x
            service = gmailAPIsetup()
            sender = mail_sender
            receiver = mail_receiver
            subject = f'CCSniper | {matching_keyword} | {price}'
            message_text = f'Nombre: {name}\n\nURL: {final_url}'
            
            message = CreateMessage(sender, receiver, subject, message_text)
            SendMessage(service, 'me', message)
        else:
            print('Couldn\'t find any product with these keywords.')


if __name__ == '__main__':
    main()