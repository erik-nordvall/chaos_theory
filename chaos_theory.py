#Based on theory from the book Strange Attractors: Creating Patterns in Chaos and
#https://www.youtube.com/watch?v=AzdpM-vfUCQ&ab_channel=CodingCassowary
import random
import math
from matplotlib import pyplot

found = 0
n=10
while found < n:

    #random starting point
    x = random.uniform(-0.5 , 0.5)
    y = random.uniform(-0.5 , 0.5)

    #random alternative point nearby
    xe = x + random.uniform(-0.5, 0.5) / 1000
    ye = y + random.uniform(-0.5, 0.5) / 1000

    #distance between the two points
    dx = xe - x
    dy = ye - y
    d0 = math.sqrt(dx*dx + dy*dy)

    #random parameter vector
    a = [random.uniform(-2, 2) for i in range(12)]

    #lists to store trajectory
    x_list = [x]
    y_list = [y]

    #initialize convergance and lyapunov 
    converging = False
    lyapunov = 0

    #iteratively pass (x,y) into the quadrtic map
    for i in range(100000):
        #compute next point (using the quadratic map)
        xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y
        ynew = a[6] + a[7]*x + a[8]*x*x + a[9]*y + a[10]*y*y + a[11]*x*y

        #check if we converge to infinity
        if xnew > 1e10 or ynew > 1e10 or xnew < -1e10 or ynew < -1e10:
            converging = True
            break

        #check if we converge to a single point
        if abs(x - xnew) < 1e-10 and abs(y-ynew) <1e-10:
            converging = True
            break

        #check for chaotic behavior
        if i > 1000:
            #compute next alternativ point
            xenew = a[0] + a[1]*xe + a[2]*xe*xe + a[3]*ye + a[4]*ye*ye + a[5]*xe*ye
            yenew = a[6] + a[7]*xe + a[8]*xe*xe + a[9]*ye + a[10]*ye*ye + a[11]*xe*ye

            #compute distance between new points
            dx = xenew - xnew
            dy = yenew - ynew
            d = math.sqrt(dx*dx + dy*dy)

            #lyapunov exponent
            lyapunov += math.log(abs(d/d0))

            #rescale alternative point
            xe = xnew +  d0*dx/d
            ye = ynew +  d0*dy/d



        #update (x,y)
        x=xnew
        y=ynew
        
        #store (x,y) in our path lists
        x_list.append(x)
        y_list.append(y)
    #if chaotic behavior has been found
    if not converging and lyapunov >= 10:
        found += 1
        print("Found a strange attractor with L = " + str(lyapunov) + "!")

        #plot design
        #pyplot.clf()

        pyplot.style.use("dark_background")
        pyplot.axis("off")
        pyplot.scatter(x_list[100:], y_list[100:], s=0.01, c="yellow")
        pyplot.show()
