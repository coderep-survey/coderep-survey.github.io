---
layout: page
title: "Representations"
permalink: /Representations-tags/
---

{% assign whitelist = "Program slices,Code Aggregate Graph (CAG),Code metrics,System Dependence Graph (SDG),Program Graph,Opcode Sequences,Contextual Source and Sink Dependency Graph (CSSDG),Contextual API Dependency Graph (CADG),Contextual ICFG (CICFG),Regular Expression,Code gadgets,Call graph,Control Flow Graph (CFG),Crucial Data Flow Graph (CDFG),Tokenizer,Token Graph,Slice Property Graph (SPG),Interprocedural Control Flow Graph (ICFG),Component Dependency Graph (CDG),Parse Tree,Component Behavior Graph (CBG),Data Flow Graph (DFG),AST+,Value Flow Graph (VFG),Propagation Chain,Property Graph,source code and Syntax based Vulnerability Candidate (sSyVC),Semantic Graph,Program Dependence Graph (PDG),API Calls,Code Property Graph (CPG),Abstract Syntax Tree (AST),intermediate code and Semantics-based Vulnerability Candidate (iSeVC),Contextual Permission Dependency Graph (CPDG),Contract Graph,Image,Contract Snippet,Simplified CPG (SCPG),Application Information" | split: "," %}

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
