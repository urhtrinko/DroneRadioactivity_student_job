import npyscreen

class FormObject( npyscreen.Form ):
    def create( self ):
        self.add( npyscreen.TitleText, name = "First Name:", value = "Maj" )

    def afterEditing( self ):
        self.parentApp.setNextForm( None )

class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm( 'MAIN', FormObject, name = "npyscreen Form" )        

if ( __name__ == "__main__" ):
    app = App().run()
