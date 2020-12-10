# Goal 

To build a virtual gallery experience using Computer Vision to display interesting groupings of art. 

Interesting groupings are those that are visually similar, but categorically different. 

# Background

The Barnes Foundation in Philadelphia, one of the premier collections of Impressionist Art, displays works in "ensembles" to show visual principles. I wanted to apply this principle to the much larger Met collection.

# Data Sets

1. Kaggle data set from 2019 and 2020 for Fine-Grained Video Classification
2. Images and JSON responses from the Met's website

# Methodology

To preprocess the data, I needed to decrease the computational complexity

* Reduce image size
* Calculate visual similarity using VGG transfer learning (convolutional neural network) using Google Colab
* Calculate categorical similarity from cosine similarity of metadata classifications with greater than 10 occurrences

# Future Work

There is much to implement with further iterations

* Incorporate dominant color, image orientation, light intensity, and other metrics that were not included due to computational complexity
* Calculate image similarity for a larger portion of the corpus
* Define a more rigorous definition of categorical similarity, rather than a Boolean
* Define a  more rigorous definition of what constitutes an ensemble 
* Visualize findings in Art Steps 
* Image generation using Style Transfer



# Tools Used 

* Pandas

* Kaggle

* Google Colab

* Google Cloud Platform

* SKLearn

* CV2

* Matplotlib

* Python JSON library

  

# Skills Demonstrated

* Unsupervised Learning
* Computer Vision
* Convolutional Neural Networks
* Topic Modeling 
* Web Scraping
