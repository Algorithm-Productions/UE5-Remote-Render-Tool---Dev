# MAINTENANCE

## Updating Unreal

Most of the components of the Render Farm Software will not need regular updating, however, the Unreal Engine itself
will require updates from time to time, and the Software has been built to accommodate these changes. However, before we
upgrade, we must first check if the version is compatible with the Software, in order to do so you can follow the steps
below:

1. Head to the Documentation Page for the new UE version, scroll to the Bottom of the sidebar navigation, and click on
   Unreal Python API Documentation link.
2. On the Search bar on the left, search for “MoviePipelinePythonHostExecutor” if the class exists, then you may update
   to
   the new version, otherwise you should wait until the Python API for that UE version is more stable.

3. In order to perform the proper update, you can follow the steps as indicated below:
1. Update the Unreal Engine in every Worker Machine.
    - If you do not have UE downloaded, you can get it from the Epic Games Store, which you can, in turn, download from
      here.
    - Make sure you are installing the new version of the Engine in the Default location the install wizard suggests.
2. Update the Unreal Engine in every Submitter Machine
    - If you do not have UE downloaded, you can get it from the Epic Games Store, which you can, in turn, download from
      here.
    - Make sure you are installing the new version of the Engine in the Default location the install wizard suggests.
3. Open the Git Repository, and change the “UNREAL_EXE” variable in the .env file. Push up the changes to the main
   branch.
4. Pull the new changes on every Worker & Submitter Machines, and you’ve now done it!

## Modifying the System

Modifications to the System are pretty straightforward. For the sake of my sanity, I won’t go into detail on how to
change every aspect of the codebase, however, and in an effort to standardize the change process, please follow the
steps below for any new changes:

- Install Python 3.11 from here.
- Add Python to the System’s Environmental Paths, see how here.
  You might also need to remove some App Execution Alias, see how here.
- Install GIT from here.
- Assure that your System has the Tank mapped to the X Drive.
  [JAMES ADD COMMENT AS TO HOW TO DO THIS]
  Restart your System to make sure all the above changes are fully implemented
- You can test that GIT is installed by running the “git” command on CMD.
- You can test that Python is installed by running the “python” command on CMD.
- Copy this Link.
  Navigate to the directory where you want to save the application, open CMD and run the following commands:

``` 
git clone https://github.com/Algorithm-Productions/UE5-Remote-Render-Tool---Dev.git
cd ./UE5-Remote-Render-Tool---Dev
python -m pip install -r requirements.txt
```

Make a new branch on the Github Repository, you can do this on the actual Repo Page found here.
Switch to the new Branch on your local machine.

Make whatever changes you’d like to make, testing them locally.
Commit and Push these changes to your new Branch.
Open a new Pull Request from your Branch to the Main Branch, wait for someone else to review these changes and approve
the request.
Pull the new changes on every Worker & Submitter Machines, and you’ve now done it!

## Adding Override Settings

Currently, the System support all possible settings that fall under the following Unreal Classes:

- Output Settings [unreal.MoviePipelineOutputSetting]
- AA Settings [unreal.MoviePipelineAntiAliasingSetting]
- Console Variable Settings [unreal.MoviePipelineConsoleVariableSetting]
- High Res Settings [unreal.MoviePipelineHighResSetting]

However, adding new settings should, in theory, be quite a simple process, as the Codebase is built to support easy
extension. If you require further settings, then you can follow the steps below to implement them:

1. Find the Unreal Object Class for the Setting.

- You can do so by looking through the Unreal Python API Documentation for the specific version of the Engine you are
  using.
- You can find the Unreal Python API Documentation by heading to the general Documentation Page for the specific UE
  version, scroll to the Bottom of the sidebar navigation, and click on Unreal Python API Documentation link.

2. Create a new Datatype Class under /util/datatypes/unreal_dt/...

- This class should inherit from /util/datatypes/abstracts/UnrealDataType, and so implement the “from_unreal”,
  “from_dict”, and “to_dict” methods. You may refer to the other Classes in /util/datatypes/unreal_dt/... for examples
  regarding how these methods should be implemented.
- Although not a hard requirement, it would be ideal that the new Object Class has all of the properties that the Unreal
  Class it refers to also has.

3. Create a new Override Map Class under /util/datatypes/overrides/…
   - This class should inherit from /util/datatypes/abstracts/UnrealOverride. You may refer to the other Classes in
   /util/datatypes/overrides/... for examples regarding how these methods should be implemented.
   Although not a hard requirement, it would be ideal that the new Object Class has all of the properties that the
   Unreal Class it refers to also has.
   It is, however, required that this class have a Flag property for each of the properties present in its respective
   UnrealDataType class.
   Add the new UnrealDataType Setting Object as a property in /util/RenderSettings.
   You might have to search for places where a RenderSettings object is initiated to include the new field.
   Add the new Override Map Class Object as a property in /util/RenderSettingsOverride.
   You might have to search for places where a RenderSettings object is initiated to include the new field.
   Modify the “getSetting” method in /util/CustomUnrealPreset to be able to return the new setting type.
   Modify the “getRenderSettings” method in /util/RenderExecutor to also include the new setting type.

 
You have now made all the required changes to the BackEnd for the new Setting type to be functional! However, a few steps also need to be taken in order to make these values be available to display on the FrontEnd. To do so, follow the steps below:

1. Update the Archive Entry HTML Template found at /manager/templates/archive_entry to include a section with the new Setting Type.
- Make sure to add both a new Section, and a new Sidebar Navigation Item.
- You may refer to the other Setting Types already implemented in the same file for examples regarding how these
  changes should be made.
2. Update the “handleTabSwitch” method in /manager/static/js/archiveUtils to include the new Sidebar Navigation Item for
  the new Setting Type.
3. Update the Submitter Form HTML Template found at /submitter/frontend/templates/new_request to include a section with the new Setting Type.
- Make sure to add both a new Section, and a new Sidebar Navigation Item.
  You may refer to the other Setting Types already implemented in the same file for examples regarding how these
  changes
  should be made.
4. Update the “handleTabSwitch” method in /submitter/frontend/static/js/documentUtils to include the new Sidebar
  Navigation
  Item for the new Setting Type.
  Update the “submitForm” method in /submitter/frontend/static/js/dataUtils to include the require Data & Override
  Mappings for the new Setting Type
  With that, you have completed all the required steps in order to implement a new Override Setting Type! It’s also
  important to note that the Render Worker will still use any Settings that are present in the Preset, whether they are
  overridable by the System or not.
