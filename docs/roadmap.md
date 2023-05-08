# ROADMAP / FUTURE IMPROVEMENTS

## Email/Text Alerts
The Software already has a Log/Notification System. One could relatively easily extend it to make use of an email client to send out proper notifications based on severity/type. This would be a significant improvement over simply checking the Web Portal for updates.

## General Refactor 
Although the current Codebase is fully functional, having all three Components, alongside the shared library, in one place can cause significant complications, especially in any attempt to fully automate setups.
In an ideal situation the application would be split into 4 parts: the shared Library (which could even be published into Pip, and so be consumed easily by other software); the Manager; the Worker; and the Submitter.

## Submitter Web Portal
As of right now, the Submitter side of the Software is running locally on the machine of anyone who might want to submit a new Render, however, as its functionality is effectively that of a form submitting its information to an API, this could easily be refactored to use the existing Web FrontEnd on the Manager.
This would reduce the setup work required, and would make it easier to submit renders from anywhere, as all you’d need would be an internet connection, and a device with Ansible enabled.

## Hardware Monitoring Dashboard
The current Manager FrontEnd is somewhat limited in what it displays, however, we could make use of Ansible/Grafana to host a more complex Dashboard, that could even monitor Hardware Stats for each of the Rendering Machines. Although a stretch goal, this data could come in handy in future optimizations.

## General Aesthetic Improvements
🙁 Sadly, due to the tight timeframe for development of this project, aesthetics were often overlooked, and so some parts of the Application FontEnd are slightly neglected, and could use some creative/artistic improvements.

## Error Handling Improvements
Although the Software does have some basic Error Detection, it is flimsy at best, and would not resist any major attempt at breaking the workflow. More complex “crash” detection regarding the Render Jobs would be incredibly beneficial, although we are somewhat limited by the Engine’s capabilities on this front.

## Load Balancing
The current Worker assignment system works by asking the Submitter to pick which Worker they’d like to execute the job on, although this is perfectly functional, it does somewhat limit the render capacity of the System. Ideally, the Manager would automatically load-balance the Render Queue, distributing jobs to any available workers as they come and go.
