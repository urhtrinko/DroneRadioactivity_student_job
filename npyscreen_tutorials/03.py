import npyscreen

class FormObject( npyscreen.Form ):
    def create( self ):

        pass


class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm( 'MAIN', FormObject, name = "npyscreen Form" )

if ( __name__ == "__main__" ):
    app = App().run()
