NetSquid-PingPong (0.1.0)
================================

**THIS REPO HAS MOVED TO https://gitlab.com/softwarequtech/netsquid-snippets/NetSquid-PingPong**

Description
-----------

This is an example _snippet_ for the [NetSquid quantum network simulator](https://netsquid.org).

This snippet is made as a guide for the beta release competition, based on the game of PingPong mentioned in the [10 minute guide](https://docs.netsquid.org/latest-release/quick_start.html) and the [tutorials](https://docs.netsquid.org/latest-release/tutorial.intro.html) available from the documentation.

In short, this snippet can be used to play PingPong between two nodes in a network using NetSquid protocols. Besides the protocol implementation, also an example of a custom delay model is given.

To take part in the beta release competition we ask you to use the same repository structure as can be created using the [snippet template](https://github.com/SoftwareQuTech/NetSquid-SnippetTemplate).

The most important parts of this structure are:
* a folder with the actual code: in this case *netsquid_pingpong*.
* a folder named *examples*, with at least one running example of your code.
* this *README* file where you can describe your snippet: its goal and key elements.

Installation
------------

See the [INSTALL file](INSTALL.md) for instruction of how to install this snippet.

Documentation
-------------

To build and see the docs see the [docs README](docs/README.md).

Usage
-----

The main simulation, which creates a network and plugs in the protocols, can be found in the *examples* directory and can be run by calling in your terminal:

```
python3 examples/example_pingpongprotocol.py
```

To adapt the protocol or the delay model used, you can check the files in the *netsquid_pingpong* directory.

As mentioned above, for the competition you can create your own snippet using the [snippet-template](https://github.com/SoftwareQuTech/NetSquid-SnippetTemplate).

Contributors
------------

- Loek Nijsten (loek.nijsten@tno.nl)
- Martijn Papendrecht (m.n.g.papendrecht@tudelft.nl)

License
-------

This snippet has the following license:

> Copyright 2020 QuTech (TUDelft and TNO)
>
>   Licensed under the Apache License, Version 2.0 (the "License");
>   you may not use this file except in compliance with the License.
>   You may obtain a copy of the License at
>
>     http://www.apache.org/licenses/LICENSE-2.0
>
>   Unless required by applicable law or agreed to in writing, software
>   distributed under the License is distributed on an "AS IS" BASIS,
>   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
>   See the License for the specific language governing permissions and
>   limitations under the License.
