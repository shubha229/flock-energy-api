# Reflection — Urja Meter Ops API

## 1. What assumptions did you make?

I treated the existing Urja Meter Ops portal as the main source of meter data. Instead of trying to build every feature available on the portal, I focused on three main operations: searching for meters, getting their location, and retrieving energy readings. I chose these features to keep the API simple and useful.

## 2. What was the hardest part, and how did you get unstuck?

The most challenging part was understanding how the portal's login and authentication worked. My initial requests failed because the portal expected certain headers along with the login request. To figure this out, I checked the requests made by the browser and compared them with my Python requests. Once I understood what was required, I was able to implement the login flow and retrieve the meter data successfully.

## 3. What would you improve with one more day?

With one more day, I would focus on making the API more reliable. I would add more tests for cases such as portal connection failures, expired sessions, and unexpected responses. I would also explore the meter hierarchy information and improve error logging. If suitable, I would consider caching some responses to avoid making repeated requests to the portal.

## 4. What mistake did you make?

Initially, I tried regular HTTP requests without fully understanding the portal's login requirements. My initial login request failed because some required headers were missing. I then used the browser's Network tab to inspect the request, identified the missing headers, and corrected the implementation. This taught me to understand how an existing system handles requests and authentication before integrating with it.

## 5. What is your self-critique?

I was able to build a working API with separate endpoints, data models, documentation, and automated tests. I also learned how to investigate an existing portal and connect it to a Python service. However, the API currently supports only a few meter operations, and there is still room to improve its reliability. I would like to add more tests with mocked portal responses and handle session expiry and different error scenarios more thoroughly. Overall, this project helped me understand the importance of investigating an existing system before building on top of it.
