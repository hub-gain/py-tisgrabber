

import ctypes as C
import os
import sys
import numpy as np


class GrabberHandle(C.Structure):
    pass
GrabberHandle._fields_ = [('unused', C.c_int)]

class TIS_GrabberDLL(object):
    tisgrabber = C.windll.LoadLibrary("tisgrabber.dll")
    
    GrabberHandlePtr = C.POINTER(GrabberHandle)
    
#     Initialize the ICImagingControl class library. This function must be called
#	only once before any other functions of this library are called.
#	@param szLicenseKey IC Imaging Control license key or NULL if only a trial version is available.
#	@retval IC_SUCCESS on success.
#	@retval IC_ERROR on wrong license key or other errors.
#	@sa IC_CloseLibrary
    InitLibrary=tisgrabber.IC_InitLibrary(None)
    
#     Get the number of the currently available devices. This function creates an
#	internal array of all connected video capture devices. With each call to this 
#	function, this array is rebuild. The name and the unique name can be retrieved 
#	from the internal array using the functions IC_GetDevice() and IC_GetUniqueNamefromList.
#	They are usefull for retrieving device names for opening devices.
#	
#	@retval >= 0 Success, count of found devices.
#	@retval IC_NO_HANDLE Internal Error.
#
#	@sa IC_GetDevice
#	@sa IC_GetUniqueNamefromList
    Anzahl_Cams= tisgrabber.IC_GetDeviceCount()

#     Get unique device name of a device specified by iIndex. The unique device name
#	consist from the device name and its serial number. It allows to differ between 
#	more then one device of the same type connected to the computer. The unique device name
#	is passed to the function IC_OpenDevByUniqueName
#
#	@param iIndex The number of the device whose name is to be returned. It must be
#				in the range from 0 to IC_GetDeviceCount(),
#	@return Returns the string representation of the device on success, NULL
#				otherwise.
#
#	@sa IC_GetDeviceCount
#	@sa IC_GetUniqueNamefromList
#	@sa IC_OpenDevByUniqueName

    get_unique_name_from_list = tisgrabber.IC_GetUniqueNamefromList
    get_unique_name_from_list.restype = C.c_char_p
    get_unique_name_from_list.argtypes = (C.c_int,)
    
#     Creates a new grabber handle and returns it. A new created grabber should be
#	release with a call to IC_ReleaseGrabber if it is no longer needed.
#	@retval IC_SUCCESS on success.
#	@retval IC_ERROR if an error occurred.
#	@sa IC_ReleaseGrabber
    create_grabber = tisgrabber.IC_CreateGrabber
    create_grabber.restype = GrabberHandlePtr
    create_grabber.argtypes = None

#    Open a video capture by using its UniqueName. Use IC_GetUniqueName() to
#    retrieve the unique name of a camera.
#
#	@param hGrabber       Handle to a grabber object
#	@param szDisplayName  Memory that will take the display name.
#
#	@sa IC_GetUniqueName
#	@sa IC_ReleaseGrabber
    open_device_by_unique_name = tisgrabber.IC_OpenDevByUniqueName
    open_device_by_unique_name.restype = C.c_int
    open_device_by_unique_name.argtypes = (GrabberHandlePtr,
                                           C.c_char_p)   
                                           
                                          
#    Returns the width of the video format.                                          
    get_video_format_width = tisgrabber.IC_GetVideoFormatWidth
    get_video_format_width.restype = C.c_int
    get_video_format_width.argtypes = (GrabberHandlePtr,)                                          
    
#    returns the height of the video format.
    get_video_format_height = tisgrabber.IC_GetVideoFormatHeight
    get_video_format_height.restype = C.c_int
    get_video_format_height.argtypes = (GrabberHandlePtr,)                            
    
    
#    Get the number of the available video formats for the current device. 
#	A video capture device must have been opened before this call.
#	
#	@param hGrabber The handle to the grabber object.
#
#	@retval >= 0 Success
#	@retval IC_NO_DEVICE No video capture device selected.
#	@retval IC_NO_HANDLE No handle to the grabber object.
#
#	@sa IC_GetVideoFormat
    GetVideoFormatCount = tisgrabber.IC_GetVideoFormatCount
    GetVideoFormatCount.restype = C.c_int
    GetVideoFormatCount.argtypes = (GrabberHandlePtr,)

#     Get a string representation of the video format specified by iIndex. 
#	iIndex must be between 0 and IC_GetVideoFormatCount().
#	IC_GetVideoFormatCount() must have been called before this function,
#	otherwise it will always fail.	
#
#	@param hGrabber The handle to the grabber object.
#	@param iIndex Number of the video format to be used.
#
#	@retval Nonnull The name of the specified video format.
#	@retval NULL An error occured.
#	@sa IC_GetVideoFormatCount
    GetVideoFormat = tisgrabber.IC_GetVideoFormat
    GetVideoFormat.restype = C.c_char_p
    GetVideoFormat.argtypes = (GrabberHandlePtr,
                               C.c_int,) 

#    Get the number of the available input channels for the current device.
#    A video	capture device must have been opened before this call.
#
#	@param hGrabber The handle to the grabber object.
#
#	@retval >= 0 Success
#	@retval IC_NO_DEVICE No video capture device selected.
#	@retval IC_NO_HANDLE No handle to the grabber object.
#
#	@sa IC_GetInputChannel                               
    GetInputChannelCount = tisgrabber.IC_GetInputChannelCount
    GetInputChannelCount.restype = C.c_int
    GetInputChannelCount.argtypes = (GrabberHandlePtr,)
    
#     Get a string representation of the input channel specified by iIndex. 
#	iIndex must be between 0 and IC_GetInputChannelCount().
#	IC_GetInputChannelCount() must have been called before this function,
#	otherwise it will always fail.		
#	@param hGrabber The handle to the grabber object.
#	@param iIndex Number of the input channel to be used..
#
#	@retval Nonnull The name of the specified input channel
#	@retval NULL An error occured.
#	@sa IC_GetInputChannelCount
    GetInputChannel = tisgrabber.IC_GetInputChannel
    GetInputChannel.restype = C.c_char_p
    GetInputChannel.argtypes = (GrabberHandlePtr,
                               C.c_int,)     
    
    
#     Get the number of the available video norms for the current device. 
#	A video capture device must have been opened before this call.
#	
#	@param hGrabber The handle to the grabber object.
#
#	@retval >= 0 Success
#	@retval IC_NO_DEVICE No video capture device selected.
#	@retval IC_NO_HANDLE No handle to the grabber object.
#	
#	@sa IC_GetVideoNorm
    GetVideoNormCount = tisgrabber.IC_GetVideoNormCount
    GetVideoNormCount.restype = C.c_int
    GetVideoNormCount.argtypes = (GrabberHandlePtr,)
    
    
#     Get a string representation of the video norm specified by iIndex. 
#	iIndex must be between 0 and IC_GetVideoNormCount().
#	IC_GetVideoNormCount() must have been called before this function,
#	otherwise it will always fail.		
#	
#	@param hGrabber The handle to the grabber object.
#	@param iIndex Number of the video norm to be used.
#
#	@retval Nonnull The name of the specified video norm.
#	@retval NULL An error occured.
#	@sa IC_GetVideoNormCount
    GetVideoNorm = tisgrabber.IC_GetVideoNorm
    GetVideoNorm.restype = C.c_char_p
    GetVideoNorm.argtypes = (GrabberHandlePtr,
                               C.c_int,)  
#    Start the live video. 
#	@param hGrabber The handle to the grabber object.
#	@param iShow The parameter indicates:   @li 1 : Show the video	@li 0 : Do not show the video, but deliver frames. (For callbacks etc.)
#	@retval IC_SUCCESS on success
#	@retval IC_ERROR if something went wrong.
#	@sa IC_StopLive

    StartLive = tisgrabber.IC_StartLive
    StartLive.restype = C.c_int
    StartLive.argtypes = (GrabberHandlePtr,
                               C.c_int,) 

    StopLive = tisgrabber.IC_StopLive
    StopLive.restype = C.c_int
    StopLive.argtypes = (GrabberHandlePtr,) 


#    Snaps an image. The video capture device must be set to live mode and a 
#	sink type has to be set before this call. The format of the snapped images depend on
#	the selected sink type. 
#
#	@param hGrabber The handle to the grabber object.
#	@param iTimeOutMillisek The Timeout time is passed in milli seconds. A value of -1 indicates, that
#							no time out is set.
#
#	
#	@retval IC_SUCCESS if an image has been snapped
#	@retval IC_ERROR if something went wrong.
#	@retval IC_NOT_IN_LIVEMODE if the live video has not been started.
#
#	@sa IC_StartLive 
#	@sa IC_SetFormat
    
    SnapImage=tisgrabber.IC_SnapImage
    SnapImage.restype = C.c_int
    SnapImage.argtypes = (GrabberHandlePtr,
                               C.c_int,) 
 
 
#    Retrieve the properties of the current video format and sink type 
#	@param hGrabber The handle to the grabber object.
#	@param *lWidth  This recieves the width of the image buffer.
#	@param *lHeight  This recieves the height of the image buffer.
#	@param *iBitsPerPixel  This recieves the count of bits per pixel.
#	@param *format  This recieves the current color format.
#	@retval IC_SUCCESS on success
#	@retval IC_ERROR if something went wrong.
                           
    GetImageDescription = tisgrabber.IC_GetImageDescription
    GetImageDescription.restype = C.c_int     
    GetImageDescription.argtypes = (GrabberHandlePtr,
                                    C.POINTER(C.c_long),
                                    C.POINTER(C.c_long),
                                    C.POINTER(C.c_int),
                                    C.POINTER(C.c_int),)
                      
     
     

    GetImagePtr = tisgrabber.IC_GetImagePtr
    GetImagePtr.restype = C.c_void_p
    GetImagePtr.argtypes = (GrabberHandlePtr,) 

                        
class TIS_CAM(object):
        @property
        def callback_registered(self):
            return self._callback_registered
      
        def __init__(self, unique_device_name):
            self._unique_device_name = unique_device_name
            
            self._handle = TIS_GrabberDLL.create_grabber()
          
            self._callback_registered = False
            self._frame = {'num'    :   -1,
                           'ready'  :   False}    
        
        
        def open(self):
            test = TIS_GrabberDLL.open_device_by_unique_name(self._handle,
                                                       self._unique_device_name)
            return test                                           

        def get_video_format_width(self):
            return TIS_GrabberDLL.get_video_format_width(self._handle)
            
        def get_video_format_height(self):    
            return TIS_GrabberDLL.get_video_format_height(self._handle)    


        def GetVideoFormats(self):
            self._Properties=[]         
            iVideoFormats = TIS_GrabberDLL.GetVideoFormatCount(self._handle)
            for i in range(iVideoFormats):
                self._Properties.append(TIS_GrabberDLL.GetVideoFormat(self._handle,i))         
            return self._Properties

        def GetInputChannels(self):
            self.InputChannels=[] 
            InputChannelscount = TIS_GrabberDLL.GetInputChannelCount(self._handle)
            for i in range (InputChannelscount):
                self.InputChannels.append(TIS_GrabberDLL.GetInputChannel(self._handle,i))
            return self.InputChannels

        def GetVideoNormCount(self):
            self.GetVideoNorm=[]
            GetVideoNorm_Count=TIS_GrabberDLL.GetVideoNormCount(self._handle)
            for i in range(GetVideoNorm_Count):
                self.GetVideoNorm.append(TIS_GrabberDLL.GetVideoNorm(self._handle, i))
            return self.GetVideoNorm
        
        def StartLive(self):
            Error = TIS_GrabberDLL.StartLive(self._handle, 1)
            return Error

        def StopLive(self):
            Error = TIS_GrabberDLL.StopLive(self._handle)
            return Error

 
        def SnapImage(self):
            Error = TIS_GrabberDLL.SnapImage(self._handle, 2000)
            return Error
 
 
        def GetImageDescription(self):
            
            lWidth=C.c_long()
            lHeight= C.c_long()
            iBitsPerPixel=C.c_int()
            COLORFORMAT=C.c_int()
            
            Error = TIS_GrabberDLL.GetImageDescription(self._handle, lWidth,
                                        lHeight,iBitsPerPixel,COLORFORMAT)
            return (lWidth.value,lHeight.value,iBitsPerPixel.value,COLORFORMAT.value)
        
        def GetImagePtr(self):
            
            ImagePtr = TIS_GrabberDLL.GetImagePtr(self._handle)
            
            return ImagePtr
           
        def GetImage(self):
            
            BildDaten = self.GetImageDescription()[:3]
            lWidth=BildDaten[0]
            lHeight= BildDaten[1]
            iBitsPerPixel=BildDaten[2]/8

            buffer_size = lWidth*lHeight*iBitsPerPixel*C.sizeof(C.c_uint8)            
            img_ptr = self.GetImagePtr()
            
            Bild = C.cast(img_ptr, C.POINTER(C.c_ubyte * buffer_size))
            
            img = np.ndarray(buffer = Bild.contents,
                         dtype = np.uint8,
                         shape = (lHeight,
                                  lWidth,
                                  iBitsPerPixel))
            return img
        
class TIS_grabber(object):
    #Initialisierung der Lib.    
    def InitLibrary(self):
        error=TIS_GrabberDLL.InitLibrary
        
        self.unique_device_names = None        
        self._Verbundene_Cam={}
        if error != 1:
            print "Error code: " + str(error)



    def Kamera_finden(self):
        test=TIS_GrabberDLL
        iDeviceCount =test.Anzahl_Cams
        self._funk=[]
        for i in range (iDeviceCount):
            self._funk.append(TIS_GrabberDLL.get_unique_name_from_list(i))
        
        return self._funk       
    
    def Kamera_verbinden(self, Cam):
        
        if Cam in self.Kamera_finden():
            if Cam not in self._Verbundene_Cam:
                self._Verbundene_Cam[Cam]=TIS_CAM(Cam)
            return self._Verbundene_Cam[Cam]

        
        

        



test=TIS_grabber()
test.InitLibrary()
Kamera_Namen = test.Kamera_finden()
test2 = test.Kamera_verbinden('DFK 21F04 30284D2F4')
a=test2.open() 
b=test2.get_video_format_width()    
c=test2.get_video_format_height()        
d=test2.GetVideoFormats()
e=test2.GetInputChannels()
f=test2.GetVideoNormCount()
g=test2.StartLive()
h=test2.SnapImage()        
i=test2.GetImageDescription()
j=test2.GetImagePtr()
k=test2.GetImage()

test_1=k[:,:,0]
test_2=k[:,:,1]
test_3=k[:,:,2]



x=test2.StopLive()      
  
        
        