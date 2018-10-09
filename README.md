# CubeRover Control API

CubeRover controls will allow us to physically control a lunar rover remotely. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine
for development and testing purposes. See deployment for notes on how to deploy the project
on a live system.
<br><br>
AirSim exposes APIs so you can interact with vehicle in the simulation programmatically.
You can use these APIs to retrieve images, get state, control the vehicle and so on.

### Python Quickstart
If you want to use Python to call AirSim APIs, we recommend using Anaconda with Python 3.5
or later versions however some code may also work with Python 2.7
([help us](https://github.com/Microsoft/AirSim/blob/master/docs/contributing.md)improve compatibility!).

The first thing you need to do is make sure you have python and pip installed on your
computer. <br><br>
Then install this package:

```
pip install msgpack-rpc-python
```

You can either get AirSim binaries from [releases](https://github.com/Microsoft/AirSim/releases)
or compile from the source ([Windows](https://github.com/Microsoft/AirSim/blob/master/docs/build_windows.md),
[Linux](https://github.com/Microsoft/AirSim/blob/master/docs/build_linux.md)).
Once you can run AirSim, choose Car as vehicle and then navigate to `PythonClient\car\` folder and run:

```
python hello_car.py
```

If you are using Visual Studio 2017 then just open AirSim.sln, set PythonClient as startup
project and choose `car\hello_car.py` as your startup script.

### Installing AirSim Package
You can also install `airsim` package simply by,

```
pip install airsim
```

You can find source code and samples for this package in `PythonClient` folder in your repo.

**Notes**
1. You may notice a file `setup_path.py` in our example folders. This file has simple code to
detect if `airsim` package is available in parent folder and in that case we use that instead
of pip installed package so you always use latest code.
2. AirSim is still under heavy development which means you might frequently need to update the
package to use new APIs.


## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python](https://www.python.org/) - Programming Language
* [Airsim](https://github.com/Microsoft/AirSim) - Virtual Simulator

## Contributing

When contributing, please make sure you write clean, efficient code using the PEP8 style guide
* [PEP8](https://www.python.org/dev/peps/pep-0008/) - Style Guide for Python Code

## Versioning

Current Version: 1.0

## Authors

* **CMU Lunar Robotics Teleoperations Team ** - *Initial work*

See also the list of [contributors](https://github.com/etapiahe/CubeRover-ControlsAPI/contributors) who participated in this project.

## License


## Acknowledgments

* Special thanks to CMU Professor Red Whittaker and the whole Astrobotic and CubeRover team

