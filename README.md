# service-status-geckoboard
Support Engineer Coding Challenge [assignment](https://gist.github.com/luise64/931fcded2801c27f7d3d5b6792815444)

#### About

The program pulls service status data from [*GitHub*](https://status.github.com/api) and [*Twilio*](https://status.twilio.com/api) APIs in regular intervals (5 minutes, since Geckoboard currently enables 5 minutes refresh rate) and pushes that data up to the datasets API.

For some reason (trial only Geckoboard account?), the Dashboard doesn't offer Text widget which was the one I originally intended to make use of. To address this I opted for Column Bar widget with slightly different usage model: the bar (one for each service) serves as status indication (full bar (value 1) signals the service is online while no bar (value 0) stands for service currently down).

To implement this I used **Python** 2.7 and [**Requests**](http://docs.python-requests.org/) 2.11.1 since I'm familiar with Python and used Requests previously. All APIs involved are well documented and concise, that allowed for straightforward code. Verified in Windows and Ubuntu environments.

#### Project Status

As of now project is in basic functionality stage and works as expected. With more time, I'd focus on adding unit tests, refactoring the code to support more services and adding functionality to handle services error message responses.
