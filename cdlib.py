# -*- coding: utf-8 -*-
"""
Created on Fri May 18 11:08:16 2012

@author: VHOEYS

EASY CD LIBRARY MANAGEMENT SYSTEM

todo:
    ignore 'the' in front for alphabetically ordering
    merging of different databases
"""

import os
import sys
import datetime

from pickle import dump, load

from tempfile import TemporaryFile
from xlwt import Workbook

class Musiclib():
    """
    Created on Fri May 18 11:08:16 2012

    @author: Stijn Van Hoey

    EASY CD LIBRARY MANAGEMENT SYSTEM:
        
    Music library class to keep overview of the CD collection
    The musiclib got Musiclib.CDlib dictionary to save the collection in
    further definitions are
    - getdata: load data from a pickle dump file    
    - makedictlower: make everythong owercase - first rough version to make prevent from easy double entries, can be improved a lot
    - savedata: dump in pickle format
    - addartist: new artist in library
    - addcd: new cd in library
    - readfromtxt: read from textfile in 'artist - cd' format
    - save2file: save library in textfile with 'artist - cd' format
    - printartist: give all cd's from a specifi artist
    - save2excel: save library to excel file
    
    """
    
    def __init__(self, dirname, owner='Stijn Van Hoey', loaddata=False,datafile=None):
        """
        Musiclib gives overview of CD's in collection
        self.CDlib is a dictionary overview of a CD collection,
        every artist is an entry, the cd's are a list of names
        """
        
        self.dirname = dirname
        self.owner = owner
        
        self.CDlib={}
        if loaddata==True:
            self.getdata(datafile)

    def getdata(self,filename):
        """
        Get CD library data from a dictionary, dumped pickle
        """
        pkl_file = open(filename, 'rb')
        newdata = load(pkl_file)
        if not isinstance(newdata,dict):
            raise Exception('The loaded data must be in dictionary format')
        pkl_file.close() 
       
        if len(self.CDlib)==0:
            self.CDlib=newdata
            self.makedictlower()
        else:
            #Data must be added to existing database
            try:
                self.makedictlower()
                self.CDlib=self.mergedata(self.CDlib,newdata) 
            except:
                print 'functionality not added yet'  
    
    def makedictlower(self):      
        dict((k.lower(), [el.lower() for el in v]) for k,v in self.CDlib.iteritems())              
                
#    def mergedata(data1,data2):
#        
#        return data
    
    def savedata(self,filename):
        """
        Dump pickle of database
        """
        output = open(filename, 'wb')
        dump(self.CDlib, output)
        output.close()        


    def addartist(self, artist):
        """
        Takes one argument, the name of the artist
        """
        self.CDlib[artist.lower()]=[]


    def addCD(self, artist, cd):
        """
        Add a CD to the collection
        """
        artist=artist.lower()
        cd=cd.lower()
        
        if artist in self.CDlib:
            #add the cd to the cd list tuple of the artist
            if cd in self.CDlib[artist]:
                print 'CD already in collection'
            else:
                
                self.CDlib[artist].append(cd)
                print 'CD added to %s list' %artist 
        else:
            self.addartist(artist)
            self.CDlib[artist].append(cd)
            
            print '%s added to the CDlib with the CD %s' %(artist,cd)

    def readfromtxt(self, txtfile):
        """
        Read the data from a text file with the format 'artist - cd'
        """
        newdata_file = open(txtfile, 'r')
        for line in newdata_file:
            info=line.split('-')
            
            if len(info)>2:
                raise Exception('no - signs in artist name or cd title allowed')
            
            if len(info)<2:
                raise Exception('make sure no  empty line is present or extra whitelines are present in the file')
            
            artist=info[0].strip().lower()
            cd=info[1].strip().lower()
            self.addCD( artist, cd)       

    def save2file(self, filename):
        """
        save the library in one text file, with artists alphabetically
        
        """      
        today = datetime.date.today()
                      
        artistlist=sorted(self.CDlib)
        write_file = open(filename, 'w')
        write_file.write('='*50+'\n')
        write_file.write('==CD collection of %s saved %s ==\n' %(self.owner,str(today)))
        write_file.write('='*50+'\n')        
        for artist in artistlist:
            for cd in self.CDlib[artist]:
                write_file.write(artist)
                write_file.write(' - ')
                write_file.write(cd)
                write_file.write('\n')
        write_file.close()
        
    def printartist(self,artist):
        '''
        print the list of cd's of 1 artist
        '''
        
        try:
            print self.CDlib[artist.lower()]
        except:
            print 'Artist not found in the current library'              
    

    def save2excel(self,fileoutname):
        """
        save all the data in an excel file
        """
        today = datetime.date.today()
        artistlist=sorted(self.CDlib)    
        
        book = Workbook()
        sheet1 = book.add_sheet('CDLIJST')     
        sheet1.write(0,0,'CD collection of %s saved %s' %(self.owner,str(today)))
        
        rowid=1
        colid=0
        for artist in artistlist:
            for cd in self.CDlib[artist]:
                sheet1.write(rowid,colid,artist)
                sheet1.write(rowid,colid+1,cd)
                rowid+=1
        if fileoutname[-4:]=='.xls':
            book.save(fileoutname)
        else:
            book.save(fileoutname+'.xls')   
            
        book.save(TemporaryFile())
        

#hier beter met module setuptools stijl werken dan als onafhankelijke uitvoeringsfile
#def main():
#    print Musiclib.__doc__
#
#if __name__ == "__main__":
#    sys.exit(main())
     
    


