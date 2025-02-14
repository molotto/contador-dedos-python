try:
    import cv2
    import mediapipe as mp
    import time


    #^ liga a câmera
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise RuntimeError("Erro ao acessar a câmera.")

    hands = mp.solutions.hands
    Hands = hands.Hands(max_num_hands=1)
    mpDwaw = mp.solutions.drawing_utils

    while True:
        success, img = video.read()
        frameRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        results = Hands.process(frameRGB) #^ analisa e detecta os pontos
        handPoints = results.multi_hand_landmarks #^ guarda os pontos da mão

        h, w, _ = img.shape #^ dimensões da imagem

        pontos = []

        if handPoints:
            for points in handPoints:
                mpDwaw.draw_landmarks(img, points,hands.HAND_CONNECTIONS) #^ desenha os pontos e conexões dos dedos

                for id, cord in enumerate(points.landmark): 
                    cx, cy = int(cord.x * w), int(cord.y * h) #^ converte os valores normalizados para pixels
                    pontos.append((cx,cy))

                dedos = [8,12,16,20] #^ dedo indicador, médio, anelar e mindinho
                contador = 0

                if pontos:
                    if pontos[4][0] < pontos[3][0]: #^ verifica se o polegar está levantado
                        contador += 1
                    for x in dedos:
                        if pontos[x][1] < pontos[x-2][1]:
                            contador +=1

                estados = {
                    0: "0",
                    1: "1",
                    2: "2",
                    3: "3",
                    4: "4",
                    5: "5"           
                }

                texto = estados.get(contador, "INDEFINIDO")
                    
                cv2.rectangle(img, (80, 10), (0,110), (76, 0, 103), -1)
                cv2.putText(img,str(contador),(0,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)
                cv2.putText(img,str(texto),(0,170),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

        cv2.imshow('image',img)

        if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:
            break
        
    cv2.destroyAllWindows()
    video.release()
except Exception as error:
    print (error)

