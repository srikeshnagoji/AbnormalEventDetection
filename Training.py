import Testing
import FramesToFeatures
import cv2
import numpy as np
import os
import pickle
#v
import VideoToFrames
#^


#########################################################################################################################################################################
        
def training_algorithm(X,S):
        #Training Section using Sparse Combination Learning
        #V  
        print str(len(S)) +" is the size of initial S"
        print str(len(X)) +" is the number of given features to be learnt (len(X))"
        #^
        print "\n\n"
        print "---------------------------------------------------------------------------------------"
        print "                                   TRAINING PHASE"
        print "---------------------------------------------------------------------------------------"
        print "\n\n"
        
        #######
        #Inputs
        #######
        #X=feature_list
        #######
        
        Xc=X
        S=[]
        B=[]
        gamma=[]
        i=1
        
        #Algorithm
        
        while(len(Xc)>10):
                #Create the initial dictionary Si using kmeans
                
                criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                flags = cv2.KMEANS_RANDOM_CENTERS
                print "Length of Xc is : ",len(Xc)
                compactness,labels,centers = cv2.kmeans(np.array(Xc,dtype="float32"),10,None,criteria,10,flags)
                centers=[(sum(val)/len(val)) for val in centers]
                Si=[centers]
                #
                print "Si"
                print Si
                print "len(Si): "+str(len(Si))
                
                
                #Reset Gamma and Beta i for next Vector generation
                
                gamma=[]
                Bi=[]
                history_2=0
                history_1=0
                epoch=0
                max_epoch=10
                start=1
                
                while(start==1 or start==2 or deltaL<0):
                        
                        if(start==2):
                                start=0
                        if(start==1):
                                deltaL=0
                                start=2
                                L2=0
                                L1=0
                        ####################Training ################
                        Bi=optimise_beta(Si,Xc)
                        Si=np.subtract(np.array(Si),(0.0001*deltaL))
                        gamma=optimise_gamma(Si,Xc,Bi,0.04)##
                        ####################Finding Loss ################
                        L1=L2
                        L2=evaluate_L(Si,Xc,Bi,gamma)
                        ####################Comparing loss ################
                        deltaL=L2-L1
                        #Print new Values
                        
                        print "\n\n"
                        print "*************Value in Iteration******************"
                        print "L = ",L2
                        epoch+=1
##                        print "Epoch : ",epoch
                        print "DeltaL : ",deltaL
                        print "*************************************************"
                        print "\n\n"
                        
                S.append(Si)
                B.append(Bi)
                
                print "\n\n"
                print "------New vector generated--------"
                print "Si = ",S
                print "S vector length= ",len(S)
                print "----------------------------------"
                print "\n\n"
                
                #Removing computed features
                
                change_index=0
                #print gamma
                for val in range(len(gamma)):
                        if(gamma[val]==0):
                                del Xc[val-change_index]
                                change_index+=1
                print "Change index"+str(change_index)              
                #Increment counter
                i+=1
                
        #Return Generated Vector set and Beta
        
        return S,B

#########################################################################################################################################################################

def optimise_beta(Si,Xc):
        #Using equation 6 optimise beta value
        
        beta=[]
        Si = np.array(Si)
        Si_transpose = np.transpose(Si)
        m=0.00000003
        
        #print Si.shape
        #print Si_transpose.shape
        
        for xj in Xc:
                numpy_xj=np.array([xj])
                Si_T_Si=np.dot(Si_transpose,Si)
                
                if(np.linalg.det(Si_T_Si)==0):
                        Si_T_Si=np.add(Si_T_Si,m*np.eye(10,10))
                        
                inverse_sit=np.linalg.inv(Si_T_Si)
                dot_in_si=np.dot(inverse_sit,Si_transpose)
                itr_beta=np.dot(dot_in_si,numpy_xj)
                beta.append(itr_beta)
        #print beta
        return beta

#########################################################################################################################################################################
        
def optimise_gamma(Si,Xc,Bi,lamda):
        #Using equation 9 optimise gamma value
        
        gamma=[]
        Si = np.array(Si)
        
        for xj in range(len(Xc)):
                #print ((np.linalg.norm(np.subtract(np.array([Xc[xj]]),np.dot(Si,np.array(Bi[xj])))))**2)
                if((((np.linalg.norm(np.subtract(np.array([Xc[xj]]),np.dot(Si,np.array(Bi[xj])))))**2)**2)<lamda):
                        gamma.append(1)
                else:
                        gamma.append(0)
        print gamma                      
        return gamma


#########################################################################################################################################################################

def evaluate_L(Si,Xc,Bi,gamma):
        #Using equation 9 optimise gamma value
        
        L=0
        Si = np.array(Si)
        temp_l=[]
        
        for xj in range(len(Xc)):
                l_iter_val=gamma[xj]*(((np.linalg.norm(np.subtract(np.array([Xc[xj]]),np.dot(Si,np.array(Bi[xj])))))**2)**2)
                temp_l.append(l_iter_val)
        
        return sum(temp_l)

#########################################################################################################################################################################
