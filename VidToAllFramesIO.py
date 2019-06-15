import cv2
import os

def vidToAllFrames(src_diry,dir_test_frames,dir_train_frames):
  diry=src_diry
  print "source directory: "+diry
  user_reqs=str(raw_input("\n Enter the video name with extention(format): "))


  user_reqs2=str(raw_input("\n\n Extract frames for \n1. Training\n2. Testing \n\n:>> "))
  if (user_reqs2=="2"):
    pathOut=dir_test_frames
    print "\n\nframes will be extracted into : ",pathOut
  elif (user_reqs2=="1"):
    pathOut=dir_train_frames
    print "\n\nframes will be extracted into : ",pathOut
  else:
    print "\ninvalid option"
  if (user_reqs2=="1" or user_reqs2=="2"):
      
    directory=pathOut
    user_req4=str(raw_input("\n\nAre you sure you want to clear the existing frames in :"+directory+"(y/n): "))
    if(user_req4=="y"):
    ##
      # If previous frames exist clear them first
      if os.path.exists(directory):
              filelist = [ f for f in os.listdir(directory)]
              #print f
              for f in filelist:
                      os.remove(str(directory+"/"+f))
      ##
      print '\n!! all frames in the directory are cleared.\n\n--------------------------------\n\n'
      user_request=str(raw_input("press enter to confirm storing frames : "))


      vidcap = cv2.VideoCapture(diry+"/"+user_reqs)
      success,image = vidcap.read()
      count = 0
      success = True
      while success:
        success,image = vidcap.read()
        if (success==False):
            break;
        cv2.imwrite(pathOut+"/frame%d.tif" % count, image)     # save frame as tif file
##        if cv2.waitKey(10) == 27:                     # exit if Escape is hit
##            break
        count += 1
      print "\n DONE !!!"
    else:
      print "\nframes are not captured!"
  else:
    print "\nprogram terminated!!"
  return success
