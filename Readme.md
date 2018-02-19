## Idle Engine
### An engine for idle/incremental/clicker games

The point of the Idle Engine is to create a content-agnostic engine for web-based clicker games.

The core of the engine is separate from the content and from the UI

The first pass of Idle Engine support
- currencies
- actions
  - costs
  - rewards
  - coditional visibility
- autoclickers
  - cooldown timer
  
This is a minimal first pass. Concepts expected to be included at some point: buffs.
I'd also quite like to include some MMO concepts by letting players interact with each other.

Three sample currencies and three sample actions are currently included in data/. There should indicate how to form your own content for the Idle Engine. UI pages are stored in templates/

Idle Engine is powered by Flask.

Trello board for progress tracking: https://trello.com/b/hqXqyGnn/idle-engine#

### Getting Started

To build your own clicker you will need:
1. Clone the repository (if you're serious about using it, you may want to fork instead?)
2. Install the Flask python module (I reccomend starting a clean virtualenv but it probably isn't necessary)
3. Look in the data/content/ folder. There are some example content definitions there to get you started while I get round to documenting the system
4. Look at templates/ for the HTML interface files. These are super bare-bones but with some love could be all shiny and CSS'y
5. When you're good to go, launch with python Launcher.py

### Feedback / Contact
You can reach me @ lukedicken@gmail.com - I'd love to hear from you
