x=7
y=x
print(y+1, id(y));print(x, id(x))





user="123"
paswd="pass"
if user=="123" and paswd=="pass":
    print("authenticated")


damn=id(user)
meh=id(paswd)

if damn=id(user) and meh=id(paswd):
    print("authenticated")

