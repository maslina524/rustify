# class Test:
#     def __format__(self, formatter):
#         return formatter

# p = Test()    
# print(f"{p}") # ` ` -> {:?}
# print(f"{p:#}") # `#` -> {:#?}

class Debug:
    @staticmethod
    def format(obj, f, indent=0):
        if f == "":
            attrs = ', '.join(f"{k}: {v!r}" for k, v in obj.__dict__.items())
            return f"{obj.__class__.__name__} {{ {attrs} }}"

        elif f == "#":
            indent_str = ' ' * (indent * 4)
            next_indent = indent + 1
            items = list(obj.__dict__.items())
            lines = []

            for i, (k, v) in enumerate(items):
                formatted_value = Debug._format_value(v, next_indent)
                comma = ',' if i < len(items) - 1 else ''   # запятая после всех, кроме последнего
                lines.append(f"{indent_str}    {k}: {formatted_value}{comma}")

            body = '\n'.join(lines)
            return f"{obj.__class__.__name__} {{\n{body}\n{indent_str}}}"

    @staticmethod
    def _format_value(val, indent):
        if isinstance(val, (type(None), str, int, float, bool, list, dict, tuple, set)):
            return repr(val)

        if hasattr(val, '__dict__'):
            return Debug.format(val, "#", indent)

        return repr(val)

def derive(*traits):
    def decorator(cls):
        if Debug in traits:
            def __format__(self, f):
                return Debug.format(self, f)
            cls.__format__ = __format__

            def __repr__(self):
                return cls.__format__(self, "")
            cls.__repr__ = __repr__
            
        return cls
    return decorator 