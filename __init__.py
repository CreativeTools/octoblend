# -*- coding: utf-8 -*-

#    Author: Ola Sikström <ola.sikstrom@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    'name': 'OctoBlend',
    'description': 'Send objects to OctoPrint server for 3D-printing',
    'author': 'Ola Sikstrom, Creative Tools AB',
    'version': (0, 1),
    'blender': (2, 70),
    'location': '',
    'category': 'Import-Export',
    'warning': 'Made for a development version of OctoPrint',
}

import bpy
import os
import requests
import tempfile


def octoprint_upload(octoprint_host, octoprint_key, filepath, filename):
    """
    Upload file to octoprint server (local storage)
    """
    headers = {'X-Api-Key':octoprint_key}
    url = octoprint_host + '/api/files/local'
    with open(filepath, 'rb') as f:
        r = requests.post(url, files ={'file':(filename,f)}, headers=headers )

    # return True on success
    return r.status_code not in (200, 201)


def main(context):
    """
    Export selected objects as stl to temporary file and upload to octoprint server
    """
    prefs = context.user_preferences.addons[__name__].preferences

    target_filename = context.active_object.name + '.stl'
    tempfile_path = tempfile.mktemp(suffix='.stl')

    # export stl to tempfile path
    bpy.ops.export_mesh.stl(check_existing=False, filepath=tempfile_path)

    # upload to octoprint
    err = octoprint_upload(prefs.server_address, prefs.api_key, tempfile_path, target_filename)

    # remove tempfile
    os.remove(tempfile_path)

    if err:
        return 'Unable to upload to Octoprint server. Check your settings!'

    return None


class OctoBlendPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    server_address = bpy.props.StringProperty(
            name = 'Server address',
            default = 'http://'
    )

    api_key = bpy.props.StringProperty(
            name = 'API Key',
            default = ''
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'server_address')
        layout.prop(self, 'api_key')


class OctoBlendSendOperator(bpy.types.Operator):
    """Send to OctoPrint"""

    bl_idname = "object.octoprint"
    bl_label = "Send To Octoprint"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        error_message = main(context)

        if error_message:
            self.report({'ERROR'}, error_message)
        else:
            self.report({'INFO'}, 'Model sent to OctoPrint')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OctoBlendSendOperator)
    bpy.utils.register_class(OctoBlendPreferences)

def unregister():
    bpy.utils.unregister_class(OctoBlendSendOperator)
    bpy.utils.unregister_class(OctoBlendPreferences)

