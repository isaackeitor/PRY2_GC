import math

class vector:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def __add__(self, v):
    return vector(self.x + v.x, self.y + v.y)
  
  def __sub__(self, v):
    return vector(self.x - v.x, self.y - v.y)
  
  def __mul__(self, k):
    return vector(self.x * k, self.y * k)
  
  def sin(self):
    if self.magnitud() == 0:
      return 0
    return self.y / self.magnitud()
  
  def cos(self):
    if self.magnitud() == 0:
      return 0
    return self.x / self.magnitud()
  
  def setAngle(self, angle):
    magnitude = self.magnitud()

    self.x = magnitude * math.cos(angle)
    self.y = magnitude * math.sin(angle)

  def magnitud(self):
    return math.hypot(self.x, self.y)
  
  def copy(self):
    return vector(self.x, self.y)
  