# DOCUMENTATION OF CODE

[System Flow Diagram]

##  Utilities and Library
/util/datatypes/abstracts/EnumProperty
Abstract Object Class to represent ENUMs used by the System.

/util/datatypes/abstracts/StorableEntity
Abstract Object Class to represent any main Entities that need to be stored by the System.

/util/datatypes/abstracts/StorableProperty
Abstract Object Class to represent Properties of an Entity that need to be stored by the System.

/util/datatypes/abstracts/UnrealDataType
Abstract Object Class to represent any Objects used by the System that have Unreal API Counterparts.

- /util/datatypes/abstracts/UnrealOverride
Abstract Object Class to represent any Override Mappings for Objects used by the System.

- /util/datatypes/enums/LogType
ENUM Representing all types of Logs emitted by the System.
Inherits from /util/datatypes/abstracts/EnumProperty.

- /util/datatypes/enums/RenderStatus
ENUM Representing all possible Statuses of a Render.
Inherits from /util/datatypes/abstracts/EnumProperty.

- /util/datatypes/overrides/...
Each Class under this Directory represents an Override Mapping for a specific Settings Object used by the System. 
They share the same properties as the actual Object, except all properties are Booleans flagging whether or not the property was overridden.
All inherit from /util/datatypes/abstracts/UnrealOverride.

- /util/datatypes/unreal_dt/...
Each Class under this Directory represents an Object used by the System that has a direct counterpart in the Unreal API.
All inherit from /util/datatypes/abstracts/UnrealDataType.

- /util/datatypes/HardwareStats
Object Class representing all Hardware Statistics tracked by the System.
Inherits from /util/datatypes/abstracts/StorableProperty.

- /util/datatypes/RenderArchive
Object Class representing an Archive Object for a specific Render Job.
Inherits from /util/datatypes/abstracts/StorableEntity.

- /util/datatypes/RenderLog
Object Class representing an Event Log emitted by the System.
Inherits from /util/datatypes/abstracts/StorableEntity.

- /util/datatypes/RenderRequest
Object Class representing a Request Object for a specific Render Job.
Inherits from /util/datatypes/abstracts/StorableEntity.

- /util/datatypes/RenderSettings
Object Class representing all Settings used by the System for a specific Render Job.
Inherits from /util/datatypes/abstracts/StorableProperty.

- /util/datatypes/RenderSettingsOverride
Object Class representing all Setting Override Maps used by the System for a specific Render Job.
Inherits from /util/datatypes/abstracts/StorableProperty

- /util/Client
Overall Object Class used by the Worker & Submitter to communicate with the Manager API.

- /util/CustomUnrealPreset
Custom Object Class Implementation of the Unreal Render Preset.
Provides some utilities to access/change/update specific Settings for the Preset.
Inherits from unreal.MoviePipelineMasterConfig.

- /util/ManagerFlaskApp
Overall Object Class used by the Manager to serve both its FrontEnd and API endpoints.
Inherits from Flask.

- /util/RenderExecutor
Custom Object Class Implementation of the Unreal Render Executor.
Overrides default Executor to actually render a Job queue.
Inherits from unreal.MoviePipelinePythonHostExecutor

- /util/Worker
Custom Object Class Implementation of a Thread, used by the Worker to continuously request new jobs, and Render them.
Inherits from threading.Thread.

## Manager
- /manager/static/darkmode/...
Contains all the CSS used by the Manager FrontEnd when the Application is in Dark Mode.

- /manager/static/fonts/...
Contains all Font files used by the Manager FrontEnd.

- /manager/static/imgs/...
Contains all Image files used by the Manager FrontEnd.

- /manager/static/js/...
Contains all JS Helper Classes used by the Manager FrontEnd.

- /manager/static/lightmode/...
Contains all the CSS used by the Manager FrontEnd when the Application is in Light Mode.

- /manager/templates/...
Contains all HTML Page Templates used by the Manager FrontEnd.

- /manager/views
Contains all FrontEnd and API Endpoints.
Uses Flask to serve all of these Endpoints.

## Submitter

- /submitter/frontend/static/css/...
Contains all the CSS used by the Submitter FrontEnd.

- /submitter/frontend/static/fonts/...
Contains all Font files used by the Submitter FrontEnd.

- /submitter/frontend/static/imgs/...
Contains all Image files used by the Submitter FrontEnd.

- /submitter/frontend/static/js/...
Contains all JS Helper Classes used by the Submitter FrontEnd.

- /submitter/frontend/templates/...
Contains all HTML Page Templates used by the Submitter FrontEnd.

- /submitter/frontend/favicon.png
Favicon Image used by the Submitter FrontEnd.

- /submitter/GUISubmitter
Main Entrypoint for the Submitter Application.
Uses EEL to distribute the Submitter Application FrontEnd.
Contains some Helper Functions to communicate with the Manager via the Client Class.

## Worker

- /worker/frontend/static/css/...
Contains all the CSS used by the Worker FrontEnd.

- /worker/frontend/static/fonts/...
Contains all Font files used by the Worker FrontEnd.

- /worker/frontend/static/imgs/...
Contains all Image files used by the Worker FrontEnd.

- /worker/frontend/static/js/...
Contains all JS Helper Classes used by the Worker FrontEnd.

- /worker/frontend/templates/...
Contains all HTML Page Templates used by the Worker FrontEnd.

- /worker/frontend/favicon.png
Favicon Image used by the Worker FrontEnd.

- /worker/GUIWorker
Main Entrypoint for the Worker Application.
Uses EEL to distribute the Worker Application FrontEnd.
Contains some Helper Functions to start/close Worker Threads, and communicate with the Manager via the Client Class.
Other Files

- /remote_render/__init__.py
Used to Initialize the Flask App that serves as the Manager.

- /remote_render/_version.py
Used to keep track of the current Version of the Software.
.env
Used to maintain all the environmental variables used by the System.

app.py
Main Entrypoint for the entire System.
Setups the working environment, and runs the component requested on launch.
Defaults to running the Manager if no component is specified.
docker-compose.yml
[NEEDS DESCRIPTION BY NICK]
Dockerfile
[NEEDS DESCRIPTION BY NICK]
init_unreal.py
Helper File used by the Engine to initialize and consume both the /util/RenderExecutor and /util/CustomUnrealPreset classes.
requirements.txt
Project Requirements File.
Makes setting up the working environment easier.
