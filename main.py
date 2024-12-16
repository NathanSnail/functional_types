from parser import parse_src

content = open("./src.func", "r").read()
print("\n".join([str(x) for x in parse_src(content)]))
