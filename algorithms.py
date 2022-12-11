#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import cv2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dist_thresholding(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    elements = bf.knnMatch(des1, des2, k=len(des1))
    results = []
    for element in elements:
        tempList = []
        for e in element:
            if threshold_value == -1:
                tempList.append(e)
            else:
                if e.distance < threshold_value:
                    tempList.append(e)
        results.append(tempList)
    return results

def nn(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    elements = bf.knnMatch(des1, des2, k=1)
    results = []
    for i in range(len(elements)):
        tempList = []
        if threshold_value == -1:
            tempList.append(elements[i][0])
        else:
            if elements[i][0].distance < threshold_value:
                tempList.append(elements[i][0])
        results.append(tempList)
    return results

def nndr(des1, des2, threshold_value) -> list:
    bf = cv2.BFMatcher()
    elements = bf.knnMatch(des1, des2, k=2)
    results = []
    for i in range(len(elements)):
        tempList = []
        r = elements[i][0].distance / elements[i][1].distance
        if threshold_value == -1:
            tempList.append(elements[i][0])
        else:
            if r < threshold_value:
                tempList.append(elements[i][0])
        results.append(tempList)
    return results
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# vim:set et sw=4 ts=4:


