# The Sound of the Stern-Brocot Tree

## Introduction
We can use the Stern-Brocot tree to define a one-to-one mapping between the set of positive rational numbers and the set of positive integers. One method of doing so requires us first to define the *kth* element of a given arbitrary binary tree.

Given a positive integer *k*, we can define the *k*th element of a tree as follows:
 - If *k=1* then the *k*th element of the tree is simply the root node.
 - If *k* is even, then the *k*th element of the tree is the *(k/2)*&#x200B;th element of the left-hand branch of the root node.
 - If *k* is odd, then the *k*th element of the tree is the *((k-1)/2)*&#x200B;th element of the right-hand branch of the root node. 

We can now define our mapping between the positive rationals and the positive integers. For a given positive integer *k*, the corresponding positive rational is the value of the *k*th element of the Stern-Brocot Tree. Due to the nature of the tree, we can claim that this mapping is one-to-one.

One consequence of this mapping is that one can begin to list all the positive rational numbers in "order", i.e. the rational associated with 1, then 2, then 3, etc.

In such a sequence, we can be sure that we will hit every positive rational number exactly once. The program contained herein works with this sequence.

## Requirements
In order to run this program, you will need:
 - Python 3.8 or later (because there are a few walrus operators and f-strings)
 - SOX as a command line tool (I've only tested this with version 14.4.2 but I think all recent versions should work)
 - The following python modules, all of which can be installed via PyPI
    - Pygame
    - Opensimplex

## Usage
```
python3.8 ./graphical.py
```

## What it does
This program provides and auralisation<sup>1</sup> of the Stern-Brocot tree by taking the elements in the order defined in the introduction, and taking the numerator and denominator of each element in turn. These, mod 7, are converted into musical notes. A value of 0 corresponds to the note C, 1 corresponds to D, and so on until 6 corresponds to B. The numerator's note and the denominator's note are played together, with the latter 3 octaves lower than the former.

The length of the note pair and the gap between adjacent note pairs is affected by simplex noise to give more texture to the melody.

<sup>1</sup>If you think that's the wrong word to use, take it up with [Shawn D.](https://english.stackexchange.com/questions/1635/visualized-equivalent-adjective-for-audio)

## Video
A video of the program running can be found [here](https://vimeo.com/478189954).

## Interesting uses

My program parameterises the Stern-Brocot tree in three ways:
 - The value for zero
 - The value for infinity
 - The mediant function

Altering any of these three parameters, or any combination thereof, gives a very different melody - some of which are quite interesting indeed.

For example, the I find the [following](https://vimeo.com/478195656) parameters interesting:
 - The value for zero is 1/1
 - The value for infinity is 2/1
 - The mediant is now the product of the two fractions, rather than the sum of the numerators divided by the sum of the denominators.

## How to change the parameters:
The values for zero and infinity are defined on lines 9 and 10 of `graphical.py` as (numerator, denominator) tuples. The `mediant` function is defined on line 73 of `tools.py`. It accepts two such tuples as parameters, and returns one likewise. 