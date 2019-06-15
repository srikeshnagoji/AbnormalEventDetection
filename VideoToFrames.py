import numpy as np
import cv2
import os
import time
import sys
import argparse
##v
print(cv2.__version__)
import VidToAllFramesIO
##^
#def main():
def videoToFrames():
#-----------------------------------------------------------------------------------------------------------------------
        ##v      Directories: 
        
        #SOURCE directory of VIDEOS from which frames are to be extracted:
        diry="/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/frames/source directory of videos"
        #Test frames directory (for extraction and dumping)
        dir_test_frames="/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/frames/Test/Test1/_gt"
        #Train frames directory (for extraction and dumping into it)
        dir_train_frames="/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/frames/Train/Train1/_gt"
        
        ##^
#-----------------------------------------------------------------------------------------------------------------------

        print "Opening Video IO\n"
        user_reqs=str(raw_input("Do you want to extract frames from...\n1. existing video \n2. From webcam\n(1/2): "))
        if(user_reqs=="1"):#existing video
                print "source directory: "+diry
                #v
                user_request=str(raw_input("\n1. one frame per second(default)\n2. all frames in the video\npress enter for default mode\n\n:>>"))
                if (user_request=="2"):
                        success=VidToAllFramesIO.vidToAllFrames(diry,dir_test_frames,dir_train_frames)
                else:
                        user_request="0"
                #^
                #from here to ...
                        vid_name=str(raw_input("\n Enter the video name with extention(format): "))
                        user_reqs2=str(raw_input("\n\n Extract frames for \n1. Training\n2. Testing \n\n(1/2):>> "))
                        numOfFrames = 0
                        if (user_reqs2=="2"):#extract into test1/_gt
                                numOfFrames=extractImages(diry+"/"+vid_name,dir_test_frames) # parameter passing--- (pathIn, pathOut)
                                print "\n\nframes are extracted into : "+dir_test_frames
                        elif (user_reqs2=="1"):#extract into train1/_gt
                                numOfFrames=extractImages(diry+"/"+vid_name,dir_train_frames)
                                print "\n\nframes are extracted into : "+dir_train_frames
                        else:
                                print "\ninvalid option" # ...till here it is indented

                
        else:#webcam
                
                user_reqs3=str(raw_input("\n\n Extract frames for \n1. Training\n2. Testing \n\n:>> "))
                if (user_reqs3=="2"):
                        convertToFrames(10,dir_test_frames)
                elif (user_reqs3=="1"):
                        convertToFrames(10,dir_train_frames)
                else:
                        print "\ninvalid option"


#########################################################################################################################################################################

                
                   
def extractImages(pathIn, pathOut):
        directory=pathOut
        user_req4=str(raw_input("\n\nAre you sure you want to clear the existing frames in :"+directory+"(y/n): "))
        if(user_req4=="y"):
        ##v
                # If previous frames exist clear them first
                if os.path.exists(directory):
                        filelist = [ f for f in os.listdir(directory)]
                        #print f
                        for f in filelist:
                                os.remove(str(directory+"/"+f))
                ##v
                print '\n!! all frames in the directory are cleared.\n\n--------------------------------\n\n'
                user_request=str(raw_input("press enter to confirm storing frames : "))

                count = 0
                vidcap = cv2.VideoCapture(pathIn)
                success,image = vidcap.read()
                success = True
                while success:
                        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    
                        success,image = vidcap.read()
                        print "Read a new frame: ",success
                        #
                        if (success == False):
                                break;
                        cv2.imwrite( pathOut + "/frame%d.tif" % count, image)     
                        count = count + 1      #frame for each one sec
                        #count = count + 0.5     #frame for each half sec
                #v
                print "<End of video>"
                return count;
                #^
        else:
                print "Frames are not extracted !"
                #v
                return count;
                #^
 
##^

#########################################################################################################################################################################



def convertToFrames(time_to_save,save_path):
        print "\n\n"
        
        #Capture arguments
        directory=save_path;
        
        cap = cv2.VideoCapture(0)

        # File index
        i=0
        ##v
        print 'directory of the frames is : '+directory+'\n--------------------------------'
        #temp=os.listdir(directory)
        #print temp
        ##^
        ##v
        user_req=str(raw_input("\n\nAre you sure you want to clear the existing frames in :"+directory+"(y/n): "))
        if(user_req=="y"):
        ##^
                # If previous frames exist clear them first
                if os.path.exists(directory):
                        filelist = [ f for f in os.listdir(directory)]
                        #print f
                        for f in filelist:
                                os.remove(str(directory+"/"+f))
                ##v
                print '\n!! all frames in the directory are cleared.\n\n--------------------------------\n\n'
                user_request=str(raw_input("press enter to confirm storing frames : "))
                ##^
                if(user_request==""):
                        #Timer start
                        s_time=time.time();
                                        
                        # Collecting and storing frames         
                        while(True):
                                # Capture frame-by-frame
                                ret, frame = cap.read()
                                
                                # Create directory to store frame
                                if not os.path.exists(directory):
                                        os.makedirs(directory)
                                                
                                # Store the resulting frame
                                os.chdir(directory);    
                                cv2.imwrite('frame'+str(i)+'.png',frame)
                                os.chdir("..");
                                i+=1
                                
                                # End after user specified seconds
                                if(time.time()-s_time>=time_to_save):
                                        break


                        # When everything done, release the capture
                        cap.release()
                        cv2.destroyAllWindows()
                        print '\nframes are captured from the webcam into the directory!'
                else:
                        print 'directory: '+directory+'\nis now empty!\n'
        else:
                print 'frames not captured!!\n'
                
#main()
