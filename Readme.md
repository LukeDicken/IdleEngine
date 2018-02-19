### Idle Engine
## An engine for idle/incremental/clicker games

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
