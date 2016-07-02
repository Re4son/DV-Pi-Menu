#!/usr/bin/env python
import sys, os, time, subprocess, commands, pygame
from pygame.locals import *
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
launch_bg=os.environ["MENUDIR"] + "launch-bg.sh"
process = subprocess.call(launch_bg, shell=True)

# Initialize pygame modules individually (to avoid ALSA errors) and hide mouse
pygame.font.init()
pygame.display.init()

pygame.mouse.set_visible(0)

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    pygame.draw.rect(screen, tron_regular, (xpo-10,ypo-10,width,height),3)
    pygame.draw.rect(screen, tron_light, (xpo-9,ypo-9,width-1,height-1),1)
    pygame.draw.rect(screen, tron_regular, (xpo-8,ypo-8,width-2,height-2),1)
    font=pygame.font.Font(None,30)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo+6))

def make_enabled_button(text, xpo, ypo, height, width, colour):
    pygame.draw.rect(screen, (colour), (xpo-10,ypo-10,width,height),3)
    pygame.draw.rect(screen, (colour), (xpo-9,ypo-9,width-1,height-1),1)
    pygame.draw.rect(screen, (colour), (xpo-8,ypo-8,width-2,height-2),1)
    font=pygame.font.Font(None,30)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo+6))


# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 21 <= touch_pos[0] <= 166 and 65 <= touch_pos[1] <=109:
            button(1)
    # button 2 event
    if 174 <= touch_pos[0] <= 319 and 65 <= touch_pos[1] <=109:
            button(2)
    # button 3 event
    if 21 <= touch_pos[0] <= 166 and 125 <= touch_pos[1] <=179:
            button(3)
    # button 4 event
    if 174 <= touch_pos[0] <= 319 and 125 <= touch_pos[1] <=179:
            button(4)
    # button 5 event
    if 21 <= touch_pos[0] <= 166 and 185 <= touch_pos[1] <=239:
            button(5)
    # button 6 event
    if 174 <= touch_pos[0] <= 319 and 185 <= touch_pos[1] <=239:
            button(6)

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def check_service(srvc):
    try:
        check = "/usr/sbin/service " + srvc + " status"
	status = run_cmd(check)
        if ("is running" in status) or ("active (running)") in status:
            return True
        else:
            return False
    except:
        return False


def toggle_dv_pi(srvc):
    check = "/usr/sbin/service " + srvc + " status"
    start = "/usr/sbin/service " + srvc + " start"
    start2 = "/usr/sbin/service mysql start"
    stop = "/usr/sbin/service " + srvc + " stop"
    stop2 = "/usr/sbin/service mysql stop"
    status = run_cmd(check)
    if ("is running" in status) or ("active (running)") in status:
        run_cmd(stop2)
        run_cmd(stop)
        return False
    else:
	run_cmd(start2)
	run_cmd(start)
        return True

# Define each button press action
def button(number):
    if number == 1:
        # X TFT
        pygame.quit()
        ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
        run_cmd("/usr/bin/sudo -u pi FRAMEBUFFER=/dev/fb1 startx")
##        run_cmd("/usr/bin/sudo FRAMEBUFFER=/dev/fb1 startx")
        os.execv(__file__, sys.argv)

    if number == 2:
        # X HDMI
        pygame.quit()
        ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
        run_cmd("/usr/bin/sudo -u pi FRAMEBUFFER=/dev/fb0 startx")
##        run_cmd("/usr/bin/sudo FRAMEBUFFER=/dev/fb0 startx")
        os.execv(__file__, sys.argv)


    if number == 3:
        # exit
        process = subprocess.call("setterm -term linux -back default -fore white -clear all", shell=True)
        pygame.quit()
        run_cmd("/usr/bin/sudo -u pi screen -RR")
        os.execv(__file__, sys.argv)

    if number == 4:
        # DV-Pi Applications
	if toggle_dv_pi("apache2"):
	    make_enabled_button("     DV-Pi", 174, 125, 54, 145, red)
	else:
	    make_button("     DV-Pi", 174, 125, 54, 145, tron_light)
	return

    if number == 5:
        # next page
        pygame.quit()
        ##startx only works when we don't use subprocess here, don't know why
        page=os.environ["MENUDIR"] + "menu_screenoff.py"
        os.execvp("python", ["python", page])
        sys.exit()

    if number == 6:
        # next page
        pygame.quit()
        ##startx only works when we don't use subprocess here, don't know why
	page=os.environ["MENUDIR"] + "menu-2.py"
	os.execvp("python", ["python", page])
        sys.exit()



# colors    R    G    B
white    = (255, 255, 255)
tron_whi = (189, 254, 255)
red      = (255,   0,   0)
green    = (  0, 255,   0)
blue     = (  0,   0, 255)
tron_blu = (  0, 219, 232)
black    = (  0,   0,   0)
cyan     = ( 50, 255, 255)
magenta  = (255,   0, 255)
yellow   = (255, 255,   0)
tron_yel = (255, 218,  10)
orange   = (255, 127,   0)
tron_ora = (255, 202,   0)

# Tron theme orange
tron_regular = tron_ora
tron_light   = tron_yel
tron_inverse = tron_whi

# Tron theme blue
##tron_regular = tron_blu
##tron_light   = tron_whi
##tron_inverse = tron_yel

# Set up the base menu you can customize your menu with the colors above

#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

# Background Color
screen.fill(black)

# Outer Border
pygame.draw.rect(screen, tron_regular, (0,0,319,239),8)
pygame.draw.rect(screen, tron_light, (2,2,319-4,239-4),2)

pi_hostname = run_cmd("hostname")
pi_hostname = "  " + pi_hostname[:-1]
# Buttons and labels
# First Row Label
make_label(pi_hostname, 32, 15, 42, tron_inverse)
# Second Row buttons 1 and 2
make_button("      X-TFT", 21, 65, 54, 145, tron_light)
make_button("    X-HDMI", 174, 65, 54, 145, tron_light)
# Third Row buttons 3 and 4
make_button("   Terminal", 21, 125, 54, 145, tron_light)
if check_service("apache2"):
     make_enabled_button("     DV-Pi", 174, 125, 54, 145, red)
else:
     make_button("     DV-Pi", 174, 125, 54, 145, tron_light)
# Fourth Row Buttons
make_button("     TFT Off", 21, 185, 54, 145, tron_light)
make_button("         >>>", 174, 185, 54, 145, tron_light)


#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            on_touch()

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
    ## Reduce CPU utilisation
    time.sleep(0.1)