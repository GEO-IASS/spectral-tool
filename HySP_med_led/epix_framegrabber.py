#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2014, Thomas G. Dimiduk, Rebecca W. Perry, Aaron Goldfain
#
# This file is part of Camera Controller
#
# Camera Controller is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HoloPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HoloPy.  If not, see <http://www.gnu.org/licenses/>.
"""
Higher Level interface to the epix framegrabber

.. moduleauthor:: Thomas G. Dimiduk <tom@dimiduk.net>
.. moduleauthor:: Rebecca W. Perry <perry.becca@gmail.com>
"""
import numpy as np
import os.path
import os
import pypylon

#epix = windll.LoadLibrary("C:\Program Files\EPIX\XCLIB\clserEPX_w64.dll")

class CameraOpenError(Exception):
    def __init__(self, mesg):
        self.mesg = mesg
    def __str__(self):
        return self.mesg

class Camera(object):
    def __init__(self):
        self.pixci_opened = False
        self.bit_depth = None
        self.roi_shape = None
        self.camera = None
        self.exposure = None
        self.roi_pos = None
        self.frametime = None
        try:
            from ctypes import c_ubyte, windll, sizeof, c_ushort
        except ImportError:
            raise CameraOpenError("Import failed")
        #print('hello')
        self.epix = windll.LoadLibrary("C:\Program Files\EPIX\XCLIB\XCLIBW64.dll")
        #self.pylon = windll.LoadLibrary

    def open(self, bit_depth=8, roi_shape=(2048, 1088), roi_pos = (0,0), camera=None, exposure = 0.1, frametime = 0):
#    def open(self, bit_depth=10, roi_shape=(500, 500), roi_pos = (0,0), camera=None, exposure = 0, frametime = 0):	
#    def open(self, bit_depth=10, roi_shape=(2048, 1088), roi_pos = (0,0), camera=Basler, exposure = 0, frametime = 0):		
        if self.pixci_opened:
            self.close()
        print('this is open camera in epixframegrabber')
        from ctypes import c_ubyte, windll, sizeof, c_ushort

        self.bit_depth = bit_depth
        self.roi_shape = roi_shape
        self.camera = camera
        self.roi_pos = roi_pos
        self.exposure = exposure
        self.frametime = frametime

        filename = "{0}_{1}bit_{2}x{3}.fmt".format(self.camera,self.bit_depth,*self.roi_shape)
        formatfile = os.path.join("formatFiles", filename)
        
        #i = self.epix.pxd_PIXCIopen("","", b"OurCamera.fmt") # standard NTSC
        i = self.epix.pxd_PIXCIopen("","", b"PhotonFocus_8bit_1024x1024.fmt") # standard NTSC
        #i = self.epix.pxd_PIXCIopen("","", filename.encode(encoding='UTF-8')) # standard NTSC
        #i = self.epix.pxd_PIXCIopen("","", "") # standard NTSC
        test = self.epix.pxd_mesgErrorCode(i)
        test2 = self.epix.pxd_mesgFault(1)
        if i == 0:
            print("Frame grabber opened successfully.")
            self.pixci_opened = True
        elif i == -13:
            raise CameraOpenError("Frame grabber can't find format file.")
        elif i == -23:
            raise CameraOpenError("Frame grabber is already open.")
        else:
            raise CameraOpenError("Opening the frame grabber failed with error code "+str(i))
            #epix.pxd_mesgFault(1)
        
        #Use pypylon to set parameters on camera

        #search camera
        available_cameras = pypylon.factory.find_devices()
        print('Available cameras are', available_cameras)
        self.cam = pypylon.factory.create_device(available_cameras[-1])

        # We can still get information of the camera back
        print('Camera info of camera object:', self.cam.device_info)

        # Open camera and grep some images
        self.cam.open()

        # Hard code exposure time
        self.cam.properties['ExposureTimeAbs'] = 15000.0 #exposure time in microseconds
        
        # Set GainRaw
        self.cam.properties['GainRaw'] = 350 #max should be 350, check manual


        ###list of properties of camera (check here for how to change parameters on camera) 
        ## uncomment this part to see the properties names
        #for key in self.cam.properties.keys():
        #    try:
        #        value = self.cam.properties[key]
        #    except IOError:
        #        value = '<NOT READABLE>'

        #    print('{0} ({1}):\t{2}'.format(key, self.cam.properties.get_description(key), value))



        #initialize serial port
        #r = self.epix.pxd_serialConfigure(0x1, 0,  9600, 8, 0, 1, 0, 0, 0)
        #if (r < 0):
        #    print('error')
        #command = 'DeviceModelName'
        ##command.encode()
        #test11 = self.epix.pxd_serialWrite(0x1, 0, command.encode())
        #test22 = self.epix.pxd_serialRead(0x1, 0)
        #buff_char =  "\0" * 100
        #buff_char.encode()
        #test22 = self.epix.pxd_serialRead(0x1, 0, buff_char)

        #command = 'GainAll = 128'
        #test23 =self.epix.pxd_serialWrite(0x1,0,command.encode())

        aa = 00
 

        
    def close(self):
        if self.open:
            self.cam.close()
            print('Camera closed successfully')
            i = self.epix.pxd_PIXCIclose("",b"NTSC","") # standard NTSC #-25
            if i == 0:
                
                print("Frame grabber closed successfully.")
                self.open = True
            elif i == -25:
                print("Failed to close the frame grabber because it wasn't open.")
            else:
                print("Closing the frame grabber failed with error code "+str(i))
        else:
            return

    def get_image(self, buffer_number=None):
        try:
            from ctypes import c_ubyte, windll, sizeof, c_ushort
        except ImportError:
            raise CameraOpenError("Import failed")

        if buffer_number is None:
            buffer_number = self.epix.pxd_capturedBuffer(1)
        # TODO: can we use the locally stored values for these? Or is
        # there some subtle way that will lead us astray?
        xdim = self.epix.pxd_imageXdim()
        ydim = self.epix.pxd_imageYdim()

        imagesize = xdim*ydim

        if self.bit_depth > 8:
            c_type = c_ushort
            cam_read = self.epix.pxd_readushort
        else:
            c_type = c_ubyte
            cam_read = self.epix.pxd_readuchar
        c_buf = (c_type * imagesize)(0)
        c_buf_size = sizeof(c_buf)

        cam_read(0x1, buffer_number, 0, 0, -1, ydim, c_buf,
                           c_buf_size, b"Gray")

        im = np.frombuffer(c_buf, c_type).reshape([xdim, ydim])
        #imshow
        
        if self.bit_depth > 8:
            # We have to return a 16 bit image, use the upper bits so that
            # outputs look nicer (max pixel intensity will be interpreted as
            # white by image viewers). i.e. linearly rescale pixel values to
            # a 16 bit scale : 0 to 65535. Note 65535 = (2**16 - 1).
            im = im * 2**(16-self.bit_depth)

        return im



    def set_tap_geometry(self, tap_geometry_value):
        if tap_geometry_value == 4:
#            print('tap 4xY')
            self.cam.properties['ClTapGeometry'] = 'Geometry1X4_1Y'
        if tap_geometry_value == 8:
#            print('tap 4xY')
            self.cam.properties['ClTapGeometry'] = 'Geometry1X8_1Y' 

    def set_pixel_clock(self, pixel_clock_value):
        if pixel_clock_value == 82:
            self.cam.properties['ClPixelClock'] = 'PixelClock82'

#    def set_pixel_size(self, pixel_size_value):
#        if pixel_size_value == 10:
#            self.cam.properties['PixelSize'] = 'Bpp10'      # error, unable to change? can't find in manual

    def set_sensor_bit_depth(self, sensor_bit_depth_value):
        if sensor_bit_depth_value == 10:
            self.cam.properties['SensorBitDepth'] = 'BitDepth10'


    def set_gain(self, gain_value):
        # Set GainRaw
        if gain_value>511:
            gain_value = 511
        if gain_value< 0:
            gain_value = 1

        self.cam.properties['GainRaw'] = gain_value #max should be 511, check manual

    def set_exposure(self, exposure_value):
        #exposure in microseconds
        if exposure_value<10862:
            exposure_value = 10862 #min value
        self.cam.properties['ExposureTimeAbs'] = exposure_value





    def get_image_new(self, buffer_number=None):
        try:
            from ctypes import c_ubyte, windll, sizeof, c_ushort
        except ImportError:
            raise CameraOpenError("Import failed")

        if buffer_number is None:
            buffer_number = self.epix.pxd_capturedBuffer(1)
        # TODO: can we use the locally stored values for these? Or is
        # there some subtle way that will lead us astray?
        xdim = self.epix.pxd_imageXdim()
        ydim = self.epix.pxd_imageYdim()

        imagesize = xdim*ydim
        #note this edit
        
        self.bit_depth = 8
        
        if self.bit_depth > 8:
            c_type = c_ushort
            cam_read = self.epix.pxd_readushort
        else:
            c_type = c_ubyte
            cam_read = self.epix.pxd_readuchar
        c_buf = (c_type * imagesize)(0)
        c_buf_size = sizeof(c_buf)

        cam_read(0x1, buffer_number, 0, 0, -1, ydim, c_buf,
                           c_buf_size, b"Gray")

        im = np.frombuffer(c_buf, c_type).reshape([xdim, ydim])
        #imshow
        
        if self.bit_depth > 8:
            # We have to return a 16 bit image, use the upper bits so that
            # outputs look nicer (max pixel intensity will be interpreted as
            # white by image viewers). i.e. linearly rescale pixel values to
            # a 16 bit scale : 0 to 65535. Note 65535 = (2**16 - 1).
            im = im * 2**(16-self.bit_depth)

        return im

    def get_frame_number(self):
        return self.epix.pxd_capturedBuffer(0x1,1)-1

    def finished_live_sequence(self):
        return self.epix.pxd_goneLive(0x1) == 0

    def start_continuous_capture(self, buffersize):
        '''
        buffersize: number of frames to keep in rolling buffer
        '''
        # This appears to give an infinitely long live seqence, however it
        # looks like it may do it by continually overwriting the same image in
        # the buffer, so it probably will not work if we want a rolling buffer
        # tgd 2014-06-16
        # you can get the same effect by changing 1000000 to 0
        #self.epix.pxd_goLive(0x1,1)
        self.epix.pxd_goLiveSeq(0x1,1,buffersize,1,1000000,1)

    def start_sequence_capture(self, n_frames):
        print('sequence capture started')
        self.epix.pxd_goLiveSeq(0x1,1,n_frames,1,n_frames,1)

    def stop_live_capture(self, ):
        print('unlive now')
        self.epix.pxd_goUnLive(0x1)
        
        
    def set_roi_pos(self, set_roi_pos):
        #not yet implemented
        self.roi_pos = [0, 0]
    
    def set_frametime(self, frametime):
        #not yet implemented
        self.frametime = 0

    def get_snapshot(self):
        self.epix.pxd_goSnap(0x1,1)





