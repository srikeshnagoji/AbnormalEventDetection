import Testing
import FramesToFeatures
import cv2
import numpy as np
import os
import pickle
#v
import VideoToFrames
import Training
import VidToAllFramesIO
#^

#-----------------------------------------------------------------------------------------------------------------------
#pre define the NUMBER of videos that are going to be given for training
vid_nos=51
#NUMBER of files in the current training cache (to be looked into before testing!!)
cache_range=63 #50

##v      Directories:

#save%d.p files directory:
dir_save='/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/Abnormal-Event-Detection-master/Code/training_cache/save'
#Test frames directory (for testing process)
dir_test_Frames='/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/frames/Test/Test1/'
#Train frames directory (for training process)
dir_train_Frames="/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/frames/Train/Train1/"

##^
#-----------------------------------------------------------------------------------------------------------------------
def main():
        ##v      user chooses the function1
        
        print "\nDo you want to:\n1. Extract frames\n2. Train and test\n"
        user_reqs=str(raw_input("\n\n(1/2) :>>   "))
        if (user_reqs=="1"):
                VideoToFrames.videoToFrames()               
        ##^
        print "\nEnter the MODE : \n"
        print "\nFor training mode type <load> and press enter..."
        print "For testing mode press enter...\n"
        user_request=str(raw_input("\n:>> "))
        S=[]
        
        if(user_request!="load"):
                #this is testing mode
                print "\n---------------You have selected <testing mode>---------------\n"
                print "\nImporting training data from cached copy..."

                for file_no in range(1,cache_range+1):     #<     'cache_range+1' instead of number
                        if(os.path.isfile(dir_save+str(file_no)+'.p')):
                                S += pickle.load(open(dir_save+str(file_no)+'.p', 'rb'))
        else:
                #this is training mode
                print "\n---------------You have selected <training mode>---------------\n"
                S=preprocess_and_training() #ref below...
                #v
                filecount=0
                for file_no in range(1,vid_nos+1):
                        if(os.path.isfile(dir_save+str(file_no)+'.p')):
                                filecount+=1
                        else:
                                pickle.dump(S, open(dir_save+str(file_no)+'.p', 'wb'))
                                break

                #pickle.dump(S, open(dir_save+'1.p', 'wb')) #CHANGE THE save file NUMBER HERE.  %d.p   <<<<<<<<<<<<<<<(FOR EACH TRAINING)
        
        print "\nlength of S: ",len(S)
        print len(S)
#v
        Testing.import_and_test_abnormal(S)
#^
###########################################################################################################################################################################
                        
def preprocess_and_training():
        #Generate features from it
        
        
        i=0
        file_list1=[]   
        for path, subdirs, files in os.walk(dir_train_Frames):
                for name in subdirs:
                
                        #print os.path.join(path, name)
                        file_list1.append(str(os.path.join(path, name)))
                        #print str(file_list1)
                        

##        file_list2=[]   
##        for path, subdirs, files in os.walk('/Users/srikeshnagoji/Desktop/myversion/frames/Train/Train2/'):
##                for name in subdirs:
##                        #
##                        file_list2.append(str(os.path.join(path, name)))
##                        #print path+name
        
        feature_list=[]
        
        for folder in file_list1:
                feature_list.append(FramesToFeatures.framesToFeatures(root=folder,pattern = "*.tif"))
                i+=1
##                print "files done (appended to feature list):",i #(folders done)
                
##        for folder in file_list2:
##                feature_list.append(FramesToFeatures.framesToFeatures(root=folder,pattern = "*.tif"))
##                i+=1
##                print "files done:",i
                
        #feature_list=FramesToFeatures.framesToFeatures(root='/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/Abnormal-Event-Detection-master/Code/frames/',pattern="*.tif")
        print "Total Feature generated : ",len(feature_list[0]) #original code- remove [0]
        
        #return
        #Training for Sparse Combination Learning
        
        S=[]
        B=[]
        ############################## PCA ###############
        feature_list=[i[:100] for i in feature_list]#this is PCA
        #v
        print "After applying PCA: len(feature_list) = "+str(len(feature_list[0]))
        print "lenth of each feature now: "+str(len(feature_list[0][0]))+"\n"
        #^
        ################################################

        for set in feature_list: #this loop runs only once since only one block is there in 3d array -feature_list
                ##print len(set) # =100
                S_temp,B_temp=Training.training_algorithm(set,S) # "Training" to be removed ...if Training.py is not used
                S+=S_temp
                B+=B_temp
                #S.append(S_temp)
                #B.append(S_temp)
        
        
        print "################Final S Vector###################"
        print "\n"
        print S
        print "\n"
        print "Length of S is : ",len(S)
        print "##################################################"
        
        return S

###########################################################################################################################################################################
        
main()


#where ever the modified or extra code is inserted that PART of the code is marked like this ##v and ##^
##v is starting
##^ is ending
