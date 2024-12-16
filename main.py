from analyse import analyse_src

content = open("./src.func", "r").read()
print("\n".join([str(x) for x in analyse_src(content)]))
