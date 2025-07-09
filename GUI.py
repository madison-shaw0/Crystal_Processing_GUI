from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QFileDialog, QPushButton, QLineEdit, QLabel, QTabWidget, QCheckBox
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from pathlib import Path
from Main import Main


class GraphsTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QGridLayout()
        #adding elements to Graphs tab

        #creating checkboxes for different graph options
        self.area_checkbox = QCheckBox(text="Area Graph")
        self.perimeter_checkbox = QCheckBox(text="Perimeter Graph")
        self.AR_checkbox = QCheckBox(text="Aspect Ratio Graph")
        self.area_checkbox.stateChanged.connect(self.area_graph_selected)
        self.image_outline_checkbox = QCheckBox(text = "Image Outline")

        #save button
        self.save_btn = QPushButton("Save Images")
        self.save_btn.clicked.connect(self.save_images)

        #adding to graphs layout
        layout.addWidget(QLabel("Select Save Filepath:"), 0, 0)
        layout.addWidget(QLabel("Select graphs:"), 2, 0)
        layout.addWidget(self.area_checkbox, 3, 0)
        layout.addWidget(self.perimeter_checkbox, 4, 0)
        layout.addWidget(self.AR_checkbox, 5, 0)
        layout.addWidget(self.image_outline_checkbox, 6, 0)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def area_graph_selected(self): #base GUI design off main class -> list of available graphs. one func for all
        if self.area_checkbox.isChecked():
            print("area graph")
        else:
            print("no area graph")


    def save_images(self):
        print("Saved Images")   


class MainTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Adding elements to Main tab
        self.layout = QGridLayout()

        #make file browser button for JSON Annotations
        file_browser_btn = QPushButton ("Browse")
        self.filename_edit = QLineEdit()
        file_browser_btn.clicked.connect(lambda: self.open_file_dialog(self.filename_edit))
    

        #make file browser button for Save Filepath
        file_save_btn = QPushButton("Browse")
        self.save_filename_edit = QLineEdit()
        file_save_btn.clicked.connect(lambda: self.open_file_dialog(self.save_filename_edit))


        #make Load JSON button
        json_load_btn = QPushButton ("Load JSONs")
        json_load_btn.clicked.connect(self.load_files)


        #adding buttons to main tab grid layout
        self.layout.addWidget(QLabel('JSON Annotations File:'), 0, 0)
        self.layout.addWidget(self.filename_edit, 0, 1)
        self.layout.addWidget(file_browser_btn, 0, 2)

        self.layout.addWidget(QLabel('Scales JSON File:'), 1, 0)
        self.layout.addWidget(self.save_filename_edit, 1, 1)
        self.layout.addWidget(file_save_btn, 1, 2)

        self.layout.addWidget(json_load_btn, 2, 0)

        self.layout.addWidget(QLabel('Scales'), 3, 0)
        #layout.addWidget(QLabel("NA165_139"), 4, 0)
        #layout.addWidget(QLineEdit("2.97"), 4, 1)  #example for now

        self.setLayout(self.layout)

    def open_file_dialog(self, target_line_edit):
        filename, x = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "JSON (*.json)"
        )
        if filename:
            path = Path(filename)
            target_line_edit.setText(str(path))


    #update Main class variable with paths
    def load_files(self):
        json_path = self.filename_edit.text()
        scales_path = self.save_filename_edit.text()

        print(json_path, " ", scales_path)

        if json_path and scales_path:
            self.parent.main_obj = Main(json_path, scales_path)
            print ("Main object created and stored")

        
        self.update_scales()

    #updates scales and values based on JSON files
    def update_scales(self):
        i = 4
        for key, value in self.parent.main_obj.scales_dict.items():
            self.layout.addWidget(QLabel(key), i, 0)
            self.layout.addWidget(QLineEdit(str(value)), i, 1)
            i+=1


    def save_scale_values(self):
        print()
        #end: should save new scales to dictionary in main class


class InfoTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        #adding elements to Info tab
        #self.info.layout=QGridLayout()
        #series = QPieSeries
        

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        #json_filepath = "C:/Users/madis/annotations_test.json"
        #scales_filepath = "C:/Users/madis/scales.json"
        #test
        self.main_obj = None

        self.setWindowTitle("Crystal Processing GUI")
        self.resize(1000,600)

        layout = QGridLayout()
        self.tabs = QTabWidget()

        #adding tabs to MainWindow
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.addTab(MainTab(self), "Main")
        self.tabs.addTab(GraphsTab(self), "Graphs")
        self.tabs.addTab(InfoTab(self), "Image Info")
    


        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.show()



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    #exit out of window
    app.exec()


#notes: fix spacing for scales so it stands out from filepath
#       add save filepath for images, allow user to make new folder if needed
#       connect to main class


#always show crystal area fraction and proportion of crystal to each other, # of crystals, point counts 
#crystal area fraction : total area of crystal/total area of image (total area of image found in image youre creating)
    # sum of all areas from JSON (separately!!) /width and height from outline func
    # should have three values & mult by 100 to get %
    # pie chart of 3 crystals (counts) just in gui ^^


'''
TO DO:
- [DONE] Organize Tabs
- Populate scales section with JSON values
- Allow user to write scales next to image names -> save and write to scales file
- Connect button click events with Main functions (should run after "save images" button pressed)
- Make new tab that has drop down menu -> calls crystal area frac func & show pie chart

- Crystal area fraction function (Main)
- Pie chart of crystal counts function (Main)
- Circularity Function (Main)
- Solidity Function (Main)
- Aspect Ratio Function (Main) -> is this different from Major vs minor axis
- Elongation Function (Main)

- Change initial window size
- fix spacing


- Streamline ability to add functions/checkboxes later on???

'''
