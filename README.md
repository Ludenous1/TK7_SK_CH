# TK7_SK_CH
This Blender addon is meant to speed up the process of modding characters particularly for Tekken 7. It has a set of modules that would modify a custom skeleton[^1] and its mesh to make it ready for Tekken quickly.

 - - - -

# Credits
I've stood on the shoulders of these giants from the Tekken modding community while making this addon: Dennis, Reborn, Saiki, and  Ressen. Without the information and / or code they've provided, so many features would've been missing. Of course, and it goes without saying but without the folks at the modding discord, I wouldn't have known Tekken's dirty little modding secrets. 

Also, I owe a huge debt of gratitude to the Blender pythonites who helped me understand how to properly define / use custom blender properties and more. Not to mention the countless amounts of code I've stolen from them. Especially from Etherlord, MercyMoon, and Vik.

 - - - -

# Compatibility

| Blender version | 2.91 | 2.93 | 3.0 |  3.1 | 3.2 | 3.3 |
| ------------- | ------------- | ------------- | ------------- |------------- |------------- |------------- |
| Compatible | :negative_squared_cross_mark:| :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

Versions not listed on the table were not tested yet.
For the ones tested, I've used 2.91.2, 2.93.4 , 3.0.1 , 3.1.0, 3.2.2, and 3.3.0.


 - - - -

# Installation
Download the `code` as a zip file and place it in a directory of your choice.
Now open up Blender and navigate to Edit->Preferences->Addons. Click on Install, select the downloaded zip file, and make sure the box that says "object: TK7_SK_CH" is checked.

![image](https://user-images.githubusercontent.com/99399209/188270597-d74265dd-91db-456d-bf8c-590856f3e4a3.png)


:exclamation: Warning: If you have multiple instances of this addon installed on the same Blender version, some of the addon features will not work. Particularly, the Skeleton Generator and the Bone Renamer modules won't work.


# Update:
If this is your first time installing the addon skip this (update) section. But if you've already installed the addon before, you need to remove it first by heading to Edit->Preferences->Addons again and searching "TK7_SK_CK". Even if it is unchecked make sure you expand it and click on remove.

![image](https://user-images.githubusercontent.com/99399209/190016274-7aabacbf-3421-4678-92d3-e7b84cf9c025.jpg)

Once you're done. Follow the installation instructions again. Note that the version should say 0.0.1 on your end.


:exclamation: Warning: If you have multiple instances of this addon installed on the same Blender version, some of the addon features will not work. Particularly, the Skeleton Generator and the Bone Renamer modules won't work.


 - - - -
 - - - -

# Modules
Going over each module on the panel from the bottom up:
 ### Skeleton Simplifier ###
  ![image](https://user-images.githubusercontent.com/99399209/190009039-07c216a1-0d38-4d49-9402-1ed87c7006a2.png)


Simplifies the active skeleton by merging bones that have the keywords listed and cleans up the material slots for all the unhidden children meshes of that active skeleton. For those who are familiar with my very first Tekken blender script, this does the same thing just for non-Tekken skeletons too and cleans up the material slots as well. Shout out to Reborn for the extra alpha blend functionality (XPS checkmark). Depending on how complicated the model is and how many bones need to be merged, it might take some time to finish the whole process. 

![SK_Simp](https://user-images.githubusercontent.com/99399209/188280415-2795bca8-f86d-48d0-8497-6449ca6a575b.gif)

<details>
  <summary>Details</summary>
  
   What it does:
  * Merges all bones weights that have the keywords listed in their names (ex: "ctr", "null", "offset",  ...) to thier parents (or ancestors).
  * Connects the main bones in the skeleton (such as the spine bones, limb bones, etc). 
  * Removes duplicate materials with different names but the exact same shader properties (material slot clean up). 
  
  Options:
  * Keep bone orientation: tries to preserve the bones' general direction while connecting them. 
  * remove bones: removes all the bones that contain listed strings (ex: "ctr", "null", "offset",  ...) in their name from the skeleton after they've got merged (Optional).
  * Join meshes: Joins the children meshes or separate them according to the materials (Either join or separate by material slots).
  * XPS: Cleans up the alpha blend settings of your mesh (Optional).
  

  Conditions for proper activation:
  * Object mode or Edit mode.
  * Applied on a single active armature on the viewport.
  * All the viewport transfroms should be applied on the skeleton prior (Ctrl + A ---> All tranforms)
  * Children meshes of the armature should all be visible on the viewport.


</details>

 - - - -

 ### Bone Renamer ###

![image](https://user-images.githubusercontent.com/99399209/190012511-8fcbf0b8-a24b-4fbe-8ca5-6ae5754cfce9.png)

Renames the bones for the active skeleton according to the current selected preset list. For those who are familiar with Reborn's original bone renamer script, this does exactly the same thing just with the ability to merge bones, store templates, and autofill the list (last feature is still unstable and experimental). There are several presets already added on the renamer thanks to Reborn, Ressen, and WTails358.

![BoneRenamer](https://user-images.githubusercontent.com/99399209/188280431-c323d60a-8c8a-4529-ac34-47806fc8ce36.gif)


<details>
  <summary>Details</summary>
  
   What it does:
   * Renames the bones of an active armature.
   * Stores renaming lists as presets for later use.
   * Allows modifying the renaming list through the UI.
   
   Options:
   * Auto bone matching: Autofills the list based on detected matching bones (Optional, Experimental, and only works for custom skeleton structures with certain features).
   * Merge bones with same / similar weights: merges bone weights for the bones that end up with the a same or similar name (Optional). The parent would be the first renamed bone if the new bone names are identical. 

  Conditions for proper activation:
  * Object mode or edit mode.
  * Applied on a single active armature on the viewport.
  * All the viewport transfroms should be applied on the skeleton (Ctrl + A ---> All tranforms) as well as the pose for the auto-populate to function properly. 



</details>

 - - - -

 ### T-Poser ###
 ![image](https://user-images.githubusercontent.com/99399209/188228392-31d948dc-9207-40eb-a8fb-095c5b9d74ff.png)

Puts the armature into T pose as long as the name of the bones matches up with the Tekken 7 bone names. Most of the main Tekken 7 bones need to be on the skeleton to avoid any errors.
 
![Tposer](https://user-images.githubusercontent.com/99399209/188280453-fd3c1dfc-930a-4846-aaa4-749f2d9dc532.gif)

 
 <details>
  <summary>Details</summary>
  
   What it does:
   * T-poses most of the main bones in a skeleton as long as the bone names follow Tekken 7's naming convetion (except for the head bone).

   Options:
   * Fix armature: connects the limb bones together in edit mode to make the skeleton ready for T posing (Optional).
   * Fix finger tips: rotates the finger tip bones so that they're pointing in the direction of the mesh they control (Optional).
   * Apply to spine bones: Attemps to make the spine bones line up vertically in pose mode (Optional).

  Conditions for proper activation:
  * Object mode or pose mode.
  * Applied on a single active armature on the viewport.
  * Most of the main Tekken 7 bones need to be present (Hand bones, spine bones, limb bones, and Neck)
  * All the viewport transfroms should be applied on the skeleton (Ctrl + A ---> All tranforms) as well as the pose (i.e. pose needs to be applied too).
  * The bones need to be already in the correct position so that the T-poser can rotate them properly.



</details>

 - - - -
 
 
 ### Pose Snapper ###
 ![image](https://user-images.githubusercontent.com/99399209/188228550-4b498802-29fa-4ab8-a8d9-7e95b75fb20c.png)
 
 Snaps bones of the active armature (last selected) to the armature selected beforehand as long as the bone names match up. The bones need to be named according to the Tekken 7 bone naming convention.
 
![PoseSnapper](https://user-images.githubusercontent.com/99399209/188280485-e8303403-6532-4200-bb5a-4fafcbf9e09d.gif)

 
  <details>
  <summary>Details</summary>
  
   What it does:
   * Snaps bones with matching names in pose mode to their corresponding psotion on the other selected armature.
   * Moves individual bones in pose mode sp that they line up.
   
   Options:
   * Autoscale: scales the entire skeleton so that the Spine1 bones line up (Optional).
   * Simple mode: moves individual bones locations in pose mode so bones with identical names between the 2 selected skeleton line up.
   * Advanced mode: moves and scales individual bones in pose mode so bones with identical names between the 2 selected skeleton line up (Experimental).


  Conditions for proper activation:
  * Object mode or pose mode.
  * Applied when exactly 2 selected armatures are selected and the adjustments will be applied to the one selected last as long as the bone names match up.
  * Most of the main Tekken 7 bones need to be present (Hand bones, spine bones, limb bones, and Neck)
  * All the viewport transfroms should be applied on the skeleton (Ctrl + A ---> All tranforms) as well as the pose (i.e. pose needs to be applied too). 



</details>

 - - - -
  
 ### Skeleton Generator ###
 ![image](https://user-images.githubusercontent.com/99399209/188228602-94363f1f-8538-4151-913e-09d6573976ca.png)
 
 Generate skeletons that work in Tekken 7. You need to select the appropriate type of export settings depending on the type of skeleton (gLTF or PSK) you're using. Big thanks to Saiki (and by extension to Ressen) for the bone roll fix guide[^2] which helped lead to the development of this module.

![Sk_gen](https://user-images.githubusercontent.com/99399209/188280510-d6884bc1-e1f6-496b-94b7-e8743fd81711.gif)

  <details>
  <summary>Details</summary>
  
   What it does:
   * Generate the skeletons for the Tekken 7 cast that work in Tekken 7 (only the skeletons without the meshes).
   * Genrates gLTF and PSK variants of the skeletons.
   * Genrates skeleton variants that have all the bones or the main bones only (any bone that doesn't have "offset" or "null" in its name)


  Conditions for proper activation:
  * Object mode



</details>

 - - - -

 
 ### Scene setup and Quick Tools ###
 ![image](https://user-images.githubusercontent.com/99399209/190008787-be57df7e-77ee-4171-8b4e-743b48b9d15a.png)

 
These include some tools that are commonly used throughout the modding process.

<details>
  <summary>Details</summary>
  
* Scene setup: adjusts the scene units based on the info Dennis provided on the original custom mesh guide[^3]. It also changes the clip settings of the viewport.
* FBX Export: Exports an active armature with the appropriate export settings for Tekken7 as long as the blend file is saved and there's one armature in the scene.
* Merge bones to: merges the weights of the bones to each bones' parent or to the last selected bone (active bone). The bones need to selected in edit mode.
* Apply Pose: applies the pose (go figure) of the active armature. 
* Fix bones: snaps the bones of the last selected armature (active armature) to the armature selected before it in edit mode and adds bones if needed and corrects the bone hierarchy.
* Disable hierarchy: temporarily disables the bone hierarchy allowing isolated movement / adjustment of bones in pose mode.
 

</details>

 
 - - - -

# Known issues:

* The bone renamer glitches at initial load and when the last preset gets removed. The preset has to be selected again for it to properly show up. 
* Some of the modules have slow runtime before they actually get executed. An issue that doesn't seem to be salient for Blender 2.9 as it is for the newer versions.

 

 - - - -

# Update log:

* Sep-3-22: 
   * Fixed a bug related to the undo operator (ctrl + z). Now you should be able to undo what the main buttons do on the modules properly.
   * Added a line to the Skeleton Simplifier layout so it makes a little more sense.

* Sep-9-22 and Sep-10-22: 
   * Added a condition for the T-poser on the Readme. Kind of forgot to mention it earlier.
   * Clarified some details about the Pose Snapper on the Readme.
   * Added a general comment about the runtime for the Simplifier on the Readme.

* Sep-13-22: Official release of version 0.0.2
   * Added two quick tools: FBX Export and Disable hierarchy.
   * Changed the description on most of the ui buttons so that it explains what they do a bit more.
   * Changed compatibility table on the ReadMe into something more accurate.
   * Added references to the ReadMe.


[^1]: The word "skeleton" and "armature" is used interchangeably. They both mean the same thing here which is the structure that holds all the bones together in a 3D model.
[^2]: https://tekkenmods.com/guide/42/fix-bone-roll-issue-without-3ds-max-for-rigging-updated
[^3]: https://tekkenmods.com/guide/51/importing-custom-meshes-to-tekken-7-using-blender
