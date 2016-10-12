
import xml.dom.minidom as MD


# XML Helpers #################################################################

def make_doc():
    return MD.Document()

def make_node(doc, tag, attrs={}, children=[]):
    node = doc.createElement(tag)

    for key in attrs:
        node.setAttribute(key, str(attrs[key]))

    for child in children:
        node.childNodes.append(child)

    return node

def simple_node(doc, tag, txt):
    return make_node(doc, tag, {}, [ doc.createTextNode(str(txt)) ])
