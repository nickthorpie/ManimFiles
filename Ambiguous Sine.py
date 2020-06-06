#!/usr/bin/env python

from manimlib.imports import *

def getPerpendicularVector(point1,point2):
    a = point2[0]-point1[0]
    b = point2[1]-point1[1]
    c = point2[2]-point1[2]
    return np.array([-b,a,c])/(a**2+b**2+c**2)**0.5/2
    

class Ambiguous(Scene):
    def construct(self):
        Text1 = TextMobject("An Ambiguous sine case can occur when you are given:")
        Text2 = TextMobject("- a side length")
        Text3 = TextMobject("- another side length")
        Text4 = TextMobject("- and an angle that is NOT between them")
        Text5 = TextMobject("This creates an unknown side length,")
        Text6 = TextMobject("and an unknown angle between the given sides like a hinge.")
        Text7 = TextMobject("If this 'hinged' length is shorter than the 'fixed' length,")
        Text8 = TextMobject("then there are two positions  the 'hinged' arm can go")
        Text9 = TextMobject("But if 'hinged' arm is longer than the fixed arm,")
        Text10 = TextMobject("then there is only one possible configuration")
        group1234 = VGroup(Text1,Text2,Text3,Text4).arrange(DOWN,aligned_edge = LEFT).to_corner(BOTTOM+LEFT).shift(DOWN*1.5)
        group56 = VGroup(Text5,Text6).arrange(DOWN,aligned_edge = LEFT).to_corner(BOTTOM+LEFT).shift(DOWN*1.5)
        group78 = VGroup(Text7,Text8).arrange(DOWN,aligned_edge = LEFT).to_corner(BOTTOM+LEFT).shift(DOWN*1.5)
        group910= VGroup(Text9,Text10).arrange(DOWN,aligned_edge = LEFT).to_corner(BOTTOM+LEFT).shift(DOWN*1.5)
        
        A = np.array([0,0,0])/2
        B = np.array([8.3867,5.4464,0])/2
        C = np.array([10.904,0,0])/2
        D = np.array([8.3867,0,0])/2
        E = np.array([5.8694,0,0])/2


        dotA = Dot().move_to(A)
        dotB = Dot().move_to(B)
        dotC = Dot().move_to(C)
        lineAB = Line(A,B,color = BLUE)
        lineAB2 = Line(A,B,color = BLUE)
        lineAD = Line(A,D)
        lineBC = Line(B,C,color = RED)
        lineAC = Line(A,C)
        lineAE = Line(A,E)
        
        LengthAB = TextMobject("10cm",color = BLUE) .move_to(lineAB.get_center() +getPerpendicularVector(A,B))
        LengthBC = TextMobject("6cm",color=RED)    .move_to(lineBC.get_center() +getPerpendicularVector(B,C))
        LengthAC = TextMobject("?")               .move_to(lineAC.get_center()+getPerpendicularVector(C,A))

        AngleA   = TextMobject("33º")             .move_to(A+np.array([1,0.3,0]))
        AngleB   = TextMobject("?")              .move_to(B+np.array([0,-0.5,0]))
        
        self.play(  Write(Text1),run_time = 3)
        
        self.play(  Write(lineAB),
                    Write(Text2,run_time = 3))
        self.play(  GrowFromPoint(LengthAB,lineAB.get_center()))
        self.play(  Write(lineBC),
                    Write(Text3),run_time = 3)
        self.add(   dotC)
        self.play(  GrowFromPoint(LengthBC,lineBC.get_center()))
        self.play(  ReplacementTransform(lineAB2,lineAE),
                    Write(Text4,run_time = 3))
        self.play(  GrowFromPoint(AngleA,A))
        self.play(  GrowFromPoint(LengthAC,lineAC.get_center()),
                    ReplacementTransform(lineAE,lineAC,run_time=3,),
                    Write(Text5,run_time = 3),
                    FadeOut(group1234))
                    
        self.wait(2)

        self.remove(dotC)
        self.play(  Rotating(lineBC,
                        radians=49.61*DEGREES,
                        about_point=B,
                        run_time = 3,
                        rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                        ),
                    GrowFromPoint(AngleB,B),
                    Write(Text6,run_time = 3)
                )
        self.play(  Rotating(lineBC,
                             radians=-49.61*DEGREES,
                             about_point=B,
                             run_time = 3,
                             rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                             )
                 )


        
                    
        self.play(FadeOut(group56),
                    Write(Text7,run_time = 3))
                    
        self.play(  Rotating(lineBC,
                    radians=-81.81*DEGREES,
                    about_point=B,
                    run_time = 3,
                    rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                    ))
        self.play(
                Rotating(lineBC,
                    radians=81.81*DEGREES,
                    about_point=B,
                    run_time = 3,
                    rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5),
                    )
            )
        
        newTriangleLocation = np.array([-6.5,0,0])
        
        lineABi = lineAB.copy().shift(newTriangleLocation)
        lineBCi = lineBC.copy().shift(newTriangleLocation)
        lineACi = Line(A,C).shift(newTriangleLocation)
        lineAEi = Line(A,E).shift(newTriangleLocation)
        LengthABi = LengthAB.copy().shift(newTriangleLocation)
        LengthBCi = LengthBC.copy().shift(newTriangleLocation)
        LengthACi = LengthAC.copy().shift(newTriangleLocation)
        AngleAi = AngleA.copy().shift(newTriangleLocation)
        AngleBi = AngleB.copy().shift(newTriangleLocation)
        Bi = B+newTriangleLocation
        

        trianglei = VGroup(lineABi,lineBCi,lineACi,LengthABi,LengthBCi,LengthACi,AngleAi,AngleBi)
        self.play(  Write(Text8,run_time = 3),
                    ShowCreation(trianglei))

        
        self.play(  Rotating(lineBCi,
                            radians=-49.61*DEGREES,
                            about_point=Bi,
                            run_time = 3,
                            rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                            ),
                    ReplacementTransform(lineACi,lineAEi,
                            run_time = 3,
                            rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                            ),
                    ApplyPointwiseFunction(lambda point: point + np.array([-0.35,0,0]),AngleBi),
                    ApplyPointwiseFunction(lambda point: point + np.array([-lineAE.get_width()/4,0,0]),LengthACi)
                 )
        ##Get rid of both triangles, new one in the middle, show the other arm rotating
        self.wait(2)
        self.play(  FadeOut(trianglei),
                    FadeOut(group78),
                    Write(Text9,run_time = 3),
                    ApplyPointwiseFunction(lambda point: point + [lineAB.get_width()-0.2,0,0],AngleA),
                    FadeOut(lineAEi)
                )
            
        lineBC.set_color(BLUE)
        LengthBC.set_color(BLUE)
        lineAB.set_color(RED)
        LengthAB.set_color(RED)
        self.wait()
        
        self.play(  Rotating(lineAB,
                    radians=81.81*DEGREES,
                    about_point=B,
                    run_time = 4,
                    rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                    ))
        self.play(  Rotating(lineAB,
                    radians=-81.81*DEGREES,
                    about_point=B,
                    run_time = 6,
                    rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                    ))
        
        self.play(  Rotating(lineAB,
                    radians=TAU/2,
                    about_point=B,
                    run_time = 4,
                    rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                    ),
                    Write(Text10,run_time = 4)
                    )
        self.play(  Rotating(lineAB,
                        radians=-TAU/2,
                        about_point=B,
                        run_time = 6,
                        rate_func= lambda t: smooth(0.9*(np.sin(TAU*t/4))**0.5)
                        ))
        

        

class FullGrid(GraphScene):
    CONFIG = {
        "y_max": 8,
        "y_axis_height": 5,
    }
    def construct(self):
        self.show_function_graph()
    
    def show_function_graph(self):
        self.setup_axes(animate=False)
    
        
        print("mothafuckin:",ValueTracker(1.5).get_value())

        self.wait()
        def func(x):
            return 0.1 * (x + 3-5) * (x - 3-5) * (x-5) + 5
        graph =self.get_graph(func,x_min=0.2,x_max=9)
        
      
        xycoord=self.coords_to_point(1,func(1))
        print("xycoord is at",xycoord)
        dot = Dot().move_to(xycoord)
        self.play(ShowCreation(dot),
                    Write(graph))
        self.wait()
        
        group = VGroup(dot,graph)
#        self.wait()
#
#    ###Warping Grid
#        grid.prepare_for_nonlinear_transform()
#
#        self.play(
#            grid.apply_function,
#            lambda p: np.array([p[0],p[1]+p[0],0,
#            ]),
#            run_time=3,)
#
#        self.play(
#            grid.apply_function,
#            lambda p: np.array([p[0],p[1]-p[0],0,
#            ]),
#            run_time=3,)

class SquareToCircle(Scene):
    def construct(self):
        A = np.array([0,0,0])/2
        C = np.array([10.904,0,0])/2
        E = np.array([5.8694,0,0])/2
        lineAC = Line(A,C)
        lineAE = Line(A,E)
        self.add(lineAE)
        self.play(ReplacementTransform(lineAE,lineAC))
        self.play(FadeOut(lineAC))

#
#        self.add(lineAB2)
#        self.play(Transform(lineAB2,lineAE))

#        self.play(FadeOut(lineAC))
#        self.wait(2)

#        obj1.set_fill([GREEN,RED],opacity = 0.3)
#        self.play(GrowFromPoint(obj1,obj1.get_center()))
#        self.add(obj1)
#        self.wait()
#        #obj1.rotation(1/8*TAU)
#        self.play(Rotating(obj1,radians=TAU,rate_func=there_and_back))
#        self.wait()
#        dot = Dot().move_to(obj1.get_left())
#        self.play(GrowFromPoint(dot,obj1.get_center()))
#
#        self.wait()
#
#        self.play(ApplyPointwiseFunction(
#            lambda point: point+2*obj1.get_right(),dot))
#
#
#        self.play(FadeOut(obj1))
#        self.play(FadeIn(obj1.set_fill([YELLOW,BLUE],opacity=0.3)))
#        self.play(Uncreate(obj1))
#        .align_points(obj2)
#        .get_anchors()
#        .get_end_anchors()
#        .get_points()
#        .make_smooth()
#        .match_style(obj2)
#        .get_bottom()
#        .get_boundary_point(DIR)
#        .get_corner()
#        .get_left()
#        .get_width()
#        .match_width()
#        .scale()
#        .repeat(count) - can make transitions smoother
#        .set_color_by_gradient(colors)
        
#        self.play(Transform(square, circle))
#        self.play(FadeOut(square))

class PartialGrid(Scene):
    def construct(self):
    
        def test():
            self.wait()
            self.play(Write(TextMobject("Test").to_corner(TOP+LEFT)))
            self.wait()
        
        Title = TextMobject("Understanding the definition of a derivative")
        derivative = TextMobject("$f'(x)$ =")
        definition = TextMobject("$\displaystyle{\lim_{h \--> \infty}}$ $\\frac{f(x-h)}{h}$")
        
        b1 = Brace(derivative).scale(0.75)
        t1 = b1.get_text("derivative").scale(1)

        b2 = Brace(definition).scale(0.75)
        t2 = b2.get_text("{Slope of tangent line at x}").scale(0.75)
        
    
        derivativeGroup = VGroup(derivative,b1,t1).arrange(DOWN)
        definitionGroup = VGroup(definition,b2,t2).arrange(DOWN)
        group = VGroup(definitionGroup,derivativeGroup)
        
        group.arrange(LEFT)
        
        VGroup(Title,group).arrange(2*DOWN)
        
        self.play(  Write(Title))
        self.wait()
        
        self.play(  FadeOut(Title),
                    Write(derivative),
                    Write(definition), )
                    
        self.wait()
        
        
        self.play(  GrowFromPoint(b1,derivative.get_center()),
                    Write(t1), )
                    
        self.wait()
        
        self.play(  GrowFromPoint(b2,definition.get_center()),
                    Write(t2), )
                    
        self.wait()
        
        derivativec = TextMobject("$f'(x)$ =")
        definitionc = TextMobject("$\displaystyle{\lim_{h \--> \infty}}$ $\\frac{f(x-h)}{h}$")
        
        groupc = VGroup(definitionc,derivativec).arrange(LEFT).to_corner(TOP+LEFT)

        self.play(  FadeOut(group),
                    GrowFromPoint(groupc,group.get_center())
                    )
       
    #############################################
    
    
    ## Draw axes
        axes = Axes(
            x_min=-1,
            x_max=4,
            y_min=0,
            y_max=4)
    
    ## Draw Graph
        toOrigin = 3*DOWN+5*LEFT

    
        graph = ParametricFunction(
            function=lambda t: np.array([t,0.2*(t-1)**2+0.5,0]),
            t_min=0.5,
            t_max=4,
            color=BLUE
        )
        
        funcWriting = TextMobject("y = f(x)",color = BLUE).move_to(toOrigin+np.array([5,3,0]))
        
        
        func = VGroup(graph,axes)
        func.shift(toOrigin)
                
        self.play(  Write(func),run_time = 3,)
        self.play(  Write(funcWriting))

        ##Make our points


        a = Dot(color = BLUE)
        b = Dot(color = BLUE)
        c = Dot(color = BLUE)
        d = Dot(color = BLUE)
        
        
        
        i1=2
        a.move_to(3*DOWN+5*LEFT+np.array([i1,0.2*(i1-1)**2+0.5,0]))
        i2=2.5
        b.move_to(3*DOWN+5*LEFT+np.array([i2,0.2*(i2-1)**2+0.5,0]))
        i3=3
        c.move_to(3*DOWN+5*LEFT+np.array([i3,0.2*(i3-1)**2+0.5,0]))
        i4=3.5
        d.move_to(3*DOWN+5*LEFT+np.array([i4,0.2*(i4-1)**2+0.5,0]))
        
        
        self.wait()
        
        self.play(  GrowFromPoint(a,toOrigin),
                    GrowFromPoint(b,a.get_center()),
                    GrowFromPoint(c,b.get_center()),
                    GrowFromPoint(d,c.get_center()) )




    ##Write Tangent

        def sumfun(t): return 0.2*(t-1)**2+0.5
        
        vals = np.linspace(i1,i4,5)
        vals2 = np.linspace(i4,i1,5)
        #np.append(vals,vals2)
        print(vals)
        
        tangentWord = VGroup(TextMobject("A Tangent Line touches",color = RED),
                             TextMobject("a curve at one point",color = RED),
                                       ).arrange(DOWN,aligned_edge=LEFT)
        tangentWord.move_to(toOrigin+np.array([8,1,0]))
        
        
        for i in range(len(vals)):
            x1 = vals[i]
            y1 = sumfun(x1)
            y2 = sumfun(x1+0.01)
            x2 = x1+0.01
            

            tangentLine2 = ParametricFunction(
                function=lambda t: np.array([ t,
                                            (y2-y1)/(x2-x1)*(t-x1)+y1,
                                            0 ]),
                t_min=-1.5,
                t_max=4,
                color=RED
            ).shift(toOrigin)

            if (i==0):
                self.play(Write(tangentLine2))
                self.play(Write(tangentWord))

            else:
                self.play(  Transform(tangentLine1,tangentLine2),
                            FadeOut(tangentLine1),
                            ShowCreation(tangentLine2,run_time=1.5))
            tangentLine1 = tangentLine2
            

        #tangentLine = tangentLine2
        
#        arrow = Arrow(tangentWord.get_center(),wordSlope.get_center(),color=RED)
#        self.play(  Write(arrow),
#                    Write(wordSlope) )
        
        self.wait(3)
        
#        self.play(  FadeOut(arrow),
#                    FadeOut(wordSlope),
        self.play(  FadeOut(tangentWord))
    ##Slide Secents
     #Initialize secantline
        x1 =i1
        y1 = sumfun(x1)
        x2 = i4
        y2 = sumfun(x2)
        obj1 = ParametricFunction(
            function=lambda t: np.array([     t,(y2-y1)/(x2-x1)*(t-x1)+y1,0]),
            t_min=-1.5,
            t_max=4,
            color=GREEN
        )
        obj1.shift(toOrigin)
        
        secantWord = VGroup(TextMobject("A secant line passes",color = GREEN),
                             TextMobject("through two points",color = GREEN),
                                ).arrange(DOWN,aligned_edge=LEFT)
        secantWord.move_to(toOrigin+np.array([8,1,0]))
    
        
        
        self.play(FadeOut(tangentLine1),
                Transform(tangentLine1,obj1),
                ShowCreation(obj1,run_time=3),
                Write(secantWord))
        
       ####
        def newfuckinline(oldLine,newx,color = None):
            x2 = newx
            y2 = sumfun(x2)
            x1 = 2
            y1 = sumfun(x1)
            obj2 = ParametricFunction(
                function=lambda t: np.array([t,(y2-y1)/(x2-x1+0.001)*(t-x1+0.001)+y1,0]),
                t_min=-1.5,
                t_max=4,
                color= color or GREEN
                ).shift(toOrigin)
            
            
            self.play(  FadeOut(obj1),
                        Transform(obj1,obj2),
                        ShowCreation(obj2,run_time=3))
            return obj2
        
        def triangle(x2):
            x1 = 2
            y1 = sumfun(x1)
            y2 = sumfun(x2)
            triangle = Polygon( np.array([x1,y1,0]),
                                np.array([x2,y1,0]),
                                np.array([x2,y2,0]),
                                color = GREEN       )
            return(triangle)
        
        self.wait(2)
     #Do the sliide
        
        secantWord2 = VGroup(   TextMobject("As two points get closer they",color = GREEN),
                                TextMobject(" start to look like a tangent",color = GREEN),
                            ).arrange(DOWN,aligned_edge=LEFT)
        secantWord2.move_to(toOrigin+np.array([8,1,0]))
        self.play(FadeOut(secantWord),
                    Write(secantWord2))

        scale = 4
       ##goin forward
        vals = np.linspace(i4,i1,scale)
        for i in range(0,scale-1):
            obj2 = newfuckinline(obj1,vals[i])
            obj1 = obj2
        
        obj2 = newfuckinline(obj1,vals[i]-0.49,color = RED)
        obj1 = obj2
       ##goin backwards
        
        obj2 = newfuckinline(obj1,vals[0])
        obj1 = obj2
        

        
    ##make the triangle
        triangle = triangle(i4)
        
    ##Write words about slope
        slopeWords = VGroup(   TextMobject("The slope of this line is found",color = WHITE),
                                TextMobject("using the rise and run method",color = WHITE),
                            ).arrange(DOWN,aligned_edge=LEFT)
        slopeWords.move_to(toOrigin+np.array([8.5,1,0]))
    
    ##Put triangle in place
        triangle.move_to(toOrigin+np.array([1/2*(i4-i1)+i1,
                                            1/2*(sumfun(i4)-sumfun(i1))+sumfun(i1),
                                            0]))
    ##Attach a rise and run tag to it
        riseWord = TextMobject("Rise").move_to(triangle.get_center()+np.array([1.25,0,0]))
        runWord = TextMobject("Run").move_to(triangle.get_center()+np.array([0,-0.75,0]))
        
        self.play(Write(triangle),
                    FadeOut(secantWord2),
                    Write(riseWord),
                    Write(runWord))
                    
        self.wait()
        self.play(Write(slopeWords))
    
    ##Replace derivative definition with m = rise/run
        mEqn = TextMobject("Slope = ").move_to(derivativec.get_center())
        slopeDefinitionEqn = TextMobject("$\\frac{Rise}{Run}$").move_to(definitionc.get_center()+np.array([-0.5,0,0]))
        
        self.play(FadeOut(derivativec),
                    FadeOut(definitionc),
                    Transform(derivativec,mEqn),
                    ShowCreation(mEqn)
                    )
        self.wait(2)
        self.play(  GrowFromPoint(slopeDefinitionEqn,riseWord.get_center()),)
        
#        for i in range(int(i1*scale),int(i4*scale)):
#
#            x2 = i/scale
#            y2 = y2 = sumfun(x2)
#            obj2 = ParametricFunction(
#                function=lambda t: np.array([t,(y2-y1)/(x2-x1+0.001)*(t-x1+0.001)+y1,0]),
#                t_min=-1.5,
#                t_max=2,
#                color=RED
#            )
#            obj2.shift(toOrigin)
#            self.play(Transform(obj1,obj2))
#            obj2 = obj1



########################################################################################################################


from manimlib.imports import *

class underline(Line):
    def __init__(self,texto,buff=0.07,**kwargs):
        Line.__init__(self,texto.get_corner(DL),texto.get_corner(DR),**kwargs)
        self.shift(DOWN*buff)

NEW_BLUE = "#68a8e1"
COLOR_SYMBOL = "#fffab3"
class Thumbnail(GraphScene):
    CONFIG = {
        "y_max": 8,
        "y_axis_height": 5,
    }

    def construct(self):
        self.add_title()
        self.show_function_graph()

    def add_title(self):
        title = self.title = TextMobject("\\sc Manim Tutorial").scale(2.3)
        title.to_edge(UP)
        
        h_line = Line(LEFT, RIGHT)
        h_line.set_height(FRAME_WIDTH - 2 * LARGE_BUFF)
        h_line.next_to(title, DOWN)
        h_line.set_stroke(WHITE,3)
        title.to_edge(UP+LEFT)
        title.shift(RIGHT)
        self.title=title
        self.lin_h = h_line

    def show_function_graph(self):
        ul=underline(self.title)
        self.setup_axes(animate=False)
        self.add_foreground_mobjects(self.title,ul)
        def func(x):
            return 0.1 * (x + 3-5) * (x - 3-5) * (x-5) + 5

        def rect(x):
            return 2.775*(x-1.5)+3.862
        recta = self.get_graph(rect,x_min=-1,x_max=5)
        graph = self.get_graph(func,x_min=0.2,x_max=9)
        graph.set_color(NEW_BLUE)
        input_tracker_p1 = ValueTracker(1.5)
        input_tracker_p2 = ValueTracker(3.5)

        def get_x_value_p1():
            return input_tracker_p1.get_value()

        def get_x_value_p2():
            return input_tracker_p2.get_value()

        def get_y_value_p1():
            return graph.underlying_function(get_x_value_p1())

        def get_y_value_p2():
            return graph.underlying_function(get_x_value_p2())
##
        def get_x_point_p1():
            return self.coords_to_point(get_x_value_p1(), 0)

        def get_x_point_p2():
            return self.coords_to_point(get_x_value_p2(), 0)
##
        def get_y_point_p1():
            return self.coords_to_point(0, get_y_value_p1())

        def get_y_point_p2():
            return self.coords_to_point(0, get_y_value_p2())
##
        def get_graph_point_p1():
            return self.coords_to_point(get_x_value_p1(), get_y_value_p1())

        def get_graph_point_p2():
            return self.coords_to_point(get_x_value_p2(), get_y_value_p2())

        def get_v_line_p1():
            return DashedLine(get_x_point_p1(), get_graph_point_p1(), stroke_width=2)

        def get_v_line_p2():
            return DashedLine(get_x_point_p2(), get_graph_point_p2(), stroke_width=2)

        def get_h_line_p1():
            return DashedLine(get_graph_point_p1(), get_y_point_p1(), stroke_width=2)

        def get_h_line_p2():
            return DashedLine(get_graph_point_p2(), get_y_point_p2(), stroke_width=2)
        #
        input_triangle_p1 = RegularPolygon(n=3, start_angle=TAU / 4)
        output_triangle_p1 = RegularPolygon(n=3, start_angle=0)
        for triangle in input_triangle_p1, output_triangle_p1:
            triangle.set_fill(WHITE, 1)
            triangle.set_stroke(width=0)
            triangle.scale(0.1)
        #
        input_triangle_p2 = RegularPolygon(n=3, start_angle=TAU / 4)
        output_triangle_p2 = RegularPolygon(n=3, start_angle=0)
        for triangle in input_triangle_p2, output_triangle_p2:
            triangle.set_fill(WHITE, 1)
            triangle.set_stroke(width=0)
            triangle.scale(0.1)
        #
        input_triangle_p1.add_updater(
            lambda m: m.move_to(get_x_point_p1(), DOWN)
        )
        output_triangle_p1.add_updater(lambda m: m.move_to(get_y_point_p1(), LEFT)
        )
        #
        input_triangle_p2.add_updater(lambda m: m.move_to(get_x_point_p2(), DOWN)
        )
        output_triangle_p2.add_updater(lambda m: m.move_to(get_y_point_p2(), LEFT)
        )
        #
        x_label_p1 = TexMobject("a")
        x_label_p1.add_updater(lambda ma: ma.next_to(input_triangle_p1, DOWN, SMALL_BUFF)
        )

        output_label_p1 = TexMobject("f(a)")
        output_label_p1.add_updater(lambda ma: ma.next_to(
                output_triangle_p1, LEFT, SMALL_BUFF)
        )
        #
        x_label_p2 = TexMobject("b")
        x_label_p2.add_updater(lambda mb: mb.next_to(input_triangle_p2, DOWN, SMALL_BUFF)
        )

        output_label_p2 = TexMobject("f(b)")
        output_label_p2.add_updater(lambda mb: mb.next_to(
                output_triangle_p2, LEFT, SMALL_BUFF)
        )
        #
        v_line_p1 = get_v_line_p1()
        v_line_p1.add_updater(lambda vla: Transform(vla, get_v_line_p1())
        )
        #
        v_line_p2 = get_v_line_p2()
        v_line_p2.add_updater(lambda vlb: Transform(vlb, get_v_line_p2())
        )
        #
        h_line_p1 = get_h_line_p1()
        h_line_p1.add_updater(lambda hla: Transform(hla, get_h_line_p1())
        )
        #
        h_line_p2 = get_h_line_p2()
        h_line_p2.add_updater(lambda hlb: Transform(hlb, get_h_line_p2())
        )
        #
        graph_dot_p1 = Dot(color=COLOR_SYMBOL)
        graph_dot_p1.add_updater(lambda ma: ma.move_to(get_graph_point_p1())
        )
        #
        graph_dot_p2 = Dot(color=COLOR_SYMBOL)
        graph_dot_p2.add_updater(lambda mb: mb.move_to(get_graph_point_p2())
        )
        #
        self.play(
            ShowCreation(graph),
        )
        # Animacion
        self.add_foreground_mobject(graph_dot_p1)
        self.add_foreground_mobject(graph_dot_p2)
        self.play(
            DrawBorderThenFill(input_triangle_p1),
            Write(x_label_p1),
            ShowCreation(v_line_p1),
            GrowFromCenter(graph_dot_p1),
            ShowCreation(h_line_p1),
            Write(output_label_p1),
            DrawBorderThenFill(output_triangle_p1),
            DrawBorderThenFill(input_triangle_p2),
            Write(x_label_p2),
            ShowCreation(v_line_p2),
            GrowFromCenter(graph_dot_p2),
            ShowCreation(h_line_p2),
            Write(output_label_p2),
            DrawBorderThenFill(output_triangle_p2),
            run_time=0.5
        )
        self.add(
            input_triangle_p2,
            x_label_p2,
            graph_dot_p2,
            v_line_p2,
            h_line_p2,
            output_triangle_p2,
            output_label_p2,
        )
        ###################
        pendiente_recta = self.get_secant_slope_group(
            1.9, recta, dx = 1.4,
            df_label = None,
            dx_label = None,
            dx_line_color = PURPLE,
            df_line_color= ORANGE,
            )
        grupo_secante = self.get_secant_slope_group(
            1.5, graph, dx = 2,
            df_label = None,
            dx_label = None,
            dx_line_color = "#942357",
            df_line_color= "#3f7d5c",
            secant_line_color = RED,
        )
        start_dx = grupo_secante.kwargs["dx"]
        start_x = grupo_secante.kwargs["x"]
        def update_func_0(group, alpha):
            dx = interpolate(start_dx, 4, alpha)
            x = interpolate(start_x, 1.5, alpha)
            kwargs = dict(grupo_secante.kwargs)
            kwargs["dx"] = dx
            kwargs["x"] = x
            new_group = self.get_secant_slope_group(**kwargs)
            group.become(new_group)
            return group
        def update_func_1(group, alpha):
            dx = interpolate(start_dx, 0.001, alpha)
            x = interpolate(start_x, 1.5, alpha)
            kwargs = dict(grupo_secante.kwargs)
            kwargs["dx"] = dx
            kwargs["x"] = x
            new_group = self.get_secant_slope_group(**kwargs)
            group.become(new_group)
            return group

        self.add(
            input_triangle_p2,
            graph_dot_p2,
            v_line_p2,
            h_line_p2,
            output_triangle_p2,
        )
        self.play(FadeIn(grupo_secante))

        kwargs = {
            "x_min" : 4,
            "x_max" : 9,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        self.graph=graph
        iteraciones=6


        self.rect_list = self.get_riemann_rectangles_list(
            graph, iteraciones,start_color=PURPLE,end_color=ORANGE, **kwargs
        )
        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5,start_color=invert_color(PURPLE),end_color=invert_color(ORANGE),**kwargs
        )
        rects = self.rect_list[0]
        self.transform_between_riemann_rects(
            flat_rects, rects,
            replace_mobject_with_target_in_scene = True,
            run_time=0.9
        )
