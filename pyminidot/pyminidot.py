import datetime
import pytz
import numpy
import logging
import sys
import argparse
import pkg_resources
import yaml
import codecs
import numpy as np

# Get the version
version_file = pkg_resources.resource_filename('pyminidot','VERSION')

with open(version_file) as version_f:
   version = version_f.read().strip()


# Setup logging module
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logger = logging.getLogger('pyminidot')


class pyminiDOT():
    """A PME miniDOT parsing object

    Author: Peter Holtermann (peter.holtermann@io-warnemuende.de)

    Usage:
       >>>filename='Cat.txt'
       >>>rbr = pyminiDOT(filename)

    Args:
       filename: The name of the datafile
       verbosity: 
       timezone: The timezone the time data is saved in

    """
    
    def __init__(self,filename,encoding='windows-1253',verbosity=logging.DEBUG,timezone=pytz.UTC):
        """
        """
        logger.setLevel(verbosity)
        logger.info(' Opening file: ' + filename)
        
        self.filename = filename
        self.timezone = timezone
        data = self.read_cat(filename,encoding=encoding)
        self.data = data

    def read_cat(self,fname,encoding='windows-1253'):
        print('Opening ' + str(fname))
        f = codecs.open(fname, "r", encoding = encoding)
        data = {}
        data['unix_time'] = []
        data['utc_time'] = []
        data['battery'] = []
        data['temp'] = []
        data['oxy'] = []
        data['oxy_sat'] = []
        data['Q'] = []
        ind_bat = None
        i = 0
        for l in f.readlines():
            i += 1
            # Get rid of double white space and trailing spaces
            # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python            
            lg = ' '.join(l.split())
            lsp = lg.split(',')
            if(i==8): # The data column identifiers
                ind_tu   = -1
                ind_date = -1
                ind_temp = -1
                ind_oxy  = -1
                ind_oxysat = -1
                ind_Q = -1
                ind_bat = -1
                for j,hd in enumerate(lsp):
                    if('unix timestamp' in hd.lower()):
                        print('Index unix time stamp in column',j)
                        ind_tu = j
                    if('saturation' in hd.lower()):
                        print('Index oxygen saturation in column',j)                        
                        ind_oxysat = j
                    elif('oxygen' in hd.lower()):
                        print('Index oxygen concentration in column',j)                        
                        ind_oxy = j                                                
                    if('date' in hd.lower()):
                        print('Index date in column',j)                        
                        ind_date = j
                    if('temperature' in hd.lower()):
                        print('Index temperature in column',j)
                        ind_temp = j
                    if('battery' in hd.lower()):
                        print('Index battery in column',j)
                        ind_bat = j                        
                    if(hd.lower() == 'q'):
                        print('Index Q in column',j)
                        ind_Q = j                                                
                
            if(i>=10):
                #print(l)
                
                #data['unix_time'].append(float(lsp[0]))
                data['unix_time'].append(float(lsp[ind_tu]))
                ttmp = datetime.datetime.strptime(lsp[ind_date].strip(),"%Y-%m-%d %H:%M:%S")
                ttmp = ttmp.replace(tzinfo=self.timezone)
                data['utc_time'].append(ttmp)
                if(ind_bat >-1):
                    #data['battery'].append(float(lsp[5]))
                    data['battery'].append(float(lsp[ind_bat]))
                if(ind_temp >-1):                    
                    #data['temp'].append(float(lsp[6]))
                    data['temp'].append(float(lsp[ind_temp]))
                if(ind_oxy >-1):                                        
                    #data['oxy'].append(float(lsp[7]))
                    data['oxy'].append(float(lsp[ind_oxy]))
                if(ind_oxysat >-1):                    
                    #data['oxy_sat'].append(float(lsp[8]))
                    data['oxy_sat'].append(float(lsp[ind_oxysat]))
                if(ind_Q >-1):                                        
                    #data['Q'].append(float(lsp[9]))
                    data['Q'].append(float(lsp[ind_Q]))

        data['utc_time']  = numpy.asarray(data['utc_time'])
        data['unix_time'] = numpy.asarray(data['unix_time'])
        if(ind_bat >-1):    
            data['battery']   = numpy.asarray(data['battery'])
        if(ind_temp >-1):                
            data['temp']      = numpy.asarray(data['temp'])
        if(ind_oxy >-1):                                        
            data['oxy']       = numpy.asarray(data['oxy'])
        if(ind_oxysat >-1):                            
            data['oxy_sat']   = numpy.asarray(data['oxy_sat'])
        if(ind_Q >-1):                        
            data['Q']         = numpy.asarray(data['Q'])                
        return data


