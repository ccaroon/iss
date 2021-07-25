# ISS
Stuff related to the International Space Station.

## Projects

### ISS Globe
Detects when the ISS is "overhead" and lights up a light.

#### Feather Huzzah
Uses a python script written for micro-python running on an AdaFruit Feather Huzzah.


### Philips Hue
* Getting Started: https://developers.meethue.com/develop/get-started-2/
* Dev Tool/Debugger: http://<bridge_addr>/debug/clip.html

#### Other Reqs
* https://github.com/benknight/hue-python-rgb-converter

#### Get Username for App
1. Push link button
2. POST /api `{"devicetype":"app_name#device"}`

Response:

```json
[
	{
		"success": {
			"username": "faKekjh6kj435kBaDc23h688L67duMmYk134hvl9"

		}
	}
]
```

#### Requests
http://<bridge_addr>/api/<username>/...
