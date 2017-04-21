from PIL import Image
import StringIO

class resize_handler():
    def resize(self,size,image_content):
        width=int(size.split('x')[0])
        height=int(size.split('x')[1])
        img = Image.open(image_content)
        if width and height:
            img = img.resize((width, height), Image.ANTIALIAS)
        elif not height:
            wpercent = (width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((width, hsize), Image.ANTIALIAS)
        elif not width:
            hpercent = (height / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(hpercent)))
            img = img.resize((wsize, height), Image.ANTIALIAS)
        tmp_img = StringIO.StringIO()
        img.save(tmp_img,'png')
        return tmp_img