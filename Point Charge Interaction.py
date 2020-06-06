from manimlib.imports import *
from scipy.optimize import minimize as minimize
from scipy import optimize as optimize


class EverybodyDoTheMessAround(Scene):
    def construct(self):

    ##This is the Electric Field Equation of two point charges
    ##isolated for y with E, x, and p2 as dependant variables
    ##The following simplifications were made to make the math pheasible,
    #1. p0 is centered about origin
    #2. p2 = {(x,0) ε R2|xεR} or p2 is fixed on the x axis
        def eField_points_function(E,c2x,d,x): return ( ( (c2x**2-2*c2x*x)/E + (1/2*c2x**2-c2x*x-1/E)**2)**0.5 - 0.5*c2x**2 + c2x*x + 1/E - x**2 )**0.5
        
        def eField_points_function_NEG(E,c2x,d,x):
            return ( ((c2x**2-2*c2x*x)/E + (1/2*c2x**2-c2x*x/2)**2      )**0.5 - 0.5*c2x**2 + c2x*x - x**2        )**0.5
    ##This gets all points around point charge 1 and 2, specify for 2 as point = "p2" All this does is change the region being broadcasted, defined as eBoundaryWidth
    ##eFieldPointsFunction only retrieves the top point, so we calculate the top y values, and then tack the negatives on the end with .extend()
    ###For loop to calculate all these pairs, and throw out any shit vals (eg 0, or NaN)
    ##Return all points, turn it into a shape later
    
        def get_eField_points(E,c2x,d,point=None):
            eBoundary_width = np.arange(boundary.get_left()[0],(0+d),0.01)
            if point == "P2" or point =="P2n": eBoundary_width = np.arange(c2x-d,boundary.get_right()[0],0.01)
            eField_points = []
            eField_points_top = []
            for i in eBoundary_width:
                x = i
                y = eField_points_function(E,c2x,d,x)
                if point == "P2n": y = eField_points_function(E,c2x,d,x)
                if x > eBoundary_width[len(eBoundary_width)-1]: break
                if y>0:
                    if y>boundary.get_top()[1]: y = boundary.get_top()[1]
                    eField_points.append(np.array([x,y,0]))
                    eField_points_top.append(np.array([x,-y,0]))
            eField_points.extend(eField_points_top[::-1])
            if len(eField_points)==0: return None       ##Bug Fix 1
            eField_points.append(eField_points[0])

            return eField_points
        
    ##Make a pulsing updater: an updater that checks on its own shape and resets to zero once it reaches a size
    ##Retrieve our ValTrackers, and use them to construct our shape with our newly defined function
    ##Then we'll check how the value is doing and reset it if it gets too big!
    #All the while we'll give it a pretty colour effect that shows the field strength
    ##We ended up keeping track of shape size by cleverly using opacity. Width would normally work but is hard to calculate since we have an irregular shape. Originally I used val tracker for E but it wouldn't let me send out multiple pulses at the same time because they all ended up having the same E
        def EF_Updater(circ,dt):
            c2_local = c2.get_value()
        ##This is our translation between opacity and E: opacity = E/Emax. We decrease it a little every rev
            Ei = circ.get_fill_opacity()*(maxE-speed*dt)
        ## If the pulse dies out, we'll reincarnate it (corresponding to smallest area)
            if circ.get_fill_opacity() <= 0: Ei = maxE-speed*dt
        ## Update the fill, and update the shape. It's imperative that these are beside eachother otherwise the whole screen flashes yellow
            circ.set_fill(color = YELLOW,opacity=Ei/maxE)
            circ.set_stroke(color = YELLOW,opacity = Ei/maxE,width = 0)
            eField_points = get_eField_points(Ei,c2_local,(c2_local-0)/2)
            if eField_points == None:         ##Bug Fix 1
                Ei = maxE-2*dt
                eField_points = get_eField_points(Ei,c2_local,(c2_local-0)/2)
            circ.set_points_as_corners(eField_points)
            self.bring_to_front(P1Pulses[i])
            if Ei<minE: circ.set_fill(YELLOW,0).set_stroke(color = YELLOW,opacity = 0,width = 0)
            
            
        def EF_Updater_P2(circ,dt):
            c2_local = c2.get_value()
            Ei = circ.get_fill_opacity()*(maxE-speed*dt)
            if circ.get_fill_opacity() <= 0: Ei = maxE-speed*dt
            circ.set_fill(color = ORANGE,opacity=Ei/maxE)
            circ.set_stroke(color = ORANGE,opacity = Ei/maxE,width = 0)
            eField_points = get_eField_points(Ei,c2_local,(c2_local-0)/2,point = "P2")
            if eField_points == None:         ##Bug Fix 1
                Ei = maxE-2*dt
                eField_points = get_eField_points(Ei,c2_local,(c2_local-0)/2,point = "P2")
            circ.set_points_as_corners(eField_points)
            self.bring_to_front(P2Pulses[i])
            if Ei<minE: circ.set_fill(ORANGE,0).set_stroke(color = ORANGE,opacity = 0,width = 0)
                
#        def EF_Updater_P2_NEG(circ,dt):
#                c2_local = c2.get_value()
#                Ei = -circ.get_fill_opacity()*(maxE-speed*dt)
#                if circ.get_fill_opacity() >= 1: Ei = -minE+speed*dt
#                circ.set_fill(color = BLUE,opacity=-Ei/maxE)
#                eField_points = get_eField_points(Ei,c2_local,(c2_local-0)/2,point = "P2n")
#                if eField_points == None:         ##Bug Fix 1
#                    Ei = minE+2*dt
#                    eField_points = get_eField_points(Ei,c2_local,(c2_local-0)/2,point = "P2n")
#                circ.set_points_as_corners(eField_points)
#                self.bring_to_back(P2Pulses[i])
#                if Ei>maxE: circ.set_fill(BLUE,0)
                
                
            ##Rewrite this tomorrow using opacity instead of ValueTrackers
            ##We're going to try to set E based on opacity and decrease by dt. Maybe a linear fit
            ##of opacity to maxE and minE, maybe try to make it so that
        
    #With some thought, we realize in this the animation the reload time is the number of iterations of dt it takes to get to minE, so n = maxE-minE / dt where dt = 1/framerate
    ## This is a standalone pulse generator, good for copy pasting into other projects
    
        def pulseGenerator(nPulses,seconds_per_pulse,starter_shape,update_function):
            copyPulses = []
            for i in range(nPulses):
                copyPulses.append(starter_shape.copy())
                copyPulses[i].add_updater(update_function)
                self.add(copyPulses[i])
                self.bring_to_front(copyPulses[i])
                self.wait(seconds_per_pulse)
                
            return copyPulses
        

    ## MAIN CODE
        #Define our initial values.
        maxE = 10
        minE = 1.2**-2
        speed = maxE
        c2 = ValueTracker(7)
        
        boundary = Rectangle(height = 4,width = 10)
        boundary.shift(np.array([boundary.get_width()/2-boundary.get_height()/2,0,0]))
        
        refresh_time = 1/15*np.log(minE/maxE)/np.log((maxE-speed/15)/maxE)
        
        initial_boundary = Square()

        
    #Initiate Point charges
        pointChargeRad = 0.2
        pointCharge1 = Circle().set_width(0.4).set_fill(color = RED,opacity=0.75)
        pointCharge2 = Circle().set_width(0.4).set_fill(color = RED,opacity=0.75)

        pointCharge1Text = TexMobject("\\text+",color=WHITE)
        pointCharge2Text = TexMobject("\\text+",color=WHITE)
        
        pointCharge1Group = VGroup(pointCharge1,pointCharge1Text)
        pointCharge2Group = VGroup(pointCharge2,pointCharge2Text)
        
        pointCharge2Group.add_updater(lambda point: point.move_to(np.array([c2.get_value(),0,0])))
        
    ##Initiate pulses
        P1 = Circle(color = None).set_width(0.5)
        P2 = Circle(color = None).set_width(0.5).move_to(np.array([c2.get_value(),0,0]))
        
        P1Pulses = []
        P2Pulses = []
        P1Group = VGroup()
        P2Group = VGroup()


    ##Script
        Text1 = TextMobject("Consider a positive point charge, P1")
        Text2 = TextMobject("Around P1 exists an electric field")
        Text3 = TextMobject("that extends out radially")
        Text4 = TextMobject("Its intensity is equal to the force that")
        Text5 = TextMobject("would be felt by a positive charge")
        
    ##Script positioning
        Text1.to_corner(TOP+LEFT,buff = 0.2)
        Group23 = VGroup(Text2,Text3).arrange(DOWN,aligned_edge=LEFT).to_corner(TOP+LEFT,buff = 0.2)
        Group45 = VGroup(Text4,Text5).arrange(DOWN,aligned_edge=LEFT).to_corner(TOP+LEFT,buff = 0.2)
    ##Start playing objects
        self.play(  Write(Text1))
        self.play(  Write(pointCharge1Group),
                    Write(initial_boundary)
        )
                    
        self.add_foreground_mobjects(pointCharge1Group)
        
        
        self.play(  FadeOut(Text1),
                    Write(Group23),
        )
        n = 2
        for i in range(n):
            P1Pulses.append(Circle(color = YELLOW).set_width(0.5))
            P1Pulses[i].add_updater(EF_Updater)
            self.add(P1Pulses[i])
            P1Group.add(P1Pulses[i])
            self.bring_to_front(P1Pulses[i])
            self.wait(refresh_time/(n))
                    
        
        
        self.play(  FadeOut(Group23),
                    Write(Group45)
        )
        self.play(  ReplacementTransform(initial_boundary,boundary))
        
        
        self.play(Write(pointCharge2Group))
        
        for i in range(n):
            P2Pulses.append(Circle(color = ORANGE).set_width(0.5))
            P2Pulses[i].add_updater(EF_Updater_P2)
            self.add(P2Pulses[i])
            P2Group.add(P2Pulses[i])
            self.bring_to_front(P2Pulses[i])
            self.wait(refresh_time/(n))
        
        self.play(c2.set_value,2,
            rate_func= exponential_decay,run_time= 8)
        
        self.play(c2.set_value,1,
            rate_func= smooth,run_time= 8)
            
        self.play(c2.set_value,8,
            rate_func= exponential_decay,run_time= 2)
    
        for i in range(n):
            P2Pulses[i].clear_updaters()
            P1Pulses[i].clear_updaters()
            
        self.play(  FadeOut(Group45),
        FadeOut(P1Group),
        FadeOut(P2Group),
        FadeOut(boundary),
        FadeOut(pointCharge2),
        FadeOut(pointCharge1),
        FadeOut(pointCharge1Text),
        FadeOut(pointCharge2Text))
