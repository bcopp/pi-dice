from gpiozero import LED 
from gpiozero import Button
from time import sleep
import time
from random import randint

print("")
print("~~~~~~ PI-DICE ~~~~~~")
print("Author <Brendan Copp>")
print("~~~~~~~~~~~~~~~~~~~~~")


# Displays numbers on up to two 7-segment displays
class display_controller():
  def __init__(self, displays: list, print_out = True):
    self.displays = displays

    self.print_out = print_out

  def display_num(self, num, duration, delay):
    if self.print_out:
      print("Num: " + str(num))
    
    if num < 10 :
      self.one_display(num, duration, delay)
    elif num < 100:
      self.two_display(num, duration, delay)
    else:
      print("ERROR: Number too large, keep below 100" + str(num))

  def one_display(self, num, duration, delay):
    d0 = self.displays["0"]

    if self.print_out:
      print("| d0 |")
      print("| " + str(num) + "  |")

    d0.display_num(num)                                    
    sleep(duration)
    d0.off()
    sleep(delay)

  def two_display(self, num, duration, delay):
    d0 = self.displays["0"]
    d1 = self.displays["1"]

    num_str = str(num)
    first_digit = int(num_str[1])
    second_digit = int(num_str[0])
    
    if self.print_out:
      print("| d1 | d0 |")
      print("| " + str(second_digit) + "  | " + str(first_digit) + "  |")
      
    t_end = time.time() + duration
    while time.time() < t_end:
      d0.display_num(first_digit)
      sleep(.005)
      d0.off()
      d1.display_num(second_digit)
      sleep(.005)
      d1.off()
        
    d0.off()
    d1.off()
    sleep(delay)
    
  def jumble(self, duration, delay, UPPER_BOUND):
    self.print_out = False
      
    t_end = time.time() + duration / 1.5 
    while time.time() < t_end:
      num = randint(1, UPPER_BOUND)
      self.display_num(num, .05, 0)
        
    self.print_out = True
        

    
class display_7seg:
  def __init__(self, pins):
    self.led_a = LED(pins["a"])
    self.led_b = LED(pins["b"])
    self.led_c = LED(pins["c"])
    self.led_d = LED(pins["d"])
    self.led_e = LED(pins["e"])
    self.led_f = LED(pins["f"])
    self.led_g = LED(pins["g"])
    self.led_h = LED(pins["h"])
  
  def zero(self):
    self.led_a.on()
    self.led_b.on()
    self.led_c.on()
    self.led_d.on()
    self.led_e.on()
    self.led_f.on()

  def one(self):
    self.led_e.on()
    self.led_f.on()
    
  def two(self):
    self.led_a.on()
    self.led_b.on()
    self.led_d.on()
    self.led_e.on()
    self.led_g.on()

  def three(self):
    self.led_a.on()
    self.led_b.on()
    self.led_c.on()
    self.led_d.on()
    self.led_g.on()

  def four(self):
    self.led_b.on()
    self.led_c.on()
    self.led_f.on()
    self.led_g.on()

  def five(self):
    self.led_a.on()
    self.led_c.on()
    self.led_d.on()
    self.led_f.on()
    self.led_g.on()

  def six(self):
    self.led_a.on()
    self.led_c.on()
    self.led_e.on()
    self.led_f.on()
    self.led_g.on()
    self.led_h.on()
    self.led_d.on()

  def seven(self):
    self.led_a.on()
    self.led_b.on()
    self.led_c.on()
    self.led_f.on()

  def eight(self):
    self.led_a.on()
    self.led_b.on()
    self.led_c.on()
    self.led_d.on()
    self.led_e.on()
    self.led_f.on()
    self.led_g.on()

  def nine(self):
    self.led_a.on()
    self.led_b.on()
    self.led_c.on()
    self.led_f.on()
    self.led_g.on()
    self.led_h.on()

  def dot(self):
    self.led_h.on()
  
  def off_dot(self):
    self.led_h.off()

  def off(self):
    self.led_a.off()
    self.led_b.off()
    self.led_c.off()
    self.led_d.off()
    self.led_e.off()
    self.led_f.off()
    self.led_g.off()
    self.led_h.off()

  def display_num(self, num):
    if num == 0:
      self.zero()
    if num == 1:
      self.one()
    if num == 2:
      self.two()
    if num == 3:
      self.three()
    if num == 4:
      self.four()
    if num == 5:
      self.five()
    if num == 6:
      self.six()
    if num == 7:
      self.seven()
    if num == 8:
      self.eight()
    if num == 9:
      self.nine()
    

class dice:
  def __init__(self, UPPER_BOUND):
    self.UPPER_BOUND = UPPER_BOUND

  def roll(self):
    return randint(1, self.UPPER_BOUND)
    
  def sides(self):
    return self.UPPER_BOUND
    
# === Dice Definitions ===

dices = (
         dice(4),
         dice(6),
         dice(8),
         dice(10),
         dice(12),
         dice(20)
         )

# === Pins ===

d0_pins = {"a": 20,
           "b": 21,
           "c": 19,
           "d": 13,
           "e": 6,
           "f": 16,
           "g": 12,
           "h": 26,}

d1_pins = {"a": 25,
           "b": 24,
           "c": 9,
           "d": 10,
           "e": 22,
           "f": 8,
           "g": 7,
           "h": 11}

# === Constants ===
DURATION = .8
DELAY = .5

# === Initialize Displays ===
d0 = display_7seg(d0_pins)
d1 = display_7seg(d1_pins)
ds = {"0": d0, "1": d1}

d_cont = display_controller(ds)
roll_button = Button(5)
dice_button = Button(2)

# === Main ===
dices_i = iter(dices)
die = next(dices_i)

while True:
  if roll_button.is_pressed:
    NUM = die.roll()
    d_cont.jumble(DURATION, DELAY, die.sides())
    d_cont.display_num(NUM, DURATION, DELAY)
  elif dice_button.is_pressed:
    try: 
      die = next(dices_i)
    except StopIteration:
      dices_i = iter(dices)
      die = next(dices_i)

    print("=== Die change ===")
    print("Value: " + str(die.sides()) )
    d_cont.display_num(die.sides(), DURATION * 1.5, DELAY)
    
	
 



