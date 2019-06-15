import cv2
import numpy as np
#v
import os
import FramesToFeatures
#^

#v

#-----------------------------------------------------------------------------------------------------------------------

#Test frames directory (for testing process)
dir_test_Frames='/Users/srikeshnagoji/Desktop/PROJECT_PACKAGE/frames/Test/Test1/'


#-----------------------------------------------------------------------------------------------------------------------

def import_and_test_abnormal(S):
        print "\n\n"
        print "---------------------------------------------------------------------------------------"
        print "                                   TESTING PHASE"
        print "---------------------------------------------------------------------------------------"
        print "\n\n"

        #Input the frame of the video to be tested
        
        test_folder_list=[]
        
        for path, subdirs, files in os.walk(dir_test_Frames):
                for name in subdirs:
                        #print os.path.join(path, name)
                        test_folder_list.append(str(os.path.join(path, name)))  
        
        feature_list=[]
        
        for folder in test_folder_list:
                if("_gt" in folder):
                        feature_list=FramesToFeatures.framesToFeatures(root=folder,pattern="*.tif")
                else:
                        feature_list=FramesToFeatures.framesToFeatures(root=folder,pattern="*.tif")
                
                file_list,result=testing_algorithm(feature_list,S,0.00001915625) #0.00001915625
                
                
                print "#####################################"
                print folder," video is :: "
                
                if(len(result)==0):
                        print "Normal"
                else:
                        for res in result:
                                print res
                        continue_key=raw_input("Press enter to show the abnormal frames : ")
                        continue_key="1"

                        key_str=""
                        while(key_str==""):
                                if(continue_key=="1"):
                                        FramesToFeatures.show_image(folder,file_list)
                                        key_str=raw_input("Press 1 to continue or enter to replay : ")
                                        
                print "program terminated.\n#####################################"

#########################################################################################################################################################################

#^
def testing_algorithm(x,S,T):
	#print S
	R=getR(S);
	#print R	
	return_list=[]
	file_list=[]
	#print xs
	i=0
	time=0
	flag=0
	for xi in x:
		i+=1
		flag=0
		mean=[]
		for Ri in R:
			val=np.linalg.norm(np.dot(np.array(Ri),np.array([xi])))**2
			mean.append(val)
			
			if(val<T):
				flag=1
				break		
		if(i==208):
				i=0
				min_mean=min(mean)
				if((str("Abnormal at time"+str(time)+" seconds.") not in return_list) and min_mean>0.00000045): 	
					return_list.append(str("Abnormal at time"+str(time)+" seconds."))
					file_list.append(time)
					#v
					#print val
					#^
				#print "time:small : ",time,min_mean
				time+=5
				mean=[]
			
	return file_list,return_list

###############################################################################################################################################

def getR(S):
	R=[];
	m=0.00000003
	
	for Si in S:
		Si = np.array(Si);
		Si_transpose = np.transpose(Si);
		Si_T_Si=np.dot(Si_transpose,Si)
		if(np.linalg.det(Si_T_Si)==0):
			Si_T_Si=np.add(Si_T_Si,m*np.eye(10,10))
		
		Ri=np.subtract(np.dot(Si,np.dot(np.linalg.inv(Si_T_Si),Si_transpose)),np.identity(len(Si)));
		R.append(Ri);

	return R;
