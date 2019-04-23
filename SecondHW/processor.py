import random
import string
import imgkit
import qrcode
import base64
from io import BytesIO


def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate(i=0):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    qr.add_data(id_generator(20))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    html = open('template.html').read().format(qr_code=str(img_str)[2:-1])

    path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
    img = imgkit.from_string(html, False, config=config)
    # time.sleep(5)
    print(str(i) + ' finished!')
    return [img, i]


if __name__ == '__main__':
    generate()
