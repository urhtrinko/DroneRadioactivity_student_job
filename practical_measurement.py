import npyscreen
import numpy as np

# Preperation for when we will test the code in a practical example
# for this we will use the ZIG-ZAG method

# SHARED PARAMETERS (USED IN BOTH ZIG-ZAG AND RANDOM FLYOVER)
A_min = 1e3; A_max = 1.5e3 # borders between which the activity of the source is randomly selected 
A_b = 5e-5 # background activity in Bq
h = 40 # hight at which the detector flies over in m
x_max = 100 # Size of the area of flyover in positive x direction in m (the whole grid extends also in the negative direction the same amount)
y_max = 100 # Size of the area of flyover in positive y direction in m (the whole grid extends also in the negative direction the same amount)
dt = 10 # the pause on each point od the grid in s
noise = [5, 5] # list that contains the standard deviation of the x and y coordinates in in m
# K = 0.8 # constant between 0 and 1 which contains the information on the quality of the detector, a better detector has a smaller constante 
        # then then an inferior detector
# F = 0.140 # factor for inhilation of Pu-239 in mSV/Bq


# ZIG_ZAG PARAMETERS
grid = 4 # Size of the grid in which the area of flyover is divided into smaller "tiles" where the detector stops and measures the number of 
         # radioactive decays. Grid is the number of these areas in x direction and y direction. It must be an INTEGER!

# We have to manually fill this dictionary
# {"m_dose": HDs, "dm_dose": dHDs, "source": source, "grid_x": grid_x, "grid_y": grid_y, "grid_x_noise": grid_x_noise, "grid_y_noise": grid_y_noise, "hotspot": maxI_range, "square_x": square_x, "square_y": square_y, "x_max": x_max, "y_max": y_max}

radiation = {'A_min': A_min, 'A_max': A_max, 'A_b': A_b}#, 'dose_factor': F}
detector = {"h": h, "dt": dt, "x_max": x_max, "y_max": y_max, "grid": grid}#, "detector_constant": K, "n_points": n_points, "max_phi": max_phi, "spiral_grid": s_grid} # the detector constant tells us the quality of the detector

##CLASS

class FormObject( npyscreen.ActionForm ): # Action -> Cancel/OK
    def create( self ):
        A_b = radiation['A_b']
        h = detector['h']; dt = detector['dt']; x_max = detector['x_max']; y_max = detector['y_max']; N_grid = detector['grid']

        square_x = (2*x_max)/N_grid; square_y = (2*y_max)/N_grid

        grid_x, grid_y = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
        grid_x_noise, grid_y_noise = np.zeros((N_grid, N_grid)), np.zeros((N_grid, N_grid))
        xs = np.linspace(-x_max + square_x/2, x_max - square_x/2, int(N_grid))
        HDs = np.zeros((int(N_grid), int(N_grid))); dHDs = np.zeros((int(N_grid), int(N_grid)))

        n, m = N_grid - 1, 0
        y = -y_max + square_y/2
        i = 1
        for x in xs:
            while abs(y) <= y_max:

                HD_str = "Enter HD for" + " (" + str(round(x, 2)) + ", " + str(round(y, 2)) + "):"
                begin_HD = len(HD_str)
                self.HD = self.add( npyscreen.TitleText, name = HD_str, begin_entry_at = begin_HD+1, use_two_lines = False)
                
                dHD_str = "Enter dHD for" + " (" + str(round(x, 2)) + ", " + str(round(y, 2)) + "):"
                begin_dHD = len(dHD_str)
                self.dHD = self.add( npyscreen.TitleText, name = dHD_str, relx=3, begin_entry_at = begin_dHD+1, use_two_lines = False)

                self.nextrely += 1
                grid_x[n, m] = x; grid_y[n, m] = y
                y += (square_y)*i
                n -= 1*i
            n += 1*i; i = i * (-1); y += (square_y)*i; m += 1


    def __str__(self):
        return self

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
        self.addForm( 'MAIN', FormObject, name = "npyscreen Form", lines=60)#, columns = 80)

if ( __name__ == "__main__" ):
    app = App().run()
