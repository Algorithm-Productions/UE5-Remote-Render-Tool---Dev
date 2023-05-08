# COMPONENT/PROJECT SETUP
## New Project

Every Project that is to use this Render Farm Software must go through a small Setup process, which would hopefully be 
streamlined into the Default Project Template. 

Regardless, here are the Steps:
1. Make sure whatever Machine hosts the Project has Python installed.
  - You can test that Python is installed by running the “python” command on CMD.
  - You can install Python 3.9 from here.
2. Make sure whatever Machine hosts the Project has GIT installed.
  -  You can test that GIT is installed by running the “git” command on CMD.
  -  You can install GIT from here.
3. Open the Project you’d like to render using the UE, navigate to Edit > Plugins, and install both the Python Editor 
Script Plugin and the Movie Render Queue Plugin.
4. Open the Project files on Explorer, navigate to Content > Python, and run the following commands:
 
    ```
    git clone https://github.com/Algorithm-Productions/UE5-Remote-Render-Tool---Dev.git
    cd ./UE5-Remote-Render-Tool---Dev
    python -m pip install -r requirements.txt
    ```

Go back to the Explorer, and extract every file from the UE5-Remote-Render-Tool---Dev Folder to the Content/Python folder itself.

## Manager
The Manager is currently running on the Algorithm WebServer, it is dockerized, and set up to auto-update when any 
changes are detected on the GitHub repository. No further setup is necessary.

To access the Manager from another device, it is only necessary to add the device to the Tailscale network.

## Submitter
There are a few distinct steps that must be taken before a computer is allowed to submit new Render Jobs:

1. Install Python 3.11 from here.
2. Add Python to the System’s Environmental Paths, see how here.
- You might also need to remove some App Execution Alias, see how here.
3. Install GIT from here.
4. Assure that your System has the Tank mapped to the X Drive. [JAMES ADD COMMENT AS TO HOW TO DO THIS]
5. Restart your System to make sure all the above changes are fully implemented
- You can test that GIT is installed by running the “git” command on CMD.
- You can test that Python is installed by running the “python” command on CMD.
6. Copy this Link.
7. Navigate to the directory where you want to save the Submitter application, open CMD and run the following commands:

    ```
    git clone https://github.com/Algorithm-Productions/UE5-Remote-Render-Tool---Dev.git
    cd ./UE5-Remote-Render-Tool---Dev
    python -m pip install -r requirements.txt
    ```

To run the Submitter after completing the steps above, you should navigate to the directory where it is saved, open CMD, and run the following command: 

    ```
    python app.py -m submitter
    ```

## Worker
Setting up the worker involves a few more steps. 

The guide below will assume that the setup process is being ran on a brand-new install of Windows 11:

1. Complete the Fresh Install of Windows.
2. Check and Complete any secondary Windows Updates.
3. Install the most recent NVIDIA Studio Drivers from here.
4. Run the Ansible New Machine Setup script.
5. Install GIT from here.
6. Assure that your System has the Tank mapped to the X Drive. [JAMES ADD COMMENT AS TO HOW TO DO THIS]
7. Install the Epic Games Store from here.
8. Download the correct version of the Unreal Engine from the Epic Games Store.
- Make sure you are installing the Engine in the Default location the install wizard suggests.
9. Restart your System to make sure all the above changes are fully implemented
- You can test that GIT is installed by running the “git” command on CMD.
- You can test that Python is installed by running the “python” command on CMD.
10. Copy this Link.
11. Navigate to the directory where you want to save the Worker application, open CMD and run the following commands:

    ```
    git clone https://github.com/Algorithm-Productions/UE5-Remote-Render-Tool---Dev.git
    cd ./UE5-Remote-Render-Tool---Dev
    python -m pip install -r requirements.txt
    ```

To run the Worker after completing the steps above, you should navigate to the directory where it is saved, open CMD, 
and run the following command:

    ```
    python app.py -m worker
    ```
