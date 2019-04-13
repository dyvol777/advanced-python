import imgkit
import qrcode
import base64


def generate():
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.jpg")

    f = open('qr.jpg', 'br').read()
    qr_code = base64.b64encode(f)

    html = open('template.html').read().format(qr_code=str(qr_code)[2:-1])
    f = open('1.html', 'w')
    f.write(html)

    path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
    imgkit.from_string(html, 'out.jpg', config=config)
