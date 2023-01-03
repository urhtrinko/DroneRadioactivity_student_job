#two forms

import npyscreen

class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm( 'MAIN', FormObject, name = "Form_1")#, lines=10, columns = 40)
        self.addForm( 'SECOND', FormObject02, name = "Form_2")


class FormObject( npyscreen.ActionForm ): # Action -> Cancel/OK
    def create( self ):
        # self.show_atx = 20
        # self.show_aty = 2
        self.fname = self.add( npyscreen.TitleText, name = "First Name:")
        # self.nextrely = 1
        self.lname = self.add( npyscreen.TitleText, name = "Last Name:")

    def afterEditing( self ):
        pass

    def on_ok(self):
        fname = self.fname.value
        lname = self.lname.value

        npyscreen.notify_confirm("Form has been saved.", "Saved" , editw=1)
        self.parentApp.switchForm('SECOND')
        
        print(fname)
        print(lname)

    def on_cancel(self):
        exiting = npyscreen.notify_yes_no("Are you sure want to Cancel?", "Cancel BUTTON", editw=1)
        if ( exiting ):
            npyscreen.notify_confirm("OK. Form has NOT been saved.", "Good bye!")
            self.parentApp.setNextForm(None)
        else:
            npyscreen.notify_confirm("You may continue working.", "Okay")

class FormObject02( npyscreen.ActionForm ): # Action -> Cancel/OK
    def create( self ):
        # self.show_atx = 20
        # self.show_aty = 2
        self.fname = self.add( npyscreen.TitleText, name = "First Name:")
        # self.nextrely = 1
        self.lname = self.add( npyscreen.TitleText, name = "Last Name:")

    def afterEditing( self ):
        pass

    def on_ok(self):
        fname = self.fname.value
        lname = self.lname.value

        npyscreen.notify_confirm("Form has been saved.", "Saved" , editw=1)
        self.parentApp.setNextForm(None)
        
        print(fname)
        print(lname)

    def on_cancel(self):
        exiting = npyscreen.notify_yes_no("Are you sure want to Cancel?", "Cancel BUTTON", editw=1)
        if ( exiting ):
            npyscreen.notify_confirm("OK. Form has NOT been saved.", "Good bye!")
            self.parentApp.setNextForm(None)
        else:
            npyscreen.notify_confirm("You may continue working.", "Okay")

if ( __name__ == "__main__" ):
    app = App().run()

