import time
import pyautogui
from pynput import mouse


# activity records
events =  []

# recording status
recording = False


# last time activity
last_time = None

def on_move(x,y) :
    global last_time
    if not recording :
        return
    
    current_time = time.time();
    
    delay = current_time - last_time
    
    events.append({
        "type" : "move",
        "x" : x,
        "y" : y,
        "delay" : delay
    })
    
    last_time = current_time
    
def on_click(x,y,button,pressed) :
    global last_time
    
    if not recording :
        return
    
    if pressed :
        current_time = time.time()
        
        delay = current_time - last_time
        
        events.append({
            "type" : "click",
            "x" : x,
            "y" : y,
            "button" : str(button),
            "delay" : delay
        })
        
        last_time = current_time
        
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click
)

listener.start()


print("<======= Zet Macro Recorder =======>")
print("Press 'r' to start recording")
print("Press 's' to stop recording")
print("Press 'p' to play recording master")

while True :
    command = input("Enter command : ").lower()
    
    if command == "r" :
        events.clear()
        
        for i in range(3,0,-1) :
            print(i)
            time.sleep(1)
        
        recording = True
        last_time = time.time()
        
        print("🔴 Recording....")
        
    elif command == "s" :
        recording = False
        print("🟢 Recording stopped")
        print("Recorded evennts : ", len(events))
        
    elif command == "p" :
        for event in events :
            time.sleep(event["delay"])
            
            if event["type"] == "move" :
                pyautogui.moveTo(event["x"], event["y"])
                
            elif event["type"] == "click" : 
                pyautogui.click(
                    event["x"],
                    event["y"],
                )
                
        print("✅ Playback completed")
        pyautogui.screenshot("success.png")
            
    elif command == "q" :
        print("Exiting...")
        listener.stop()
        recording = False
        break
