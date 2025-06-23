├── .gitignore
├── LICENSE
├── README.md
├── account
    └── account_sample.py
├── blueprint.py
├── blueprint_data.py
├── botlib.py
├── build.py
├── chat.py
├── combat.py
├── farming.py
├── gather.py
├── inventory.py
├── mine.py
├── movement.py
├── pybot.py
├── test.py
├── ui.py
└── workarea.py


/.gitignore:
--------------------------------------------------------------------------------
 1 | # Python
 2 | __pycache__/
 3 | *.pyc
 4 | 
 5 | # General
 6 | .DS_Store
 7 | 
 8 | # MSFT
 9 | .vs
10 | *.mdproj
11 | *.sln
12 | 


--------------------------------------------------------------------------------
/LICENSE:
--------------------------------------------------------------------------------
  1 |                                  Apache License
  2 |                            Version 2.0, January 2004
  3 |                         http://www.apache.org/licenses/
  4 | 
  5 |    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
  6 | 
  7 |    1. Definitions.
  8 | 
  9 |       "License" shall mean the terms and conditions for use, reproduction,
 10 |       and distribution as defined by Sections 1 through 9 of this document.
 11 | 
 12 |       "Licensor" shall mean the copyright owner or entity authorized by
 13 |       the copyright owner that is granting the License.
 14 | 
 15 |       "Legal Entity" shall mean the union of the acting entity and all
 16 |       other entities that control, are controlled by, or are under common
 17 |       control with that entity. For the purposes of this definition,
 18 |       "control" means (i) the power, direct or indirect, to cause the
 19 |       direction or management of such entity, whether by contract or
 20 |       otherwise, or (ii) ownership of fifty percent (50%) or more of the
 21 |       outstanding shares, or (iii) beneficial ownership of such entity.
 22 | 
 23 |       "You" (or "Your") shall mean an individual or Legal Entity
 24 |       exercising permissions granted by this License.
 25 | 
 26 |       "Source" form shall mean the preferred form for making modifications,
 27 |       including but not limited to software source code, documentation
 28 |       source, and configuration files.
 29 | 
 30 |       "Object" form shall mean any form resulting from mechanical
 31 |       transformation or translation of a Source form, including but
 32 |       not limited to compiled object code, generated documentation,
 33 |       and conversions to other media types.
 34 | 
 35 |       "Work" shall mean the work of authorship, whether in Source or
 36 |       Object form, made available under the License, as indicated by a
 37 |       copyright notice that is included in or attached to the work
 38 |       (an example is provided in the Appendix below).
 39 | 
 40 |       "Derivative Works" shall mean any work, whether in Source or Object
 41 |       form, that is based on (or derived from) the Work and for which the
 42 |       editorial revisions, annotations, elaborations, or other modifications
 43 |       represent, as a whole, an original work of authorship. For the purposes
 44 |       of this License, Derivative Works shall not include works that remain
 45 |       separable from, or merely link (or bind by name) to the interfaces of,
 46 |       the Work and Derivative Works thereof.
 47 | 
 48 |       "Contribution" shall mean any work of authorship, including
 49 |       the original version of the Work and any modifications or additions
 50 |       to that Work or Derivative Works thereof, that is intentionally
 51 |       submitted to Licensor for inclusion in the Work by the copyright owner
 52 |       or by an individual or Legal Entity authorized to submit on behalf of
 53 |       the copyright owner. For the purposes of this definition, "submitted"
 54 |       means any form of electronic, verbal, or written communication sent
 55 |       to the Licensor or its representatives, including but not limited to
 56 |       communication on electronic mailing lists, source code control systems,
 57 |       and issue tracking systems that are managed by, or on behalf of, the
 58 |       Licensor for the purpose of discussing and improving the Work, but
 59 |       excluding communication that is conspicuously marked or otherwise
 60 |       designated in writing by the copyright owner as "Not a Contribution."
 61 | 
 62 |       "Contributor" shall mean Licensor and any individual or Legal Entity
 63 |       on behalf of whom a Contribution has been received by Licensor and
 64 |       subsequently incorporated within the Work.
 65 | 
 66 |    2. Grant of Copyright License. Subject to the terms and conditions of
 67 |       this License, each Contributor hereby grants to You a perpetual,
 68 |       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
 69 |       copyright license to reproduce, prepare Derivative Works of,
 70 |       publicly display, publicly perform, sublicense, and distribute the
 71 |       Work and such Derivative Works in Source or Object form.
 72 | 
 73 |    3. Grant of Patent License. Subject to the terms and conditions of
 74 |       this License, each Contributor hereby grants to You a perpetual,
 75 |       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
 76 |       (except as stated in this section) patent license to make, have made,
 77 |       use, offer to sell, sell, import, and otherwise transfer the Work,
 78 |       where such license applies only to those patent claims licensable
 79 |       by such Contributor that are necessarily infringed by their
 80 |       Contribution(s) alone or by combination of their Contribution(s)
 81 |       with the Work to which such Contribution(s) was submitted. If You
 82 |       institute patent litigation against any entity (including a
 83 |       cross-claim or counterclaim in a lawsuit) alleging that the Work
 84 |       or a Contribution incorporated within the Work constitutes direct
 85 |       or contributory patent infringement, then any patent licenses
 86 |       granted to You under this License for that Work shall terminate
 87 |       as of the date such litigation is filed.
 88 | 
 89 |    4. Redistribution. You may reproduce and distribute copies of the
 90 |       Work or Derivative Works thereof in any medium, with or without
 91 |       modifications, and in Source or Object form, provided that You
 92 |       meet the following conditions:
 93 | 
 94 |       (a) You must give any other recipients of the Work or
 95 |           Derivative Works a copy of this License; and
 96 | 
 97 |       (b) You must cause any modified files to carry prominent notices
 98 |           stating that You changed the files; and
 99 | 
100 |       (c) You must retain, in the Source form of any Derivative Works
101 |           that You distribute, all copyright, patent, trademark, and
102 |           attribution notices from the Source form of the Work,
103 |           excluding those notices that do not pertain to any part of
104 |           the Derivative Works; and
105 | 
106 |       (d) If the Work includes a "NOTICE" text file as part of its
107 |           distribution, then any Derivative Works that You distribute must
108 |           include a readable copy of the attribution notices contained
109 |           within such NOTICE file, excluding those notices that do not
110 |           pertain to any part of the Derivative Works, in at least one
111 |           of the following places: within a NOTICE text file distributed
112 |           as part of the Derivative Works; within the Source form or
113 |           documentation, if provided along with the Derivative Works; or,
114 |           within a display generated by the Derivative Works, if and
115 |           wherever such third-party notices normally appear. The contents
116 |           of the NOTICE file are for informational purposes only and
117 |           do not modify the License. You may add Your own attribution
118 |           notices within Derivative Works that You distribute, alongside
119 |           or as an addendum to the NOTICE text from the Work, provided
120 |           that such additional attribution notices cannot be construed
121 |           as modifying the License.
122 | 
123 |       You may add Your own copyright statement to Your modifications and
124 |       may provide additional or different license terms and conditions
125 |       for use, reproduction, or distribution of Your modifications, or
126 |       for any such Derivative Works as a whole, provided Your use,
127 |       reproduction, and distribution of the Work otherwise complies with
128 |       the conditions stated in this License.
129 | 
130 |    5. Submission of Contributions. Unless You explicitly state otherwise,
131 |       any Contribution intentionally submitted for inclusion in the Work
132 |       by You to the Licensor shall be under the terms and conditions of
133 |       this License, without any additional terms or conditions.
134 |       Notwithstanding the above, nothing herein shall supersede or modify
135 |       the terms of any separate license agreement you may have executed
136 |       with Licensor regarding such Contributions.
137 | 
138 |    6. Trademarks. This License does not grant permission to use the trade
139 |       names, trademarks, service marks, or product names of the Licensor,
140 |       except as required for reasonable and customary use in describing the
141 |       origin of the Work and reproducing the content of the NOTICE file.
142 | 
143 |    7. Disclaimer of Warranty. Unless required by applicable law or
144 |       agreed to in writing, Licensor provides the Work (and each
145 |       Contributor provides its Contributions) on an "AS IS" BASIS,
146 |       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
147 |       implied, including, without limitation, any warranties or conditions
148 |       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
149 |       PARTICULAR PURPOSE. You are solely responsible for determining the
150 |       appropriateness of using or redistributing the Work and assume any
151 |       risks associated with Your exercise of permissions under this License.
152 | 
153 |    8. Limitation of Liability. In no event and under no legal theory,
154 |       whether in tort (including negligence), contract, or otherwise,
155 |       unless required by applicable law (such as deliberate and grossly
156 |       negligent acts) or agreed to in writing, shall any Contributor be
157 |       liable to You for damages, including any direct, indirect, special,
158 |       incidental, or consequential damages of any character arising as a
159 |       result of this License or out of the use or inability to use the
160 |       Work (including but not limited to damages for loss of goodwill,
161 |       work stoppage, computer failure or malfunction, or any and all
162 |       other commercial damages or losses), even if such Contributor
163 |       has been advised of the possibility of such damages.
164 | 
165 |    9. Accepting Warranty or Additional Liability. While redistributing
166 |       the Work or Derivative Works thereof, You may choose to offer,
167 |       and charge a fee for, acceptance of support, warranty, indemnity,
168 |       or other liability obligations and/or rights consistent with this
169 |       License. However, in accepting such obligations, You may act only
170 |       on Your own behalf and on Your sole responsibility, not on behalf
171 |       of any other Contributor, and only if You agree to indemnify,
172 |       defend, and hold each Contributor harmless for any liability
173 |       incurred by, or claims asserted against, such Contributor by reason
174 |       of your accepting any such warranty or additional liability.
175 | 
176 |    END OF TERMS AND CONDITIONS
177 | 
178 |    APPENDIX: How to apply the Apache License to your work.
179 | 
180 |       To apply the Apache License to your work, attach the following
181 |       boilerplate notice, with the fields enclosed by brackets "[]"
182 |       replaced with your own identifying information. (Don't include
183 |       the brackets!)  The text should be enclosed in the appropriate
184 |       comment syntax for the file format. We also recommend that a
185 |       file or class name and description of purpose be included on the
186 |       same "printed page" as the copyright notice for easier
187 |       identification within third-party archives.
188 | 
189 |    Copyright [yyyy] [name of copyright owner]
190 | 
191 |    Licensed under the Apache License, Version 2.0 (the "License");
192 |    you may not use this file except in compliance with the License.
193 |    You may obtain a copy of the License at
194 | 
195 |        http://www.apache.org/licenses/LICENSE-2.0
196 | 
197 |    Unless required by applicable law or agreed to in writing, software
198 |    distributed under the License is distributed on an "AS IS" BASIS,
199 |    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
200 |    See the License for the specific language governing permissions and
201 |    limitations under the License.
202 | 


--------------------------------------------------------------------------------
/README.md:
--------------------------------------------------------------------------------
 1 | # pybot - A Minecraft bot written in Python using Mineflayer
 2 | 
 3 | pybot is a Minecraft bot written using the Mineflayer framework via the Python to Javascript bridge. It is built for practical utility automating such tasks as mining for resources, mining out rooms or long corridors, building bridges, farming, chopping wood, building structures and moving around resources between chests. It has a partially complete UI written in Tk.
 4 | 
 5 | Tested with Java Edition 1.16.5.
 6 | It will *NOT* work with 1.18 or 1.19.
 7 | 
 8 | ### Authors
 9 | 
10 | Guido Appenzeller, Daniel Appenzeller
11 | 
12 | ### License
13 | 
14 | Released under Apache 2.0
15 | 
16 | ## Requirements
17 | 
18 | To run the bot, your system needs to have:
19 | - A recent version of Python. On macOS, the easiest is to install Python 3 from the www.python.org website. Homebrew python may require the additional install of tkinter.
20 | - The Python/JavaScript bridge. 'pip3 install javascript' should do the trick.
21 | 
22 | ## Setup
23 | 
24 | Copy the account_sample.py to account/account.py and edit the following fields:
25 | - User Name
26 | - Password
27 | - Server IP or name
28 | - "master" is the in-game name of the player that the bot should take commands from (i.e. your in-game name)
29 | - version to the server's minecraft version
30 | 
31 | You can also specify locations in this file. This is mostly useful to have the bot transfer contents between chests.
32 | 
33 | Normally the bot will open a Window, but you can also run it without any graphical UX using the "--nowindow" option.
34 | 
35 | ## Functionality
36 | 
37 | Simple commands are given via chat. The bot has a specific "master" player that it will listen to. Try "come", "inventory" or "status" to get an idea. Other users can also give commands but need to preface it with a callsign.
38 | 
39 | Many activities can be stopped with the command "stop". 
40 | 
41 | PyBot starts most complex activities around a chest. There are two types:
42 | - For an activity that doesn't need a specific direction, like farming an area, it's just a chest. Material (e.g. seeds) and resources (e.g. wheat) will be taken from or, after collecting them, placed into that chest.
43 | - For activities that do have a direction (e.g. dig a tunnel in a specific direction), starting point is a chest and the direction is indicated by placing a torch on the ground directly next to the chest. 
44 | 
45 | For these activities, have the bot come next to the chest and once it is there tell it to "farm" or "mine 3x3".
46 | 
47 | ### Farming
48 | 
49 | To start, place a chest in the area you want to farm and start with "farm". The bot will take seeds from the cest, and plant them in any nearby farmland that it can reach. If there are fully grown crops, the pot will harvest them and place them and any extra seeds in the chest. Chat "stop" to stop the bot. Right now, only Wheat is in the code, but other crops are easy to add.
50 | 
51 | ### Chop Wood
52 | 
53 | Right now only works with mega spruce trees as they are the most efficient. Plant 2x2 saplings and get a tree with up to 100 blocks of wood. Place a chest within 25 blocks from the tree, place a few stone axes and bread as food in the chest and start with "chop". The bot will do a spiral cut up the trunk and then cut down. It will continue to chop down trees as long as it finds them and deposit the wood into the chest.
54 | 
55 | Right now, this activity can't be aborted with stop.
56 | 
57 | ### Mining
58 | 
59 | Supports:
60 | - Use "mine fast" to start strip mining. By default it will clear a 11 wide and 9 high area of all valuable blocks (it can see through walls to find it)
61 | - Mine large corridors, try "mine 3x3" or "mine 5x5"
62 | - The bot will looking for valuable ores off corridors, usually with a default distance of 5
63 | - The bot will also look in ceilings and the floor up to 2 deep
64 | - Try "boxmine" to mine out large areas for underground rooms
65 | - The bot will automatically bridge across chasms/lava
66 | - It will not defend itself yet, but it will run away when taking damage and ninja-log when below 50%
67 | - It will light up tunnels
68 | - If you put a wall sign close to the chest, the bot will record its progress on that sign (e.g. length of tunnel, dangers etc.)
69 | 
70 | If there is a chest-in-a-minecart next to the starting chest, the bot will deposit into the minecart, and restock from the chest. That makes it easy to keep it supplied with tools while hauling away resources automatically
71 | 
72 | ### Movement
73 | 
74 | Try "come" to make the bot come to the player
75 | 
76 | ### Building
77 | 
78 | Still early, but if you add a blueprint to blueprint_list.py, the bot can build it. Starting point is a chest with a torch. The bot can build a full sorting system with "build sorter".
79 | 


--------------------------------------------------------------------------------
/account/account_sample.py:
--------------------------------------------------------------------------------
 1 | #
 2 | # Account information
 3 | #
 4 | # Copy this file to account.py and fill in the real values for the Minecraft account.
 5 | #
 6 | # 
 7 | #
 8 | #
 9 | 
10 | account = {
11 |         "user"      : 'your@login.com',
12 |         "password"  : 'your_password',
13 |         "master"    : 'minecraft_name_who_the_bot_will_listen_to',
14 |         "host"      : 'exampleserver.whatever.com',
15 |         "version"   : '1.16.5',
16 | }
17 | 
18 | #
19 | # List of world locations you can use in commands
20 | #
21 | 
22 | locations = {
23 |         "minedrop": [29,13,-19],
24 |         "farmdrop": [42.5,89,-15.5],
25 |         "minecenter": [20.5,12,-23.5],
26 | }


--------------------------------------------------------------------------------
/blueprint.py:
--------------------------------------------------------------------------------
 1 | #
 2 | # Class for encapsulating special build instructions for a specific block
 3 | # in a blueprint
 4 | #
 5 | 
 6 | from dataclasses import dataclass
 7 | from javascript import require
 8 | Vec3     = require('vec3').Vec3
 9 | 
10 | @dataclass
11 | class SpecialBuild:
12 |     bot_pos : Vec3 = None
13 |     block_against : Vec3 = None
14 |     block_surface : Vec3 = None
15 |     placement_type: str = None
16 |     sneak : bool = False
17 |     jump : bool = False
18 | 
19 | #
20 | # Class that stores a blueprint
21 | #
22 | 
23 | class Blueprint:
24 | 
25 |     def __init__(self, name, width=0, height=0, depth=0, bpData=None, buildFunction=None):
26 |         self.name = name
27 |         self.buildFunction = buildFunction
28 |         self.bpData = bpData
29 |         self.width = width
30 |         self.width2 = int((width-1)/2)
31 |         self.height = height
32 |         self.depth = depth
33 |         
34 |     def xRange(self):
35 |         return range(-self.width2, self.width2+1)
36 | 
37 |     def yRange(self):
38 |         return range(0,self.height)
39 | 
40 |     def zRange(self):
41 |         return range(0,self.depth)
42 | 
43 |     def blockAt(self,v):
44 |         return self.block(v.x,v.y,v.z)
45 | 
46 |     def block(self,x,y,z):
47 |         if x not in self.xRange() or y not in self.yRange() or z not in self.zRange():
48 |             print(f'*** error blueprint {self} index out of range {x} {y} {z}.')
49 |             return False
50 |         # Note: need to invert the y axis
51 |         # print(f'[{x+self.width2}][{self.height-1-y}][{z}]')
52 |         return self.bpData[z][self.height-1-y][x+self.width2]
53 | 
54 |     def __str__(self):
55 |         return(self.name)


--------------------------------------------------------------------------------
/blueprint_data.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Blueprints for construction
  3 | #
  4 | 
  5 | from javascript import require
  6 | Vec3     = require('vec3').Vec3
  7 | 
  8 | from blueprint import SpecialBuild, Blueprint
  9 | 
 10 | 
 11 | # Test Blueprint 1x2x1
 12 | 
 13 | bp_test = [
 14 |         [
 15 |                 ["Torch"],
 16 |                 ["Cobblestone"],
 17 |         ]
 18 | ]
 19 | 
 20 | # Sorting System
 21 | # 3 x 4 x 6
 22 | # Two parts as we have to build the Chests first
 23 | 
 24 | bp_sorter_1 = [
 25 |   [
 26 |     ["Air"          , "Air"          , "Air" , ],
 27 |     ["Chest"        , "Chest"        , "Air" , ],
 28 |     ["Chest"        , "Chest"        , "Air" , ],
 29 |     ["Chest"        , "Chest"        , "Air" , ],
 30 |   ]
 31 | ]
 32 | 
 33 | bp_sorter_2 = [
 34 |   [
 35 |     ["Air"          , "Air"          , "Stone Bricks" , ],
 36 |     ["Chest"        , "Chest"        , "Stone Bricks" , ],
 37 |     ["Chest"        , "Chest"        , "Stone Bricks" , ],
 38 |     ["Chest"        , "Chest"        , "Stone Bricks" , ],
 39 |   ],
 40 |   [
 41 |     ["Hopper"       , "Hopper"       , "Hopper"       , ],
 42 |     ["Hopper"       , "Hopper"       , "Hopper"       , ],
 43 |     ["Hopper"       , "Air"          , "Hopper"       , ],
 44 |     ["Air"          , "Hopper"       , "Hopper"       , ],
 45 |   ],
 46 |   [
 47 |     ["Redstone Comparator", "Redstone Comparator", "Redstone Comparator", ],
 48 |     ["Stone Bricks" , "Stone Bricks" , "Stone Bricks" , ],
 49 |     ["Redstone Wall Torch", "Redstone Wall Torch", "Redstone Wall Torch", ],
 50 |     ["Air"          , "Air"          , "Air"          , ],
 51 |   ],
 52 |   [
 53 |     ["Redstone Wire", "Redstone Wire", "Redstone Wire", ],
 54 |     ["Stone Bricks" , "Stone Bricks" , "Stone Bricks" , ],
 55 |     ["Stone Bricks" , "Stone Bricks" , "Stone Bricks" , ],
 56 |     ["Air"          , "Air"          , "Air"          , ],
 57 |   ],
 58 |   [
 59 |     ["Redstone Wire", "Redstone Wire", "Redstone Wire", ],
 60 |     ["Stone Bricks" , "Stone Bricks" , "Stone Bricks" , ],
 61 |     ["Redstone Repeater", "Redstone Repeater", "Redstone Repeater", ],
 62 |     ["Stone Bricks" , "Stone Bricks" , "Stone Bricks" , ],
 63 |   ],
 64 |   [
 65 |     ["Air"          , "Air"          , "Air"          , ],
 66 |     ["Redstone Wire", "Redstone Wire", "Redstone Wire", ],
 67 |     ["Stone Bricks" , "Stone Bricks" , "Stone Bricks" , ],
 68 |     ["Air"          , "Air"          , "Air"          , ],
 69 |   ],
 70 | ]
 71 | 
 72 | def bp_sorter_buildf_1(x,y,z):
 73 |     # right chest halves place against left
 74 |     if x == 0 and y < 3:
 75 |         s = SpecialBuild()
 76 |         s.block_surface = Vec3(1,0,0)
 77 |         s.block_against = Vec3(-1,y,0)
 78 |         return s
 79 | 
 80 | def bp_sorter_buildf_2(x,y,z):
 81 | 
 82 |     # Redstone repeaters
 83 |     if y== 1 and z == 4:
 84 |         s = SpecialBuild()
 85 |         s.bot_pos = Vec3(x,2,z+1.5)
 86 |         return s
 87 | 
 88 |     # Hoppers. What a mess.
 89 |     if z == 1:
 90 |         if y == 0:
 91 |             #bottom row
 92 |             if x == 0:
 93 |                 s = SpecialBuild()
 94 |                 s.bot_pos = Vec3(0,0,2)
 95 |                 s.block_against = Vec3(0,0,0)
 96 |                 s.block_surface = Vec3(0,0,1)
 97 |                 return s
 98 |             if x == 1:
 99 |                 s = SpecialBuild()
100 |                 s.bot_pos = Vec3(1,0,2)
101 |                 s.block_against = Vec3(0,0,1)
102 |                 s.block_surface = Vec3(1,0,0)
103 |                 return s
104 |         if y == 1:
105 |             #2nd row
106 |             if x == -1:
107 |                 s = SpecialBuild()
108 |                 s.bot_pos = Vec3(-1,0,2)
109 |                 s.block_against = Vec3(-1,1,0)
110 |                 s.block_surface = Vec3(0,0,1)
111 |                 return s
112 |             if x == 1:
113 |                 s = SpecialBuild()
114 |                 s.bot_pos = Vec3(0,0,2)
115 |                 return s
116 |         if y == 2:
117 |             #3rd row
118 |             if x == -1:
119 |                 s = SpecialBuild()
120 |                 s.bot_pos = Vec3(-2,0,2)
121 |                 return s
122 |             if x == 0:
123 |                 s = SpecialBuild()
124 |                 s.bot_pos = Vec3(0,0,2)
125 |                 s.block_against = Vec3(0,2,0)
126 |                 s.block_surface = Vec3(0,0,1)
127 |                 return s
128 |             if x == 1:
129 |                 s = SpecialBuild()
130 |                 s.bot_pos = Vec3(2,0,2)
131 |                 return s
132 |         if y == 3:
133 |             #3rd row
134 |             if x == -1:
135 |                 s = SpecialBuild()
136 |                 s.bot_pos = Vec3(0,0,2)
137 |                 s.block_against = Vec3(-1,3,2)
138 |                 s.block_surface = Vec3(0,0,-1)
139 |                 return s
140 |             if x == 0:
141 |                 s = SpecialBuild()
142 |                 s.bot_pos = Vec3(0,0,2)
143 |                 s.block_against = Vec3(0,3,2)
144 |                 s.block_surface = Vec3(0,0,-1)
145 |                 return s
146 |             if x == 1:
147 |                 s = SpecialBuild()
148 |                 s.bot_pos = Vec3(0,0,2)
149 |                 s.block_against = Vec3(1,3,2)
150 |                 s.block_surface = Vec3(0,0,-1)
151 |                 return s
152 | 
153 | #
154 | # Phases of a build are named NAME_1, NAME_2 etc.
155 | #
156 | 
157 | def init(pybot):
158 |     pybot.learnBlueprint( Blueprint("sorter_1",3,4,1,bp_sorter_1, bp_sorter_buildf_1) )
159 |     pybot.learnBlueprint( Blueprint("sorter_2",3,4,6,bp_sorter_2, bp_sorter_buildf_2) ) 
160 |     pybot.learnBlueprint( Blueprint("test_1",  1,2,1,bp_test,     None)               )
161 | 


--------------------------------------------------------------------------------
/botlib.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Utility functions that didn't fit anywhere else
  3 | #
  4 | 
  5 | import time
  6 | import datetime
  7 | 
  8 | from javascript import require
  9 | 
 10 | from math import sqrt, atan2, sin, cos
 11 | 
 12 | Vec3  = require('vec3').Vec3
 13 | 
 14 | def myTime():
 15 |     now = datetime.datetime.now()
 16 |     return now.strftime("%H:%M:%S")
 17 | 
 18 | def myDate():
 19 |     now = datetime.datetime.now()
 20 |     return now.strftime("%m/%d/%y %H:%M")
 21 | 
 22 | 
 23 | 
 24 | #
 25 | # Math helper functions
 26 | #
 27 | 
 28 | def addVec3(v1,v2):
 29 |     return Vec3(v1.x+v2.x,v1.y+v2.y,v1.z+v2.z)
 30 | 
 31 | def subVec3(v1,v2):
 32 |     return Vec3(v1.x-v2.x,v1.y-v2.y,v1.z-v2.z)
 33 | 
 34 | def invVec3(v1):
 35 |     return Vec3(-v1.x,-v1.y,-v1.z)
 36 | 
 37 | 
 38 | def lenVec3(v):
 39 |     return sqrt(v.x*v.x+v.y*v.y+v.z*v.z)
 40 | 
 41 | # Minecraft is a right-handed coordinate system
 42 | #
 43 | #    0--------X------->  
 44 | #    |      North
 45 | #    Z   West   East
 46 | #    |      South
 47 | #    V    
 48 | 
 49 | def rotateLeft(v):
 50 |     return Vec3(v.z,0,-v.x)
 51 | 
 52 | def rotateRight(v):
 53 |     return Vec3(-v.z,0,v.x)
 54 | 
 55 | def directionStr(v):
 56 |     if abs(v.x) > abs(v.z):
 57 |         if v.x > 0:
 58 |             return "East"
 59 |         else:
 60 |             return "West"
 61 |     else:
 62 |         if v.z > 0:
 63 |             return "South"
 64 |         else:
 65 |             return "North"
 66 | 
 67 | def strDirection(d_str):
 68 |     d = d_str.lower()[0]
 69 |     if   d == 'n':
 70 |         return Vec3(0,0,-1)
 71 |     elif d == 's':
 72 |         return Vec3(0,0, 1)
 73 |     elif d == 'e':
 74 |         return Vec3(1,0, 0)
 75 |     elif d == 'w':
 76 |         return Vec3(-1,0,0)
 77 |     else:
 78 |         return None                
 79 | 
 80 | 
 81 | def distanceVec3(v1,v2):
 82 |     if not v1:
 83 |         print("*** error: v1 in distanceVec3() is null.")
 84 |         return None
 85 |     if not v2:
 86 |         print("*** error: v2 in distanceVec3() is null.")
 87 |         return None
 88 |     dv = subVec3(v1,v2)
 89 |     return lenVec3(dv)
 90 | 
 91 | def walkTime(v1,v2):
 92 |     if not v1:
 93 |         print("*** error: v1 in walkTime() is null.")
 94 |         return None
 95 |     if not v2:
 96 |         print("*** error: v2 in walkTime() is null.")
 97 |         return None
 98 |     d = distanceVec3(v1,v2)
 99 |     return d/4.3+0.1
100 | 
101 | def getViewVector (pitch, yaw):
102 |     csPitch = cos(pitch)
103 |     snPitch = sin(pitch)
104 |     csYaw = cos(yaw)
105 |     snYaw = sin(yaw)
106 |     #print(f'ViewVector {pitch} / {yaw} -> {-snYaw * csPitch},{snPitch},{-csYaw * csPitch}' )
107 |     return Vec3(-snYaw * csPitch, snPitch, -csYaw * csPitch)
108 | 
109 | # Generator that steps through the outer part of a rectangle of w x h centered around 0,0
110 | 
111 | def rectangleBorder(w,h):
112 | 
113 |     if w == 0 and h == 0:
114 |         yield 0,0
115 |     elif h == 0:
116 |         for dx in range(-w,w+1):
117 |             yield dx,0
118 |     elif w == 0:
119 |         for dy in range(-h,h+1):
120 |             yield 0,dy
121 |     else:
122 |         for dx in range(-w,w+1):
123 |             yield dx,h
124 |         for dy in range(h-1,-h-1,-1):
125 |             yield w,dy
126 |         for dx in range(w-1,-w-1,-1):
127 |             yield dx,-h
128 |         for dy in range(-h+1,h):
129 |             yield -w,dy
130 | 
131 | def checkIntArg(x, min, max):
132 |     if not x.lstrip('-').isdigit():
133 |         return None
134 |     x = int(x)
135 |     if x >= min and x <= max:
136 |         return x
137 |     else:
138 |         return None
139 | 
140 | def directionToVector(block):
141 |     m = block.metadata
142 | 
143 |     if   m == 1: #North  001 vs 010
144 |         return Vec3(0,0,-1)
145 |     elif m == 3: # South 011 vs 011
146 |         return Vec3(0,0,1)
147 |     elif m == 5: # West  101 vs 100
148 |         return Vec3(-1,0,0)
149 |     elif m == 7: # East  111 vs 101
150 |         return Vec3(1,0,0)
151 |     else:
152 |         return False
153 | 
154 | # Return a color based on current/max
155 | 
156 | def colorHelper(x,max):
157 |     if x/max > 0.95:
158 |         return "white","green"
159 |     elif x/max > 0.75:
160 |         return "black","yellow"
161 |     elif x/max > 0.5:
162 |         return "black","orange"
163 |     else:
164 |         return "white","red"
165 | 
166 | 
167 | 
168 | 
169 | 
170 | 
171 | 
172 | 
173 | 
174 | 
175 | 
176 | 


--------------------------------------------------------------------------------
/build.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Build various blueprints
  3 | #
  4 | 
  5 | from javascript import require
  6 | from botlib import *
  7 | 
  8 | Vec3     = require('vec3').Vec3
  9 | 
 10 | from blueprint import *
 11 | from workarea import *
 12 | 
 13 | import blueprint_data
 14 | 
 15 | #
 16 | # Main class that has the build, analyze and helper functions
 17 | #
 18 | 
 19 | class BuildBot:
 20 | 
 21 |     def __init__(self):
 22 |         self.blueprintList = []
 23 |         print('build ', end='')
 24 |         blueprint_data.init(self)
 25 | 
 26 |     def learnBlueprint(self,b):
 27 |         self.blueprintList.append(b)
 28 | 
 29 |     def listBlueprints(self):
 30 |         return ' '.join([str(n) for n in Blueprint.bpList])
 31 | 
 32 |     def getBlueprint(self,name):
 33 |         for b in self.blueprintList:
 34 |             if str(b) == name:
 35 |                 return b
 36 |         else:
 37 |             return None
 38 | 
 39 | 
 40 |     emptyBlocks = {
 41 |         "Air",
 42 |         "Cave Air",
 43 |         "Void Air",
 44 |     }
 45 | 
 46 |     # Blocks where the inventory item is different from the block in the world
 47 | 
 48 |     blockW2I = {
 49 |         "Redstone Wire": "Redstone Dust",
 50 |         "Redstone Wall Torch": "Redstone Torch",
 51 |     }
 52 | 
 53 |     # Blocks that require sneak to place against (chests, repeaters etc.)
 54 | 
 55 |     interactiveBlocks = [
 56 |         "Redstone Repeater",
 57 |         "Redstone Comparator",
 58 |         "Chest",
 59 |         "Hopper",
 60 |     ]
 61 | 
 62 |     #
 63 |     #  Translate world blocks to inventory items
 64 |     #
 65 | 
 66 |     def world2inv(self,block_name):
 67 |         if block_name in self.blockW2I:
 68 |             return self.blockW2I[block_name]
 69 |         else:
 70 |             return block_name
 71 | 
 72 |     #
 73 |     # Build an Thing
 74 |     #
 75 | 
 76 |     def doBuild(self,args):
 77 | 
 78 |         if len(args) == 0:
 79 |             self.chat('Need to specify blueprint to build.')
 80 |         else:
 81 |             bp_name = args[0]
 82 | 
 83 |         stage = 1
 84 | 
 85 |         while not self.stopActivity:
 86 | 
 87 |             bp = self.getBlueprint(bp_name+"_"+str(stage))
 88 | 
 89 |             # Special handling for the first phase
 90 |             if stage == 1:
 91 |                 if not bp:
 92 |                     print(f'Cant find blueprint {bp_name}.')
 93 |                     break
 94 |             else:
 95 |                 if bp:
 96 |                     print(f'Phase {stage} is starting.')
 97 |                 else:
 98 |                     # Done, no next phase
 99 |                     break
100 | 
101 |             # Define the area - may be different for each phase
102 |             area = workArea(self,bp.width,bp.height,bp.depth)
103 |             if not area.valid:                
104 |                 break
105 | 
106 |             # Analyze what we need, and what is already there
107 | 
108 |             need= {"Bread":2}
109 | 
110 |             for v in area.allBlocks():
111 |                 old_b = area.blockAt(v).displayName
112 |                 new_b = bp.blockAt(v)
113 | 
114 |                 if old_b not in self.emptyBlocks:
115 |                     # something is there already
116 |                     if old_b != new_b:
117 |                         # and it's now what we expect
118 |                         print(f'*** error: wrong object {old_b} instead of {new_b} at position {v}. Clear the area.')
119 |                         self.endActivity()
120 |                         return False
121 |                 elif new_b not in self.emptyBlocks:
122 |                     new_inv = self.world2inv(new_b)
123 |                     need[new_inv] = need.get(new_inv,0) + 1
124 |                 else:
125 |                     # This is an empty space
126 |                     pass
127 | 
128 |             if need:
129 |                 print(need)
130 |                 area.restock(need)
131 |             else:
132 |                 print("  all needed items already in inventory.")
133 | 
134 |             sneak = False
135 |             jump = False
136 | 
137 |             # Build, back to front, bottom to top
138 |             for z in range(bp.depth-1,-1,-1):
139 |                 for y in bp.yRange():
140 |                     for x in bp.xRange():
141 |                         if self.stopActivity:
142 |                             break
143 | 
144 |                         block_type = bp.blockAt(Vec3(x,y,z))
145 | 
146 |                         # Just air in the blueprint? Continue...
147 |                         if block_type in self.emptyBlocks:
148 |                             continue
149 | 
150 |                         # Correct block already there? Continue...
151 |                         if area.blockAt(Vec3(x,y,z)).displayName == block_type:
152 |                             continue
153 | 
154 |                         bot_v = area.toWorld(x,0,z-1.5)
155 |                         bot_v_center = Vec3(bot_v.x+0.5, bot_v.y, bot_v.z+0.5)
156 | 
157 |                         # Figure out how we can place this block.
158 |                         # This is complicated...
159 | 
160 |                         placement_type = "unknown"
161 | 
162 |                         if bp.buildFunction:
163 |                             spec = bp.buildFunction(x,y,z)
164 |                         else:
165 |                             spec = None
166 | 
167 |                         if area.blockAt(Vec3(x,y-1,z)).displayName not in self.emptyBlocks:
168 |                             # Easiest case: block below the block we want to place is not empty.
169 |                             against_v = area.toWorld(x,y-1,z)
170 |                             direction_v = Vec3(0,1,0)
171 |                             placement_type = " (top)"
172 |                         elif area.blockAt(Vec3(x,y,z+1)).displayName not in self.emptyBlocks:
173 |                             # Block behind the block we want to palce is there, let's place against that
174 |                             against_v = area.toWorld(x,y,z+1)
175 |                             direction_v = Vec3(-area.d.x,0,-area.d.z)
176 |                             placement_type = " (front)"
177 |                         elif not spec:
178 |                             # Nothing works, no special instructions
179 |                             print(f'*** error ({x:3},{y:3},{z:3}) {block_type} no placement strategy found')
180 |                             self.stopActivity = True
181 |                             break
182 | 
183 |                         if spec:
184 |                             placement_type +=" S"
185 |                             if spec.jump:
186 |                                 placement_type +=" jmp"
187 |                             if spec.sneak:
188 |                                 placement_type +=" snk"
189 |                             if spec.placement_type:
190 |                                 placement_type = spec.placement_type
191 | 
192 |                             if spec.bot_pos:
193 |                                 bot_v = area.toWorldV3(spec.bot_pos)
194 |                                 bot_v_center = Vec3(bot_v.x+0.5, bot_v.y, bot_v.z+0.5)
195 |                                 placement_type +=" pos"
196 | 
197 |                             if spec.block_against:
198 |                                 against_v = area.toWorldV3(spec.block_against)
199 |                                 placement_type +=" @ "
200 | 
201 |                             if spec.block_surface:
202 |                                 direction_v = area.dirToWorldV3(spec.block_surface)
203 |                                 placement_type +=" dir"
204 | 
205 |                             self.safeWalk(bot_v_center,0.1)
206 |                             time.sleep(1)
207 | 
208 |                         else:
209 |                             self.safeWalk(bot_v_center,0.2)
210 |                             time.sleep(1)
211 | 
212 |                         against_type = self.bot.blockAt(against_v).displayName
213 | 
214 |                         # Let's do this
215 | 
216 |                         print(f'  ({x:3},{y:3},{z:3}) {block_type} -> {against_type} {placement_type}')
217 | 
218 |                         if not self.wieldItem(self.world2inv(block_type)):
219 |                             print(f'*** aborting, cant wield item {block_type}')
220 |                             self.stopActivity = True
221 |                             break
222 | 
223 |                         if against_type in self.interactiveBlocks:
224 |                             self.bot.setControlState('sneak', True)
225 |                             time.sleep(0.5)
226 |                             sneak = True
227 | 
228 |                         if spec and spec.sneak:
229 |                             self.bot.setControlState('sneak', True)
230 |                             time.sleep(0.2)
231 |                             sneak = True
232 | 
233 |                         if spec and spec.jump:
234 |                             self.bot.setControlState('jump', True)
235 |                             time.sleep(0.2)
236 |                             jump = True
237 | 
238 |                         if not self.safePlaceBlock(against_v,direction_v):
239 |                             print(f'*** aborting, cant place block {block_type} at {x}, {y}, {z}')
240 |                             self.stopActivity = True
241 |                             break
242 | 
243 |                         if sneak:
244 |                             self.bot.setControlState('sneak', False)
245 |                             sneak = False
246 | 
247 |                         if jump:
248 |                             self.bot.setControlState('jump', False)
249 |                             jump = False
250 | 
251 |             stage += 1
252 | 
253 |             self.safeWalk(area.start)
254 |             time.sleep(1)
255 | 
256 |         self.endActivity()
257 | 
258 |     #
259 |     # Analyze the area in front and print in python format
260 |     #
261 | 
262 |     def analyzeBuild(self,width=3,height=4, depth=6):
263 | 
264 |         area = workArea(self,width,height,depth)
265 | 
266 |         if not area.valid:
267 |             return False
268 | 
269 |         w2 = int((width-1)/2)    # offset from center for width
270 | 
271 |         print(f'# Minebot Blueprint')
272 |         print(f'# {width} x {height} x {depth}')
273 |         print(f'')
274 |         print(f'bpData = [')
275 | 
276 |         for z in range(0,depth):
277 |             print(f'  [')
278 |             for y in range(height-1,-1,-1):
279 |                 print(f'    [',end="")
280 |                 for x in range(-w2, w2+1):
281 |                     b = self.bot.blockAt(area.toWorld(x,y,z))
282 |                     s = '"'+b.displayName+'"'
283 |                     print(f'{s:15}',end=", ")
284 |                 print(f'],')
285 |             print(f'  ],')
286 |         print(f']')
287 | 


--------------------------------------------------------------------------------
/chat.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Misc chat functions
  3 | #
  4 | 
  5 | import time
  6 | import datetime
  7 | import botlib
  8 | 
  9 | from javascript import require, On, Once, AsyncTask, once, off
 10 | pathfinder = require('mineflayer-pathfinder')
 11 | 
 12 | class ChatBot:
 13 | 
 14 |     stopActivity = True
 15 |     activity_start = 0
 16 |     activity_name = "None"
 17 |     activity_major = False
 18 |     activity_last_duration = 0
 19 | 
 20 |     def __init__(self):
 21 |         print('chat ', end='')
 22 | 
 23 |         # Command : [function, name, major activity flag, min_arguments]
 24 | 
 25 |         self.commandList = {
 26 |                 "analyze":      [self.analyzeBuild,             "Analyze building",     False, 0],
 27 |                 "build":        [self.doBuild,                  "Build a blueprint",    True,  1],                
 28 |                 "chop":         [self.chopWood,                 "Chop wood",            True,  0],                
 29 |                 "deposit":      [self.depositToChest,           "Deposit all in chest", False, 0],
 30 |                 "eat":          [self.eatFood,                  "Eat Something",        False, 0],
 31 |                 "farm":         [self.doFarming,                "Farming",              True , 0],
 32 |                 "hello":        [self.sayHello,                 "Say Hello",            False, 0],
 33 |                 "inventory":    [self.printInventory,           "List Inventory",       False, 0],
 34 |                 "mine":         [self.doMining,                 "Mine for resources",   True,  1],
 35 |                 "sleep":        [self.sleepInBed,               "Sleep in a bed",       False, 0],
 36 |                 "stop":         [self.stopThis,                 "Stop all activities",  False, 0],
 37 |                 "status":       [self.sayStatus,                "Report status",        False, 0],
 38 |                 "wake":         [self.wakeUp,                   "Stop sleeping",        False, 0],
 39 |                 "yeet":         [self.exitGame,                 "Exit the game",        False, 0],
 40 |         }
 41 | 
 42 |     def chat(self,txt):
 43 |         self.bot.chat(txt)
 44 |         self.pdebug(f'  chat: {txt}',0)
 45 | 
 46 |     def sayStatus(self):
 47 |         self.pdebug(f'  level : {self.bot.experience.level}',0)
 48 |         self.pdebug(f'  health: {int(100*self.bot.health/20)}%',0)
 49 |         self.pdebug(f'  food  : {int(100*self.bot.food/20)}%',0)
 50 | 
 51 |     def sayHello(self):
 52 |         self.chat('hello to you too!')
 53 | 
 54 |     def startActivity(self, name):
 55 |         t_str = botlib.myTime()
 56 |         self.pdebug(60*'-',1)
 57 |         self.pdebug(f'{name:47} {t_str}',1)
 58 |         self.pdebug(60*'-',1)
 59 |         self.activity_start = time.time()
 60 |         self.activity_name = name
 61 |         self.stopActivity = False
 62 |         self.activity_major = True
 63 |         self.dangerType = None 
 64 |         self.speedMode = False
 65 | 
 66 |     def endActivity(self):
 67 |         if self.activity_major:
 68 |             t_str = botlib.myTime()
 69 |             d_str = str(datetime.timedelta(seconds=int(time.time()-self.activity_start)))
 70 |             self.pdebug(f'Activity {self.activity_name} ended at {t_str} (duration: {d_str})',1)
 71 |             self.bot.clearControlStates('sneak', False)
 72 |             self.eatFood()
 73 |         self.activity_last_duration = d_str
 74 |         self.bot.stopActivity = True
 75 |         self.activity_major = False
 76 | 
 77 |     def safeSleep(self,t):
 78 |         for i in range(0,t):
 79 |             time.sleep(1)
 80 |             if self.stopActivity:
 81 |                 return False
 82 |         return True
 83 | 
 84 |     def stopThis(self):
 85 |         self.stopActivity = True
 86 | 
 87 |     def sleepInBed(self):
 88 |         bed = self.findClosestBlock("White Bed",xz_radius=3,y_radius=1)
 89 |         if not bed:
 90 |             self.chat('cant find a White Bed nearby (I only use those)')
 91 |         else:
 92 |             self.bot.sleep(bed)
 93 |             self.chat('good night!')
 94 | 
 95 |     def wakeUp(self):
 96 |             self.bot.wake()
 97 |             self.chat('i woke up!')
 98 | 
 99 |     def exitGame(self):
100 |             # exit the game
101 |             off(self.bot, 'chat', onChat)
102 | 
103 |     def handleChat(self,sender, message, this, *rest):
104 | 
105 |         # check if order is incorrect to fix a bug we are seeing between Guido and Daniel
106 |         if type(sender) != type(""):
107 |             # reorder
108 |             t = sender
109 |             sender = message
110 |             message =  this
111 |             this = t
112 | 
113 |         message = message.strip()
114 | 
115 |         # Is this for me, or for someone else?
116 |         if message.startswith(self.callsign):
117 |             print(f'{sender} messaged me "{message}"')
118 |             message = message[len(self.callsign):]
119 |         elif sender != self.bossPlayer():
120 |             return
121 | 
122 |         self.handleCommand(message,sender)
123 | 
124 |     def handleCommand(self, message, sender):
125 | 
126 |         # Handle standard commands
127 | 
128 |         message = message.lower()
129 |         cmd = message.split()[0]
130 |         args = message.split()[1:]
131 | 
132 |         if cmd in self.commandList:
133 |             c = self.commandList[cmd]
134 |             call_function = c[0]
135 |             if c[2]:
136 |                 # Major activity
137 |                 if self.activity_major:
138 |                     self.pdebug(f'*** error: major activity in progress, stop it first {self.activity_name}.')
139 |                     return
140 |                 self.startActivity(c[1])
141 |                 @AsyncTask(start=True)
142 |                 def asyncActivity(task):
143 |                     if c[3] > 0:
144 |                         call_function(args)
145 |                     else:
146 |                         call_function()
147 |             else:
148 |                 if c[3] > 0:
149 |                     call_function(args)
150 |                 else:
151 |                     call_function()
152 |             return
153 | 
154 |         # Legacy commands, need to clean up
155 | 
156 |         # come - try to get to the player
157 |         if 'come' in message or 'go' in message:
158 |             if message == 'come':
159 |                 player = self.bot.players[sender]
160 |             elif 'go to' in message:
161 |                 player = self.bot.players[message[6:]]
162 |             else:
163 |                 self.chat("No Clear Target")
164 |             target = player.entity
165 |             if not target:
166 |                 self.chat("I don't see you!")
167 |                 return
168 |             pos = target.position
169 |             @AsyncTask(start=True)
170 |             def doCome(task):
171 |                 self.walkTo(pos.x, pos.y, pos.z)
172 | 
173 |         if 'follow' in message:
174 |             if message == 'follow':
175 |                 player = self.bot.players[sender]
176 |             elif len(message) > 6:
177 |                 player = self.bot.players[message[7:]]
178 |             else:
179 |                 self.chat("No Clear Target")
180 |             target = player.entity
181 |             if not target:
182 |                 self.chat("I don't see you!")
183 |                 return
184 |             @AsyncTask(start=True)
185 |             def follow(task):
186 |                 while self.stopActivity != True:
187 |                     self.bot.pathfinder.setGoal(pathfinder.goals.GoalFollow(player.entity, 1))
188 |                     time.sleep(2)
189 | 
190 |         if message.startswith('moveto'):
191 |             args = message[6:].split()
192 |             if len(args) != 1:
193 |                 self.chat('Need name of location to move to.')
194 |                 return
195 |             @AsyncTask(start=True)
196 |             def doMoveTo(task):
197 |                 gotoLocation(self.bot,args[0])
198 | 
199 |         if message.startswith('transfer to'):
200 |             args = message[11:].split()
201 |             if len(args) != 1:
202 |                 self.chat('Need name of target chest.')
203 |                 return
204 |             @AsyncTask(start=True)
205 |             def doTransfer(task):
206 |                 transferToChest(self.bot,args[0])
207 | 
208 | 
209 | 


--------------------------------------------------------------------------------
/combat.py:
--------------------------------------------------------------------------------
 1 | #
 2 | # Functions for running away
 3 | #
 4 | 
 5 | from javascript import require, On, Once, AsyncTask, once, off
 6 | from botlib import *
 7 | 
 8 | import sys
 9 | 
10 | class CombatBot:
11 | 
12 |     # Special flag that is set while healing up
13 |     healMode = False
14 | 
15 |     def __init__(self):
16 |         print('combat ', end='')
17 |         self.healMode = True
18 | 
19 |     def healthCheck(self):
20 |         h = 100*self.bot.health/20
21 |         f = 100*self.bot.food/20
22 | 
23 |         self.refreshStatus()
24 |         self.pdebug(f'    health: {h}%   food: {f}%',4)    
25 | 
26 |         if self.healMode:
27 |             return True
28 | 
29 |         if h <= 50:
30 |             # Health 50%. Panic and ninja-log.
31 |             self.pdebug(f'PANIC: Health at {h}%. Quitting immediately.',1)
32 |             self.bot.end()
33 |             sys.exit()
34 |         elif h <= 90:
35 |             # Health 90%. Stop current activity.
36 |             self.pdebug(f'WARNING: Health at {h}%. Stopping current activity.',1)
37 |             self.stopActivity = True
38 |             self.dangerType = "danger: health"
39 | 
40 |         # Check Food
41 |         if f <= 80:
42 |             self.pdebug(f'WARNING: Food at {f}%.',1)
43 |         elif f <= 50:
44 |             self.pdebug(f'WARNING: Food at {f}%. Stopping current activity.',1)
45 |             self.stopActivity = True
46 |             self.dangerType = "out of food"
47 | 
48 |         # Check if damage is from lava 
49 | 
50 |         # Check for air
51 | 
52 |     def healToFull(self):
53 |         if self.bot.health == 20 and self.bot.food > 18:
54 |             return
55 |         self.healMode = True
56 |         self.pdebug(f'Bot is injured or hungry, resting.',2)    
57 |         h = 0
58 |         while self.bot.health < 20 or self.bot.food < 18:
59 |             if self.bot.health > h:
60 |                 self.pdebug(f'  health: {int(100*self.bot.health/20)}%   food: {int(100*self.bot.food/20)}%',3)
61 |                 h = self.bot.health
62 |             if not self.eatFood():
63 |                 break
64 |             time.sleep(2)
65 |         self.pdebug(f'  health: {int(100*self.bot.health/20)}%   food: {int(100*self.bot.food/20)}%',3)
66 |         self.pdebug(f'done.',2)
67 |         self.healMode = False
68 | 


--------------------------------------------------------------------------------
/farming.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Farming
  3 | #
  4 | 
  5 | from javascript import require
  6 | Vec3       = require('vec3').Vec3
  7 | pathfinder = require('mineflayer-pathfinder')
  8 | 
  9 | from inventory import *
 10 | from botlib import *
 11 | from workarea import *
 12 | import time
 13 | 
 14 | class FarmBot:
 15 | 
 16 |     farming_blocks = ["Wheat Crops"]
 17 |     farming_items  = ["Wheat"]
 18 |     farming_seeds  = ["Wheat Seeds"]
 19 | 
 20 |     farmingEquipList = {
 21 |       "Wheat Seeds":64,
 22 |       "Wheat":0,
 23 |       "Bread":5,
 24 |     }
 25 | 
 26 |     def __init__(self):
 27 |         print('farming ', end='')
 28 | 
 29 |     #
 30 |     # Main farming loop. To start, the bot should be next to a chest, or deposit wont work
 31 |     #
 32 |     # Main loop
 33 |     # - plant new crops
 34 |     # - harvest ripe crops
 35 |     # - deposit in chest
 36 | 
 37 |     def findHarvestable(self, r):
 38 |         return self.findClosestBlock(self.farming_blocks, r, y_radius=1, metadata=7 )
 39 | 
 40 |     def findSoil(self,center,r):
 41 |         return self.findClosestBlock("Farmland", r, y_radius=1, spaceabove=True )
 42 | 
 43 |     def doFarming(self):
 44 | 
 45 |         break_interval = 32
 46 |         max_range = 25
 47 |         up = Vec3(0, 1, 0)
 48 | 
 49 |         area = workArea(self,1,1,1,notorch=True)
 50 |         if not area.valid:
 51 |             self.endActivity()
 52 |             return False
 53 |         area.restock(self.farmingEquipList)
 54 | 
 55 |         # Main loop. Keep farming until told to stop.
 56 | 
 57 |         while not self.stopActivity:
 58 |             long_break = 0
 59 | 
 60 |             # Harvest
 61 |             self.pdebug(f'Harvesting.',2)
 62 |             for t in range(0,break_interval):
 63 |                 if self.stopActivity:
 64 |                     break
 65 |                 self.refreshActivity(['Harvesting',' ❓ searching for crops'])
 66 |                 b = self.findHarvestable(max_range)
 67 |                 if b and not self.stopActivity:
 68 |                     self.refreshActivity(['Harvesting',f' ✅ {b.displayName}'])
 69 |                     self.walkToBlock(b)
 70 |                     self.pdebug(f'  {b.displayName}  ({b.position.x}, {b.position.z}) ',3)
 71 |                     try:
 72 |                         self.bot.dig(b)
 73 |                     except Exception as e:
 74 |                         self.pexception("error while harvesting:",e)
 75 |                     #time.sleep(0.2)
 76 |                 else:
 77 |                     self.pdebug('  no more harvestable crops',2)
 78 |                     self.refreshActivity(['Harvesting',' ❌ no more harvestable crops.'])
 79 |                     long_break += 1
 80 |                     break
 81 | 
 82 |             # Plant
 83 |             self.pdebug(f'Planting.',2)
 84 |             crop = self.wieldItemFromList(self.farming_seeds)
 85 |             if crop:
 86 |                 for t in range(0,break_interval):
 87 |                     if self.stopActivity:
 88 |                         break
 89 |                     self.refreshActivity(['Planting',' ❓ searching for soil'])
 90 |                     b = self.findSoil(area.origin,max_range)
 91 |                     self.refreshActivity(['Planting',f' ✅ empty soil'])
 92 |                     if b:
 93 |                         self.walkOnBlock(b)
 94 |                         if not self.checkInHand(crop):
 95 |                             self.refreshActivity(['Planting',f' ❌ no seeds for {crop}'])
 96 |                             self.pdebug(f'Out of seeds of type {crop}.',2)
 97 |                             break
 98 |                         self.pdebug(f'  {crop} ({b.position.x}, {b.position.z})',3)
 99 |                         try:
100 |                             self.bot.placeBlock(b,up)
101 |                         except Exception as e:
102 |                             self.pexception("error while planting:",e)
103 |                     else:
104 |                         self.refreshActivity(['Planting',f' ❌ no more empty soil'])
105 |                         self.pdebug('  no more empty soil',3)
106 |                         long_break += 1
107 |                         break
108 |             else:
109 |                 self.refreshActivity(['Planting',f' ❌ no more seeds'])
110 |                 self.pdebug('  no plantable seeds in inventory.',2)
111 | 
112 |             # Deposit
113 |             area.walkToStart()
114 |             area.restock(self.farmingEquipList)
115 | 
116 |             if not self.stopActivity:
117 |                 if long_break < 2:
118 |                     time.sleep(0.5)
119 |                 else:
120 |                     self.refreshActivity(['Taking a break.'])
121 |                     self.pdebug('Nothing to do, taking a break.',2)
122 |                     self.safeSleep(30)
123 | 
124 |         self.endActivity()
125 |         return True
126 | 


--------------------------------------------------------------------------------
/gather.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Gathering Functionality for the bot
  3 | #
  4 | 
  5 | from inventory import *
  6 | from botlib import *
  7 | from workarea import *
  8 | 
  9 | class BoundingBox:
 10 | 
 11 |     # Computes the bounding block of a set of connected blocks
 12 |     # For example, give it part of a tree trunk, get back the bounding box of all of the tree's wood
 13 | 
 14 |     def __init__(self, pybot, block):
 15 |         self.pybot = pybot
 16 |         b_type = block.displayName
 17 |         x_max = block.position.x
 18 |         x_min = block.position.x
 19 |         y_max = block.position.y
 20 |         y_min = block.position.y
 21 |         z_max = block.position.z
 22 |         z_min = block.position.z
 23 |     
 24 |         found = True
 25 | 
 26 |         while found:
 27 |             found = False
 28 |             for x in range(x_min-1, x_max+2):
 29 |                 for y in range(y_min-1, y_max+2):
 30 |                     for z in range(z_min-1, z_max+2):
 31 |                         b = pybot.blockAt(x,y,z)
 32 |                         if b.displayName == b_type:
 33 |                             if x_min <=x and x_max >= x and y_min <= y and y_max >= y and z_min <= z and z_max >= z:
 34 |                                 continue
 35 |                             x_min = x if x < x_min else x_min
 36 |                             x_max = x if x > x_max else x_max
 37 |                             y_min = y if y < y_min else y_min
 38 |                             y_max = y if y > y_max else y_max
 39 |                             z_min = z if z < z_min else z_min
 40 |                             z_max = z if z > z_max else z_max
 41 |                             found = True
 42 |         self.pybot.pdebug(f'    bounding box: {x_min}:{x_max}  {y_min}:{y_max}  {z_min}:{z_max}',4)
 43 |         self.x_min = x_min
 44 |         self.x_max = x_max
 45 |         self.y_min = y_min
 46 |         self.y_max = y_max
 47 |         self.z_min = z_min
 48 |         self.z_max = z_max
 49 | 
 50 |     def dx(self):
 51 |         return self.x_max-self.x_min+1
 52 | 
 53 |     def dy(self):
 54 |         return self.y_max-self.y_min+1
 55 | 
 56 |     def dz(self):
 57 |         return self.z_max-self.z_min+1
 58 | 
 59 | 
 60 | 
 61 | class GatherBot:
 62 | 
 63 |     chopEquipList = {
 64 |       "Stone Axe":5,
 65 |       "Spruce Log":0,
 66 |       "Spruce Sapling":0,
 67 |       "Stick":0,
 68 |     }
 69 | 
 70 |     def __init__(self):
 71 |         print('gather ', end='')
 72 | 
 73 |     def chopBlock(self,x,y,z):
 74 |         v = Vec3(x,y,z)
 75 |         b = self.bot.blockAt(v)
 76 | 
 77 |         if b.displayName != "Air":
 78 |             self.pdebug(f'  chop   ({x},{y},{z}) {b.displayName}',3)
 79 |             self.bot.dig(b)
 80 |             if self.bot.blockAt(v).displayName == "Air":
 81 |                 return 1
 82 |             else:
 83 |                 return 0
 84 |         return 1
 85 | 
 86 |     def chop(self,x,y,z,height):
 87 |         self.wieldItem("Stone Axe")
 88 |         for h in range(0,height):
 89 |             self.chopBlock(x,y+h,z)
 90 | 
 91 |     def chopBigTree(self):
 92 |         self.pdebug(f'Looking for tree block...',3)
 93 |         self.refreshActivity([' ❓ searching: giant spruce'])
 94 |         b0 = self.findClosestBlock("Spruce Log",xz_radius=25,y_radius=1)
 95 |         if self.stopActivity:
 96 |             return False
 97 |         if not b0:
 98 |             self.perror('Cant find any tree to chop down nearby')
 99 |             return False
100 |         self.pdebug(f'  found at {b0.position.x},{b0.position.z}',3)
101 |         box = BoundingBox(self,b0)
102 | 
103 |         if box.dx() != 2 or box.dz() != 2 or box.dy() < 5:
104 |             self.perror(f'Tree has wrong dimensions {box.dx()} x {box.dy()} x {box.dz()}')
105 |             return False
106 |         
107 |         self.refreshActivity([f'🌲 Tree at {b0.position.x},{b0.position.z}',f'  height: {box.dy()}'])
108 |         self.pdebug(f'Found big tree of height {box.dy()}',2)
109 | 
110 |         self.walkToBlock(box.x_min-1, box.y_min, box.z_min-1)
111 | 
112 |         x0 = box.x_min
113 |         y  = box.y_min
114 |         z0 = box.z_min
115 | 
116 |         self.walkToBlock(x0-1, y, z0-1)
117 |         self.chop(x0-1, y, z0-1, 3)
118 |         self.walkToBlock(x0-1, y, z0-1)
119 | 
120 |         while True:
121 |             self.chop(x0,y+1, z0,3)
122 |             self.walkOnBlock(x0,y,z0)
123 |             self.refreshActivity([f'🌲 Tree at {b0.position.x},{b0.position.z}',f'  height: {box.dy()}',f'  y: {y-box.y_min}','  ⬆️ heading up'])
124 |             time.sleep(0.5)
125 |             self.chop(x0+1,y+2, z0,3)
126 |             self.walkOnBlock(x0+1,y+1,z0)
127 |             self.refreshActivity([f'🌲 Tree at {b0.position.x},{b0.position.z}',f'  height: {box.dy()}',f'  y: {y-box.y_min+1}','  ⬆️ heading up'])
128 |             time.sleep(0.5)
129 |             self.chop(x0+1,y+3, z0+1,3)
130 |             self.walkOnBlock(x0+1,y+2,z0+1)
131 |             self.refreshActivity([f'🌲 Tree at {b0.position.x},{b0.position.z}',f'  height: {box.dy()}',f'  y: {y-box.y_min+2}','  ⬆️ heading up'])
132 |             time.sleep(0.5)
133 |             self.chop(x0,y+4, z0+1,3)
134 |             self.walkOnBlock(x0,y+3,z0+1)
135 |             self.refreshActivity([f'🌲 Tree at {b0.position.x},{b0.position.z}',f'  height: {box.dy()}',f'  y: {y-box.y_min+3}','  ⬆️ heading up'])
136 |             time.sleep(0.5)
137 |             if y+8 >= box.y_max:
138 |                 break
139 |             else:
140 |                 y = y + 4
141 | 
142 |         self.pdebug(f'At the top, chopping down',2)
143 | 
144 |         self.eatFood()
145 | 
146 |         y = box.y_max
147 | 
148 |         while y >= box.y_min:
149 |             self.chop(x0,  y, z0,   1)
150 |             self.chop(x0+1,y, z0,   1)
151 |             self.chop(x0+1,y, z0+1, 1)
152 |             self.chop(x0,  y, z0+1, 1)
153 |             y = y - 1
154 |             self.refreshActivity([f'🌲 Tree at {b0.position.x},{b0.position.z}',f'  height: {box.dy()}',f'  y: {y-box.y_min}','  ⬇️ heading down'])
155 |             self.healToFull()
156 | 
157 |         return True
158 | 
159 |     def chopWood(self):
160 | 
161 |         area = workArea(self,1,1,1,notorch=True)
162 |         if area.valid:            
163 |             while not self.stopActivity:                
164 |                 area.restock(self.chopEquipList)
165 |                 if not self.chopBigTree():
166 |                     break
167 |         self.refreshActivity(['Restocking'])
168 |         area.restock(self.chopEquipList)
169 |         self.endActivity()
170 |         return True
171 | 


--------------------------------------------------------------------------------
/inventory.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Functions to manage inventory and eqipment
  3 | #
  4 | 
  5 | import time
  6 | from botlib import *
  7 | 
  8 | foodList = [
  9 |   "Sweet Berries",
 10 |   "Bread"
 11 | ]
 12 | 
 13 | def js_Minecart_With_Chest(entity):
 14 |     if entity.name == "chest_minecart":
 15 |         return True
 16 |     else:
 17 |         return False
 18 | 
 19 | class Chest:
 20 | 
 21 |     def __init__(self,pybot,chesttype="Chest",silent=False):
 22 |         self.pybot = pybot
 23 | 
 24 |         # How we find it depends on the type:
 25 |         # Chests are blocks
 26 |         if chesttype == "Chest":
 27 |             self.object = self.pybot.findClosestBlock(chesttype,2)
 28 |             self.chestType = chesttype
 29 |         # Minecarts are entities
 30 |         elif chesttype == "Minecart with Chest":
 31 |             self.object = pybot.bot.nearestEntity(js_Minecart_With_Chest)
 32 |             if self.object:
 33 |                 # print(self.object, self.pybot.bot.entity)
 34 |                 if lenVec3(subVec3(self.object.position, self.pybot.bot.entity.position)) > 2:
 35 |                     self.object = None 
 36 |             self.chestType = chesttype
 37 |         if self.object == None:
 38 |             if not silent:
 39 |                 self.pybot.perror(f'Cant find any {chesttype} nearby.')
 40 |         self.container = None
 41 | 
 42 |     def open(self):
 43 |             if self.container:
 44 |                 return True
 45 |             #print(self.object)
 46 |             self.container = self.pybot.bot.openContainer(self.object)
 47 |             if not self.container:
 48 |                 self.pybot.perror("Can't open chest.")
 49 |                 return False
 50 |             time.sleep(0.2)
 51 |             return True
 52 | 
 53 |     def close(self):
 54 |             self.container.close()
 55 |             self.container = None
 56 | 
 57 |     def spaceAvailable(self):
 58 |         if self.open():
 59 |             chest_size = self.container.inventoryStart
 60 |             empty = chest_size
 61 |             # count empty slots in chest
 62 |             for s in self.container.slots:
 63 |                 if s != None and s.slot < chest_size:
 64 |                     empty -= 1
 65 |             return empty
 66 |         else:
 67 |             return 0
 68 | 
 69 |     def printContents(self, debug_lvl=1):
 70 |         if self.open():
 71 |             self.pybot.pdebug(f'Chest contents:', debug_lvl)
 72 |             empty = True
 73 |             for i in self.container.containerItems():
 74 |                 empty = False
 75 |                 self.pybot.pdebug(f'  {i.count:2} {i.displayName}', debug_lvl)
 76 |             if empty:
 77 |                 self.pybot.pdebug(f'  (none)', debug_lvl)
 78 | 
 79 |     def printItems(self, items):
 80 |         self.pybot.pdebug(f'  Item List:',1)
 81 |         for i in items:
 82 |             self.pybot.pdebug(f'    {i.slot:3}: {i.count:3} x {i.displayName}',1)
 83 | 
 84 |     def itemCount(self,item_arg):
 85 | 
 86 |         item_type, item_name = self.pybot.itemTypeAndName(item_arg)
 87 | 
 88 |         count = 0
 89 |         inventory = self.container.containerItems()
 90 |         if inventory != []:
 91 |             # Count how many items we have of this type
 92 |             for i in inventory:
 93 |                 if item_type == i.type:
 94 |                     count += i.count
 95 | 
 96 |         return count
 97 | 
 98 |     def depositItem(self,item_type,count=None):
 99 |         itemObj = self.pybot.Item(item_type,1)
100 |         item_name = itemObj.displayName
101 |         if self.spaceAvailable() < 2:
102 |             self.pybot.perror('chest is full')
103 |             return False
104 |         count_max = self.pybot.invItemCount(item_type)
105 |         if not count or count < 1:
106 |             count = count_max
107 |         elif count > count_max:
108 |             self.pybot.pdebug(f'  warning: deposit of {count} x {item_name} exceeds inventory ({count_max})',2)
109 |             count = count_max
110 | 
111 |         self.pybot.pdebug(f'  > {count:2} x {item_name}   ({item_type})',3)
112 |         try:
113 |             newChest = self.container.deposit(item_type,None,count)
114 |             if newChest:
115 |                 self.container = newChest
116 |         except Exception as e:
117 |             self.pybot.pexception(f'depositing {count} of item {item_name} type {item_type}',e)
118 |             return False
119 |         return True
120 | 
121 |     def withdrawItem(self,item_type,count=None):
122 |         itemObj = self.pybot.Item(item_type,1)
123 |         item_name = itemObj.displayName
124 |         count_max = self.itemCount(item_type)
125 |         if count < 1:
126 |             count = count_max
127 |         elif count > count_max:
128 |             self.pybot.pdebug(f'  warning: withdrawal of {count} x {item_name} exceeds inventory ({count_max})',2)
129 |             count = count_max
130 |             
131 |         self.pybot.pdebug(f'  < {count} x {item_name}   ({item_type})',3)
132 |         try:
133 |             newChest = self.container.withdraw(item_type,None,count)
134 |             if newChest:
135 |                 self.container = newChest
136 |         except Exception as e:
137 |             self.pybot.pexception(f'*** withdrawing {count} of item {item_name} ({count_max} left)',e)
138 |             return False
139 |         return True
140 | 
141 |     # Depost items in chest
142 |     # - If whitelist is present, only deposit those items. Otherwise everything.
143 |     # - If blacklist is present, do NOT depost those items.
144 | 
145 |     def deposit(self, whitelist=[], blacklist=[]):
146 |         if not self.open():
147 |             self.pybot.perror('Cant open chest to deposit Items.')
148 |             return False
149 |         empty_slots = self.spaceAvailable()
150 |         self.pybot.pdebug(f'Depositing ({empty_slots}/{self.container.inventoryStart} free):',3)
151 |         itemList = self.pybot.bot.inventory.items()
152 |         for i in itemList:
153 |             if whitelist != [] and i.displayName not in whitelist:
154 |                 continue
155 |             elif blacklist != [] and i.displayName in blacklist:
156 |                 continue
157 |             self.depositItem(i.type)
158 | 
159 |     # For any item on <itemList> make sure you have the right amount
160 |     # - If too many, deposit
161 |     # - If too few, take
162 |     # Other items are ignored
163 | 
164 |     def restock(self, itemList):
165 |         if not self.open():
166 |             self.pybot.perror('Cant open chest to restock Items.')
167 |             return False
168 | 
169 |         self.pybot.pdebug("Restocking goals for chest:",4)
170 | 
171 |         for name,n_goal in itemList.items():
172 |             n_inv = self.pybot.invItemCount(name)
173 |             if n_goal > 0:
174 |                 self.pybot.pdebug(f'  {name} {n_inv}/{n_goal}',4)
175 | 
176 |         self.pybot.pdebug("Restocking operations:",3)
177 | 
178 |         nothing = True
179 |         for name,n_goal in itemList.items():
180 |             n_inv = self.pybot.invItemCount(name)
181 | 
182 |             if n_inv > n_goal:
183 |                 # deposit
184 |                 dn = n_inv-n_goal
185 |                 invList = self.pybot.bot.inventory.items()
186 |                 for i in invList:
187 |                     if i.displayName == name:
188 |                         count = min(i.count,dn)
189 |                         #print(f'res {i.displayName} i:{n_inv} g:{n_goal} slt:{i.count} -> dep:{count}')
190 |                         if count > 0:
191 |                             self.depositItem(i.type,count)
192 |                             nothing = False
193 |                             dn -= count
194 |                         if dn == 0:
195 |                             continue
196 |             elif n_goal > n_inv:
197 |                 # withdraw
198 |                 dn = n_goal-n_inv
199 | 
200 |                 for i in self.container.containerItems():
201 |                     if i.displayName == name:
202 |                         count = min(i.count,dn)
203 |                         if count > 0:
204 |                             #print(f'res {i.displayName} i:{n_inv} g:{n_goal} slt:{i.count} -> draw:{count}')
205 |                             self.withdrawItem(i.type,count)
206 |                             nothing = False
207 |                             dn -= count
208 |                         if dn == 0:
209 |                             continue
210 |             else:
211 |                 self.pybot.pdebug(f'  {name} {n_inv}/{n_goal} -- no action',5)
212 | 
213 |         if nothing:
214 |             self.pybot.pdebug(f'  nothing to do.',5)
215 | 
216 | 
217 | #
218 | # Mixin Class for the Bot. Has all the inventory and equipment functions
219 | #
220 | 
221 | class InventoryManager:
222 | 
223 |     def __init__(self):
224 |         print('inventory ', end='')
225 | 
226 |     #
227 |     # Returns a pair of (item name, item type)
228 |     # Input can be:
229 |     # - displayName of an Item
230 |     # - ID of an item
231 |     # - an Item
232 |     #
233 | 
234 |     def itemTypeAndName(self,item_arg):
235 |         if isinstance(item_arg,int):
236 |             item_type = item_arg
237 |             itemObj = self.Item(item_type,1)
238 |             item_name = itemObj.displayName
239 |         elif isinstance(item_arg,str):
240 |             item_name = item_arg
241 |             # Find this item in the inventory
242 |             if self.bot.inventory.items != []:
243 |                 # find in inventory list
244 |                 for item in self.bot.inventory.items():
245 |                     if item.displayName == item_name:
246 |                         item_type = item.type
247 |                         break
248 |                 else:
249 |                     item_type = None
250 |         elif item_arg.type and item_arg.displayName:
251 |             item_type = item_arg.type
252 |             item_name = item_arg.displayName
253 |         else:
254 |             item_type = None
255 |             item_name = "Unknown"
256 | 
257 |         return item_type, item_name
258 | 
259 |     def checkMinimumList(self, items):
260 |         for i in items:
261 |             #print(i, self.invItemCount(i), items[i])
262 |             if self.invItemCount(i) < items[i]:
263 |                 self.pdebug(f'Insufficient Items: {i} {self.invItemCount(i)}/{items[i]}',1)
264 |                 return False
265 |         return True
266 | 
267 |     def invItemCount(self,item_arg):
268 | 
269 |         item_type, item_name = self.itemTypeAndName(item_arg)
270 | 
271 |         count = 0
272 |         inventory = self.bot.inventory.items()
273 |         if inventory != []:
274 |             # Count how many items we have of this type
275 |             for i in inventory:
276 |                 if item_type == i.type:
277 |                     count += i.count
278 | 
279 |         return count
280 | 
281 | 
282 |     # Print current inventory. Aggregate slots to numbers.
283 | 
284 |     def printInventory(self):
285 |         inventory = self.bot.inventory.items()
286 |         iList = {}
287 |         if inventory != []:
288 |             self.pdebug(f'Inventory Slots:',4)
289 | 
290 |             # Count how many items we have of each type
291 |             for i in inventory:
292 |                 self.pdebug(f'  -> {i.count:2} {i.displayName}',4)
293 |                 iname = i.displayName
294 |                 if iname not in iList:
295 |                     iList[iname] = 0
296 |                 iList[iname] += i.count
297 | 
298 |             self.pdebug(f'Inventory:',1)
299 | 
300 |             # Now show the list
301 |             for i in iList:
302 |                 self.pdebug(f'  {iList[i]:3} {i}',1)
303 |         else:
304 |             self.bot.chat('empty')
305 | 
306 |     #
307 |     # Check if a specific item is in hand
308 |     #
309 | 
310 |     def checkInHand(self,item_arg):
311 | 
312 |         if not self.bot.heldItem:
313 |             return False
314 | 
315 |         item_type, item_name = self.itemTypeAndName(item_arg)
316 | 
317 |         if self.bot.heldItem.type == item_type:
318 |             return True
319 |         else:
320 |             return False
321 | 
322 |     def itemInHand(self):
323 | 
324 |         if not self.bot.heldItem:
325 |             return None, "None"
326 |         return self.bot.heldItem.type, self.bot.heldItem.displayName
327 |     #
328 |     # Equip an Item into the main hand.
329 |     #
330 |     # item can be:
331 |     # - an Item in the inventory
332 |     # - an Item ID
333 |     # - displayName of an Item
334 |     #
335 |     # Returns name of the item in hand
336 |     #
337 | 
338 |     def wieldItem(self,item_arg):
339 | 
340 |         if not item_arg:
341 |             self.perror("trying to equip item 'None'.")
342 |             return None
343 | 
344 |         # Translate argument into type and name
345 | 
346 |         item_type, item_name = self.itemTypeAndName(item_arg)
347 | 
348 |         # check if we found it
349 |         if item_type == None:
350 |             self.perror(f'cant find item {item_name} ({item_type}) to wield.')
351 |             return None
352 | 
353 |         time.sleep(0.25)
354 |         # Am I already holding it?
355 |         if self.checkInHand(item_type):
356 |             return item_name
357 | 
358 |         # Equip the item
359 |         self.pdebug(f'      equip {item_name} ({item_type})',3)
360 | 
361 |         # Try wielding 5 times
362 |         for i in range(0,5):
363 |             try:
364 |                 self.bot.equip(item_type,"hand")
365 |             except Exception as e:
366 |                 hand_type, hand_name = self.itemInHand()
367 |                 self.pexception(f'wieldItem() try #{i}. In hand {hand_name} vs {item_name}',e)
368 |                 # Did it raise an exception, but we still have the right item? If yes, all good.
369 |                 if self.checkInHand(item_type):
370 |                     return item_name
371 |                 time.sleep(1)
372 |             else:
373 |                 break
374 | 
375 |         time.sleep(0.25)
376 |         self.refreshEquipment()
377 |         if not self.checkInHand(item_name):
378 |             self.perror(f'Wielding item {item_name} failed after max retries!')
379 |             return None
380 | 
381 |         return item_name
382 | 
383 |     #
384 |     # Equip an item from a list of names
385 |     #
386 | 
387 |     def wieldItemFromList(self,iList):
388 |         if iList == None:
389 |             print("error: equip list is empty.")
390 |             return None
391 | 
392 |         # check if we have anything
393 |         if self.bot.inventory.items == []:
394 |             print("error: empty inventory, can't wield anything")
395 |             return None
396 | 
397 |         # find in inventory list
398 |         for i in self.bot.inventory.items():
399 |             if i.displayName in iList:
400 |                 return self.wieldItem(i)
401 | 
402 |         # check if we found it
403 |         print("error: can't find a useful item to wield.")
404 |         return None
405 | 
406 |     def printEquipment(self):
407 |         print("In Hand: ",bot.heldItem.displayName)
408 | 
409 |     #
410 |     # Update a sign. This requires destroying it first.
411 |     # And it's also hard due to an issue in Mineflayer
412 |     #
413 | 
414 |     def updateSign(self,txt_arg,tryonly=False):
415 | 
416 |         if type(txt_arg) is list:
417 |             txt = txt_arg
418 |         else:
419 |             txt = ["",txt_arg,"",""]
420 |         
421 |         # Total hack, should use block tags...
422 |         sign_block = self.findClosestBlock("Spruce Wall Sign",4)
423 |         if not sign_block:
424 |             if not tryonly:
425 |                 self.perror('cant find any sign close by to update.')
426 |             return False
427 | 
428 |         p_sign = sign_block.position
429 |         dv = directionToVector(sign_block)
430 |         p_against = subVec3(p_sign,dv)
431 | 
432 |         self.safeWalk(Vec3(p_sign.x+0.5, self.bot.entity.position.y, p_sign.z+0.5),0.2)
433 | 
434 |         # Mine up the sign
435 |         sign_name = sign_block.displayName
436 |         p = sign_name.find('Wall')
437 |         if p > 0:
438 |             sign_name = sign_name[0:p]+sign_name[p+5:]
439 | 
440 |         self.pdebug(f'Updating {sign_name} to "{txt[0]} {txt[1]}..."',2)
441 |         self.mineBlock(sign_block.position)
442 |         time.sleep(2)
443 | 
444 |         if self.wieldItem(sign_name) != sign_name:
445 |             return False
446 | 
447 |         self.safePlaceBlock(p_against,dv)
448 | 
449 |         d = { "location": p_sign, "text1": txt[0], "text2": txt[1], "text3": txt[2], "text4": txt[3], }
450 | 
451 |         try:
452 |             r = self.bot._client.write('update_sign', d)
453 |         except Exception as e:
454 |             self.pexception("Updating text of sign",e)   
455 | 
456 |         return True
457 | 
458 | 
459 |     #
460 |     # Eat food, but only if hungry
461 |     #
462 | 
463 |     def eatFood(self):
464 |         # Check if hungry
465 |         if self.bot.food > 18:
466 |             return True
467 | 
468 |         # Wield food in hand
469 |         foodname = self.wieldItemFromList(foodList)
470 |         if foodname:
471 |             self.pdebug(f'eating food {foodname}',3)
472 |             self.bot.consume()
473 |             return True
474 |         else:
475 |             self.pdebug(f'food level {int(100*self.bot.food/20)}, but no food in inventory!',1)
476 |             return False
477 | 
478 |     #
479 |     #  Chest Management
480 |     #
481 | 
482 |     def chestSpaceAvailable(self,chest):
483 |         chest_size = chest.inventoryStart
484 |         empty = chest_size
485 |         # count empty slots in chest
486 |         for s in chest.slots:
487 |             if s != None and s.slot < chest_size:
488 |                 empty -= 1
489 |         return empty
490 | 
491 |     def depositOneToChest(self,chest,i,count=None):
492 |         if self.chestSpaceAvailable(chest) < 2:
493 |             print('chest is full')
494 |             return False
495 |         if not count:
496 |             count = i.count
497 |         print(f'  > {count} x {i.displayName}')
498 |         try:
499 |             # print("Deposit:",i,count)
500 |             chest.deposit(i.type,None,count)
501 |         except Exception as e:
502 |             print(f'*** error depositing {count} of item {i.displayName} ({i.count} in inventory)')
503 |             return False
504 |         return True
505 | 
506 |     def withdrawOneFromChest(self,chest,i,count=None):
507 |         if not count:
508 |             count = i.count
509 |         print(f'  < {count} x {i.displayName}')
510 |         try:
511 |             chest.withdraw(i.type,None,count)
512 |         except Exception as e:
513 |             print(f'*** error withdrawing {count} of item {i.displayName} ({i.count} left)')
514 |             return False
515 |         return True
516 | 
517 |     #
518 |     # Depost items in chest
519 |     # - If whitelist is present, only deposit those items. Otherwise everything.
520 |     # - If blacklist is present, do NOT depost those items.
521 | 
522 |     def depositToChest(self, whitelist=[], blacklist=[]):
523 |         chest = Chest(self)
524 |         chest.deposit(whitelist,blacklist)
525 |         chest.close()
526 | 
527 |     #
528 |     # Find closest chest and restock from it according to the list
529 |     #
530 | 
531 |     def restockFromChest(self, itemList):
532 |         
533 |         # If we have both cart and chest we deposit into cart
534 |         # and then restock from chest
535 |         cart = Chest(self,"Minecart with Chest",silent=True)
536 |         if cart.object:
537 |             cart.restock(itemList)
538 |             cart.close()
539 |             time.sleep(1)
540 |         chest = Chest(self)
541 |         chest.restock(itemList)
542 |         chest.close()
543 | 
544 |     #
545 |     #  Transfer all of the content of the closest chest, to the destination chest
546 |     #
547 | 
548 |     def transferToChest(self, target):
549 | 
550 |         c1 = Chest(self)
551 |         if c1.block == None:
552 |             self.perror("Can't transfer chest contents - no chest found near starting point")
553 |             return False
554 | 
555 |         self.startActivity("Transfer chest contents to "+target)
556 | 
557 |         while not self.stopActivity:
558 | 
559 |             # Pick up from the source chest
560 |             c1.open()
561 |             self.pdebug("Taking:",3)
562 |             slots = 0
563 |             for i in c1.chestObj.containerItems():
564 |                 if i.count > 0:
565 |                     c1.withdrawItem(i.type,i.count)
566 |                     time.sleep(0.2)
567 |                     slots += 1
568 |                     if slots > 27:
569 |                         break
570 |             c1.close()
571 | 
572 |             if slots == 0:
573 |                 print(f'  nothing left')
574 |                 break
575 | 
576 |             # Drop all into the destination chest
577 |             self.gotoLocation(target)
578 |             self.depositToChest()
579 |             self.safeWalk(chest_block.position)
580 | 
581 |         self.stopActivity()
582 | 


--------------------------------------------------------------------------------
/mine.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Functions for mining blocks
  3 | #
  4 | 
  5 | import itertools
  6 | 
  7 | from javascript import require
  8 | Vec3     = require('vec3').Vec3
  9 | 
 10 | from botlib import *
 11 | from inventory import *
 12 | from workarea import *
 13 | 
 14 | class MineBot:
 15 | 
 16 |     needs_iron_pickaxe = ["Gold Ore", "Redstone Ore", "Diamond Ore", "Emerald Ore"]
 17 |     needs_diamond_pickaxe = ["Obsidian"]
 18 |     needs_shovel = ["Dirt", "Gravel", "Sand"]
 19 | 
 20 |     # This is what we are looking for
 21 | 
 22 |     valuable_blocks = [
 23 |         "Coal Ore",
 24 |         "Copper Ore",
 25 |         "Lapis Lazuli Ore",
 26 |         "Iron Ore",
 27 |         "Gold Ore",
 28 |         "Redstone Ore",
 29 |         "Diamond Ore",
 30 |         "Emerald Ore",
 31 |         "Block of Coal",
 32 |     ]
 33 | 
 34 |     # These blocks never get mined up
 35 | 
 36 |     ignored_blocks = [
 37 |         "Torch",
 38 |         "Wall Torch",
 39 |         "Sign",
 40 |         "Air",
 41 |         "Cave Air",
 42 |         "Void Air",
 43 |         "Chest",
 44 |         "Crafting Table",
 45 |         "Furnace",
 46 |         "Ladder",
 47 |         "Glass",
 48 |         "Stone Bricks",
 49 |         "Chiseled Stone Bricks",
 50 |         "Stone Brick Stairs",
 51 |         "Water",
 52 |         "Flowing Water",
 53 |         "Bubble Column",
 54 |     ]
 55 | 
 56 |     # These blocks we need to bridge over
 57 | 
 58 |     dangerBlocks = {
 59 |         "Air",
 60 |         "Cave Air",
 61 |         "Void Air",
 62 |         "Lava",
 63 |         "Water",
 64 |         "Infested Stone",
 65 |     }
 66 | 
 67 |     # These blocks will drop down, we need to dig them up until done
 68 | 
 69 |     block_will_drop = [
 70 |         "Gravel",
 71 |         "Sand",
 72 |         "Red Sand",
 73 |         "Pointed Dropstone",
 74 |         "Anvil,"
 75 |     ]
 76 | 
 77 |     block_will_flow = [
 78 |         "Lava",
 79 |         "Water",
 80 |     ]
 81 | 
 82 |     # Blocks that will drop down on you
 83 | 
 84 |     dangerDropBlocks = block_will_flow + block_will_drop
 85 | 
 86 |     # These blocks we use to fill holes or build bridges
 87 | 
 88 |     fillBlocks = {
 89 |         "Stone Bricks",
 90 |         "Cobblestone",
 91 |         "Dirt"
 92 |     }
 93 | 
 94 |     # Inventory goals for normal mining
 95 | 
 96 |     miningEquipList= {
 97 |         "Bread":5,
 98 |         "Stone Pickaxe":5,
 99 |         "Stone Shovel":2,
100 |         "Iron Pickaxe":2,
101 |         "Torch": 10,
102 |         "Cobblestone" : 64,
103 |         "Stone Bricks" : 256,
104 |         "Dirt" : 0,
105 |         "Andesite" : 0,
106 |         "Diorite" : 0,
107 |         "Granite" : 0,
108 |         "Sandstone" : 0,
109 |         "Sand" : 0,
110 |         "Gravel" : 0,
111 |         "Flint" : 0,
112 |         "Raw Iron" : 0,
113 |         "Raw Gold" : 0,
114 |         "Raw Copper" : 0,
115 |         "Coal" : 0,
116 |         "Redstone Dust" : 0,
117 |         "Diamond" : 0,
118 |         "Lapis Lazuli" : 0,
119 |         "Emerald" : 0,
120 |         "Chiseled Stone Bricks" : 0,
121 |         "Block of Coal" : 0,
122 |     }
123 | 
124 |     miningMinimumList = {
125 |         "Bread":1,
126 |         "Stone Pickaxe":2,
127 |         "Stone Shovel":1,
128 |         "Iron Pickaxe":1,
129 |         "Torch": 5,
130 |     }
131 | 
132 |     def __init__(self):
133 |         print('mining ', end='')
134 | 
135 |     # Checks if walking to a specific block is considered safe
136 | 
137 |     def mining_safety_check(self,position):
138 |         n = self.bot.blockAt(position).displayName
139 |         if n in self.block_will_flow:
140 |             self.stopActivity = True
141 |             self.dangerType = "danger: "+n
142 |             self.pdebug(f'danger: {n}, aborting mining',1)
143 |             return False
144 |         return True
145 | 
146 |     #
147 |     # Mine a block with the right tool
148 |     # Takes a Vector or x,y,z as input
149 | 
150 |     def mineBlock(self,x,y=None,z=None):
151 |         if not y and not z:
152 |             v = x
153 |         else:
154 |             v = Vec3(x,y,z)
155 |         
156 |         b = self.bot.blockAt(v)
157 | 
158 |         self.pdebug(f'    mine block   ({v.x},{v.y},{v.z}) {b.displayName} t:{b.digTime(274)}',3)
159 | 
160 |         t = b.digTime(274)
161 |         if b.displayName:
162 |             if b.displayName == "Copper Ore":
163 |                 t = 200
164 | 
165 |         if t > 100 and b.displayName not in self.ignored_blocks:
166 |             # Ok, this looks mineable
167 |             # Try 20 times, in case gravel is dropping down
168 |             for attempts in range(0,20):
169 |                 if not self.mining_safety_check(self.bot.entity.position): return 0
170 | 
171 |                 self.pdebug(f'    trying to mine',4)
172 | 
173 |                 # Check for the right tool
174 |                 if b.displayName in self.needs_shovel:
175 |                     if self.invItemCount("Stone Shovel") > 0:
176 |                         self.wieldItem("Stone Shovel")
177 |                     else:
178 |                         self.wieldItem("Stone Pickaxe")
179 |                 elif b.displayName in self.needs_iron_pickaxe:
180 |                     self.wieldItem("Iron Pickaxe")
181 |                 else:
182 |                     self.wieldItem("Stone Pickaxe")
183 | 
184 |                 # dig out the block
185 |                 try:
186 |                     self.bot.dig(b)
187 |                 except Exception as e:
188 |                     self.pexception(f'dig failed for block {v.x},{v.y},{v.z}) {b.displayName} t:{b.digTime(274)}',e)
189 | 
190 |                 # Check if successful
191 |                 b = self.bot.blockAt(v)
192 |                 if b.digTime(274) == 0:
193 |                     return 1
194 |         else:
195 |             #print(f'  ignore ({x},{y},{z}) {b.displayName}')
196 |             return 0
197 | 
198 | 
199 |     
200 |     #
201 |     # Mine a 1-wide path from start to end of height height
202 |     # Assumes the bot is at start
203 |     #
204 | 
205 |     def minePath(self,start,end,height, area=None):
206 | 
207 |         self.pdebug(f'minePath({start},{end},{height})',4)
208 |         c = Vec3(start.x, start.y, start.z)
209 |         d = Vec3( (end.x-start.x)/max(abs(end.x-start.x),1), 0, (end.z-start.z)/max(abs(end.z-start.z),1) )
210 | 
211 |         while True:
212 | 
213 |             # Check if path is safe
214 |             bb = self.blockAt(c.x,c.y-1,c.z)
215 |             if bb.displayName in self.dangerBlocks:
216 |                 self.perror(f'  stopping, dangerous block {bb.displayName} ')
217 |                 return False
218 | 
219 |             # Mine the column. May need a few tries due to gravel
220 | 
221 |             wait_t = 0
222 | 
223 |             for tries in range(0,30):
224 | 
225 |                 if self.stopActivity:
226 |                     return True
227 | 
228 |                 # check if we have gravel or sand. If yes we need to check longer.
229 |                 for h in range(0,height+1):
230 |                     b_name = self.bot.blockAt(Vec3(c.x,c.y+h,c.z)).displayName
231 |                     if b_name in self.block_will_drop:
232 |                         wait_t = 1
233 |                         break
234 | 
235 |                 # mine
236 |                 for h in range(0,height):
237 |                     cc = self.mineBlock( c.x,c.y+h,c.z)
238 |                     if area:
239 |                         area.blocks_mined += cc
240 | 
241 |                 if wait_t:
242 |                     time.sleep(wait_t)
243 | 
244 |                 for h in range(0,height):
245 |                     b_name = self.bot.blockAt(Vec3(c.x,c.y+h,c.z)).displayName
246 |                     if b_name not in self.ignored_blocks:
247 |                         self.pdebug(f'  block not cleared: {b_name}.',2)
248 |                         break
249 |                 else:
250 |                     break
251 | 
252 |             if tries > 30:
253 |                 self.perror("can't clear this column.")
254 |                 self.stopActivity = True
255 |                 return False
256 | 
257 |             if not self.mining_safety_check(c): return 0
258 | 
259 |             self.safeWalk(c,0.3)
260 | 
261 |             # Check if we are done
262 |             if c.x == end.x and c.z == end.z:
263 |                 return True
264 | 
265 |             if c.x != end.x:
266 |                 c.x += d.x
267 |             if c.z != end.z:
268 |                 c.z += d.z
269 | 
270 |     #
271 |     # Mine a rectangle of dx times dz, height h around a chest
272 |     #
273 | 
274 |     def roomMine(self,dx_max,dz_max, height):
275 | 
276 |         dx_max = int( (checkIntArg(dx_max, 3, 99)-1)/2)
277 |         dz_max = int( (checkIntArg(dz_max, 3, 99)-1)/2)
278 |         height = checkIntArg(height, 2, 8)
279 | 
280 |         if not dx_max or not dz_max or not height:
281 |             self.chat('Try: mine room <dx 3-99> <dz 3-99> <height 2-8>')
282 |             return False
283 | 
284 |         area = workArea(self,1,1,1,notorch=True)
285 |         if not area.valid:
286 |             return False
287 |         start = area.start
288 | 
289 |         self.refreshActivity([f'Room mining started'])
290 |         self.pdebug(f'Mining out area of {2*dx_max+1} x {2*dz_max+1} x {height} blocks.',2)
291 | 
292 |         for dz in range(0,dz_max+1):    
293 | 
294 |             todo = False
295 |             for dx in range(-dx_max,dx_max+1):
296 |                 for h in range(0,height):
297 |                     if self.bot.blockAt(Vec3(start.x+dx, start.y+h, start.z+dz)).displayName not in self.ignored_blocks:
298 |                         todo = True
299 |                         break
300 |                     if self.bot.blockAt(Vec3(start.x+dx, start.y+h, start.z-dz)).displayName not in self.ignored_blocks:
301 |                         todo = True
302 |                         break
303 |                 if todo:
304 |                     break
305 | 
306 |             if not todo:
307 |                 continue
308 | 
309 |             self.refreshActivity("Restocking.")
310 |             area.restock(self.miningEquipList)
311 |             time.sleep(1)
312 |             if not self.checkMinimumList(self.miningMinimumList):
313 |                 return False
314 | 
315 |             if not self.stopActivity:
316 | 
317 |                 # Carve initial column
318 |                 self.refreshActivity( [ f'Blocks Mined: {area.blocks_mined}', f'Row: {dz}' ] )
319 |                 row_c = Vec3(start.x,start.y,start.z+dz)
320 |                 self.pdebug(f'walking to {row_c.x} {row_c.y} {row_c.z}',3)
321 |                 self.walkTo(row_c)
322 |                 self.minePath(row_c,Vec3(row_c.x-dx_max,row_c.y,row_c.z),height, area=area)
323 |                 self.walkTo(row_c)
324 |                 self.minePath(row_c,Vec3(row_c.x+dx_max,row_c.y,row_c.z),height, area=area)
325 | 
326 |             if not self.stopActivity:
327 | 
328 |                 self.refreshActivity( [ f'Blocks Mined: {area.blocks_mined}', f'Row: {dz}' ] )
329 |                 row_c = Vec3(start.x,start.y,start.z-dz)
330 |                 self.walkTo(row_c)
331 |                 self.minePath(row_c,Vec3(row_c.x-dx_max,row_c.y,row_c.z),height, area=area)
332 |                 self.walkTo(row_c)
333 |                 self.minePath(row_c,Vec3(row_c.x+dx_max,row_c.y,row_c.z),height, area=area)
334 | 
335 | 
336 |             if self.stopActivity:
337 |                 break
338 | 
339 |         # Mining ended
340 |         area.restock(self.miningEquipList)
341 | 
342 |         return True
343 | 
344 |     #
345 |     #  Find Valuables in a side corridor
346 |     #  Returns max_x, max_y of the furthest
347 | 
348 |     def findValuables(self,area, max_x, max_y, z, min_y=0):
349 |         if max_x < 0:
350 |             r = range(0,max_x-1,-1)
351 |         elif max_x > 0:
352 |             r = range(0,max_x+1,1)
353 |         else:
354 |             return 0,0
355 | 
356 |         bx = 0
357 |         by = 0
358 |         name = None
359 | 
360 |         for x in r:
361 |             for y in range(min_y,max_y):
362 |                 n = area.blockAt(x,y,z).displayName
363 |                 if n in self.valuable_blocks:
364 |                     bx = x
365 |                     by = max(y,by)
366 |                     name = n
367 |         if name:
368 |             self.pdebug(f'  @{z:3} found {name}    {bx}/{by}',2)
369 |             area.valuables = name
370 |         return bx, by
371 | 
372 |     def bridgeIfNeeded(self, area, x, z):
373 |         if area.blockAt(x,-1,z).displayName in self.dangerBlocks:
374 |             v_place = area.toWorld(x,-1,z-1)
375 |             # Try three times.
376 |             for ii in range (0,3):
377 |                 self.wieldItemFromList(self.fillBlocks)
378 |                 self.bridgeBlock(v_place,area.forwardVector)
379 |                 if area.blockAt(x,-1,z).displayName not in self.dangerBlocks:
380 |                     break
381 |             else:                            
382 |                 self.perror(f'*** fatal error. Cant bridge dangerous block {area.blockAt(x,-1,z).displayName}')
383 |                 area.status = "blocked/drop"
384 |                 self.stopActivity = True
385 |                 return False
386 |             area.blocks_mined += 1
387 |         return True
388 | 
389 |     
390 |     #
391 |     # Mine up a column of a specific height
392 |     # Bridge afterwards if needed.
393 |     #
394 | 
395 |     def mineColumn(self, area, x, z, height):
396 | 
397 |         if self.stopActivity: return False
398 |         self.pdebug(f'mineColumn(x:{x},z:{z},height:{height})',5)
399 | 
400 |         # Check if we need to do anything
401 |         for y in range(0,height):                      
402 |             if area.blockAt(x,y,z).displayName not in self.ignored_blocks:
403 |                 break
404 |         else:
405 |             return True
406 | 
407 |         # Check for infested
408 |         for y in range(0,height):
409 |             if area.blockAt(x,y,z).displayName == "Infested Stone":
410 |                 self.pdebug(f'  located {area.blockAt(x,y,z).displayName}, aborting!',1)
411 |                 area.status = "* Silverfish *"
412 |                 self.stopActivity = True
413 |                 return False
414 | 
415 |         # Try to mine the column. May take multiple attempts due to gravel.
416 |         for tries in range(0,10):
417 |             done = True
418 |             for y in range(0,height):                     
419 |                 if self.stopActivity: return True
420 |                 if area.blockAt(x,y,z).displayName not in self.ignored_blocks:
421 |                     # We need to clear this
422 |                     done = False
423 |                     if area.blockAt(x,y+1,z).displayName in self.block_will_drop:
424 |                         self.mineBlock( area.toWorld(x,y,z) )
425 |                         time.sleep(1)
426 |                     else:
427 |                         self.mineBlock( area.toWorld(x,y,z) )
428 |                     area.blocks_mined += 1
429 |             if done:
430 |                 break
431 |                     
432 |         for y in range(0,height):                      
433 |             if area.blockAt(x,y,z).displayName not in self.ignored_blocks:
434 |                 self.perror(f'aborting - block not cleared: {area.blockAt(x,y,z).displayName}.')
435 |                 area.status = "blocked"
436 |                 self.stopActivity = True
437 |                 return False
438 |                 
439 |         return True
440 | 
441 | #
442 | # Check for goodies in the floor. Works best to about 2 deep.
443 | #
444 | 
445 |     def floorMine(self, area, x, z, depth):
446 |         if self.stopActivity: return False
447 | 
448 |         if depth > 0:
449 |             max_d = 0
450 |             for d in range(1,depth+1):
451 |                 if area.blockAt(x,-d,z).displayName in self.valuable_blocks:
452 |                     max_d = d
453 |             if max_d > 0:
454 |                 # Ok, we found something
455 |                 for d in range(1,max_d+1):
456 |                     self.mineBlock( area.toWorld(x,-d,z) )
457 |                 # Now fill it up, which gets us the blocks. Best effort.
458 |                 for d in range(max_d, 0, -1):
459 |                     v_place = area.toWorld(x,-d-1,z)
460 |                     self.wieldItemFromList(self.fillBlocks)
461 |                     self.safePlaceBlock(v_place,Vec3(0,1,0))
462 |                     time.sleep(0.2)
463 |         return True
464 | 
465 |     def ceilingMine(self, area, x, z, max_height):
466 |         if self.stopActivity: return False
467 | 
468 |         # Check the ceiling up to max reachable height (7 above)
469 |         max_y = 0
470 |         for y in range(2,max_height):
471 |             if area.blockAt(x,y,z).displayName in self.valuable_blocks:
472 |                 max_y = y
473 |         if max_y > 0:
474 |             # Ok, we found something
475 |             for y in range(2,max_y+1):
476 |                 if area.blockAt(x,y,z).displayName not in self.ignored_blocks:
477 |                     if area.blockAt(x,y+1,z).displayName in self.dangerDropBlocks:
478 |                         self.pdebug(f'  cant mine ceiling, {area.blockAt(x,y+1,z).displayName} above.',2)
479 |                         return False
480 |                     self.mineBlock( area.toWorld(x,y,z) )
481 | 
482 |     #
483 |     # Mine up a row. Unlike minePath, this works in an area
484 |     #
485 | 
486 |     def mineRow(self, area, max_x, height, z, floor_mine=0, ceiling_mine=0):
487 |         #print(f'mineRow(max_x:{max_x},height:{height},z:{z},floor_mine:{floor_mine},ceiling_mine:{ceiling_mine})')
488 |         if max_x == 0:
489 |             return False
490 |         elif max_x < 0:
491 |             dx = -1
492 |         elif max_x > 0:
493 |             dx = 1
494 | 
495 |         r = range(dx*area.width2+dx, max_x+dx,dx)
496 |         area.walkToBlock3(dx*area.width2,0,z)
497 |         height = max(2,height)
498 | 
499 |         for x in r:
500 |             if self.stopActivity : break
501 |             if not self.mineColumn(area, x, z, height):
502 |                 return False
503 |             # Check floors
504 |             if floor_mine > 0:
505 |                 self.floorMine(area, x, z, floor_mine)
506 |             if ceiling_mine > 0:
507 |                 self.ceilingMine(area, x, z, ceiling_mine)
508 |             # Bridge if needed
509 |             if area.blockAt(x,-1,z).displayName in self.dangerBlocks:
510 |                 v_place = area.toWorld(x-dx,-1,z)
511 |                 # Try three times.
512 |                 self.wieldItemFromList(self.fillBlocks)
513 |                 self.bridgeBlock(v_place,area.dirToWorldV3(Vec3(dx,0,0)))
514 |                 if area.blockAt(x,-1,z).displayName in self.dangerBlocks:
515 |                         self.pdebug(f'    cant reach, bridging failed {area.blockAt(x,-1,z).displayName}.',2)
516 |                         area.walkToBlock3(0,0,z)
517 |                         return False
518 |             if not self.mining_safety_check(area.toWorld(x,0,z)): return False
519 |             area.walkToBlock3(x,0,z)
520 |         time.sleep(0.5)
521 |         return True
522 | 
523 |     # Helper function for UI
524 | 
525 |     def mineActivity(self,area,z,txt1="",txt2=""):
526 |             l = [
527 |                     f'Depth: {z}    ⏱️ {int(100*(area.blocks_mined-area.last_break)/area.break_interval)}%',
528 |                     f'Status: {area.status}', 
529 |                     txt1,
530 |                     txt2
531 |                 ]
532 |             self.refreshActivity(l)
533 | 
534 |     #
535 |     #  Build a strip mine of a specific height and width and light it up
536 |     #
537 | 
538 |     def stripMine(self,width=3,height=3,valrange=3):
539 | 
540 |         z_torch = 0
541 |         z =0
542 |         area = workArea(self,width,height,99999)
543 |         if not area.valid:
544 |             return False
545 |         self.speedMode = True   # explore fast until we find something
546 | 
547 |         self.refreshActivity([f'Mining started'])
548 | 
549 |         while not self.stopActivity:
550 |             # Get ready
551 |             self.mineActivity(area,z,"Restocking.")
552 |             area.restock(self.miningEquipList)
553 |             area.last_break = area.blocks_mined
554 |             time.sleep(1)
555 |             if not self.checkMinimumList(self.miningMinimumList):
556 |                 return False
557 | 
558 |             self.mineActivity(area,z,"Walking back to work")
559 |             while area.blocks_mined-area.last_break < area.break_interval and not self.stopActivity:
560 |                 if not self.mining_safety_check(area.toWorld(0,0,z)): break
561 |                 area.walkToBlock3(0,0,z-1)
562 | 
563 |                 if area.blocks_mined > 0: self.speedMode = False
564 | 
565 |                 # Step 0 - Check if we are still good
566 |                 if not self.checkMinimumList(self.miningMinimumList):
567 |                     self.perror("Aborting, out of required equipment.")
568 |                     self.stopActivity = True
569 |                     area.status = "out of tools"
570 |                     break
571 | 
572 |                 # Step 1 - Mine the main tunnel
573 |                 self.mineActivity(area,z,"Walking back to work", f'Mining main tunnel')
574 |                 for x in area.xRange():
575 |                     self.mineColumn(area, x, z, height)
576 |                     self.floorMine(area, x, z, 2)
577 |                     self.ceilingMine(area, x, z, height+2)
578 |                     
579 |                 # Step 2 - Bridge if needed 
580 |                 for x in area.xRange():
581 |                     self.bridgeIfNeeded(area, x, z)
582 |                 if self.stopActivity: break
583 | 
584 |                 area.walkToBlock3(0,0,z)
585 |                 # Step 3 - Look for Valuables Left and Right
586 | 
587 |                 bx, by  = self.findValuables(area, -area.width2-valrange, height+2, z, min_y=-2)
588 |                 by = min(by,height-1)
589 |                 if bx != 0:
590 |                     self.mineActivity(area, z, f'Found: {area.valuables}✨', f'⬅️ Left side {bx}/{by+1}')
591 |                     self.mineRow(area, bx, by+1, z, floor_mine=2, ceiling_mine=height+2)
592 |                     area.walkToBlock3(0,0,z)
593 | 
594 |                 bx, by  = self.findValuables(area, area.width2+valrange, height+2, z, min_y=-2)
595 |                 by = min(by,height-1)
596 |                 if bx != 0:
597 |                     self.mineActivity(area, z, f'Found: {area.valuables}✨', f'➡️ Right side {bx}/{by+1}')
598 |                     self.mineRow(area, bx, by+1, z, floor_mine=2, ceiling_mine=height+2)
599 |                     area.walkToBlock3(0,0,z)
600 | 
601 |                 # Step 4 - Light up if needed and move forward by one.
602 |                 if z > z_torch:
603 |                     self.mineActivity(area, z, f'Placing Torch')
604 |                     # try to place a torch
605 |                     torch_v = area.toWorld(area.width2,1,z)
606 |                     wall_v  = area.toWorld(area.width2+1,1,z)
607 |                     dv = subVec3(torch_v, wall_v)
608 |                     if self.bot.blockAt(wall_v).displayName not in self.ignored_blocks:
609 |                         if self.bot.blockAt(torch_v).displayName != "Wall Torch":
610 |                             self.pdebug("  placing torch.",2)
611 |                             self.wieldItem("Torch")
612 |                             self.safePlaceBlock(wall_v,dv)
613 |                         z_torch += 6
614 |                 z += 1
615 | 
616 |             # ...and back to the chest to update sign and restock
617 |             self.speedMode = False
618 |             self.mineActivity(area, z, f'Walking to Chest')
619 |             area.walkToStart()
620 |             if self.dangerType:
621 |                 s = self.dangerType
622 |             else:
623 |                 s = area.status
624 |             self.mineActivity(area, z, f'Updating Sign')
625 |             txt = [f'Mine {area.directionStr()} {width}x{height}', f'Length: {z}', myDate(), s ]
626 |             self.updateSign(txt,tryonly=True)
627 | 
628 |         # Mining ended
629 |         area.restock(self.miningEquipList)
630 | 
631 | 
632 |     #
633 |     # Mine a vertical shaft of N x N down to depth D
634 |     #
635 | 
636 |     def shaftMine(self,d,min_y):
637 | 
638 |         r = int( (checkIntArg(d, 1, 99)-1)/2)
639 |         d = r*2+1
640 |         min_y = checkIntArg(min_y, -64, 320)
641 | 
642 |         if r == None or min_y == None:
643 |             print(r,min_y)
644 |             self.chat('Try: mine shaft <diameter: 1 to 99> <bottom: -65 to 320>')
645 |             return False
646 | 
647 |         area = workArea(self,d,d,1,notorch=True)
648 |         if not area.valid:
649 |             return False
650 |         start = area.start
651 |         area.restock(self.miningEquipList)
652 | 
653 |         self.refreshActivity([f'Shaft mining started'])
654 |         self.pdebug(f'Mining vertical shaft of {d} x {d} down to level {min_y}',2)
655 | 
656 |         for y in range(0, min_y-start.y-1, -1):
657 |             for dz in range(0,r+1):    
658 | 
659 |                 if not self.stopActivity:
660 |                     self.refreshActivity( [ f'Vertical Shaft {d}x{d} to lvl {min_y}',f'Blocks Mined: {area.blocks_mined}', f'Depth: {y}' ] )
661 |                     area.walkToBlock(0,y,dz)
662 |                     self.minePath(area.toWorld(0,y,dz),area.toWorld(-r,y,dz),2, area=area)
663 |                     area.walkToBlock(0,y,dz)
664 |                     self.minePath(area.toWorld(0,y,dz),area.toWorld( r,y,dz),2, area=area)
665 | 
666 |                 if not self.stopActivity:
667 | 
668 |                     self.refreshActivity( [ f'Vertical Shaft {d}x{d} to lvl {min_y}',f'Blocks Mined: {area.blocks_mined}', f'Depth: {y}' ] )
669 |                     area.walkToBlock(0,y,-dz)
670 |                     self.minePath(area.toWorld(0,y,-dz),area.toWorld(-r,y,-dz),2, area=area)
671 |                     area.walkToBlock(0,y,-dz)
672 |                     self.minePath(area.toWorld(0,y,-dz),area.toWorld( r,y,-dz),2, area=area)
673 | 
674 |                 if self.stopActivity:
675 |                     break
676 | 
677 |         # Mining ended - no deposit as we may not be able to get up the shaft
678 | 
679 |         return True
680 |      
681 | 
682 |     def doMining(self,args):
683 | 
684 |         if len(args) == 0:
685 |             self.chat('Need to specify type of mine. Try "fast", "3x3" or "5x5".')
686 |         else:
687 |             mtype = args[0]
688 |             if mtype == '3x3':
689 |                 self.activity_name = "Mine 3x3"
690 |                 self.stripMine(3,3,5)
691 |             elif mtype == 'tunnel3x3':
692 |                 self.activity_name = "Tunnel 3x3"
693 |                 self.stripMine(3,3,0)
694 |             elif mtype == '5x5':
695 |                 self.activity_name = "Mine 5x5"
696 |                 self.stripMine(5,5,5)
697 |             elif mtype == 'tunnel5x5':
698 |                 self.activity_name = "Tunnel 5x5"
699 |                 self.stripMine(5,5,0)
700 |             elif mtype == 'branch' or mtype == 'fast':
701 |                 self.activity_name = "Branchmine"
702 |                 self.stripMine(1,5,5)
703 |             elif mtype == 'room':
704 |                 if len(args) < 4:
705 |                     self.chat('Try: mine room <length> <width> <height>')
706 |                 else:
707 |                     self.activity_name = f'Mine Room {args[1]}x{args[2]}x{args[3]}'
708 |                     self.roomMine(args[1],args[2],args[3])
709 |             elif mtype == 'shaft':
710 |                 if len(args) < 3:
711 |                     self.chat('Try: mine shaft <diameter> <layer of shaft bottom>')
712 |                     self.activity_name = f'Mine Vertical Shaft {args[1]}x{args[1]} to level {args[2]}'
713 |                 else:
714 |                     self.shaftMine(args[1],args[2])
715 |             else:
716 |                 self.chat(f'I don\'t know how to mine a \'{mtype}\'.')
717 | 
718 |         self.endActivity()
719 |         time.sleep(1)
720 |         return True


--------------------------------------------------------------------------------
/movement.py:
--------------------------------------------------------------------------------
  1 | #
  2 | #  Various functions to deal with blocks, locations and movement
  3 | #
  4 | 
  5 | import time
  6 | 
  7 | from javascript import require
  8 | from math import sqrt, atan2, sin, cos
  9 | from botlib import *
 10 | 
 11 | Vec3     = require('vec3').Vec3
 12 | pathfinder = require('mineflayer-pathfinder')
 13 | 
 14 | 
 15 | #
 16 | # Movement functions for bot
 17 | #
 18 | 
 19 | class MovementManager:
 20 | 
 21 |     empty_blocks = [ "Water", "Lava", "Air", "Cave Air", "Void Air"]
 22 | 
 23 |     def __init__(self):
 24 |         print('movement ', end='')
 25 | 
 26 |     # Versatile blockAt, takes 3 coordinates or vector
 27 | 
 28 |     def blockAt(self, x, y=None, z=None):
 29 |         if y:
 30 |             v = Vec3(x,y,z)
 31 |         else:
 32 |             v = x
 33 |         return self.bot.blockAt(v)
 34 | 
 35 |     def safeWalk(self, toPosition, radius=1):
 36 |         self.pdebug(f'    safeWalk to {toPosition.x} {toPosition.y} {toPosition.z}  r={radius}',4)
 37 |         if not toPosition:
 38 |             print('*** error: toPosition is not defined.')
 39 |             return False
 40 |         if not toPosition.x:
 41 |             print('*** error: toPosition has no x coordinate. Not a position vector?')
 42 |             return False
 43 |         try:
 44 |             p = self.bot.pathfinder
 45 |             if p == None:
 46 |                 print('  *** error: pathfinder is None in safeWalk.')
 47 |                 return False
 48 |             p.setGoal(pathfinder.goals.GoalNear(toPosition.x,toPosition.y,toPosition.z,radius))
 49 |         except Exception as e:
 50 |             print(f'*** error in safeWalk {e}')
 51 |             return False
 52 |         t = walkTime(toPosition,self.bot.entity.position)
 53 |         if not self.speedMode:
 54 |              time.sleep(t)
 55 |         return True
 56 | 
 57 |     def walkTo(self,x,y=None,z=None):
 58 |         if hasattr(x, 'position') and x.position:
 59 |             v = Vec3(x.position.x,x.position.y,x.position.z)
 60 |             self.safeWalk(v,1)
 61 |         elif not y:
 62 |             self.safeWalk(x,1)
 63 |         else:
 64 |             v = Vec3(x,y,z)
 65 |             self.safeWalk(v,1)
 66 | 
 67 |     def walkToBlock(self,x,y=None,z=None):
 68 |         if hasattr(x, 'position') and x.position:
 69 |             v = Vec3(x.position.x+0.5,x.position.y,x.position.z+0.5)
 70 |             self.safeWalk(v)
 71 |         elif not y:
 72 |             v = Vec3(x.x+0.5,x.y,x.z+0.5)
 73 |             self.safeWalk(v)
 74 |         else:
 75 |             v = Vec3(x+0.5,y,z+0.5)
 76 |             self.safeWalk(v)
 77 | 
 78 |     def walkToBlock3(self,x,y=None,z=None):
 79 |         if hasattr(x, 'position') and x.position:
 80 |             v = Vec3(x.position.x+0.5,x.position.y,x.position.z+0.5)
 81 |             self.safeWalk(v,0.3)
 82 |         elif not y:
 83 |             v = Vec3(x.x+0.5,x.y,x.z+0.5)
 84 |             self.safeWalk(v,0.3)
 85 |         else:
 86 |             v = Vec3(x+0.5,y,z+0.5)
 87 |             self.safeWalk(v,0.3)
 88 | 
 89 | 
 90 |     # Walks on top of this block
 91 | 
 92 |     def walkOnBlock(self,x,y=None,z=None):
 93 |         if hasattr(x, 'position') and x.position:
 94 |             v = Vec3(x.position.x+0.5,x.position.y+1,x.position.z+0.5)
 95 |             self.safeWalk(v)
 96 |         elif not y:
 97 |             v = Vec3(x.x+0.5,x.y+1,x.z+0.5)
 98 |             self.safeWalk(v)
 99 |         else:
100 |             v = Vec3(x+0.5,y+1,z+0.5)
101 |             self.safeWalk(v)
102 | 
103 | 
104 |     # this will attempt to walk on to block at v, and place a block in the direction d
105 | 
106 |     def safePlaceBlock(self,v,dv):
107 |         v_gap = addVec3(v,dv)
108 |         b     = self.bot.blockAt(v)
109 |         b_gap = self.bot.blockAt(v_gap)
110 | 
111 |         if b_gap.displayName not in self.empty_blocks:
112 |             self.perror(f'cant place block in space occupied by {b_gap.displayName}.')
113 |             self.perror(f'{b_gap.displayName} @{v_gap.x}/{v_gap.y}/{v_gap.z} against {b.displayName} @{v.x}/{v.y}/{v.z}')
114 |             return False
115 |         if b.displayName in self.empty_blocks:
116 |             self.perror(f'place {b_gap.displayName} @{v_gap.x}/{v_gap.y}/{v_gap.z} against {b.displayName} @{v.x}/{v.y}/{v.z}')
117 |             return False
118 |         try:
119 |             self.bot.placeBlock(b,dv)
120 |             return True
121 |         except Exception as e:
122 |             self.pexception(f'{b_gap.displayName} @{v_gap.x}/{v_gap.y}/{v_gap.z} against {b.displayName} @{v.x}/{v.y}/{v.z}',e)
123 |             return False
124 | 
125 |     def bridgeBlock(self, v, d):
126 | 
127 |         v_gap = addVec3(v,d)
128 | 
129 |         b     = self.bot.blockAt(v)
130 |         b_gap = self.bot.blockAt(v_gap)
131 | 
132 |         d_inv = Vec3(-d.x,-d.y,-d.z)
133 | 
134 |         self.pdebug(f'  bridging {b_gap.displayName} @{v_gap.x}/{v_gap.y}/{v_gap.z} against {b.displayName} @{v.x}/{v.y}/{v.z}',2)
135 | 
136 |         self.walkToBlock(v.x,v.y+1,v.z)
137 |         time.sleep(1)
138 | 
139 |         # Code from mineflayer.pathfinder
140 |         # Target viewing direction while approaching edge
141 |         # The Bot approaches the edge while looking in the opposite direction from where it needs to go
142 |         # The target Pitch angle is roughly the angle the bot has to look down for when it is in the position
143 |         # to place the next block
144 | 
145 |         targetYaw = atan2(d.x, d.z)
146 |         targetPitch = -1.421
147 |         viewVector = getViewVector(targetPitch, targetYaw)
148 |         pos = self.bot.entity.position
149 |         if not pos:
150 |             print("*** error: position is None in bridgeBlock.")
151 |             return False
152 |         p = pos.offset(viewVector.x, viewVector.y, viewVector.z)
153 |         self.bot.lookAt(p, True)
154 |         self.bot.setControlState('sneak', True)
155 |         time.sleep(0.5)
156 |         self.bot.setControlState('back', True)
157 |         time.sleep(0.5)
158 |         self.bot.setControlState('back',False)
159 |         if not self.safePlaceBlock(v,d):
160 |             return False
161 | 
162 |         self.walkToBlock(v.x,v.y+1,v.z)
163 |         self.bot.setControlState('sneak',False)
164 |         time.sleep(0.5)
165 |         return
166 | 
167 |     #
168 |     #  Find closest (taxi geometry) block with specific content
169 |     #  target can be a list or an item
170 | 
171 |     def findClosestBlock(self,target,xz_radius=2,y_radius=1,metadata=None,spaceabove=False):
172 |         best_block = None
173 |         best_dist  = 999
174 | 
175 |         p = self.bot.entity.position
176 | 
177 |         if type(target) is not list:
178 |             target = [target]
179 | 
180 |         # Search larger and larger rectangles
181 | 
182 |         for r in range(0,xz_radius+1):
183 |             for dx, dz in rectangleBorder(r,r):
184 |                 for dy in range(-y_radius,y_radius+1):
185 |                         b = self.bot.blockAt(Vec3(p.x+dx,p.y+dy,p.z+dz))
186 |                         #print(dx,dy,dz,b.displayName,target)
187 |                         if b.displayName in target:
188 |                             if metadata and b.metadata != metadata:
189 |                                 continue
190 |                             if spaceabove:
191 |                                 b_above = self.bot.blockAt(Vec3(p.x+dx,p.y+dy+1,p.z+dz))
192 |                                 if not b_above or b_above.type != 0:
193 |                                     continue
194 |                             dist = sqrt(dx*dx+dy*dy+dz*dz)
195 |                             # print("Found at ",v," distance ",dist)
196 |                             if best_block == None or best_dist > dist:
197 |                                 best_block = b
198 |                                 best_dist = dist
199 |             if best_block:
200 |                 return best_block
201 |         return False
202 | 
203 | 
204 |     def gotoLocation(self,l):
205 |         if not l in self.myLocations:
206 |             print(f'*** error: cant find location {l}')
207 | 
208 |         c = self.myLocations[l]
209 |         print(f'moving to {l}')
210 |         self.safeWalk(Vec3(c[0], c[1], c[2]), 1 )
211 |         print("done.")
212 | 


--------------------------------------------------------------------------------
/pybot.py:
--------------------------------------------------------------------------------
  1 | #
  2 | #  The python Minecraft Bot to rule them all.
  3 | #  Poggers!
  4 | #
  5 | #  (c) 2021 by Guido Appenzeller & Daniel Appenzeller
  6 | #
  7 | 
  8 | import javascript
  9 | from javascript import require, On, Once, AsyncTask, once, off
 10 | import time
 11 | import asyncio
 12 | import argparse
 13 | 
 14 | from inventory import *
 15 | from movement import *
 16 | from farming import *
 17 | from mine import *
 18 | from build import *
 19 | from chat import *
 20 | from combat import *
 21 | from gather import *
 22 | 
 23 | 
 24 | #
 25 | # Main Bot Class
 26 | #
 27 | # Additional Methods are added via Mixin inheritance and are in the various modules
 28 | #
 29 | 
 30 | class PyBot(ChatBot, FarmBot, MineBot, GatherBot, BuildBot, CombatBot, MovementManager, InventoryManager):
 31 | 
 32 |     def __init__(self,account):
 33 |         # This is the Mineflayer bot
 34 |         self.bot = None
 35 |         self.account = account
 36 |         self.callsign = self.account['user'][0:2]+":"
 37 |         self.debug_lvl = 3
 38 |         self.lastException = None
 39 | 
 40 |         self.stopActivity = False
 41 |         self.dangerType = None
 42 | 
 43 |         self.speedMode = False # Move fast 
 44 | 
 45 |         mineflayer = require('mineflayer')
 46 | 
 47 |         bot = mineflayer.createBot(
 48 |             {
 49 |             'host'    : self.account['host'],
 50 |             'username': self.account['user'],
 51 |             'password': self.account['password'],
 52 |             'version': self.account['version'],
 53 |             'hideErrors': False,
 54 |             } )
 55 | 
 56 |         self.mcData   = require('minecraft-data')(bot.version)
 57 |         self.Block    = require('prismarine-block')(bot.version)
 58 |         self.Item     = require('prismarine-item')(bot.version)
 59 |         self.Vec3     = require('vec3').Vec3
 60 | 
 61 |         # Setup for the pathfinder plugin
 62 |         pathfinder = require('mineflayer-pathfinder')
 63 |         bot.loadPlugin(pathfinder.pathfinder)
 64 |         # Create a new movements class
 65 |         movements = pathfinder.Movements(bot, self.mcData)
 66 |         movements.blocksToAvoid.delete(self.mcData.blocksByName.wheat.id)
 67 |         bot.pathfinder.setMovements(movements)
 68 |         self.bot = bot
 69 | 
 70 |         # Initialize modules
 71 |         # Python makes this hard as __init__ of mixin classes is not called automatically
 72 | 
 73 |         print(f'pybot - a smart minecraft bot by Guido and Daniel Appenzeller.')
 74 | 
 75 |         classes = PyBot.mro()
 76 |         print('  modules: ', end='')
 77 |         for c in classes[1:]:
 78 |             c.__init__(self)
 79 |         print('.')
 80 | 
 81 |     # Debug levels: 
 82 |     #   0=serious error
 83 |     #   1=important info or warning 
 84 |     #   2=major actions or events
 85 |     #   3=each action, ~1/second
 86 |     #   4=spam me!
 87 |     #   5=everything
 88 | 
 89 |     def perror(self, message):
 90 |         print(f'*** error: {message}')
 91 | 
 92 |     def pexception(self, message,e):
 93 |         print(f'*** exception: {message}')
 94 |         if self.debug_lvl >= 4:
 95 |             print(e)
 96 |         else:
 97 |             with open("exception.debug", "w") as f:
 98 |                 f.write("PyBit Minecraft Bot - Exception Dump")
 99 |                 f.write(str(e))
100 |                 f.write("")
101 |         self.lastException = e
102 | 
103 |     def pinfo(self, message):
104 |         if self.debug_lvl > 0:
105 |             print(message)
106 | 
107 |     def pdebug(self,message,lvl=4,end="\n"):
108 |         if self.debug_lvl >= lvl:
109 |             print(message,end=end)
110 | 
111 |     # Dummy functions, they get overriden by the GUI if we have it
112 | 
113 |     def mainloop(self):
114 |         pass
115 | 
116 |     def refreshInventory(self):
117 |         pass
118 | 
119 |     def refreshEquipment(self):
120 |         pass
121 | 
122 |     def refreshStatus(self):
123 |         pass
124 | 
125 |     def refreshActivity(self,txt):
126 |         pass
127 | 
128 |     def bossPlayer(self):
129 |         return self.account["master"]
130 | 
131 | #
132 | # Run the bot. 
133 | # Note that we can run with or without UI
134 | #
135 | 
136 | if __name__ == "__main__":
137 | 
138 |     parser = argparse.ArgumentParser(prog='python pybot.py')
139 |     parser.add_argument('--nowindow', action='store_true', help='run in the background, i.e. without the Tk graphical UI')
140 |     parser.add_argument('--verbose', '-v', action='count', default=0, help='verbosity from 1-5. Use as -v, -vv, -vvv etc.')
141 |     args = parser.parse_args()
142 |     argsd = vars(args)
143 | 
144 |     # Import credentials and server info, create the bot and log in
145 |     from account import account
146 |     if  argsd["nowindow"]:
147 |         pybot = PyBot(account.account)
148 |     else:
149 |         from ui import PyBotWithUI
150 |         pybot = PyBotWithUI(account.account)
151 |     pybot.pdebug(f'Connected to server {account.account["host"]}.',0)
152 |     if 'verbose' in argsd:
153 |         pybot.debug_lvl = argsd['verbose']
154 | 
155 |     # Import list of known locations. Specific to the world.
156 |     if account.locations:
157 |         pybot.myLocations = account.locations
158 | 
159 |     #
160 |     # Main Loop - We are driven by chat commands
161 |     #
162 | 
163 |     # Report status
164 |     while not pybot.bot.health:
165 |         time.sleep(1)
166 | 
167 |     @On(pybot.bot, 'chat')
168 |     def onChat(sender, message, this, *rest):
169 |         pybot.handleChat(sender, message, this, *rest)
170 | 
171 |     @On(pybot.bot, 'health')
172 |     def onHealth(arg):
173 |         pybot.healthCheck()
174 | 
175 |     @AsyncTask(start=True)
176 |     def asyncInitialHeal(task):
177 |         pybot.healToFull()
178 | 
179 |     if pybot.debug_lvl >= 4:
180 |         pybot.printInventory()
181 |     pybot.pdebug(f'Ready.',0)
182 | 
183 |     pybot.mainloop()
184 |     # The spawn event
185 |     #once(pybot.bot, 'login')
186 |     #pybot.bot.chat('Bot '+pybot.bot.callsign+' joined.')
187 | 


--------------------------------------------------------------------------------
/test.py:
--------------------------------------------------------------------------------
 1 | #
 2 | #  Test Routines for the bot
 3 | #
 4 | 
 5 | import time
 6 | from inventory import *
 7 | 
 8 | def wieldTest(pybot):
 9 |     delay_t = 0.0
10 | 
11 |     pybot.printInventory()
12 | 
13 |     print('-- Static tests')
14 |     print(f'Stone Pickaxe: {pybot.mcData.itemsByName.stone_pickaxe.id}')
15 |     print(f'Stone Axe:     {pybot.mcData.itemsByName.stone_axe.id}')
16 |     print(f'End Crystal:   {pybot.mcData.itemsByName.end_crystal.id}')
17 | 
18 |     print('--- Test stone pickaxe:')
19 |     if pybot.wieldItem(pybot.mcData.itemsByName.stone_pickaxe.id) != "Stone Pickaxe":
20 |         print('Exception:')
21 |         print(pybot.lastException)
22 |         return
23 |     else:
24 |         print('passed')
25 | 
26 |     print('--- Test stone axe:')
27 |     if pybot.wieldItem("Stone Axe") != "Stone Axe":
28 |         print('Exception:')
29 |         print(pybot.lastException)
30 |         return
31 |     else:
32 |         print('passed')
33 | 
34 |     print('')
35 |     print('--- Item equip long-term stability test.')
36 |     i = 0
37 |     while True:
38 |         r = pybot.wieldItem('Stone Pickaxe')
39 |         if r != "Stone Pickaxe": 
40 |             break
41 |         time.sleep(delay_t)
42 |         i = i+1
43 |         r = pybot.wieldItem('Stone Axe')
44 |         if r != "Stone Axe": 
45 |             break
46 |         time.sleep(delay_t)
47 |         i = i+1
48 | 
49 |     print(f'error after {i} equip operations.')
50 |     print('')
51 |     print('Exception:')
52 |     print(pybot.lastException)
53 | 
54 | def chestTest1(pybot):
55 | 
56 |     chest = Chest(pybot)
57 | 
58 |     while True:
59 |         chest.open()
60 |         for i in chest.chestObj.containerItems():
61 |             if i.count > 0:
62 |                 chest.withdrawItem(i,i.count)
63 |         chest.close()
64 | 
65 |         time.sleep(1)
66 | 
67 |         chest.open()
68 |         chest.deposit()
69 |         chest.close()
70 | 
71 | def chestTest2(pybot):
72 | 
73 |     q = [1,5,20,40,63,64,60,15,2]
74 |     i = 0
75 | 
76 |     chest = Chest(pybot)
77 | 
78 |     while True:
79 | 
80 |         i = (i +1) % len(q)
81 | 
82 |         restockList = {
83 |             "Stone Pickaxe":q[i],
84 |             "Stone Axe":q[i],
85 |             "Bread":q[i],
86 |             "Cobblestone":q[i],
87 |             "Dirt":q[i],
88 |             "Torch":q[i],
89 |         }
90 | 
91 |         chest.open()
92 |         chest.restock(restockList)
93 |         chest.close()
94 |         time.sleep(2)


--------------------------------------------------------------------------------
/ui.py:
--------------------------------------------------------------------------------
  1 | #
  2 | #
  3 | #
  4 | 
  5 | import tkinter as tk
  6 | import tkinter.scrolledtext
  7 | from tkinter import ttk, PhotoImage
  8 | import time
  9 | import datetime
 10 | from functools import partial
 11 | from javascript import require, On, Once, AsyncTask, once, off
 12 | Vec3     = require('vec3').Vec3
 13 | 
 14 | from pybot import PyBot
 15 | from mine import MineBot
 16 | import botlib
 17 | 
 18 | 
 19 | #            10             20
 20 | # 0  Status  |   MicroMap   |    Inventory
 21 | # 
 22 | #10 --------------------------------------
 23 | #
 24 | #    Commands
 25 | #
 26 | #20 --------------------------------------
 27 | #
 28 | #    Log
 29 | #
 30 | 
 31 | class LogFrame(tk.Frame):
 32 | 
 33 |     max_log_lines = 200
 34 | 
 35 |     def __init__(self, master):
 36 | 
 37 |         tk.Frame.__init__(self, master)
 38 |         self.logObj = tk.scrolledtext.ScrolledText(width=60, height=20, font = ("TkFixedFont", 11))
 39 |         self.place = self.logObj.place
 40 |         self.logObj.configure(state ='disabled')
 41 | 
 42 |     def log(self,txt):
 43 |         self.logObj.configure(state ='normal')
 44 |         l = int(self.logObj.index('end').split('.')[0])
 45 |         if l > self.max_log_lines:
 46 |             self.logObj.delete("1.0",f'{l-self.max_log_lines}.0\n')
 47 |         self.logObj.insert(tk.END,f'{txt}\n')
 48 |         self.logObj.see(tk.END)
 49 |         self.logObj.configure(state ='disabled')
 50 | 
 51 | class PyBotWithUI(PyBot):
 52 | 
 53 |     # List means first is color (or None) second is icon
 54 | 
 55 |     block_icons = {
 56 |         "Air"           : None,
 57 |         "Cave Air"      : None,
 58 |         "Void Air"      : None,
 59 |         "Torch"         : None,
 60 |         "Wall Torch"    : None,
 61 |         "Redstone Torch": None,
 62 |         "Rail"          : [None,"#"],
 63 |         "Chest"         : ["brown","📦"],
 64 |         "Spruce Log"    : "brown",
 65 |         "Spruce Leaves" : "dark green",
 66 |         "Wheat Crops"   : ["green","🌾"],
 67 |         "Lava"          : "red",
 68 |         "Water"         : "blue", 
 69 |         "Bubble Column" : "blue",
 70 |         "Crafting Table": "brown",
 71 |     }
 72 | 
 73 |     inv_icons = {
 74 |         "Lapis Lazuli":"✨",
 75 |         "Raw Iron":"🪙",
 76 |         "Raw Copper":"🥉",
 77 |         "Raw Gold":"✨",
 78 |         "Redstone Dust":"🔴",
 79 |         "Diamond":"💎",
 80 |         "Emerald":"✨",
 81 |         "Wheat":"🌽",
 82 |         "Spruce Log":"🪵",
 83 |         "Spruce Sapling":"🌲",
 84 |         "Wheat Seeds":"🌿",
 85 |         "Coal":"🪨",
 86 |     }
 87 | 
 88 |     hand_icons = {
 89 |         "Wheat Seeds":"🌿",    
 90 |         "Stone Axe":"🪓",
 91 |         "Iron Axe":"🪓",
 92 |         "Diamond Axe":"🪓",
 93 |         "Stone Pickaxe":"⛏️",
 94 |         "Iron Pickaxe":"⛏️",
 95 |         "Diamond Pickaxe":"⛏️",
 96 |         "Cobblestone":"🪨",
 97 |         "Stone Brick":"🧱",
 98 |         "Bread":"🍞",
 99 |         "Stone Shovel":"⚒️",
100 |         "Iron Shovel":"⚒️",
101 |         "Diamond Shovel":"⚒️",
102 |         "Stone Sword":"🗡️",
103 |         "Iron Sword":"🗡️",
104 |         "Diamond Sword":"🗡️",
105 |     }
106 | 
107 |     button_mapping = [
108 |         ["Come here"     , "come"],
109 |         ["Follow me"     , "follow"],
110 |         ["Farm Crops"    , "farm"],
111 |         ["Chop Wood"     , "chop"],
112 |         ["Deposit All"   , "deposit"],
113 |         ["STOP!"         , "stop"],
114 |         ["Mine Fast"     , "mine fast"],
115 |         ["Mine 3x3"      , "mine 3x3"],
116 |         ["Mine 5x5"      , "mine 5x5"],
117 |         ["Mine Room"     , "mine room 5 5 3"],
118 |         ["Mine Hall"     , "mine room 11 11 5"],
119 |         ["Mine Shaft"    , "mineshaft 5 10"],
120 |     ]
121 | 
122 |     def blockToIcon(self,name):
123 |         if name in self.block_icons:
124 |             return self.block_icons[name]
125 |         else:
126 |             return "grey"
127 | 
128 |     def blockToColor(self,name):
129 |         if name in self.block_icons:
130 |             l = self.block_icons[name]
131 |             if type(l) == list:
132 |                 return l[0]
133 |             else:
134 |                 return l
135 |         else:
136 |             return "grey"
137 | 
138 |     def perror(self, message):
139 |         self.logFrame.log(f'*** error: {message}')
140 | 
141 |     def pexception(self, message,e):
142 |         self.logFrame.log(f'*** exception: {message}')
143 |         if self.debug_lvl >= 4:
144 |             self.logFrame.log(str(e))
145 |         else:
146 |             with open("exception.debug", "w") as f:
147 |                 f.write("PyBit Minecraft Bot - Exception Dump")
148 |                 f.write(str(e))
149 |                 f.write("")
150 |         self.lastException = e
151 | 
152 |     def pinfo(self, message):
153 |         if self.debug_lvl > 0:
154 |             self.logFrame.log(message)
155 | 
156 |     def pdebug(self,message,lvl=4,end=""):
157 |         if self.debug_lvl >= lvl:
158 |             self.logFrame.log(message)
159 | 
160 |     def uiInventory(self, items):
161 |         for widget in self.invUI.winfo_children():
162 |             widget.destroy()
163 | 
164 |         if len(items) > 0:
165 |             for i in items:
166 |                 if i not in self.inv_icons:
167 |                     ttk.Label(self.invUI, text = f'{items[i]:>3} x {i}', width=25, anchor="w").pack(side=tk.TOP, anchor="w", padx=5)
168 |             ttk.Separator(self.invUI).pack(side=tk.TOP, padx=10, pady=5, fill="x")
169 |             for i in items:
170 |                 if i in self.inv_icons:
171 |                     label = self.inv_icons[i]
172 |                     ttk.Label(self.invUI, text = f'{items[i]:>3} x {label}{i}', width=27, anchor="w").pack(side=tk.TOP, anchor="w", padx=5)
173 |         else:
174 |             tk.Label(self.invUI, text = f'    Inventory is Empty', width=27, anchor="w").pack(side=tk.TOP, anchor="w", padx=5)
175 | 
176 |     def uiStatus(self, health, food, oxygen):
177 |         for widget in self.statusUI.winfo_children():
178 |             widget.destroy()
179 | 
180 |         if oxygen > 18:
181 |             oxygen = 20
182 | 
183 |         fg_c, bg_c = botlib.colorHelper(health,20)
184 |         h = tk.Label(self.statusUI, text = f'{int(100*health/20):>3}%  Health', background=bg_c, foreground=fg_c, width=130)
185 |         h.pack(side=tk.TOP, anchor="w", padx=5, pady=1 )
186 | 
187 |         fg_c, bg_c = botlib.colorHelper(food,20)
188 |         f = tk.Label(self.statusUI, text = f'{int(100*food/20):>3}%  Food', background=bg_c, foreground=fg_c,  width=130)
189 |         f.pack(side=tk.TOP, anchor="w", padx=5, pady=1)
190 | 
191 |         fg_c, bg_c = botlib.colorHelper(oxygen,20)
192 |         o = tk.Label(self.statusUI, text = f'{int(100*oxygen/20):>3}%  Oxygen', background=bg_c, foreground=fg_c,  width=130)
193 |         o.pack(side=tk.TOP, anchor="w", padx=5, pady=1)
194 | 
195 |     def uiMap(self, blocks):
196 |         self.map.delete("all")
197 |         y = 0
198 |         for x in range(0,13):
199 |             for z in range(0,13):
200 |                 n = self.blockToIcon(blocks[y][x][z])
201 |                 if n:
202 |                     if type(n) != list:
203 |                         self.map.create_rectangle(10+x*14,10+z*14, 10+x*14+14, 10+z*14+14, fill=n)
204 |                     else:
205 |                         self.map.create_text(10+x*14+7,10+z*14+7, text=n[1])                        
206 |         self.map.create_text(100, 100, text='🤖')
207 | 
208 |     def uiEquipment(self,item):
209 |         if item in self.hand_icons:
210 |             item = f'✋:  {self.hand_icons[item]} {item}'
211 |         self.mainHandLabel.configure(text=item)
212 | 
213 |     def refreshMap(self):
214 |         p = self.bot.entity.position
215 | 
216 |         blocks = []
217 |         for x in range(0,13):
218 |             new = []
219 |             for z in range(0,13):
220 |                 new.append(0)
221 |             blocks.append(new)
222 | 
223 |         for x in range(0,13):
224 |             for z in range(0,13):
225 |                 v = Vec3(p.x+x-6,p.y+0.3,p.z+z-6)
226 |                 n = self.bot.blockAt(v).displayName
227 |                 blocks[x][z] = n
228 | 
229 |         self.uiMap([blocks])
230 | 
231 |     def refreshWorldStatus(self):
232 | 
233 |         t = self.bot.time.timeOfDay
234 |         h = (int(t/1000)+6) % 24
235 |         m = int( 60*(t % 1000)/1000)
236 |         time_str = f'{h:02}:{m:02}'
237 |         p = self.bot.entity.position
238 |         pos_str = f'x: {int(p.x)}   y: {int(p.y)}   z: {int(p.z)}'
239 |         if self.bot.time.isDay:
240 |             self.timeLabel.configure(text=f'  Time: 🌞 {time_str}', background="light grey", foreground="black")
241 |         else:
242 |             self.timeLabel.configure(text=f'  Time: 🌙 {time_str}', background="dark blue", foreground="white")
243 | 
244 |         self.placeLabel.configure(text=f'  🧭  {pos_str}')
245 | 
246 |         self.connLabel.configure(text=f'  🌐 {self.account["host"]}   {self.bot.player.ping} ms')
247 | 
248 |         #tk.Label(self.equipUI, text = f'    Hand: {hand}').pack(side=tk.TOP, anchor="w", padx=5)
249 | 
250 |     def refreshInventory(self):
251 |         inventory = self.bot.inventory.items()
252 |         iList = {}
253 |         if inventory != []:
254 |             for i in inventory:
255 |                 iname = i.displayName
256 |                 if iname not in iList:
257 |                     iList[iname] = 0
258 |                 iList[iname] += i.count
259 |         self.uiInventory(iList)
260 | 
261 |     def refreshEquipment(self):
262 |         i_type, item = self.itemInHand()
263 |         self.uiEquipment(item)
264 |         pass
265 | 
266 |     def refreshStatus(self):
267 |         o = self.bot.oxygenLevel
268 |         if not o:
269 |             o = 100
270 |         self.uiStatus(self.bot.health, self.bot.food, o)
271 |         pass
272 | 
273 |     def refreshActivity(self, txt):            
274 |         if self.activity_major == False:
275 |             status = f' ({self.activity_last_duration})'
276 |         elif self.stopActivity:
277 |             status = "🛑 Stop"
278 |         else:
279 |             status = str(datetime.timedelta(seconds=int(time.time()-self.activity_start)))
280 |         self.activityTitleLabel.configure(text=f'{self.activity_name} {status}')
281 | 
282 |         if txt:
283 |             if isinstance(txt,str):
284 |                 lines = [txt]
285 |             elif isinstance(txt,list):
286 |                 lines = txt
287 |             else:
288 |                 return
289 |             while len(lines) < 6:
290 |                 lines.append("")
291 |             for i in range(0,6):
292 |                 self.activityLine[i].configure(text=lines[i])
293 | 
294 |     def bossPlayer(self):
295 |         return self.bossNameVar.get()
296 | 
297 |     def refresherJob(self):
298 |         while True:
299 |             self.refreshActivity(None)
300 |             self.refreshWorldStatus()
301 |             self.refreshStatus()
302 |             self.refreshInventory()
303 |             self.refreshMap()
304 |             time.sleep(1)
305 | 
306 |     def do_command(self,cmd):
307 |         if cmd != "stop":
308 |             if self.activity_major == True:
309 |                 return False
310 |         self.handleCommand(cmd, self.bossPlayer())
311 | 
312 |     def initUI(self):
313 |         win = tk.Tk()
314 |         self.win = win
315 |         win.title("PyBot - The friendly Minecraft Bot")
316 |         win.geometry("680x800")
317 |         win.resizable(False, False)
318 | 
319 |         #  0 --------------------------------------------------------------------------------
320 | 
321 |         self.worldUI = ttk.LabelFrame(win, text='World Status')
322 |         self.worldUI.place(x=20, y=10, width=200, height=100)
323 | 
324 |         self.timeLabel = tk.Label(self.worldUI, text = f'  🌞 00:00', width=130)
325 |         self.timeLabel.pack(side=tk.TOP, anchor="w", padx=5)
326 | 
327 |         self.placeLabel = ttk.Label(self.worldUI, text = f'  Location TBD')
328 |         self.placeLabel.pack(side=tk.TOP, anchor="w", padx=5, pady=2)
329 | 
330 |         self.connLabel = ttk.Label(self.worldUI, text = f'  Not Connected')
331 |         self.connLabel.pack(side=tk.TOP, anchor="w", padx=5, pady=2)
332 | 
333 | 
334 |         # -
335 | 
336 |         self.statusUI = ttk.LabelFrame(win, text='Player Status')
337 |         self.statusUI.place(x=20, y=120, width=200, height=100)
338 | 
339 |         # -
340 | 
341 |         self.equipmentUI = ttk.LabelFrame(win, text='Equipment')
342 |         self.equipmentUI.place(x=20, y=230, width=200, height=180)
343 | 
344 |         self.mainHandLabel = ttk.Label(self.equipmentUI, text = f'Main Hand: empty')
345 |         self.mainHandLabel.pack(side=tk.TOP, anchor="w", padx=5)
346 | 
347 |         self.armorLine = [None,None,None,None,None,None]
348 |         for i in range(0,4):
349 |             self.armorLine[i] = ttk.Label(self.equipmentUI, text = f'')
350 |             self.armorLine[i].pack(side=tk.TOP, anchor="w", padx=5)
351 | 
352 |         # -----------
353 | 
354 |         self.areaUI = tk.Frame(win)
355 |         self.areaUI.place(x=240, y=10, width=200, height=200)
356 | 
357 |         #ttk.Label(self.areaUI, text='Area Map').pack(side=tk.TOP,anchor="w")
358 | 
359 |         self.map = tk.Canvas(self.areaUI, bg="#222", height=200, width=200)
360 |         self.map.pack(side=tk.TOP)
361 |         
362 |         self.activityUI = ttk.LabelFrame(win, text='Activity')
363 |         self.activityUI.place(x=240, y=230, width=200, height=180)
364 | 
365 |         self.activityTitleLabel = ttk.Label(self.activityUI, text = f'No Activity')
366 |         self.activityTitleLabel.pack(side=tk.TOP, anchor="w", padx=5)
367 | 
368 |         self.activityLine = [None,None,None,None,None,None]
369 |         for i in range(0,6):
370 |             self.activityLine[i] = ttk.Label(self.activityUI, text = f'')
371 |             self.activityLine[i].pack(side=tk.TOP, anchor="w", padx=5)
372 | 
373 |         # -----------
374 | 
375 |         self.invUI = ttk.LabelFrame(win,text='Inventory')
376 |         self.invUI.place(x=460, y=10, width=200, height=400)
377 | 
378 |         # 10 --------------------------------------------------------------------------------
379 | 
380 |         ttk.Separator(win,orient='horizontal').place(x=0, y=430, width=680)
381 | 
382 |         self.commandUI = ttk.Frame(win)
383 |         self.commandUI.place(x=10,y=440,width=660,height=100)
384 | 
385 |         self.commandButton = []
386 |         but_i = 0
387 |         for r in range(0,2):
388 |             self.commandButton.append(None)
389 |             self.commandButton[r] = []
390 |             for c in range(0,6):
391 |                 self.commandUI.grid_columnconfigure(c, weight=1)
392 |                 self.commandButton[r].append(None)
393 |                 txt = self.button_mapping[but_i][0]
394 |                 f = partial(self.do_command,self.button_mapping[but_i][1])
395 |                 self.commandButton[r][c] = ttk.Button(self.commandUI, text=txt, command=f)
396 |                 self.commandButton[r][c].grid(row=r, column=c, sticky="we")
397 |                 but_i += 1
398 | 
399 |         self.cmdFrame = ttk.Frame(self.commandUI)
400 |         self.cmdFrame.grid(row=10, column=0, columnspan=30, sticky="we")
401 | 
402 |         self.botCmd = tk.StringVar()
403 |         ttk.Label(self.cmdFrame, text="Command:").grid(row=1, column=0, sticky="W")
404 |         self.cmdEntry = ttk.Entry(self.cmdFrame, width=25, textvariable=self.botCmd)
405 |         self.cmdEntry.grid(row=1, column=1, sticky="EW")
406 |         ttk.Button(self.cmdFrame, text="Do it!", command=self.do_command).grid(row=1, column=2, sticky="W")
407 | 
408 |         self.bossNameVar = tk.StringVar()
409 |         ttk.Label(self.cmdFrame, text="Boss:").grid(row=1, column=4,  sticky="W")
410 |         self.bossName = ttk.Entry(self.cmdFrame, width=13, textvariable=self.bossNameVar)
411 |         self.bossName.grid(row=1, column=5, sticky="EW")
412 |         self.cmdFrame.grid_columnconfigure(3, weight=1)
413 | 
414 |         if hasattr(self,'account'):
415 |             self.bossNameVar.set(self.account["master"])        
416 | 
417 |         # 20 --------------------------------------------------------------------------------
418 |         
419 |         ttk.Separator(win,orient='horizontal').place(x=0, y=550, width=680)
420 | 
421 |         ttk.Label(win, text="Activity Log").place( x=20, y=560)
422 |         self.logFrame = LogFrame(win)
423 |         self.logFrame.place(x=0, y=580, width=680, height=220)
424 | 
425 |     def mainloop(self):
426 |         @AsyncTask(start=True)
427 |         def doRefresher(task):
428 |             self.refresherJob()
429 | 
430 |         self.win.mainloop()
431 | 
432 |     def __init__(self, account):
433 |         super().__init__(account)
434 |         self.initUI()
435 | 
436 | if __name__ == "__main__":
437 |     # Run in test mode
438 |     print("UI Test - Part of PyBot, the friendly Minecraft Bot.")
439 |     pybot = PyBotWithUI.__new__(PyBotWithUI)
440 |     pybot.initUI()
441 | 
442 |     items = MineBot.miningEquipList
443 | 
444 |     pybot.uiInventory(items)
445 | 
446 |     pybot.uiStatus(20,15,10)
447 | 
448 |     blocks = [ [ ["grey"]*13 ] *13 ]
449 |     blocks[0][6][5] = "Air"
450 |     blocks[0][6][6] = "Air"
451 |     blocks[0][6][7] = "Air"
452 | 
453 |     pybot.uiMap(blocks)
454 |     pybot.uiEquipment("Stone Pickaxe")
455 |     pybot.refreshActivity(["Test1", "Test2", "Test3"])
456 | 
457 |     a = 1
458 |     while True:
459 |         pybot.logFrame.log(f'{a} test and {a}*{a} = {a*a}')
460 |         pybot.win.update_idletasks()
461 |         pybot.win.update()
462 |         a += 1
463 |         time.sleep(.1)
464 | 
465 |     time.sleep(5)
466 | 
467 |     pybot.win.mainloop()


--------------------------------------------------------------------------------
/workarea.py:
--------------------------------------------------------------------------------
  1 | #
  2 | # Definition of a work area to do stuff in (e.g. build, mine etc.)
  3 | # Main purpose is to handle relative to absolute coordinates
  4 | #
  5 | 
  6 | from botlib import *
  7 | 
  8 | # Area in front of chest+torch
  9 | #   x is lateral (torch is 0)
 10 | #   z is depth (torch is at -1)
 11 | #   y is height (chest is at 0)
 12 | #
 13 | #   NOTE: This means this is a LEFT HANDED coordinate system while
 14 | #         Minecraft uses a RIGHT HANDED coordinate system. Yes, I know.
 15 | #         It still makes more sense this way.
 16 | 
 17 | class workArea:
 18 | 
 19 |     #
 20 |     # Initialize a work area
 21 |     #
 22 | 
 23 |     valuables = None
 24 |     status = "all good"
 25 |     blocks_mined = 0
 26 |     last_break = 0
 27 |     break_interval = 100
 28 | 
 29 |     def __init__(self,pybot,width,height,depth, notorch=False):
 30 |         self.valid = False
 31 |         self.pybot = pybot
 32 | 
 33 |         if width % 2 != 1:
 34 |             self.pybot.perror(f'Error: width={width} but only odd width work areas are supported.')
 35 |             return None
 36 | 
 37 |         self.width = width
 38 |         self.width2 = int((width-1)/2)
 39 |         self.height = height
 40 |         self.depth = depth
 41 | 
 42 | 
 43 |         self.start_chest = pybot.findClosestBlock("Chest",xz_radius=3,y_radius=1)
 44 | 
 45 |         if not self.start_chest:
 46 |             self.pybot.chat("Can't find starting position. Place a chest on the ground to mark it.")
 47 |             return None
 48 | 
 49 |         if notorch:
 50 |             # Area with arbitrary direction, we pick point in front of chest
 51 |             p = self.start_chest.getProperties()
 52 |             self.d = strDirection(p["facing"])
 53 |             self.start = addVec3(self.start_chest.position,self.d)
 54 | 
 55 |             # Origin
 56 |             self.origin = self.start
 57 | 
 58 |         else:
 59 |             # Determine "forward" direction from chest+torch
 60 |             torch   = pybot.findClosestBlock("Torch",xz_radius=3,y_radius=1)
 61 |             r_torch = pybot.findClosestBlock("Redstone Torch",xz_radius=3,y_radius=1)
 62 | 
 63 |             # Redstone Torch has precedence
 64 |             if r_torch:
 65 |                 self.start_torch = r_torch
 66 |             else:
 67 |                 self.start_torch = torch
 68 | 
 69 |             if not self.start_torch:
 70 |                 self.pybot.chat("Can't find starting position. Place chest, and torch on the ground next to it to mark the direction.")
 71 |                 return None
 72 | 
 73 |             if self.start_torch.position.y != self.start_chest.position.y:
 74 |                 self.pybot.chat("Can't find starting position. Chest and torch at different levels??")
 75 |                 return None
 76 | 
 77 |             # Direction of the Area
 78 |             self.d = subVec3(self.start_torch.position, self.start_chest.position)
 79 |             if lenVec3(self.d) != 1:
 80 |                 self.pybot.chat("Can't find starting position. Torch is not next to chest.")
 81 |                 return None
 82 | 
 83 |             self.start = self.start_chest.position
 84 | 
 85 |             # Origin
 86 |             self.origin = Vec3(self.start.x+2*self.d.x,self.start.y,self.start.z+2*self.d.z)
 87 | 
 88 |         # Vector directions
 89 |         self.forwardVector = self.d
 90 |         self.backwardVector = invVec3(self.d)
 91 | 
 92 |         # Note that we flip build area vs. world coordinates. Left Handed vs Right handed.
 93 |         self.leftVector = rotateLeft(self.d)
 94 |         self.rightVector = rotateRight(self.d)
 95 | 
 96 |         self.latx = self.rightVector.x
 97 |         self.latz = self.rightVector.z
 98 | 
 99 |         # Done. Set flag.
100 |         self.valid = True
101 | 
102 |     def xRange(self):
103 |         return range(-self.width2, self.width2+1)
104 | 
105 |     def yRange(self):
106 |         return range(0,self.height)
107 | 
108 |     def zRange(self):
109 |         return range(0,self.depth)
110 | 
111 | 
112 |     def toWorld(self,x,y,z):
113 |         return Vec3(self.origin.x+self.latx*x+self.d.x*z,
114 |                     self.origin.y+y,
115 |                     self.origin.z+self.latz*x+self.d.z*z)
116 | 
117 |     # Convert position relative to absolute coordinates
118 | 
119 |     def toWorldV3(self,v):
120 |         return Vec3(self.origin.x+self.latx*v.x+self.d.x*v.z,
121 |                     self.origin.y+v.y,
122 |                     self.origin.z+self.latz*v.x+self.d.z*v.z)
123 | 
124 | 
125 |     # Convert direction relative to absolute coordinates
126 | 
127 |     def dirToWorldV3(self,v):
128 |         return Vec3(self.latx*v.x+self.d.x*v.z,
129 |                     v.y,
130 |                     self.latz*v.x+self.d.z*v.z)
131 | 
132 |     # Minecraft block at relative coordinates
133 | 
134 |     def blockAt(self,*argv):
135 |         if len(argv) == 3:
136 |             return self.pybot.bot.blockAt(self.toWorld(argv[0],argv[1],argv[2]))
137 |         else:
138 |             return self.pybot.bot.blockAt(self.toWorldV3(argv[0]))
139 | 
140 |     # Returns a list of all blocks in the workArea
141 | 
142 |     def allBlocks(self):
143 |         blocks = []
144 | 
145 |         for z in self.zRange():
146 |             for y in self.yRange():
147 |                 for x in self.xRange():
148 |                     blocks.append(Vec3(x,y,z))
149 |         return blocks
150 | 
151 |     # Returns a list of all blocks in the workArea
152 | 
153 |     def allBlocksWorld(self):
154 |         blocks = []
155 | 
156 |         for z in self.zRange():
157 |             for y in self.yRange():
158 |                 for x in self.xRange():
159 |                     blocks.append(self.toVec3(x,y,z))
160 |         return blocks
161 | 
162 |     # Convert position relative to absolute coordinates
163 | 
164 |     def walkTo(self, *argv):
165 |         if len(argv) == 3:
166 |             v = self.toWorld(argv[0],argv[1],argv[2])
167 |         else:
168 |             v = self.toWorldV3(argv[0])
169 |         self.pybot.walkTo(v)
170 | 
171 |     def walkToBlock(self, *argv):
172 |         if len(argv) == 3:
173 |             v = self.toWorld(argv[0],argv[1],argv[2])
174 |         else:
175 |             v = self.toWorldV3(argv[0])
176 |         self.pybot.walkToBlock(v)
177 | 
178 |     # More precise version (0.3 blocks)
179 | 
180 |     def walkToBlock3(self, *argv):
181 |         if len(argv) == 3:
182 |             v = self.toWorld(argv[0],argv[1],argv[2])
183 |         else:
184 |             v = self.toWorldV3(argv[0])
185 |         self.pybot.walkToBlock3(v)
186 | 
187 | 
188 |     # String area direction as North, South etc.
189 | 
190 |     def directionStr(self):
191 |         return directionStr(self.d)
192 | 
193 |     # Walk back to Torch
194 | 
195 |     def walkToStart(self):
196 |         self.pybot.walkToBlock3(self.start)        
197 | 
198 |     # Restock from Chest
199 | 
200 |     def restock(self, item_list):
201 |         self.walkToStart()
202 |         self.pybot.restockFromChest(item_list)
203 |         self.pybot.eatFood()
204 | 
205 | 


--------------------------------------------------------------------------------