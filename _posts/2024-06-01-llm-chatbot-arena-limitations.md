---
layout: post
title:  How much should we read into LLM Chatbot Arena leaderboard ranks?
date: 2024-06-01 15:00:05 +05:30
categories: eval
description: The limitations of Chatbot Arena
keywords: chat arena, eval, evaluation, overfitting, data contamination, leaderboards
image: /assets/img/llmchatbotarena/thumbs-up-dreamy.jpg
---

[LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/?leaderboard=) offers incredible insight. The excitement when a new model jumps in the leaderboard is quite palpable. But are we reading too much into it?

I think it’s important to step back to assess what these rankings *truly* imply with respect to LLM capabilities.

## What’s great about the Arena Leaderboard

LLM benchmarks face several challenges, as described in [The Evolving Landscape of LLM Evaluation](https://newsletter.ruder.io/p/the-evolving-landscape-of-llm-evaluation) by [Sebastian Ruder](https://x.com/seb_ruder):
* Benchmarks becoming less dependable.
- Rapid LLM progress is saturating benchmarks.
- There is a risk of memorization due to data leaking into training sets.
- Overfitting occurs due to incentives, generating synthetic data to align with evaluation test sets or using the same LLM that will eventually be the judge.

In contrast, the Chatbot Arena Leaderboard offers several advantages:
* **Aligned Metrics**: *If we assume* the goal of the leaderboard rank/Elo score is “what people like,” then there’s no [Goodharting](https://en.wikipedia.org/wiki/Goodhart%27s_law). The metric tracks the goal.
* **Dataset Integrity**: The leaderboard is largely immune to dataset contamination and metric hacking since the “test sets” are always “new.” Evaluators can input any prompt, see two blinded outputs, and rank them.
* **Diverse and Dynamic Testing**: Users bring a lot of creativity and ingenuity to their prompts, ensuring diverse and high-volume testing. This includes edge-cases, favorite prompts that trip LLMs, puzzles, and work-related tasks.


## The Limitations of Arena Leaderboards

I think we should take Arena leaderboard ranks with a grain of salt. That’s not to say that there’s zero correlation between the leaderboard ranking and the quality on any given task. But it’s important to realize how strong we should expect it to be.

# Selection bias of test set and evaluators

There’s a selection bias since only questions users are likely to ask a general-purpose chatbot contribute to the ranking. It’s a *Chatbot* Arena after all. I expect the demographic of voters is likely skewed towards tech enthusiasts and researchers.

The Arena may therefore fail to represent a diversity of use-cases and users.

# May not correlate with the performance on tasks involving long input contexts or complex reasoning

The UX/form-factor does not invite very long input contexts or reasoning over complex documents. E.g. it’s not possible to upload documents (even if they would fit the context window). In that sense, Chatbot Arena assesses the early 2023 ChatGPT-like use-case before ChatGPT allowed file-uploads, data analysis, etc. 

Specifically, the leaderboard may only be weakly correlated with quality on tasks like understanding or summarizing long or complex documents.

It’s worth noting that Chatbot Arena is focused on non-multimodal LLMs with text input/outputs. Similar efforts like [Vision Arena for testing VLMs side-by-side](https://huggingface.co/spaces/WildVision/vision-arena) try to address VLMs.

# Impact of Fine-Tuning

Weak base LLMs, when fine-tuned for chat, can yield disproportionately better results. This shows the power of fine-tuning but may give a boosted sense of quality compared to other LLMs that haven’t been similarly fine-tuned.

E.g. without improving on reasoning or math abilities, it may be possible to boost an LLM’s rank by this sort of fine-tuning to “behave like a good Chatbot”.

# Diversity of user prompts

How diverse are users’ tests, *really*? I don’t know if there’s any analysis on:
* the distribution of Arena users’ prompts across languages. Are they 90% in English? How often do people ask questions in their non-English native languages?
* the clustering of users’ prompts to see if there are big clusters of common (lazy?) prompt like “tell me a joke”, enquiring about the LLM, and so on
* how often do people ask reasoning, math, domain-specific questions

# User pandering

Some LLMs may exhibit [sycophancy](https://arxiv.org/abs/2310.13548) or compliment the user to elicit higher votes. This can skew results by making users feel better about themselves.

# May penalize refusals

The voters may penalize refusals for harmful or biased questions, giving an advantage to models not RLHF’ed to refuse. This is not what we may want in a user-facing PG13 product.

## The importance of doing your own evals

The Chatbot Arena Leaderboard should be one data point in model selection. Developers should also consider standardized LLM benchmarks. 

Neither of those is a substitute for what I think is most important: We should do our own evals — create our own test sets and define rubrics and metrics on what matter _for our use-case_. 

Let [me](https://x.com/ashutoshmehra) know what you think.

{% include postimg.html url="llmchatbotarena/thumbs-up-dreamy.jpg" %}