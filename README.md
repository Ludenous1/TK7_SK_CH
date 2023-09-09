# TK7_SK_CH

Blender addon to speed up the process of modding rigged characters into Tekken 7. 

## Contents
1. [Credits](#credits)
2. [Compatibility](#compatibility)
3. [Installation](#installation)
4. [Update](#update)
5. [Quick Tools](#quick_tools)
6. [Vertex Group Merger](#vertex_group_merger)
7. [Skeleton Generator](#skeleton_generator)
8. [Pose Snapper](#pose_snapper)
9. [T_poser](#t_poser)
10. [Bone Renamer](#boner_renamer)
11. [Skeleton Simplifier](#skeleton_simplifier)
12. [Usage demonstation](#demo)
---

<a name="credits"></a>
## Credits
I owe a lot to the following members of the Tekken modding community who provided their code and/or info which shaped the addon you see before you:
* [**Dennis**](https://github.com/DennisStanistan)
* [**Reborn**](https://github.com/CDDTreborn)
* **Saiki**
* **Ressen**
* **Stoner_037**
 
I also owe a a lot to the following members from the Blender development community:
* [**Etherlord**](https://etherlord.gumroad.com/)
* MercyMoon
* Vik


If you happen to run into any inconveniences while using the addon, you have [my thick-headedness](https://github.com/Ludenous1) to thank for that[^1]. 

---

<a name="compatibility"></a>
## Compatibility
| Blender version | 2.91 | 2.93 | 3.0 |  3.1 | 3.2 | 3.3 | 3.5 |3.6 |
| ------------- | ------------- | ------------- | ------------- |------------- |------------- |------------- |------------- |------------- |
| Compatible | :negative_squared_cross_mark:| :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |


---

<a name="installation"></a>
## Installation
1. Download the latest release from GitHub [here](https://github.com/Ludenous1/TK7_SK_CH/releases).
2. In Blender, open the Preferences window (Edit>Preferences) and select the Add-ons tab.
3. Press the 'Install...' button and select the .zip file you downloaded.
4. Enable the add-on and save preferences if you want it to always be available.

---
<a name="update"></a>
### Update
1. Save current Blender file.
2. Open the Preferences window in Blender (Edit>Preferences) and select the Add-ons tab.
3. Search for the addon by typing 'TK7_SK_CH' on the search box.
4. Expand the addon's preferences.
5. Click on 'Check now for tk7_sk_ch update'.
   
![AddonUpdater](https://github.com/Ludenous1/TK7_SK_CH/assets/99399209/7bdc4929-0daf-401b-97d5-2530fa87673f)

---
<a name="quick_tools"></a>
### Quick Tools
These include some tools that are commonly used throughout the modding process.

![image](https://user-images.githubusercontent.com/99399209/190008787-be57df7e-77ee-4171-8b4e-743b48b9d15a.png)

<details>
  <summary>Details</summary>
  
+ `Scene setup`: Adjusts the scene units based on the info Dennis provided on the original [custom mesh import guide](https://tekkenmods.com/guide/51/importing-custom-meshes-to-tekken-7-using-blender). 
+ `FBX Export`: Exports an active armature with the appropriate export settings for Tekken7 as long as the blend file is saved and there's only one armature on the scene.
+ `Merge bones to`: Merges the weights of the bones to each bones' `parents` or to the `active` bone (the last selected bone). The bones need to be selected in edit mode.
+ `Apply Pose`: Applies the pose of the active armature. 
+ `Fix bones`: Copies the bone properties in edit mode from a selected reference armature onto the last selected armature.
+ `Disable hierarchy`: Temporarily disables the bone hierarchy for the active armature allowing isolated movement / adjustment of bones in pose mode.
 

</details>


---
<a name="vertex_group_merger"></a>
### Vertex Group Merger
Merges the vertex groups for the the active mesh. It is the UI implementation of Stoner_037's Vertex Group Merging script.
 
![Blender-D-FIles-Projects-Blender](https://github.com/Ludenous1/TK7_SK_CH/assets/99399209/cb161c95-9a64-4e39-93b7-3105152c8c3f)


  <details>
  <summary>Details</summary>
  
  ![VertexGroupMerger](https://github.com/Ludenous1/TK7_SK_CH/assets/99399209/027879a1-eeee-4262-8619-dd29f34e6b4b)

   What it does:
   + Merges the vertex groups for an active mesh. 
   + If the new vertex group's name already exists, it'll create a new group with a similar name unless the old one was removed.


   Options:
   + - [x] **Remove merged vertex groups**:  Removes all the vertex groups that were merged and only keeps the one with the new name.


  Conditions for proper activation:
  + Object mode or Edit mode
</details>


---
<a name="skeleton_generator"></a>
### Skeleton Generator
Generate skeletons for Tekken characters without any meshes. Credit to Saiki (and by extension to Ressen) for the [bone roll fix guide](https://tekkenmods.com/guide/42/fix-bone-roll-issue-without-3ds-max-for-rigging-updated) which helped lead to the development of this module.
 
![Sk_gen](https://user-images.githubusercontent.com/99399209/188280510-d6884bc1-e1f6-496b-94b7-e8743fd81711.gif)


  <details>
  <summary>Details</summary>
  
  ![image](https://user-images.githubusercontent.com/99399209/188228602-94363f1f-8538-4151-913e-09d6573976ca.png)
  
   What it does:
   + Generates the skeletons for the Tekken 7 cast including Noctis and Geese. 
   + The bones in the generated skeleton have the correct roll and are in the correct position (I've tested it on about 13 characters).
   + It only generates the skeletons for the characters selected without any meshes.


   Options:
   + `Char`: The abreviation for the character you want to generate the skeleton of (Set to `aki` or Armor King by default).
   + `Type`: Specifies the type of skeleton generated whether it's in `glTF` or `PSK` format (Set to `glTF` by default).
   + `Bones included`: Specifies what bones to include in the generated skeleton. `All bones` generates all staple bones within a character's skeleton while `Main bones only` just generates the bones that don't have "offset" or "null" in their name (Set to `All bones` by default).


  Conditions for proper activation:
  + Object mode



</details>

---
<a name="pose_snapper"></a>
### Pose Snapper
Moves the bones of the active armature (last selected) to the positions of the bones of the other selected armature according to the name of the bone. 
 
 
![PoseSnapper](https://user-images.githubusercontent.com/99399209/188280485-e8303403-6532-4200-bb5a-4fafcbf9e09d.gif)
 

 
  <details>
  <summary>Details</summary>
  
  ![image](https://user-images.githubusercontent.com/99399209/188228550-4b498802-29fa-4ab8-a8d9-7e95b75fb20c.png)
  
   What it does:
   + Moves bones with matching names in pose mode to their corresponding position on the other selected armature.
   + Doesn't change the rotation of the bones, just their position.

   
   Options:
   + - [x] **Autoscale**: Scales the entire skeleton so that the 'Spine1' bones in both skeletons line up (Optional).
   + `Simple`: Moves individual bones locations in pose mode so bones with identical names between the 2 selected skeleton line up.
   + `Advanced`: Moves and scales individual bones in pose mode so bones with identical names between the 2 selected skeleton line up (Experimental).


  Conditions for proper activation:
  + Object mode or pose mode.
  + Applied when exactly 2 armatures are selected and the adjustments will be applied to the one selected last.
  + Most of the main Tekken 7 bones need to be present and following the same naming convention as Tekken 7 (Only required if *Autoscale* or `advanced` mode is set)
  + All the viewport transfroms should be applied on the skeleton (Ctrl + A ---> All tranforms) as well as the pose (i.e. pose needs to be applied too). 



</details>



---
<a name="t_poser"></a>
### T_poser
Puts the armature into T pose as long as the name of the bones matches up with the Tekken 7 bone names. Most of the main Tekken 7 bones need to be on the skeleton to avoid any errors.

![Tposer](https://user-images.githubusercontent.com/99399209/188280453-fd3c1dfc-930a-4846-aaa4-749f2d9dc532.gif)
 

 
 <details>
  <summary>Details</summary>
  
  ![image](https://user-images.githubusercontent.com/99399209/198875887-e7723dc0-53b8-4193-ad40-29d50a0c60b7.png)
  
   What it does:
   + T-poses most of the main bones in a skeleton as long as the bone names follow Tekken 7's naming convetion (except for the head bone).

   Options:
   + - [x] **connect main bones**: Connects the limb bones together in edit mode to make the skeleton ready for T posing (Optional, On by default).
   + - [ ] **Fix finger tips**: Rotates the finger tip bones so that they're pointing in the direction of the mesh they control (Optional, Off by default).
   + - [ ] **Apply to spine bones**: Attemps to make the spine bones line up vertically in pose mode (Optional, Off by default).

  Conditions for proper activation:
  + Object mode or pose mode.
  + Applied on a single active armature on the viewport.
  + Most of the main Tekken 7 bones need to be present and following the same naming convention as Tekken 7 (Hand bones, spine bones, limb bones, and Neck).
  + All the viewport transfroms should be applied on the skeleton (Ctrl + A ---> All tranforms) as well as the pose (i.e. pose needs to be applied too).
  + The bones need to be already in the correct position so that the T-poser can rotate them properly.



</details>

---

<a name="boner_renamer"></a>
### Bone_Renamer
Renames the bones for the active skeleton according to the current selected preset list. It is a UI implementation of Reborn's original bone renamer script. There are several presets already added on the renamer thanks to Reborn, Ressen, and WTails358.

![BoneRenamer](https://user-images.githubusercontent.com/99399209/188280431-c323d60a-8c8a-4529-ac34-47806fc8ce36.gif)




<details>
  <summary>Details</summary>
  
  ![image](https://user-images.githubusercontent.com/99399209/190012511-8fcbf0b8-a24b-4fbe-8ca5-6ae5754cfce9.png)
  
   What it does:
   + Renames the bones of an active armature.
   + Stores renaming lists as presets for later use.
   + Allows modifying the renaming list through the UI.
   
   Options:
   + ![image](https://user-images.githubusercontent.com/99399209/197341581-9fd7be25-c5d5-47dd-ab80-22fccc1482cf.png)
`Auto bone matching`: Autofills the selected list based on detected matching bones (Optional and Experimental. It only works for custom skeleton structures with certain features[^2]).
   + - [ ] **Merge bones with same / similar names**:  Merges bone weights for the bones that end up with the a same or similar name. The parent would be the first renamed bone if the new bone names are identical. If the new bone name is the same as that of an existing bone, the bone weights are still going to get merged even if they're aren't both shown on the list (Optional, Off by default)

  Conditions for proper activation:
  + Object mode or edit mode.
  + Applied on a single active armature on the viewport.
  + All the viewport transfroms should be applied on the skeleton (Ctrl + A ---> All tranforms) as well as the pose for the *Auto bone matching* to function properly.
</details>

---

<a name="skeleton_simplifier"></a>
### Skeleton Simplifier
Merges the weights of bones with certain names onto their parents and cleans up materials. Credit to Reborn for the code to change the alpha blend mode on the materials to *Hashed* (XPS checkmark). The simplification process might take time to complete. 

![SK_Simp](https://user-images.githubusercontent.com/99399209/188280415-2795bca8-f86d-48d0-8497-6449ca6a575b.gif)

<details>
  <summary>Details</summary>
  
  ![image](https://user-images.githubusercontent.com/99399209/198875863-e7423e48-835f-40f7-ab7d-a54b1686495e.png)
  
   What it does:
  + Merges all bones weights that have the keywords listed in their names (ex: "ctr", "null", "offset",  ...) to thier parents (or ancestors).
  + Connects the main bones in the skeleton (such as the spine bones, limb bones, etc). 
  + Removes duplicate materials with different names but the exact same shader properties (material slot clean up).
  + Changes the blend mode for all materials to *Hashed*
  
  Options:
  +  - [x] **connect main bones**: Connect the main limb bones and the spine bones in edit mode (Optional, On by default).
  +  - [x] **remove bones**: Remove all the bones that contain listed keywords (ex: "ctr", "null", "offset",  ...) in their name from the skeleton after they've got merged (Optional, On by default).
  + - [ ] **Join meshes**: Joins the children meshes or separates them according to the materials (Optional, Off by default so it will separate them according to the material slots if left unchecked)
  + - [x] **XPS**: Changes the alpha blend mode settings on every material on all the meshes attached to the skeleton to *Hashed* (Optional, On by default).
  

  Conditions for proper activation:
  + Object mode or Edit mode.
  + Applied on a single active armature on the viewport.
  + All the viewport transfroms should be applied on the skeleton prior (Ctrl + A ---> All tranforms)
  + Children meshes of the armature should all be visible on the viewport.


</details>

---
<a name="demo"></a>
### Usage Demonstration

[![image](https://user-images.githubusercontent.com/99399209/192145961-e3c3dff3-e64b-4959-81e9-6c0d3e0c0e39.png)](https://www.youtube.com/watch?v=kA3ey4t1XMg)


 - - - -


[^1]: Most of these individuals were ordered according to when their code got fully implemented or when usage permission was granted.
[^2]: The skeletons must have 2 spine bones and one hip bone, the hand bones should be the furthest on the x axis, the feet bones should be the lowest bones and above the world origin, and there should be only 2 bones in chain moving from the shoulders to the hands as well as moving from the hip to the feet (a regular biped rig). 
