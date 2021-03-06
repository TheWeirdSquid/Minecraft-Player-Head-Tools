import bpy

class MPH_PT_panel(bpy.types.Panel):
    bl_idname = "MPH_PT_panel"
    bl_label = "MC Player Head Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MC Head Tools"

    def headIsSelected(self, context):
        if not context.active_object:
            return False
        test1 = True if 'Inner Skin' in context.active_object.name else False
        test2 = True if 'Outer Skin' in context.active_object.name else False
        return (test1 or test2)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Head creation tools
        col = layout.column()
        col.label(text="Creation Tools")
        col.operator("mph.add_head_model", text="New Player Head")

        col.label(text="Texture Tools")
        col.operator('mph.skin_from_blockdata', text="Skin From Blockdata")
        col.operator('mph.skin_from_username', text="Skin From Username")
        col.operator('mph.skin_from_file', text="Skin From File")

        col.label(text="Editing Tools")
        col.operator('mph.prime_cursor', text="Prime Cursor")
        col.operator("mph.delete_faces", text="Delete Faces")

        if self.headIsSelected(context):
            col.label(text="Set Rotation")

            col.label(text="Cardinal Rotation")
            grid = col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
            grid.prop(context.active_object.head_properties, 'cardinal_rotation', expand=True)
            
            col.label(text="Adjust Rotation")
            row = col.row(align=True)
            row.label(icon='REMOVE')
            row.operator('mph.adjust_rotation', text="45°").rotation = -45.0
            row.operator('mph.adjust_rotation', text="45°").rotation = 45.0
            row.label(icon='ADD')
            row = col.row(align=True)
            row.label(icon='REMOVE')
            row.operator('mph.adjust_rotation', text="22.5°").rotation = -22.5
            row.operator('mph.adjust_rotation', text="22.5°").rotation = 22.5
            row.label(icon='ADD')

            col.label(text="Alignment Tools")
            box = col.box()
            box_col = box.column(align = True)
            box_col.label(text = 'Floor Alignment')
            box_col.prop(context.active_object.head_properties, 'floor_alignment', expand=True)
            row = col.row(align=True)
            row.operator('mph.set_to_wall', text="Set to Wall")
            row.operator('mph.set_to_floor', text="Set to Floor")

            col.label(text="Options")
            col.prop(context.scene.mph_panel_settings, 'rotate_to_match_floor_alignment', text="Rotate to Match Floor Alignment")