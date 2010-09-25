# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Willow Garage, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# author: Wim Meeussen

import roslib; roslib.load_manifest('tf2_py')
import rospy
import tf2
import tf2_py
from tf2_msgs.srv import FrameGraph, FrameGraphResponse

class Buffer(tf2.BufferCore, tf2_py.BufferInterface):
    def __init__(self, cache_time = None, debug = True):
        if cache_time != None:
            tf2.BufferCore.__init__(self, cache_time)
        else:
            tf2.BufferCore.__init__(self)
        tf2_py.BufferInterface.__init__(self)

        if debug:
            self.frame_server = rospy.Service('~tf_frames', FrameGraph, self.__get_frames)

    def __get_frames(self, req):
       return FrameGraphResponse(self.allFramesAsYAML()) 
        
    # lookup, simple api 
    def lookupTransform(self, target_frame, source_frame, time, timeout=rospy.Duration(0.0)):
        self.canTransform(target_frame, source_frame, time, timeout)
        return self.lookupTransformCore(target_frame, source_frame, time)

    # lookup, advanced api 
    def lookupTransformFull(self, target_frame, target_time, source_frame, source_time, fixed_frame, timeout=rospy.Duration(0.0)):
        self.canTransformFull(target_frame, target_time, source_frame, source_time, fixed_frame, timeout)
        return self.lookupTransformFullCore(target_frame, target_time, source_frame, source_time, fixed_frame)


    # can, simple api
    def canTransform(self, target_frame, source_frame, time, timeout=rospy.Duration(0.0)):
        start_time = rospy.Time.now()
        while (rospy.Time.now() < start_time + timeout and 
               not self.canTransformCore(target_frame, source_frame, time)):
            rospy.Duration(0.05).sleep()
        return self.canTransformCore(target_frame, source_frame, time)
    
    # can, advanced api
    def canTransformFull(self, target_frame, target_time, source_frame, source_time, fixed_frame, timeout=rospy.Duration(0.0)):
        start_time = rospy.Time.now()
        while (rospy.Time.now() < start_time + timeout and 
               not self.canTransformFullCore(target_frame, target_time, source_frame, source_time, fixed_frame)):
            rospy.Duration(0.05).sleep()
        return self.canTransformFullCore(target_frame, target_time, source_frame, source_time, fixed_frame)

