


# ---------------------------------------------------
# MetaSubclassRegister
# ---------------------------------------------------

class MetaSubclassRegister(type):

    def __new__(mcs, name, bases, fields):
        cls = super().__new__(mcs, name, bases, fields)
        for base in bases:
            register_subclass = getattr(base, '_register_subclass', None)
            if not register_subclass or register_subclass.__class__ == cls: continue
            register_subclass(cls)
        return cls

