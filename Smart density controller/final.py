import cv2
from tracker import *
import time
import math

con = 0
counting = ['none','none1']
counting1=['n1','n2']
timing=1
time_counting=1
vehicel_no_time=0
vehicel_no_ref=0

con1 = 0
counting2 = ['none','none1']
counting22=['n1','n2']
timing2=1
time_counting1=1
vehicel_no_time1=0
vehicel_no_ref=0

con3 = 0
counting3 = ['none','none1']
counting33=['n1','n2']
timing=1
time_counting2=1
vehicel_no_time2=0
vehicel_no_ref=0
#__________________________________________
tracker = EuclideanDistTracker()
tracker1 = EuclideanDistTracker()
tracker3 = EuclideanDistTracker()
#____________________________________________


# cap = cv2.VideoCapture("video.mp4")
video_capture_1 = cv2.VideoCapture ("highway.mp4")
video_capture_0 = cv2.VideoCapture ("video.mp4")
video_capture_03 = cv2.VideoCapture ("bikes_20210806171141352_s01.mp4")
#______________________________________________________



object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
object_detector1 = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
object_detector3 = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
#___________________________________________________________________

tim1=[0,0,0]
tim2=[0,0,0]
tim3=[0,0,0]


time_lis=[0,0,0]
def traffic_time_allocation(a,b,c,density,lane):
    time_lis.clear()
    if a>=6:
        time_lis.append(23)
    elif a>=4:
        time_lis.append(15)
    elif a>=2:
        time_lis.append(10)
    elif a>=0:
        time_lis.append(8)


    if b>=6:
        time_lis.append(23)
    elif b>=4:
        time_lis.append(15)
    elif b>=2:
        time_lis.append(10)
    elif b>=0:
        time_lis.append(8)
    
    if c>=6:
        time_lis.append(23)
    elif c>=4:
        time_lis.append(15)
    elif c>=2:
        time_lis.append(10)
    elif c>=0:
        time_lis.append(8)
    print("the list ----------------------->   ", time_lis,lane ,"> ",density)
    
    return time_lis
    





def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

start = time.time()

density1=[]
avg_density1=0

density2=[]
avg_density2=0

density3=[]
avg_density3=0

x_num=0
y_num=0
z_num=0

#_________________________________________________________________________________
while True:
    print("----------------------------------------------------------->",timing)
    ret0, frame = video_capture_0.read()
    ret1, frame1 = video_capture_1.read()
    ret3, frame3 = video_capture_03.read()
    
# _____________________________________________________frame1______________________________________________________________________
    if (ret0):
        if timing//10==time_counting:
            
            time_counting+=1
            density1.append(vehicel_no_time)
            avg_density1=sum(density1)/len(density1)

            # if avg_density1>=6:
            #     x=23
            # elif avg_density1 >=4:

             
            tim1=traffic_time_allocation(avg_density1,0,0,'lane 1',avg_density1)

            print("timing harshavardhan lane 1 ------------------------------->",tim1)

            x_num=tim1[0]
        

            if len(density1)==6:
                density1.pop(0)


            vehicel_no_time=0
        
       
        font = cv2.FONT_HERSHEY_SIMPLEX   
        cv2.putText(frame,
                    'NO OF VEHICLES f1 : '+str(con) +"   "+"  Timer : "+ str(timing), 
                    (10, 50),
                    font, 1,
                    (0, 0, 0), 
                    #(258, 104, 123), 
                    2, 
                    cv2.LINE_4)
            
        font = cv2.FONT_HERSHEY_SIMPLEX   
      
        cv2.putText(frame,'Vehicles passing in  10 sec : '+str(vehicel_no_time), (10, 100),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame,'density of the lane : '+str(avg_density1), (10, 150),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame,'Allotted timing :     '+ str(x_num), (700, 50),font, 1,(0, 0, 0), 2, cv2.LINE_4)
      
        
        # print("-------------------------------------->",vehicel_no_time)
        
        roi = frame[ 550: 720,0: 600] 
        cv2.rectangle(img=frame, pt1=(600, 720), pt2=(0,550), color=(0, 0, 255), thickness=2)

        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        detections = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>15000:                         
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])    
                
                                
        boxes_ids = tracker.update(detections)   
        counting.append(len(boxes_ids))  
        

        if counting[-1]!=counting1[-1]:
            counting1.append(len(boxes_ids))
            con += int(counting1[-1])
            vehicel_no_time+=int(counting1[-1])
        
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            
            cv2.putText(roi,str('car'), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
            
                               
        frame = rescale_frame(frame, percent=50)
        # circle=cv2.circle(frame, (350, 20), 2, (0, 255, 0), 23)
        # cv2.imshow("circle",circle)
        # cv2.imshow("Frame", frame)
        # cv2.imshow("Fe", mask)
# _____________________________________________________frame2______________________________________________________________________
        
        
    if (ret1):
        # density1=
        
        if timing//10==time_counting1:
            
            time_counting1+=1
            density2.append(vehicel_no_time1)
            avg_density2=sum(density2)/len(density2)
            tim2=traffic_time_allocation(0,avg_density2,0,'lane 2',avg_density2)
            if len(density2)==6:
                density2.pop(0)
            
            vehicel_no_time1=0

            y_num=tim2[1]

        

        font1 = cv2.FONT_HERSHEY_SIMPLEX   
        cv2.putText(frame1,
 
                    'NO OF VEHICLES f2 : '+str(con1) +"   "+"  Timer : "+ str(timing), 
                    # 'NO OF VEHICLES : '+str(con1), 
                    (10, 50),
                    font1, 1,
                    (0,0,0), 
                    #(258, 104, 123), 
                    2, 
                    cv2.LINE_4)
        
        font = cv2.FONT_HERSHEY_SIMPLEX  

       
        cv2.putText(frame1,'Vehicles in 10 sec : '+str(vehicel_no_time1), (10, 100),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame1,'density of the lane : '+str(avg_density2), (10, 150),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame1,'Allotted timing :     '+ str(y_num), (700, 50),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        # cv2.putText(frame1,'light ', (10, 300),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        
        # roi1 = frame1[ 550: 720,100: 600] 
        roi1 = frame1[ 550: 720,400: 900] 
        
        # cv2.rectangle(img=frame1, pt1=(600, 720), pt2=(100,550), color=(0, 0, 255), thickness=2)
        cv2.rectangle(img=frame1, pt1=(900, 720), pt2=(400,550), color=(0, 0, 255), thickness=2)

        mask1 = object_detector1.apply(roi1)
        _, mask1 = cv2.threshold(mask1, 254, 255, cv2.THRESH_BINARY)
        contours1, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        detections1 = []

        for cnt1 in contours1:
            area1 = cv2.contourArea(cnt1)
            if area1 > 1300:                         
                x1, y1, w1, h1 = cv2.boundingRect(cnt1)
                detections1.append([x1, y1, w1, h1])    
                
                            
        boxes_ids1 = tracker1.update(detections1)   
        counting2.append(len(boxes_ids1))  
        

        if counting2[-1]!=counting22[-1]:
            counting22.append(len(boxes_ids1))
            con1 += int(counting22[-1])
            vehicel_no_time1+=int(counting22[-1]) 
            print("counting ---------------------------------------->",vehicel_no_time1)


        
        for box_id1 in boxes_ids1:
            x1, y1, w1, h1, id = box_id1
            
            cv2.putText(roi1,str(len(boxes_ids1)), (x1, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
        
        # cv2.imshow("Frame1", frame1)
        # cv2.imshow("Fe", mask1)
        frame1 = rescale_frame(frame1, percent=50)
# _____________________________________________________frame3______________________________________________________________________
    if (ret3):

        if timing//10==time_counting2:
            
            time_counting2+=1

            density3.append(vehicel_no_time2)

            avg_density3=sum(density3)/len(density3)
            tim3=traffic_time_allocation(0,0,avg_density3,'lane 3',avg_density3)
            z_num=tim3[2]
            if len(density3)==6:
                density3.pop(0)

            

            vehicel_no_time2=0
        
        font3 = cv2.FONT_HERSHEY_SIMPLEX   
        cv2.putText(frame3,
 
                    # 'NO OF VEHICLES f3 : '+str(con3),
                    'NO OF VEHICLES f2 : '+str(con3) +"   "+"  Timer : "+ str(timing),
                    (10, 50),
                    font3, 1,
                    (0, 0, 0), 
                    #(258, 104, 123), 
                    2, 
                    cv2.LINE_4)
        
        font = cv2.FONT_HERSHEY_SIMPLEX   
        cv2.putText(frame3,'Vehicles in 10 sec : '+str(vehicel_no_time2), (10, 100),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame3,'density of the lane : '+str(avg_density3), (10, 150),font, 1,(0, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame3,'Allotted timing :     '+ str(z_num), (700, 50),font, 1,(0, 0, 0), 2, cv2.LINE_4)
          
        # roi3 = frame3[ 350: 538,170: 650]
        roi3 = frame3[ 550: 683,270: 850] 


        # cv2.rectangle(img=frame3, pt1=(650, 538), pt2=(170,350), color=(0, 0, 255), thickness=2)
        cv2.rectangle(img=frame3, pt1=(850, 683), pt2=(270,550), color=(0, 0, 255), thickness=2)



        mask3 = object_detector3.apply(roi3)
        _, mask3 = cv2.threshold(mask3, 254, 255, cv2.THRESH_BINARY)
        contours3, _ = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        detections3 = []

        for cnt3 in contours3:
            area3 = cv2.contourArea(cnt3)
            if area3>800:                         
                x3, y3, w3, h3 = cv2.boundingRect(cnt3)
                detections3.append([x3, y3, w3, h3])    
                
                            
        boxes_ids3 = tracker3.update(detections3)  
        counting3.append(len(boxes_ids3))  
        

        if counting3[-1]!=counting33[-1]:
            counting33.append(counting3[-1])

            con3 += int(counting3[-1])
            vehicel_no_time2+=int(counting3[-1])

        for box_id3 in boxes_ids3:
            x3, y3, w3, h3, id = box_id3
         
            cv2.putText(roi3,str(len(boxes_ids3)), (x3, y3 - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi3, (x3, y3), (x3 + w3, y3 + h3), (255, 255, 255), 2)
        
            
                               
        counting3=[]
        frame3 = rescale_frame(frame3, percent=50)

        # cv2.imshow("Frame3", frame3)
    
    
    # print("--------#####------------------------------>",frame3.shape[0],frame3.shape[1])
    frame4= cv2.imread('photo.png')
    
    

    circle=cv2.circle(frame, (495, 20), 2, (0, 255, 0), 20)
    circle=cv2.circle(frame1, (495, 20), 2, (0, 255, 0), 20)
    circle=cv2.circle(frame3, (495, 20), 2, (0, 255, 0), 20)

    im_h = cv2.hconcat([frame, frame1])
    im_h1 = cv2.hconcat([frame3, frame4])

    im_v = cv2.vconcat([im_h, im_h1])
    

    cv2.imshow('cars', im_v)

    end = time.time()
    
    num=end - start
    timing = math.ceil(num)
    # print("-------------------------->",timing)

    # a=avg_density1
    # b=avg_density2
    # c=avg_density3
    # traffic_time_allocation(a,b,c)

    # print("+++++++++++++++++++++++++++++++>>>>", a,b,c)

    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        
        break



video_capture_0.release()
video_capture_1.release()
video_capture_03.release()

cv2.destroyAllWindows()

# print("????????????????????????  ",tim1)


# print("density === ",density1)