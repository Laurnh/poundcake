# Poundcake

Greetings! I developed Poundcake to help women who are beginner weightlifters venture into the gym with more confidence. When I first started lifting, I was so nervous to explore the weight room alone that I had to hire a personal trainer as a bodyguard. I also found it challenging to find quality videos on YouTube of women demonstrating how to lift. Poundcake is a free-standing web application that allows a woman to walk into any gym and upload a photo of a piece of equipment that she is unfamiliar with. The app classifies the equipment in the photo and recommends a series of relevant YouTube videos featuring women demonstrating how to use the equipment. Poundcake is designed to simulate the experience of hiring a personal trainer without the big expense. It also aims to counter the myth held by many women that if they lift weights they will bulk up and look too masculine. By making the weight room more accessible and breaking down barriers to strength training, my goal is to encourage women to ditch the Barbie weights and realize their full potential.

Poundcake was built as part of a three-week project for Insight Data Science in June 2018.

Visit Poundcake at [www.poundcake.fun](http://www.poundcake.fun)!

## Working with the data

The problem of classifying gym equipment is harder than it seems. There is a huge variety of colors, shapes, and configurations just within one class of equipment. For example, a bench press could have a blue bench cushion or a black bench cushion, or theoretically any color cushion. It could be structured in a simple "H" shape or could be more complicated (e.g. could be attached to a large structure behind the barbell that houses weight plates). A gym-goer could take a photo of a bench press from any angle or any configuration (e.g. with the barbell, without the barbell, with an empty barbell, or with a barbell loaded with plates). 

In an initial effort to pull together a large training set of gym equipment photos, I scraped Google Images for five classes of equipment:

* the bench press (Googled for 'flat bench press machine')
* the hyperextension bench (Googled for 'hyperextension bench')
* the leg press (Googled for 'leg press 45 degree')
* the plyometric box (Googled for 'plyometric box')
* the power rack/squat rack (Googled for 'power rack')

These Google searches resulted in an abundance of photos of equipment with static, white backgrounds. Surprisingly, there were not enough photos of equipment in real gym settings that were appropriate for this purpose. This was problematic since a gym-goer in a real gym setting would most likely take photos of equipment with very noisy backgrounds including mirrors, people, and other equipment.

To simulate a large training set of "real-life" equipment photos, I created a data augmentation pipeline that combined many combinations of (1) images of gym equipment with white backgrounds and (2) images of gym interiors. The gym interior images were scraped off of Google images using the search 'interior weight room.' The simulated images were further augmented with shearing, zooming, and flipping to take into account the variety of angles from which a gym-goer could photograph equipment.

See the data_augmentation folder for relevant code.

## Classification

The classifier was trained on simulated images of equipment using a three-layer Convolutional Neural Network (CNN). The CNN was implemented using Keras (a Python package) with a Tensorflow back-end. The CNN was tested on a hold-out set of simulated images and validated on a hold-out set of "real-life" photos. The validation set consists of around 100 photos that I took in my gym, friends took in their gyms, and other photos I scraped off of Google Images. 

See the classifier folder for relevant code.

## Deploying the web application

The web application front-end was built with HTML, JavaScript, and Flask. The back-end was built with Python, Keras, and Tensorflow. It was deployed on Amazon Web Services. 

See the web_app folder for relevant code.

## Authors

* **Lauren Holzbauer** - [linkedin.com/in/LHolzbauer](http://www.linkedin.in/lholzbauer)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thank you to all of the fellows at Insight for your support!

