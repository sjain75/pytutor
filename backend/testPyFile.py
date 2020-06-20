def a():
    print("A")
def b():
    print("B")
    a()

print("C")
a()
b()