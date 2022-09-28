import cv2 as cv
import numpy as np
import pyautogui 

#) Desenvolva um software que acesse a câmera do 
#dispositivo e através da detecção de algum 
#objeto pela cor dele, capture a posição do 
#mesmo e de acordo com a movimentação da 
#posição desta cor, mova o mouse do 
#computador.

# 1 cor mouse
# 2 cor click
# 3 2 click
# 4 3 fecha


camera = cv.VideoCapture(0, cv.CAP_DSHOW)

screen = pyautogui.size()



while 1:
    _, frame = camera.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    blueLower = np.array([0, 231, 188]) #Mouse Control
    blueUpper = np.array([135, 200, 187])

    redLower = np.array([161, 174, 160])#if see the red close the program
    redUpper = np.array([255, 255, 255])
    
    yelloLwower = np.array([0, 152, 196]) #if see the color click whit the mouse
    yellowUpper = np.array([0, 230, 187])
    
    purpleLower = np.array([136, 201, 188]) #if see the color double click whit the mouse
    purpleUpper = np.array([255, 255, 255])
    
    mask = cv.inRange(hsv, blueLower, blueUpper) 
    mask2 = cv.inRange(hsv, redLower, redUpper)
    mask3 = cv.inRange(hsv, yelloLwower, yellowUpper)
    mask4 = cv.inRange(hsv, purpleLower, purpleUpper)

    result = cv.bitwise_and(frame, frame, mask=mask,mask2,mask3,mask4)

    gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    _, borda = cv.threshold(gray, 3, 255, cv.THRESH_BINARY)

    contornos, _ = cv.findContours(
        borda, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    #if see the color close the program
    for c in contornos:
        area = cv.contourArea(c)
        if area > 3000:
            M = cv.moments(c)
            if (M["m00"] == 0): M["m00"] = 1
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            cv.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv.putText(frame, "Red", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            pyautogui.hotkey('esc') #tecla pra sair do programa
            break
    
    #if see the color click whit the mouse
    for c in contornos:
        area = cv.contourArea(c)
        if area > 3000:
            M = cv.moments(c)
            if (M["m00"] == 0): M["m00"] = 1
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            cv.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv.putText(frame, "Yellow", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            pyautogui.click()
            break

    #if see the color double click whit the mouse
    for c in contornos:
        area = cv.contourArea(c)
        if area > 3000:
            M = cv.moments(c)
            if (M["m00"] == 0): M["m00"] = 1
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            cv.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv.putText(frame, "Purple", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            pyautogui.doubleClick()
            break

    #Mouse Control   
    for contorno in contornos:
        area = cv.contourArea(contorno)
        if area > 800:
            (x, y, w, h) = cv.boundingRect(contorno)
            #cv.drawContours(frame, contorno, -1, (255,0,0), 2)
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
            cv.putText(
                frame,
                str(f"x: {x} y: {y}"),
                (x, y-20),
                cv.FONT_HERSHEY_SIMPLEX,
                1, 1
            )

            x = x * screen[0] / frame.shape[1]
            y = y * screen[1] / frame.shape[0]
            pyautogui.moveTo(x, y)
            

    #cv.imshow("result mask", borda)
    cv.imshow("result", frame)
    k = cv.waitKey(60)
    if k == 27:
        break

camera.release()
cv.destroyAllWindows()