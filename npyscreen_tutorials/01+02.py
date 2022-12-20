import npyscreen

def myFunction(*args):
    F = npyscreen.Form(name='My Test Application')
    myFW = F.add(npyscreen.TitleText, name="First Widget")   # <------- Change 1
    F.edit()
    return myFW.value   # <------- Change 2

if __name__ == '__main__':
    print(npyscreen.wrapper_basic(myFunction)) # <---- and change 3