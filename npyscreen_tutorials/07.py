import npyscreen

class FormObject( npyscreen.ActionForm ): # Action -> Cancel/OK
    def create( self ):
        # self.show_atx = 20
        # self.show_aty = 2
        self.fname = self.add( npyscreen.TitleText, name = "First Name:")
        # self.nextrely = 1
        self.lname = self.add( npyscreen.TitleText, name = "Last Name:")

    def afterEditing( self ):
        self.parentApp.setNextForm( None )

    def on_ok(self):
        # self.fname.value = "OK button was pressed."
        pass
        # OK button pressed.

    def on_cancel(self):
        # self.lname.value = "Cancel button was pressed." 
        pass
        # Cancel button pressed.

class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm( 'MAIN', FormObject, name = "npyscreen Form", lines=10, columns = 40)

if ( __name__ == "__main__" ):
    app = App().run()
