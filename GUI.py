from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QGridLayout, QWidget, QFileDialog, QPushButton, QLineEdit, QLabel, QTabWidget, QCheckBox
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QColor, QFont
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
        self.image_outline_checkbox = QCheckBox(text = "Image Outline")

        #save button
        self.save_btn = QPushButton("Save Images")
        self.save_btn.setStyleSheet("background-color : #75BFEC")
        self.save_btn.clicked.connect(self.save_images)

        #folder path
        self.folder_path = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(lambda: self.pick_folder(self.folder_path))


        #adding to graphs layout
        layout.addWidget(QLabel("Select Save Folder:"), 0, 0)
        layout.addWidget(self.folder_path, 0, 1)
        layout.addWidget(self.browse_btn, 0, 3)

        select_graphs_label = QLabel("Select graphs:")
        select_graphs_label.setStyleSheet("font-size: 11pt; font-weight:bold;")
        layout.addWidget(select_graphs_label, 2, 0)

        layout.addWidget(self.area_checkbox, 3, 0)
        layout.addWidget(self.perimeter_checkbox, 4, 0)
        layout.addWidget(self.AR_checkbox, 5, 0)
        layout.addWidget(self.image_outline_checkbox, 6, 0)
        layout.addWidget(self.save_btn, 7, 1)

        layout.setRowStretch(8, 1)

        self.setLayout(layout)


    def pick_folder(self, target_line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder:
            path = Path(folder)
            target_line_edit.setText(str(path))

    #When save images button clicked -> if any of these are checked, runs Main class functions that create + save graphs
    def save_images(self):
        save_folder_path = self.folder_path.text()

        if self.area_checkbox.isChecked():
            self.parent.main_obj.make_area_hist(save_folder_path)
            print("Saved area graph")

        if self.perimeter_checkbox.isChecked():
            self.parent.main_obj.make_perimeter_hist(save_folder_path)
            print("Saved perimeter graph")

        if self.AR_checkbox.isChecked():
            self.parent.main_obj.make_ellipse_scatter(save_folder_path)
            print("Saved AR graphs")
        if self.image_outline_checkbox.isChecked():
            self.parent.main_obj.make_outlines(save_folder_path)
            print("Saved outline images")   


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
        json_load_btn.setStyleSheet("background-color : #75BFEC")
        json_load_btn.clicked.connect(self.load_files)

        # make Save Changes button
        save_changes_btn = QPushButton("Save Changes")
        save_changes_btn.setStyleSheet("background-color : #75BFEC")
        save_changes_btn.clicked.connect(self.save_scale_values)


        #adding buttons to main tab grid layout
        self.layout.addWidget(QLabel('JSON Annotations File:'), 0, 0)
        self.layout.addWidget(self.filename_edit, 0, 1)
        self.layout.addWidget(file_browser_btn, 0, 2)

        self.layout.addWidget(QLabel('Scales JSON File:'), 1, 0)
        self.layout.addWidget(self.save_filename_edit, 1, 1)
        self.layout.addWidget(file_save_btn, 1, 2)

        self.layout.addWidget(json_load_btn, 2, 1)

        scales_label = QLabel("Scales")
        scales_label.setStyleSheet("font-size: 11pt; font-weight:bold;")
        self.layout.addWidget(scales_label, 3, 0)
        self.layout.addWidget(save_changes_btn, 3, 2)

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
        
        self.load_scales()
        self.parent.info_tab.update_info()



    #loads scales and values based on JSON files
    def load_scales(self):
        i = 4

        for key in self.parent.main_obj.point_dict.keys():
            self.layout.addWidget(QLabel(key), i, 0)
            header = (key[0:9])

            #if group of images (ex. NA165-136) is already in scales.json, populates box with value
            if header in self.parent.main_obj.scales_dict.keys():
                self.layout.addWidget(QLineEdit(str(self.parent.main_obj.scales_dict[header])), i, 1)
            else:
                self.layout.addWidget(QLineEdit(), i, 1)

            i+=1


    def save_scale_values(self):
        print()
        #end: should save new scales to dictionary in main class


class InfoTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout=QGridLayout()
        self.setLayout(self.layout)

        self.image_selector = QComboBox()
        self.image_selector.addItem(" ")
        self.image_selector.currentTextChanged.connect(lambda: self.display_graphs(self.image_selector.currentText()))
        
        self.layout.addWidget(QLabel("Select Image: "), 0, 0)
        self.layout.addWidget(self.image_selector, 0, 1)


    def update_info(self):
        if not self.parent.main_obj:
            print ("Please Load JSON files first")
            return
        
        image_names = self.parent.main_obj.point_dict.keys()
        self.image_selector.addItems(image_names)
        
    def display_graphs(self, img_name):
        """ for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget and self.layout.getItemPosition(i)[0] != 0:  # keep row 0 (dropdown + label)
                widget.setParent(None) """


        self.create_pie_chart(img_name)
        self.get_crystal_area_percent(img_name)

    def create_pie_chart(self, img_name):
        if not self.parent.main_obj:
            print ("Please Load JSON files first")
            return
        
        self.crystal_count_dict = self.parent.main_obj.get_crystal_counts()
        

        series = QPieSeries()
        counts = self.crystal_count_dict[img_name]

        color_map = {
                "Pyroxene" : QColor("#00FFFF"),
                "Olivine" : QColor("#1e90ff"),
                "Feldspar" : QColor("#FF00FF"),
                "Vesicles" : QColor("#0AC90A")
        }

        i = 0
        for key, value in counts.items():
            slice = series.append(key, value)
            slice.setBrush(color_map[key])

            self.layout.addWidget(QLabel(f"{key}: {value}"), 2, i)
            i+=1

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle(f"Crystal Counts Pie Chart: {img_name}")

        chartview = QChartView(chart)
        self.layout.addWidget(chartview, 0, 0)

        self.get_crystal_area_percent(img_name)



    def get_crystal_area_percent(self, img_name):
        if not self.parent.main_obj:
            print ("Please Load JSON files first")
            return
        
        self.crystal_areas = self.parent.main_obj.get_crystal_area_percent()

        self.layout.addWidget(QLabel("Crystal Area Percentages: "), 3, 0)
        i = 4
        for key, value in self.crystal_areas[img_name].items():
            self.layout.addWidget(QLabel(key), i, 0)
            self.layout.addWidget(QLabel(str(f"{value:.2f}%")), i, 1)
            i+=1
        
        

        

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.main_obj = None

        self.setWindowTitle("Crystal Processing GUI")
        self.resize(1000,600)

        layout = QGridLayout()
        self.tabs = QTabWidget()

        self.main_tab = MainTab(self)
        self.graphs_tab = GraphsTab(self)
        self.info_tab = InfoTab(self)
        
        #adding tabs to MainWindow
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.graphs_tab, "Graphs")
        self.tabs.addTab(self.info_tab, "Image Info")
    


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
- [DONE] Populate scales section with JSON values
- Allow user to write scales next to image names -> save and write to scales file
- [DONE] Connect button click events with Main functions (should run after "save images" button pressed)
- Make new tab that has drop down menu -> calls crystal area frac func & show pie chart

- Crystal area fraction function (Main)
- [DONE] Pie chart of crystal counts function (Main)
- Get Pie Chart to show numbers and label
- Circularity Function (Main)
- Solidity Function (Main)
- Aspect Ratio Function (Main) -> is this different from Major vs minor axis
- Elongation Function (Main)

- [Change initial window size
- fix spacing


- Streamline ability to add functions/checkboxes later on???

'''


'''
Questions:
Will all images in image group (ex. NA165-136) have the same scaling? Otherwise, in scales.json, would have to do them all individually.
Would it be easier to have all checkboxes in graphs tab start checked?
'''
