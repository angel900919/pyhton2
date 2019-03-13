# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Program Files (x86)\Python37-32\Project\Fcas\FCAS2.ui',
# licensing of 'C:\Program Files (x86)\Python37-32\Project\Fcas\FCAS2.ui' applies.
#
# Created: Tue Mar 12 10:39:32 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

import matplotlib.pyplot as plt
import csv
import pandas as pd
import shutil
from PySide2 import QtCore, QtGui, QtWidgets
import os


class Ui_Form(object):


    #Global vars
    path_deviceName = ''
    path_DataRecord = ''
    dirs1 = ''
    selected_directory = ''  # global variable
    destination_folder = ''
    start_time = ''
    end_time = ''
    dataTypeAux = ''
    DeviceNameAux = ''
    RecordPath = ''
     # Data to be copied in new folder
    TSS_Data = []
    CSS_Data = []  # data to be copied in new folder
    TSS_Data_File = ""
    Data_To_Plot = ""
    path_Fcas_Files = ""
    head = ''
    tail = ''

    newcsv = []
    newcsv2 = []



    def update_parameters(self):

        self.Processing()



    def Processing(self):

        self.start_time = self.StartDate_2.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.end_time = self.endDate.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.dataTypeAux = self.comboBox_DataType.currentText()
        self.DeviceNameAux = self.comboBox_DeviceName.currentText()
        self.RecordPath = self.path_DataRecord + self.DeviceNameAux + "\\" + self.dataTypeAux

        if (self.end_time < self.start_time):
            QtWidgets.QMessageBox.information(None, "Info", "Incorrect time Interval")  # pop up window
            return

        else:
            self.head, self.tail = os.path.split(self.RecordPath) #To determine if TSS or CSS

            ###$################TSS###################################################################################
            if self.tail == 'tss':
                self.TSS_Data = []
                tss_var = 22  # the trigger time length is 22 positions 2018_10_15_04_52_15.csv

                index = 0
                listdata = os.listdir(self.RecordPath)

                for records in os.listdir(self.RecordPath):
                    stringlenght = len(records) - 1  # string start form 0
                    records = records[stringlenght - tss_var:stringlenght - 3]  # 3 = to eliminate .csv
                    str1 = records[0:10].replace('_', '-')
                    str2 = records[11:len(records)].replace('_', ':')
                    listdata[index] = str1 + ' ' + str2
                    index = index + 1

                lisdataindex = []
                position = 0

                for comparedate in listdata:
                    if comparedate >= self.start_time and comparedate <= self.end_time:
                        lisdataindex.append(position)
                    position = position + 1

                fulldatatss = os.listdir(self.RecordPath)

                for dataAux in lisdataindex:
                    self.TSS_Data.append(fulldatatss[dataAux])  # list of data to be copied


                index = 0
                self.comboBox_TSS_file.clear()
                for fileData in self.TSS_Data:
                    if index <= 10:
                        self.comboBox_TSS_file.addItem(fileData)
                        index = index + 1
                    else: break

            ############################### CSS ############################################################################

            elif self.tail == 'css':

                self.CSS_Data = []  # restart the variable
                css_var = 13  # start date

                index = 0
                listdata2 = os.listdir(self.RecordPath)

                for records in os.listdir(self.RecordPath):
                    stringlenght = len(records) - 1  # string start form 0
                    records = records[stringlenght - css_var:stringlenght - 3]  # 3 = to eliminate .csv
                    listdata2[index] = records.replace('_', '-')  # + ' 00:00:00'
                    index = index + 1

                lisdataindex = []
                position = 0

                for comparedate in listdata2:
                    if comparedate >= self.StartDate_2.date().toString(
                            'yyyy-MM-dd') and comparedate <= self.endDate.date().toString('yyyy-MM-dd'):
                        lisdataindex.append(position)
                    print(comparedate)
                    print(self.start_time)
                    print(self.end_time)

                    position = position + 1

                fulldatatss = os.listdir(self.RecordPath)
                # print(listdata2)

                for dataAux in lisdataindex:
                    self.CSS_Data.append(fulldatatss[dataAux])  # list of data to be copied

                if len(self.CSS_Data) > 0 and len(self.CSS_Data) <= 2:

                    self.splitMergeCSV()

                elif self.CSS_Data==1:
                    self.splitFile() # split file if required

                if len(self.CSS_Data) > 2:
                    QtWidgets.QMessageBox.information(None, "Info", "No more than 2 days is allowed")  # pop up window


                else:
                    QtWidgets.QMessageBox.information(None, "Info", "No Data for selected Time")  # pop up window



    def splitMergeCSV(self):


            with open(self.RecordPath + '/' + self.CSS_Data[0], newline='') as csvDataFile:
                data1 = list(csv.reader(csvDataFile))
            with open(self.RecordPath + '/' + self.CSS_Data[1], newline='') as csvDataFile:
                data2 = list(csv.reader(csvDataFile))

            end_time = self.endDate.time().toString('hh:mm:ss')
            start_time = self.StartDate_2.time().toString('hh:mm:ss')

            self.newcsv2 = []
            self.newcsv2 = data1[0:7] # header of the file

            for date_string in data1[7:]:
                if date_string[1] >= start_time:
                    self.newcsv2.append(date_string)

            for date_string2 in data2[7:]:
                if date_string2[1] <= end_time:
                    self.newcsv2.append(date_string2)

            indexList = []
            indexCount = 1
            maxVal = len(self.newcsv2[7:])
            for index in self.newcsv2:
                if (maxVal)
                len(self.newcsv2[7:])
                indexList.append(self.newcsv2)



            TemCsvFile = open("TempFolder/Temp2.csv", "w")
            TemCsvFile.close()

            with open("TempFolder/Temp2.csv", 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerows(self.newcsv2)




    def splitFile(self):



            with open(self.RecordPath + '/' + self.CSS_Data[0], newline='') as csvDataFile:
                data = list(csv.reader(csvDataFile))

            end_time = self.endDate.time().toString('hh:mm:ss')
            start_time = self.StartDate_2.time().toString('hh:mm:ss')

            self.newcsv = []
            self.newcsv = data[0:7] # header of the file


            for date_string in data[7:]:
                if date_string[1] >= start_time and date_string[1] <= end_time:
                    self.newcsv.append(date_string)


            TemCsvFile = open("TempFolder/Temp.csv", "w")
            TemCsvFile.close()

            with open("TempFolder/Temp.csv", 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerows(self.newcsv)


    def update_TSS_DATA(self):
        self.TSS_Data_File = self.comboBox_TSS_file.currentText()
        self.Data_To_Plot = self.TSS_Data_File
        print(self.TSS_Data_File)



    def loginCheck(self):
        if ((self.selected_directory != '') and (self.destination_folder != '')):

            error_var = 0
        ##########################TSS#####################################
            if self.tail == 'tss':
                destinationfoldaer = self.destination_folder
                for file_name in self.TSS_Data:
                    full_file_name = os.path.join(self.RecordPath, file_name)
                    if (os.path.isfile(full_file_name)):

                        try:
                            shutil.copy(full_file_name, destinationfoldaer)
                        except IOError as e:
                            QtWidgets.QMessageBox.information(None, "Info", "Unable to copy file. %s" % e)
                            error_var =1
                            break
                        except:
                            QtWidgets.QMessageBox.information(None, "Info", "Unexpected error:", sys.exc_info())
                            error_var = 1
                            break

                if(error_var == 0):
                    QtWidgets.QMessageBox.information(None, "Info", "Data Exported Correctly")  # pop up window

            ###########################CSS####################################
            elif self.tail == 'css':
                destinationfoldaer = self.destination_folder


                for file_name in self.CSS_Data:
                    full_file_name = os.path.join(self.RecordPath, file_name)
                    if (os.path.isfile(full_file_name)):
                        shutil.copy(full_file_name, destinationfoldaer)
                QtWidgets.QMessageBox.information(None, "Info", "Data Exported Correctly")  # pop up window
        else:
            QtWidgets.QMessageBox.information(None, "Info", "Incorrect Data selection")  # pop up window



    def plot_tss(self):

        if len(self.TSS_Data) > 0 and len(self.TSS_Data) < 2:
            #print(len(self.TSS_Data))
            self.plot_func()

        elif len(self.TSS_Data) > 1 and len(self.TSS_Data) <= 10:  # maximun 10 TSS recodrs can be viewed.
            #print(len(self.TSS_Data))
            self.plot_func()

        elif len(self.TSS_Data) > 10:
            QtWidgets.QMessageBox.information(None, "Info", "Too many TSS, reduce the time interval")  # pop up window
            self.plot_func()

        else:
            QtWidgets.QMessageBox.information(None, "Info", "NO TSS data for selected time")  # pop up window


    def plot_func(self):

        with open(self.RecordPath + '/' + self.Data_To_Plot, newline='') as csvDataFile:
            data = list(csv.reader(csvDataFile))

        header = data[6]
        header.pop(1)
        header.pop(0)

        dataAux = data
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)

        dataTemp = []

        for innerdata in dataAux:
            dataTemp.append(innerdata[1])


        df = pd.read_csv(self.RecordPath + '/' + self.Data_To_Plot, names=header, skiprows=7,
                         skip_blank_lines=True, error_bad_lines=False)

        df[header].plot()

        plt.show()



    def plot_css(self):

        data = self.newcsv

        header = data[6]
        header.pop(1)
        header.pop(0)

        dataAux = data
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)
        dataAux.pop(0)

        dataTemp = []

        for innerdata in dataAux:
            dataTemp.append(innerdata[1])




        df = pd.read_csv("TempFolder/Temp.csv", names=header, skiprows=7,skip_blank_lines=True, error_bad_lines=False)

        df[header].plot()

        plt.show()

        #plt.plot(self.newcsv)

        #plt.show()





    def plotFCAS(self):

        #self.Processing()
        if self.tail == 'tss':
            self.plot_tss()


        elif self.tail == 'css':
            self.plot_css()


    def update_options(self):

        self.comboBox_DataType.clear()
        deviceName = self.comboBox_DeviceName.currentText()
        dirs2 = os.listdir(self.path_DataRecord + deviceName)  # will print the data save in the device css or tss
        for fileData in dirs2:
            if fileData == 'css' or fileData == 'tss':
                self.comboBox_DataType.addItem(fileData)
                print('data selected')
            else:
                print('data incorrect')  #prevent to show others values but css and tss



    def selectDestinationFolder(self):

        self.destination_folder = QtWidgets.QFileDialog.getExistingDirectory()
        self.lineEdit_2.setText(self.destination_folder )  # show diredctory

        print('selected_directory:', self.destination_folder)



    def selectDirectory(self):

        self.selected_directory = QtWidgets.QFileDialog.getExistingDirectory()

        if self.selected_directory.find('ExportFolder') > 0:

            self.path_deviceName = self.selected_directory
            self.path_DataRecord = self.path_deviceName + "/"
            self.dirs1 = os.listdir(self.path_deviceName)

            self.comboBox_DeviceName.clear()
            self.comboBox_DataType.clear()

            for fileDevice in self.dirs1:
                self.comboBox_DeviceName.addItem(fileDevice)

            devicename = self.comboBox_DeviceName.currentText()
            dirs2 = os.listdir(self.path_DataRecord + devicename)  # will print the data save in the device css or tss

            for fileData in dirs2:
                if fileData == 'css' or fileData == 'tss':
                    self.comboBox_DataType.addItem(fileData)
                    print('data selected')
                else:
                    print('data incorrect')

            # This sentence will update the second drop-down menu.
            self.comboBox_DeviceName.currentIndexChanged.connect(self.update_options)

            self.lineEdit.setText(self.selected_directory) #show diredctory



        else:

            self.selected_directory=''
            self.comboBox_DeviceName.clear()
            self.comboBox_DataType.clear()
            QtWidgets.QMessageBox.information(None, "Info", "Incorrect Path Selection") #pop up window



    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(422, 313)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 160, 112))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DeviceName = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.DeviceName.setObjectName("DeviceName")
        self.verticalLayout.addWidget(self.DeviceName)
        self.comboBox_DeviceName = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_DeviceName.setObjectName("comboBox_DeviceName")
        self.verticalLayout.addWidget(self.comboBox_DeviceName)
        self.label_DataType = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_DataType.setObjectName("label_DataType")
        self.verticalLayout.addWidget(self.label_DataType)
        self.comboBox_DataType = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_DataType.setObjectName("comboBox_DataType")
        self.verticalLayout.addWidget(self.comboBox_DataType)
        self.comboBox_TSS_file = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_TSS_file.setMouseTracking(False)
        self.comboBox_TSS_file.setObjectName("comboBox_TSS_file")
        self.verticalLayout.addWidget(self.comboBox_TSS_file)
        self.comboBox_TSS_file.currentIndexChanged.connect(self.update_TSS_DATA)  # AR chaneg
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(220, 80, 181, 86))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.StartDate_Label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.StartDate_Label.setObjectName("StartDate_Label")
        self.verticalLayout_2.addWidget(self.StartDate_Label)
        self.StartDate_2 = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget_2)
        self.StartDate_2.setObjectName("StartDate_2")
        self.StartDate_2.setDateTime(QtCore.QDateTime.currentDateTime()) # AR


        self.StartDate_2.setCalendarPopup(True)  #### By AR to display the calendar
        self.verticalLayout_2.addWidget(self.StartDate_2)
        self.EndDate_Label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.EndDate_Label.setObjectName("EndDate_Label")
        self.verticalLayout_2.addWidget(self.EndDate_Label)
        self.endDate = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget_2)
        self.endDate.setObjectName("endDate")
        self.endDate.setDateTime(QtCore.QDateTime.currentDateTime()) #AR
        self.endDate.setCalendarPopup(True)  #### By AR to display the calendar
        self.verticalLayout_2.addWidget(self.endDate)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 210, 160, 83))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Save_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.Save_button.setObjectName("Save_button")
        self.verticalLayout_3.addWidget(self.Save_button)
        self.Save_button.clicked.connect(self.update_parameters)  #### By AR to display the calendar
        self.export_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.export_button.setObjectName("export_button")
        self.verticalLayout_3.addWidget(self.export_button)
        self.export_button.clicked.connect(self.loginCheck)  #### By AR to display the calendar
        self.plot_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.plot_button.setObjectName("plot_button")
        self.verticalLayout_3.addWidget(self.plot_button)
        self.plot_button.clicked.connect(self.plotFCAS)  #### By AR to display the calendar
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(220, 210, 186, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 0, 1, 1)
        self.toolButton_2 = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout.addWidget(self.toolButton_2, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.toolButton_2.clicked.connect(self.selectDestinationFolder)  # AR
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 391, 44))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolButton = QtWidgets.QToolButton(self.gridLayoutWidget_2)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_2.addWidget(self.toolButton, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.toolButton.clicked.connect(self.selectDirectory)  # AR
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setAcceptDrops(True)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.DeviceName.setText(QtWidgets.QApplication.translate("Form", "Device Name", None, -1))
        self.label_DataType.setText(QtWidgets.QApplication.translate("Form", "Data Type", None, -1))
        self.StartDate_Label.setText(QtWidgets.QApplication.translate("Form", "Start Date", None, -1))
        self.EndDate_Label.setText(QtWidgets.QApplication.translate("Form", "End Date", None, -1))
        self.Save_button.setText(QtWidgets.QApplication.translate("Form", "Save Changes", None, -1))
        self.export_button.setText(QtWidgets.QApplication.translate("Form", "Export Files", None, -1))
        self.plot_button.setText(QtWidgets.QApplication.translate("Form", "Plot", None, -1))
        self.toolButton_2.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "FCAS Destination Folder", None, -1))
        self.toolButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Select FCAS Folder", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.setWindowTitle("Fcas Data Management Tool")
    Form.setWindowIcon(QtGui.QIcon('insulectLogo.jpg'))
    Form.show()
    sys.exit(app.exec_())

