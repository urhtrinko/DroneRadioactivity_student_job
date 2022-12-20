import npyscreen

class FormObject( npyscreen.Form ):
    def create( self ):
        # self.show_atx = 20
        # self.show_aty = 2
        self.add( npyscreen.TitleText, name = "First Name:")
        # self.nextrely = 1
        self.add( npyscreen.TitleText, name = "Last Name:")


    def afterEditing( self ):
        self.parentApp.setNextForm( None )

class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm( 'MAIN', FormObject, name = "npyscreen Form", lines=10, columns = 40)

if ( __name__ == "__main__" ):
    app = App().run()
