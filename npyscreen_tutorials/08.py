import npyscreen

class FormObject( npyscreen.ActionForm ): # Action -> Cancel/OK
    def create( self ):
        # self.show_atx = 20
        # self.show_aty = 2
        self.fname = self.add( npyscreen.TitleText, name = "First Name:")
        # self.nextrely = 1
        self.lname = self.add( npyscreen.TitleText, name = "Last Name:")

    def afterEditing( self ):
        # self.parentApp.setNextForm( None )
        pass

    def on_ok(self):
        npyscreen.notify_confirm("Form has been saved.", "Saved" , editw=1)
        self.parentApp.setNextForm(None)
        # pass
        # OK button pressed.

    def on_cancel(self):
        exiting = npyscreen.notify_yes_no("Are you sure want to Cancel?", "Cancel BUTTON", editw=1)
        if ( exiting ):
            npyscreen.notify_confirm("OK. Form has NOT been saved.", "Good bye!")
            self.parentApp.setNextForm(None)
        else:
            npyscreen.notify_confirm("You may continue working.", "Okay")


        # pass
        # Cancel button pressed.

class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm( 'MAIN', FormObject, name = "npyscreen Form", lines=10, columns = 40)

if ( __name__ == "__main__" ):
    app = App().run()

