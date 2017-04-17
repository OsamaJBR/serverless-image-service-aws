from PIL import Image
import cStringIO
import PIL

class resize_handler():
    def resize(self,size,image_content):
        width=int(size.split('x')[0])
        height=int(size.split('x')[1])

        img = Image.open(image_content)
        if width and height:
            img = img.resize((width, height), PIL.Image.ANTIALIAS)
        elif not height:
            wpercent = (width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
        elif not width:
            hpercent = (height / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(hpercent)))
            img = img.resize((wsize, height), PIL.Image.ANTIALIAS)
        tmp_image = cStringIO.StringIO()
        img.save(tmp_image)
        return tmp_image