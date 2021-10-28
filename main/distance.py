class Distance:
  marker_length = 3.1
  black_color = (0,0,0)
  blue_color = (255, 0, 0)
  green_color = (0, 255, 0)
  red_color = (0, 0, 255)
  yellow_color = (0,255,255)

  def distance(x,y):
    return ((x[0]-y[0])**2 + (x[1]-y[1])**2) ** (1/2)

  def real_distance(marker_length, std_length,color_length):
      return round(marker_length * color_length / std_length, 2)