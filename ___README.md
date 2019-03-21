# Cat Feeder

A food dispenser for pets that runs on micropython and relies on Home Assistant, Nodered and MQTT.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Hardware Prerequisites

- esp8266 v2 running micropython
- mg996r servo motor
- ultrasonic sensor HC-SR04
- motor shield for esp8266
- 2 x push button
- piezo speaker (optional and not implemented yet)

### Software Prerequisites

- Nodered
- Home Assistant
- MQTT

### Wiring

![Alt text](pictures/wiring.png?raw=true "Wiring")

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Authors

* **Bruno-Pierre Jobin** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Dave Hylands https://github.com/dhylands/upy-rtttl
* pythoncoder on the micropython forum for answering lots of questions I was about to ask.

