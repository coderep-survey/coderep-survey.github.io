---
layout: page
title: "Models"
permalink: /models-tags/
---

{% assign whitelist = "Light Gradient Boosting Machine,GraphCodeBERT,Bidirectional RNN for Vulnerability Detection and Locating,Feature Attention- Graph Convolutional Network,Linear Regression,Encoder-Decoder,Graph Neural Network,Bagging,BERT,Decision Tree (final),Hierarchical attention network,Gated Graph Neural Network,Tree augmented naive Bayes,adaboost,Long Short Term Memory,Discrete Fourier Transform,Bidirectional Graph Neural Network,Code2vec (final),Temporal Convolutional Network,C-Support Vector Classification Variant of Support Vector Machine,Graph Attention Network (final),K Nearest Neighbor (final),self attention networks,Graph Convolutional Network,Bidirectional Gated Recurrent Unit,Logistic Regression (final),Paragraph Vector Distributed Memory,attention neural network,JavaBERT,GPT,ensemble,Gradient Boosting Decision Tree,Recurrent Neural Network,Multiple,doc2vec,multiple kernel learning SVM,Text Convolutional Neural Network,deep belief network,Deep Pyramid Convolutional Neural Network,Deep Learning Attention-based Convolutional Gated Recurrent Unit,Abstract Syntax Tree Neural Network,Gaussian Naive Bayes,Transformer,bidirectional Recurrent Neural Network,autoencoder,clustering,Linear Discriminant Analysis,Random NN,Naive Bayes (final),Recurrent Graph Convolutional Network,deep learning,Neural Memory Network,Convolutional Neural Network,Bidirectional Long Short Term Memory,Extra-trees classifier,complex Deep Neural Network,Support Vector Machine (final),Random Forest (final),Nearest Neighbor,k-median clustering,seq2seq,Extreme Gradient Boosting,CoForest,k-means clustering (final),Gated Recurrent Unit,CodeBERT (final),online learning,Boosting,Passive Aggressive Classifier,Density-Based Spatial Clustering of Applications with Noise,Multi Layer Perceptron,Deep Neural Network,Neural Network,word2vec,Extreme Learning Machine" | split: "," %}

{% for tag in site.tags %}
  {% if whitelist contains tag[0] %}
  <h2>{{ tag[0] }}</h2>
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url | absolute_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}
