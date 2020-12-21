# Toggle CUCM PSTN Block

Learning application based on a real world requirement

## Requirement

Acme Corp has a large facility that mines and manufactures various widgets. This facility operates as a small town, with it's on own
on site emergency response team, and lodging for 5000 employees and their families. In the event of an emergency Acme requires all
PSTN inbound and outbound calling to be routed through the Acme Emergency Operations Centre.

In normal operation there all IP Phones are allowed to dial out to the PSTN. During an emergency, authorized personnel must be able
to trigger the PSTN lockdown with minimal effort.

## Learning tak Objectives

- Manage user authentication with MS Azure AD B2C
- Store local user profile data in a Mongo Database
- Implement FASTAPI (or FLASK?) web framework
- Provide web based interface
- Provide API's that can integrated into other applications
- Provide a WebEx Teams Bot interface
- Provide a Finesse Gadget interface
- From All Interfaces provide Ability to:
  - Check Status (open to all users)
  - Enable lock down (all EOC personnel)
  - Disable lock down (senior EOC personnel)

### Other ideas

- when lockdown is initiated create a new team space and invite EOC members
- Allow EOC personnel to log inbound / outbound call requests
  - log via Finesse Gadget or Teams Bot
  - store in Mongo DB
- add nginx
- create web application w/ embedded webex teams for end users to submit call requests

### Considerations

- how to tie in Meetings API's? and Collaboration Endpoint API's

## Folder structure

```
├── app             # main folder contains application
    ├── api         # contains api views
    ├── bot         # webex teams bot handler
    ├── config      # contains config files / variables
    ├── gadget      # finesse Gadget
    ├── models      # data models
    ├── services    # services will perform the bulk of the work, and return the data for consumption by API's or Views
    ├── static      # static files to be served (CSS, images, etc.)
    ├── templates   # jinja2 html templates
    ├── views       # code for html views
```
