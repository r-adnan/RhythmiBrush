import time
import math

class Brush:
    def __init__(self, color, size):
        self.color = color
        self.size = size
        self.target_color = color
        self.start_time = time.time()

    def set_target_color(self, target_color):
        self.target_color = target_color

    def update(self):
        t = (time.time() - self.start_time) / 123  # Adjust the divisor for speed
        t = min(t, 1)  # Clamp between 0 and 1

        # Update color using lerp
        self.color = (
            int(self.lerp(self.color[0], self.target_color[0], t)),
            int(self.lerp(self.color[1], self.target_color[1], t)),
            int(self.lerp(self.color[2], self.target_color[2], t))
        )

        # Vibrate size and color
        valz = self.vibrate(self.size, 4, 1, time.time())
        self.size = valz if  3 < valz < 30 else 6
        self.color = (
            int(self.vibrate(self.color[0], 50, 1, time.time())),
            self.color[1],
            self.color[2]
        )

    def lerp(self, a, b, t):
        
        return a + t * (b - a)


    def vibrate(self, value, amplitude, frequency, time):
        
        return int(value + amplitude * math.sin(frequency * time))

# Example usage
# brush = Brush((255, 0, 0), 10)
# brush.set_target_color((0, 255, 0))
# 
# while True:
    # brush.update()
    # print(brush.color, brush.size)
    # time.sleep(0.1)
