import os
from PIL import Image, ImageDraw
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math
import json
import cv2

class Main:

    def __init__(self, json_path, scales_path):
        #Opens JSON annotation file
        with open(json_path, 'r') as file:
            self.data = json.load(file)
        self.point_dict = {}

        #opens scales JSON file -> in format "Image_Name": number
        with open(scales_path, "r+") as f:
            self.scales_dict = json.load(f)

        self.colors = {
                "Pyroxene" : "cyan",
                "Olivine" : "dodgerblue",
                "Feldspar" : "magenta"
        }

        #image width and height
        self.width, self.height = 1920, 1200

        #populates point_dict
        for key in self.data.keys():
            point_list = []
            for i in range(len(self.data[key])):        
                point_list.append((self.data[key][i]["points"], self.data[key][i]["label_short_code"], self.data[key][i]["perimeter"], self.data[key][i]["area"]))
            
            #37-46 index for sample
            #48-54 index for image #
            self.point_dict[key[38:47] + "_" + key[48:54]] = point_list



#Making outlines from JSON
    def make_outlines(self, filesave_path):
        
        label = {'Pyroxene': 100, 'Olivine': 0, 'Feldspar': 200}
        for key in self.point_dict.keys(): 
            image = Image.new("L", (self.width, self.height), color=255)  
            draw = ImageDraw.Draw(image)
            for entry in self.point_dict[key]:
                vertices = entry[0]
                polygon = [(int(x), int(y)) for x, y in vertices]
                gray = label[entry[1]]
                draw.polygon(polygon, fill=gray, outline=0)  

            image.save(os.path.join(filesave_path, f"{key}_outline.png"))



#Creating Area Histogram - One image with 3 separate histograms for each crystal
    def make_area_hist(self, filesave_path):
        for key in self.point_dict.keys():

            areas_by_label = {
                "Pyroxene" : [],
                "Olivine" : [],
                "Feldspar" : []
            }

            #dictionary with each crystal having list of areas from image
            for entry in self.point_dict[key]:
                areas_by_label[entry[1]].append(entry[3])
            
            fig, axs = plt.subplots (1, 3, figsize = (18, 5), sharey=True)

            for ax, (label, areas) in zip(axs, areas_by_label.items()):
                ax.hist(areas, bins = 10, color = self.colors[label])
                ax.set_title(label)
                ax.set_xlabel("Area")
                ax.set_ylabel("Frequency")
                ax.grid(True)

            fig.suptitle(f"Area Distribution by Crystal - {key}")

            plt.savefig(os.path.join(filesave_path, f"{key}_area_graph.png"))



#Creating Perimeter Histogram - One image with 3 separate histograms for each crystal
    def make_perimeter_hist(self, filesave_path):
        for key in self.point_dict.keys():

            perimeters_by_label = {
                "Pyroxene" : [],
                "Olivine" : [],
                "Feldspar" : []
            }

            #dictionary with each crystal having list of perimeters from image
            for entry in self.point_dict[key]:
                perimeters_by_label[entry[1]].append(entry[2])
            
            fig, axs = plt.subplots (1, 3, figsize = (18, 5), sharey=True)

            for ax, (label, perimeters) in zip(axs, perimeters_by_label.items()):
                ax.hist(perimeters, bins = 10, color = self.colors[label])
                ax.set_title(label)
                ax.set_xlabel("Perimeter")
                ax.set_ylabel("Frequency")
                ax.grid(True)

            fig.suptitle(f"Perimeter Distribution by Crystal - {key}")

            plt.savefig(os.path.join(filesave_path, f"{key}_perimeter_graph.png"))


#fitting ellipses around annotations
#Open cv limitation >5 points to make an elliipse. section in graph that say able to ellipse XX/XX total annotations

    def make_ellipse_scatter(self, filesave_path):
        for key in self.point_dict.keys():

            ellipses_by_label = {
                "Olivine" : {
                    "major_axis_list": [],
                    "minor_axis_list": []
                }, 
                "Feldspar": {
                    "major_axis_list": [],
                    "minor_axis_list": []
                },
                "Pyroxene": {
                    "major_axis_list": [],
                    "minor_axis_list": []
                }, 
            }
            

            for entry in self.point_dict[key]:
                pts = np.array (entry[0], dtype = np.float32)

                if len(pts) >= 5:
                    ellipse = cv2.fitEllipse(pts)

                    axes= ellipse[1]
                    ellipses_by_label[entry[1]]["major_axis_list"].append(max(axes))
                    ellipses_by_label[entry[1]]["minor_axis_list"].append(min(axes))

            
            fig, axs = plt.subplots (1, 3, figsize = (18, 5), sharey=True)

            for ax, (label, axes) in zip(axs, ellipses_by_label.items()):
                ax.scatter(axes["major_axis_list"], axes["minor_axis_list"], color = self.colors[label])
                ax.set_title(label)
                ax.set_xlabel("Major Axis")
                ax.set_ylabel("Minor Axis")
                ax.grid(True)

                slopes = [0.2, 0.4, 0.8, 1.0, 1.5, 2]
                x_min, x_max = ax.get_xlim()
                x_vals = np.linspace(x_min, x_max, 100)

                for slope in slopes:
                    y_vals = slope * x_vals
                    ax.plot(x_vals, y_vals, linestyle='--', linewidth=1, label=f"AR = {slope}")
                ax.legend()
                


            fig.suptitle(f"AR - {key}")

            plt.savefig(os.path.join(filesave_path, f"{key}_axes_graph.png"))
                    
    
    def calculate_crystal_area_frac(self):
        image_area = self.width * self.height
        #add calculation :), return dict
            

test = Main("C:/Users/madis/annotations_test.json", "C:/Users/madis/scales.txt")
#test.make_perimeter_hist("C:/Users/madis/image_outlines")