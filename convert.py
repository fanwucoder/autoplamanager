from PIL import Image
fn="公告"
a=Image.open(fn+".png")
a.save(fn+".bmp")