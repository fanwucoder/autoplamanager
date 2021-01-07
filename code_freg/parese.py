# -*- coding: utf-8 -*-
from lxml import etree

a = etree.parse("ui.xml")
data = a.xpath("//node[@text='main.lua']")[0]
ret = data.attrib.get("bounds")


b = etree.parse("ui1.xml")
data = b.xpath("//node[@text='立即运行']")[0]
print(data.attrib.get("bounds"))
