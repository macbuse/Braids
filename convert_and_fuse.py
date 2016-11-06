import bpy


def apply_boolean(obj_A, obj_B, bool_type='INTERSECT'):
    
    print('+++',obj_A, obj_B)
    bpy.ops.object.select_all(action='DESELECT')
    obj_A.select= True
    
    bpy.context.scene.objects.active = obj_A
    bpy.ops.object.modifier_add(type='BOOLEAN')

    mod = obj_A.modifiers
    mod[0].name = obj_A.name + bool_type
    mod[0].object = obj_B
    mod[0].operation = bool_type

    bpy.ops.object.modifier_apply(apply_as='DATA', 
								  modifier=mod[0].name)


def decimate_selection(num_iters=2):
    ''
    obs = bpy.context.selected_objects

    for obj_A in obs:
        print(obj_A.name)
        bpy.context.scene.objects.active = obj_A
        bpy.ops.object.modifier_add(type='DECIMATE')
       
        mod = obj_A.modifiers
        mod[0].name = 'xx'
        mod[0].decimate_type = 'UNSUBDIV'
        mod[0].iterations = num_iters
      

        bpy.ops.object.modifier_apply(apply_as='DATA', 
    								  modifier=mod[0].name)


#convert selection to meshes 
#and then fusion for 3D printing

obs = bpy.context.selected_objects
for y in obs[:]:
    y.select = True
    bpy.ops.object.convert(target = 'MESH')


x = obs[0]
for y in obs[1:]:
    apply_boolean(x,y, bool_type = 'UNION')
