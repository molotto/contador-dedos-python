try:
    import cv2
    import mediapipe as mp
    import time

    video = cv2.VideoCapture(0)

    hands = mp.solutions.hands
    Hands = hands.Hands(max_num_hands=1)
    mpDwaw = mp.solutions.drawing_utils

    while True:
        
        success, img = video.read()
        frameRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = Hands.process(frameRGB)
        handPoints = results.multi_hand_landmarks
        h, w, _ = img.shape
        pontos = []
        if handPoints:
            for points in handPoints:
                mpDwaw.draw_landmarks(img, points,hands.HAND_CONNECTIONS)
                for id, cord in enumerate(points.landmark):
                    cx, cy = int(cord.x * w), int(cord.y * h)
                    pontos.append((cx,cy))

                dedos = [8,12,16,20]
                contador = 0
                if pontos:
                    if pontos[4][0] < pontos[3][0]:
                        contador += 1
                    for x in dedos:
                        if pontos[x][1] < pontos[x-2][1]:
                            contador +=1

                estados = {
                    0: "1",
                    1: "2",
                    2: "3",
                    3: "4",
                    4: "5",
                    5: "6"
                }

                texto = estados.get(contador, "INDEFINIDO")
                    
                cv2.rectangle(img, (80, 10), (0,110), (76, 0, 103), -1)
                cv2.putText(img,str(contador),(0,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)
                cv2.putText(img,str(texto),(0,170),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

        cv2.imshow('image',img)
        if cv2.waitKey(1) == ord('q'):
            break
        
        if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
            break      

    cv2.destroyAllWindows()
    video.release()
except Exception as error:
    print (error)

