---
layout: page
title: "Tasks"
permalink: /tasks-tags/
---

{% assign whitelist = "Binary Source Code Matching,Malicious Code Localization,Unprotected API Vulnerability Discovery,Vulnerable Code Clone Detection,Malicious Code Detection,Malicious Behavior Detection,Malware Prediction,Vulnerability Classification,Injection Attack Detection,Vulnerability Detection,Vulnerability Repair,Security Patch Identification,Security Analysis,Vulnerability Analysis,Vulnerability Localization,Malicious Package Detection,Malware Classification,Vulnerability Extrapolation,Vulnerability Testing,Malicious Code Classification,Cryptography Misuse,Malware Detection,Vulnerable Commits Detection,Password Leaks,Malicious Code Deobfuscation,Vulnerability Prediction,Classifying Android Sources & Sinks,Reentrancy Detection,Buffer Overrun Prediction,Malicious Code Filtering" | split: "," %}

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
