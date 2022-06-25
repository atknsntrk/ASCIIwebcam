import cv2
from fastapi import FastAPI, WebSocket
import numpy as np
import json
import asyncio

app = FastAPI()

#0 is internal webcam
video = cv2.VideoCapture(0)

#ascii scales
gscaleOne = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~i!lI;:,\"^`". '
gscaleTwo = "Ñ@#W$9876543210?!abc;:+=-,._           ";
gscaleThree = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '; 
gscaleFour = "oIIccvv::++!!~~\"\"..,,                       " 
gscaleFive = "@@BBRR**##$$PPXX00wwoo@@@@@@@@@@@@@@@@@@@@@@"

#SCALE changes the "sensitivity" of the gscales
#scale 1 begins at 15
#scale 2 begins at 20
#scale 3 begins at 15
#scale 4 begins at 20 but I like it the most at 40
#scale 5 begins at 20
SCALE = 15

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:

        _, frame = video.read()

        frame = cv2.flip(frame, 1)

        
        resized = cv2.resize(frame, (0,0), fx=0.1, fy=0.1)
        brightness = np.sum(resized, axis=2)

        height = int(len(brightness))
        width = int(len(brightness[0]))
        asciiTemp = []

        for x in range(height):
            temp = []
            for y in range(width):
                temp.append(gscaleThree[int(brightness[x][y]/SCALE)])
            asciiTemp.append(temp)

        
        for x in range(len(asciiTemp)):
            for y in range(len(asciiTemp[x])):
                if asciiTemp[x][y] == " ":
                    asciiTemp[x][y] = '&nbsp;'
            asciiTemp[x].append('<br/>')
            
        ascii = ''.join(str(item) for innerlist in asciiTemp for item in innerlist)

        data = {
            "ascii": ascii
        }

        await websocket.send_json(json.loads(json.dumps(data)))

        await asyncio.sleep(0.1)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


@app.get("/")
async def root():
    return{"It": "works"}