import bpy

class MPH_OT_set_floor_alignment(bpy.types.Operator):
    """Sets the floor alignment for the current head based on the alignment selection in the MC Heads panel"""
    bl_idname = 'mph.set_floor_alignment'
    bl_label = 'Set Floor Alignment'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        test1 = True if 'Inner Skin' in context.active_object.name else False
        test2 = True if 'Outer Skin' in context.active_object.name else False
        return (test1 or test2)
    
    def execute(self, context):
        alignment = context.active_object.head_properties.floor_alignment

        # get if inner head or outer head
        iteration = context.active_object.name[10:]
        if 'Inner Skin' in context.active_object.name:
            obj_name = 'Inner Skin' + iteration
            update_obj = bpy.data.objects['Outer Skin' + iteration]
        if 'Outer Skin' in context.active_object.name:
            obj_name = 'Outer Skin' + iteration
            update_obj = bpy.data.objects['Inner Skin' + iteration]

        obj = bpy.data.objects[obj_name]

        # if the alignment is set to none, just keep position and update enum select. No use running all this code for no reason
        if alignment != 'NONE':

            # lock horizantal movement
            obj.lock_location[0] = True # locks x movement
            obj.lock_location[1] = True # locks y movement

            # get z position
            head_x = obj.location.x
            head_y = obj.location.y

            # get block offset
            head_offset_x = head_x % 1
            head_offset_y = head_y % 1

            # get block position
            head_block_x = head_x - head_offset_x
            head_block_y = head_y - head_offset_y

            # check if rotate to match floor alignment is enabled
            fix_rot = context.scene.mph_panel_settings.rotate_to_match_floor_alignment


            if alignment == 'CENTER':
                # set x and y to center of the block (0.5)
                x_offset = 0.5
                y_offset = 0.5
                obj.location.x = head_block_x + x_offset
                obj.location.y = head_block_y + y_offset
            elif alignment == 'NORTH':
                # set y to 0.25 and x to 0.5
                x_offset = 0.5
                y_offset = 0.25
                obj.location.x = head_block_x + x_offset
                obj.location.y = head_block_y + y_offset
                if fix_rot:
                    obj.head_properties.cardinal_rotation = 'SOUTH'
            elif alignment == 'EAST':
                # set y to 0.5 and x to 0.75
                x_offset = 0.75
                y_offset = 0.5
                obj.location.x = head_block_x + x_offset
                obj.location.y = head_block_y + y_offset
                if fix_rot:
                    obj.head_properties.cardinal_rotation = 'WEST'
            elif alignment == 'SOUTH':
                # set y to 0.75 and x to 0.5
                x_offset = 0.5
                y_offset = 0.75
                obj.location.x = head_block_x + x_offset
                obj.location.y = head_block_y + y_offset
                if fix_rot:
                    obj.head_properties.cardinal_rotation = 'NORTH'
            elif alignment == 'WEST':
                # set y to 0.5 and x to 0.25
                x_offset = 0.25
                y_offset = 0.5
                obj.location.x = head_block_x + x_offset
                obj.location.y = head_block_y + y_offset
                if fix_rot:
                    obj.head_properties.cardinal_rotation = 'EAST'
            elif alignment == 'OTHER':
                pass
            else:
                return {'CANCELLED'}
        else:
            # unlock horizantal movement
            obj.lock_location[0] = False # unlock x movement
            obj.lock_location[1] = False # unlock y movement

        if update_obj.head_properties.floor_alignment != alignment:
            bpy.context.view_layer.objects.active = update_obj
            update_obj.head_properties.floor_alignment = alignment
        else:
            bpy.context.view_layer.objects.active = update_obj
        
        return {'FINISHED'}
    
    def run_update(self, context):
        # this way, the function called (this one) returns None
        bpy.ops.mph.set_floor_alignment()