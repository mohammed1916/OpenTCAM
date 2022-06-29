from tabulate import tabulate
import numpy as np
import pandas as pd
import logging
import yaml
import json
import sys
import os

# ===========================================================================================
# ======================================= Begin Class =======================================
# ===========================================================================================

class TableMapping:
    # ----------------------------------------------------------------- Variables
    def __init__(self):
        # ------------------- public vars
        self.prjWorkDir                 = str()
        self.tcamTableConfigsFilePath   = str()
        self.tcamTableConfigsFileName   = str()
        self.tcamTableXlsxFilePath      = str()
        self.tcamTableXlsxFileName      = str()
        self.sramTableXlsxFilePath      = str()
        self.sramTableXlsxFileName      = str()
        # ------------------- protected vars
        self._tcamTableConfigs  = dict()        # = {}
        self._tcamTable         = pd.DataFrame
        self._sramTable         = pd.DataFrame
        # ------------------- private vars
        self.__tcamQueryStrLen  = int()
        self.__tcamSubStrLen    = int()
        self.__tcamTotalSubStr  = int()
        self.__tcamPotMatchAddr = int()
        self.__sramTableRows    = int()
        self.__sramTableCols    = int()
        self.__tcamRows         = list()
        self.__tcamCols         = list()
        self.__tcamColVec       = list()
        self.__sramRows         = list()
        self.__sramRowVec       = list()
        self.__sramCols         = list()
        
        
        # logging config
        logging.basicConfig(level=logging.DEBUG, filename='./logs/tableMapping.log',
                            format='%(asctime)s | %(filename)s | %(funcName)s | %(levelname)s | %(lineno)d | %(message)s')
    
    # ----------------------------------------------------------------- Functions
    def getPrjDir(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        self.prjWorkDir=os.getcwd()
        logging.info('Project working dir: {:<s}'.format(self.prjWorkDir))
        return self.prjWorkDir
    
    
    def getYAMLFilePath(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # get tcamTables config file path
        tempPath = os.path.join(self.prjWorkDir,'compiler/configs/tcamTables.yaml')
        if os.path.isfile(tempPath) is True:
            self.tcamTableConfigsFilePath = tempPath
            self.tcamTableConfigsFileName = os.path.basename(tempPath)
            logging.info('"FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
            return self.tcamTableConfigsFilePath
        else:
            logging.error('"NOT FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
            sys.exit('"NOT FOUND": TCAM table config file path: {:<s}'.format(self.tcamTableConfigsFilePath))
    
    
    def readYAML(self,filePath):
        """
        what does this func do ?
        input args:
        return val:
        """
        with open(filePath) as file:
            self._tcamTableConfigs=yaml.full_load(file)
        # print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Read TCAM table config file: {:<s}'.format(self.tcamTableConfigsFilePath))
        return self._tcamTableConfigs
    
    
    def printYAML(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        print(json.dumps(self._tcamTableConfigs,indent=4))
        # print(yaml.dump(self._tcamTableConfigs,sort_keys=False,default_flow_style=False))
        logging.info('Printed TCAM table configs')
    
    
    def getTCAMConfig(self,tcamConfig):
        """
        what does this func do ?
        input args:
        return val:
        """
        # look for specific tcam config in compiler/configs/tcamTables.yaml
        if tcamConfig in self._tcamTableConfigs.keys():
            tempConfig = self._tcamTableConfigs[tcamConfig]
            # save tcam config vars
            self.__tcamQueryStrLen  = tempConfig['queryStrLen']
            self.__tcamSubStrLen    = tempConfig['subStrLen']
            self.__tcamTotalSubStr  = tempConfig['totalSubStr']
            self.__tcamPotMatchAddr = tempConfig['potMatchAddr']
            # print specific tcam config
            print(json.dumps(tempConfig, indent=4))
            logging.info('"FOUND" Required TCAM Config [{:<s}]'.format(tcamConfig))
        else:
            logging.error('"NOT FOUND": TCAM Config [{:<s}]'.format(tcamConfig))
            sys.exit('"NOT FOUND": Required TCAM table config [{:<s}]'.format(tcamConfig))
    
    
    def getTCAMTableFilePath(self,tcamConfig):
        """
        what does this func do ?
        input args:
        return val:
        """
        # find the specific tcam table map in compiler/lib/
        tempPath = os.path.join(self.prjWorkDir,'compiler/lib/'+tcamConfig+'.xlsx')
        if os.path.isfile(tempPath) is True:
            self.tcamTableXlsxFilePath = tempPath
            self.tcamTableXlsxFileName = os.path.basename(tempPath)
            logging.info('"FOUND" TCAM table map XLSX file path: {:<s}'.format(self.tcamTableXlsxFilePath))
            return self.tcamTableXlsxFilePath
        else:
            logging.error('"NOT FOUND": TCAM table map XLSX file path: {:<s}'.format(self.tcamTableXlsxFilePath))
            sys.exit('"NOT FOUND": TCAM table map XLSX file path {:<s}'.format(self.tcamTableXlsxFilePath))
    
    
    def printDF(self,dataFrame):
        """
        what does this func do ?
        input args:
        return val:
        """
        print('\n')
        print(tabulate(dataFrame,headers='keys', showindex=True, disable_numparse=True, tablefmt='github'),'\n')
        logging.info('Printed dataframe')
    
    
    def readTCAMTable(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # store tcam table in dataframe
        self._tcamTable = pd.read_excel(self.tcamTableXlsxFilePath, skiprows=2, index_col=None, engine='openpyxl')
        # print(self._tcamTable)
        # get num of rows and col from tcam table
        tcamTableRows = self._tcamTable.shape[0]
        tcamTableCols = self._tcamTable.shape[1]
        # print('tcam table map:  ',tcamTableRows,tcamTableCols)
        # print('tcam table conf: ',self.__tcamPotMatchAddr,self.__tcamQueryStrLen)        
        # compare row/col of tcam table with respective yaml config
        if (tcamTableRows == self.__tcamPotMatchAddr and 
            tcamTableCols - 1 == self.__tcamQueryStrLen):
            logging.info('"MATCH FOUND": TCAM table map rows == TCAM table YAML config potMatchAddr')
            logging.info('"MATCH FOUND": TCAM table map cols == TCAM table YAML config queryStrLen')
            return [tcamTableRows, tcamTableCols]
        else:
            logging.info('"MATCH NOT FOUND": TCAM table map rows != TCAM table YAML config potMatchAddr')
            logging.info('"MATCH NOT FOUND": TCAM table map cols != TCAM table YAML config queryStrLen')
            sys.exit('"MATCH NOT FOUND": MISMATCH in TCAM table map and YAML config rows/cols')
    
    
    def getSRAMTableDim(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        self.__sramTableRows = self.__tcamTotalSubStr * pow(2,self.__tcamSubStrLen)
        self.__sramTableCols = self.__tcamPotMatchAddr
        logging.info('SRAM table rows [{:>4d}] cols [{:>4d}]'.format(self.__sramTableRows,self.__sramTableCols))
        # print(sramTableRows,sramTableCols)
        return [self.__sramTableRows, self.__sramTableCols]
    
    
    def genSRAMTable(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # create temp vars
        sramTableAddrList = list()
        sramColHeadings = list()
        # create row address
        for i in range(self.__tcamTotalSubStr):
            for j in range(2**self.__tcamSubStrLen):
                padding = '0'+str(self.__tcamSubStrLen)+'b'
                # sramTableAddrList.append(format(j, '#012b'))  # with 0b prefix
                sramTableAddrList.append(format(j, padding))    # without 0b prefix
            logging.info('Created [{:>4d}] SRAM addresses from search query [{:>4d}]'.format(j+1,i))
        # create col headings
        for k in reversed(range(self.__tcamPotMatchAddr)):
            heading = 'D'+str(k)
            sramColHeadings.append(heading)
        logging.info('Created [{:>4d}] data fields from potential match addresses'.format(k+1))
        # gen empty m*n sram table
        self._sramTable = pd.DataFrame(index=np.arange(self.__sramTableRows), columns=np.arange(self.__sramTableCols))
        # rename column headings
        self._sramTable.columns = sramColHeadings
        # insert addr col at position 0
        self._sramTable.insert(0,'Addresses',sramTableAddrList,allow_duplicates=True)
        # logging.info('Created empty [{:d} x {:d}] SRAM table'.format(self.__sramTableRows,self.__sramTableCols))
        logging.info('Created empty [{:d} x {:d}] SRAM table'.format(self._sramTable.shape[0],self._sramTable.shape[1]))
    
    
    def createSRAMExcel(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # create sramTables dir if it doesnt exist
        tempPath = os.path.join(self.prjWorkDir,'sramTables')
        if os.path.exists(tempPath) is False:
            os.makedirs('sramTables')
            logging.info('Created sramTables dir: {:<s}'.format(tempPath))
        # create sram table file path
        self.sramTableXlsxFileName = os.path.basename(self.tcamTableXlsxFileName.replace('tcam','sram'))
        self.sramTableXlsxFilePath = os.path.join(tempPath,self.sramTableXlsxFileName)
        # create empty excel file in dir sramTables
        writer = pd.ExcelWriter(self.sramTableXlsxFilePath,engine='xlsxwriter')
        writer.save()
        self._sramTable.to_excel(excel_writer=self.sramTableXlsxFilePath, sheet_name=self.sramTableXlsxFileName,
                                    na_rep='', header=True, index=True, engine='xlsxwriter')
        logging.info('Created SRAM table XLSX file {:<s}'.format(self.sramTableXlsxFilePath))
        return self.sramTableXlsxFilePath
    
    
    def splitRowsAndCols(self):
        """
        what does this func do ?
        input args:
        return val:
        """
        # store tcam and sram table in temp vars
        tcamDF = self._tcamTable
        sramDF = self._sramTable
        logging.info('TCAM table (r*c): {0}'.format(tcamDF.shape))
        logging.info('SRAM table (r*c): {0}'.format(sramDF.shape))
        # create tcamRows vector
        self.__tcamRows = np.arange(0,self.__tcamPotMatchAddr,1).tolist()
        logging.info('TCAM table row vector: {0}'.format(self.__tcamRows))
        # create tcamCols vector
        self.__tcamCols = np.arange(1,self.__tcamQueryStrLen+1,1).tolist()
        logging.info('TCAM table col vector: {0}'.format(self.__tcamCols))
        # create tcamColVec vector and split in equal pieces
        self.__tcamColVec = np.array_split(self.__tcamCols,self.__tcamTotalSubStr)
        for i in range(len(self.__tcamColVec)):
            self.__tcamColVec[i] = self.__tcamColVec[i].tolist()
            logging.info('TCAM table col split vector [{0}]: {1}'.format(i,self.__tcamColVec[i]))
        # create sramRows vector
        self.__sramRows = np.arange(0,self.__tcamTotalSubStr * 2**self.__tcamSubStrLen,1).tolist()
        logging.info('SRAM table row vector: {0}'.format(self.__sramRows))
        # create sramRowVec vector and split in equal pieces
        self.__sramRowVec = np.array_split(self.__sramRows,self.__tcamTotalSubStr)
        for i in range(len(self.__sramRowVec)):
            self.__sramRowVec[i] = self.__sramRowVec[i].tolist()
            logging.info('SRAM table row split vector [{0}]: {1}'.format(i,self.__sramRowVec[i]))
        # create sramCols vector
        self.____sramCols = np.arange(1,self.__tcamPotMatchAddr+1,1).tolist()
        logging.info('SRAM table col vector: {0}'.format(self.____sramCols))
    
    
    

