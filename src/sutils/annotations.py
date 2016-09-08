

from .primitives import qdict

# ---------------------------------------------------
# Annotation
# ---------------------------------------------------

class Annotation(object):

    def __init__(self, base_field):
        self.base_field = base_field


    def set(self, obj, path, value ):
        if not isinstance(path, list):
            path = list(path)
        path.append(self.base_field)
        node = obj
        print "\n\n set", "-"*50, obj, path, value
        while path:
            key = path.pop()
            print "---->", key, node
            if len(path) == 0:
                setattr(node,key,value)
                return node
            if not hasattr(node,key):
                setattr(node,key,qdict())
            node = getattr(node,key)


    def get(self, obj, path, default = None):
        if not isinstance(path, list):
            path = list(path)
        path.append(self.base_field)
        node = obj
        print "\n\n get", "-"*50, obj, path, default
        while path:
            key = path.pop()
            print "---->", key, node
            if not hasattr(node,key):
                if len(path) == 0:
                    setattr(node,key,default)
                else:
                    setattr(node,key,qdict())
            node = getattr(node,key)
        return node


    def append(self, obj, path, value):
        annotation = self.get(obj, path, [] )
        annotation.append(value)
        return annotation


