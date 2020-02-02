# jobbly

## A job application for Bootcamp grads

As part of the Bootcamp process, graduates are expected to stay on top of their job applications by using a complex Google Sheets document with several different tabs. Jobbly was born out of a desire to streamline this process, allowing users to focus on the job search instead of the tracking process.

![Application Detail View](https://i.imgur.com/Md67kMu.png)

Track details of each application, including related events and contacts.

![Calendar](https://i.imgur.com/NyHo226.png)

Get a summary of your events and follow-up reminders in the Jobbly Calendar view.

![Jobbly Dashboard](https://i.imgur.com/VMAOIf5.png)

Search for jobs, review tech news, track your applications, and get an overview of upcoming events in the dashboard.

## Getting Started

You can access the app on Heroku [here](https://jobbly-tracker.herokuapp.com/). More into DIY? Feel free to clone the repo, but remember that you will need your own News API, AWS, and CareerJet API keys!

## The planning stages

The pitch deck is available [here](https://docs.google.com/presentation/d/10yUvMnNGTcP0CqpA5ak_AdUjC4EvJczOQ4-DEybtLmk/edit#slide=id.p).

## Models

![Entity Relationship Diagrams](https://i.imgur.com/uZ5GQLi.jpg)

#### Application Model

The main purpose of Jobbly is tracking job applications; the Application Model is very much the star of the show. The application model stores pertinent job information, such as the position applied for, company, the link of the job description if there is one. Users can also upload their resume and take notes, both with an aim of providing an easy reference for employees before heading for an interview. Users can also track landmarks associated with each application (phone interviews, technical interviews, etc.) and contact info for individuals associated with the application. The relationship between other models is listed below:
User Model -< Application Model
Application Model -< Landmarks Model
Application Model 0-< Contact Model

#### Landmark Model

Landmarks represent events that occur for each application. Examples of landmarks include a phone screening, in-person interview, or job offer. For each landmark, users have the option of entering start and end times and follow-up dates, all of which will appear in their calendar. Users can also record the location of interviews for easy reference.

#### Contact Model

Contacts are associated with users, and may also be associated with applications. They include basic information such as name, phone number, email, or linkedin details about someone you've met during the job search, as well as a notes section to remind you of conversation points or items to discuss further with the individual.

#### User Model

Jobbly uses the built in Django user model for authentication.

#### Profile Model

The profile model has a one-to-one relationship with the user model, and allows the user to track some of their job search resources, such as their LinkedIn and Github pages, as well as their preferences to make the job search easier (ideal position and job location). These preferences are then used to generate the default job search inputs on the User's home page, making searching easier than ever.

## APIs and Tools

#### Job Search API - CareerJet

Jobbly uses the careerjet API to allow users to search for positions in their desired location without leaving the site. Users can even begin a Jobbly Application Entry with basic job info prepopulated from the API!

#### FullCalendar.io

Fullcalendar.io is used to render weekly and monthly calendar views of users upcoming events and follow-up reminders.

#### New API

The News API is used to provide a tech news feed in the user homepage. It's always good to stay abreast of current topics to make conversation during interviews!

## Meet the Team

All three members of the team acted together as full-stack engineers to make Jobbly happen, but the three of us had individual responsibilities as well:

#### Bridget Asser

Bridget channeled her passion for web development on both the front and back-end, with special dedication on wrangling the S3 resume upload and delete functionality. You can see more examples of her ninja-dev skills on her github page [here](https://github.com/Bridgta).

#### Michelle Pitts

Coming from a background in engineering, Michelle applied her analytical mindset to corral the Jobbly Data Models, Job Search API, calendar functionality and devOps. You can check out Michelle's other work on her github page [here](https://github.com/meeschka).

#### Suzy Nakayama

Suzy's meticulous attention to detail made her the perfect front end engineer, controlling most of the design and css for Jobbly. She also implemented the News API and the contact search. You can see more of her fantastic looking (and high-performing!) applications on her github page [here](https://github.com/suzynakayama).

### UX Consultant

#### Annie Squarecircle

With a background in industrial and furniture design, Annie's devotion to User Experience helped us guide Jobbly's design to be intuitive for the user's journey. You can check out Annie's work on her portfolio page [here](https://www.anniesquarecircle.com).

## Next Steps

The Jobbly team would like to continue working to make Jobbly a truly full-service job search tracker. Possible features include:

-   implementing additional job search APIs to provide a wider range of possible jobs
-   sync with google calendar to manage application landmarks
-   sync with Google maps to track your interview locations
