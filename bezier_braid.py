import bpy
import numpy as np

#Blender 2.77

_weight = 1 # weight


def MakePolyLine(obj_name, 
                curve_name, 
                pts):
                    
    #this is some generic tutorial code
                     
    curve_data = bpy.data.curves.new(name=curve_name, 
                                    type='CURVE')
    curve_data.dimensions = '3D'
    
    obj_data = bpy.data.objects.new(obj_name, 
                                    curve_data)
    bpy.context.scene.objects.link(obj_data)

    polyline = curve_data.splines.new('POLY')
    #add the 'empty' pts first
    polyline.points.add(len(pts)-1)
    for k,pt in enumerate(pts):
        x, y, z = pt
        polyline.points[k].co = (x, y, z, _weight)
        
    
    #added the return 
    return obj_data
        
            
def add_bevel(obj,
              bevel_name='Bevel'):
     #set the bevel object
    try:
        curve = obj.data
        curve.dimensions = '3D'
        curve.bevel_object = bpy.data.objects.get(bevel_name) 
    except:
        print('*warning* no Bevel')



def spiral_pts(npts = 40): 
    rr = 1.
    T = np.linspace(-2*np.pi,2*np.pi, npts)
    R = .25+ 2*(T/2/np.pi)**2

    X = R*np.cos(T)
    Y = R*np.sin(T)
    Z = .5*(rr)*T
    return X,Y,Z,R,T

def double_spiral(npts = 40):
    X,Y,Z,R,T = spiral_pts(npts = npts)

    X = np.append(X, X)
    Y = np.append(Y, Y)
    Z = np.append(Z, Z[:] + 2*Z[-1])

    pts = [v[:] for v in zip(X,Y,Z)]

    obj = MakePolyLine("Double_Spiral", 
                      "spiral_curve", 
                      pts)    
                    
    add_bevel(obj)
    
    return obj

def pipe_spiral():
    
    X,Y,Z,R,T = spiral_pts()
    
    X = np.append(X, [X[-1]] )
    Y = np.append(Y, [Y[-1]])
    
    #smooth off before adding a vertical pipe
    npts = len(T)
    cv_npts = npts/4
    T2 = np.linspace(0,1,cv_npts) 
    cutoff_height = Z[npts - cv_npts]
    Z2 = (1 - np.sqrt(1 - T2))*(Z[-1] - cutoff_height)
    Z = np.append(Z[:npts - cv_npts], Z2 + cutoff_height)
    
    #top off
    Z = np.append(Z, [3*np.pi])
   
    pts = [v[:] for v in zip(X,Y,Z)]
    obj = MakePolyLine("pipe_Spiral", 
                      "spiral_curve", 
                      pts)    
                    
    add_bevel(obj)
    return obj
    
#add the three strands of the braid
double_spiral()

pp = pipe_spiral()
pp.rotation_euler = [0,0,2*np.pi/3]

pp = pipe_spiral()
pp.rotation_euler = [0,np.pi,np.pi/3]
pp.location = [0,0,2*np.pi] 

#add a bottom circle 

bpy.ops.curve.primitive_bezier_circle_add(location = [0,0, -np.pi] )
cc = bpy.context.scene.objects.active
rr = 2.24
cc.scale = [rr,rr,rr]
add_bevel(cc, bevel_name='Bevel2' )

#add a top circle 

bpy.ops.object.duplicate()
cc = bpy.context.scene.objects.active
cc.location = [0,0, 3*np.pi]
