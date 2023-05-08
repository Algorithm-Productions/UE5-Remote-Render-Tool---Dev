# OVERVIEW
The application is separated into 3 different components. These are:
## Manager
The manager runs on the server and receives requests from the other components and communicates across the network.
[Image of the Manager Software]

## Submitter
This is the software run by the machine that wishes to issue a render to the manager. It can specify which worker it would like to complete the render.
It can override existing settings such as resolution, AA render location etc.
[Image of the Submitter Software]

## Worker
This is the software run by the machine that is actually doing the render.
This machine will require access to the unreal project and correct version of the engine locally(or tank).

[Image of the Worker Software]

# CORE FUNCTIONALITY

- Submit renders to remote machines
- View job progress and manage active renders
- Keep record of all render details for archived jobs including:
- Settings
- Machine
- Issuer
- Frametime Graph
- Modify render settings at submission:
- AA
- Output Location
- Resolution
- Console Variables
- High Resolution Tiling
