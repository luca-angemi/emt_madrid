# EMT Madrid Bus custom compontent for Home Assistant
EMT Madrid Bus integration for Home Assistant

## Install

Copy `emt_madrid` folder to `custom_components` folder in your config folder.

Restart HA.

## Setup


1. Configuration > Integration > Add Integration > EMT Madrid
2. Enter your  EMT Email and Password along with your preferred bus stop number.


## Features

The integration will create a new `sensor` with the waiting time to the next arrival for each bus line present at the bus stop.

<img width="552" height="577" alt="image" src="https://github.com/user-attachments/assets/6ddb05ba-ce0b-4dfe-8c47-372d0d47ba3e" />

The sensor has also `lat` and `lon` with the next bus position as attributes, so its movements can be tracked on a map. 


<img width="602" height="340" alt="image" src="https://github.com/user-attachments/assets/70aec338-d84b-4bb9-a023-cbcf7e9239d9" />



[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/luca.angemi)
