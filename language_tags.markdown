---
layout: page
title: "Languages"
permalink: /language-tags/
---

{% assign whitelist = "powershell,CSS,Solidity,PHP,Ruby,C#,JavaScript,Rust,XML,Java,TypeScript,SQL,Gecko,Go,C,smali,HTML,C++,SpiderMonkey,XUL,Python" | split: "," %}

{% for tag in site.tags %}
  {% if whitelist contains tag[0] %}
  {{ tag[0] }}
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url | absolute_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}