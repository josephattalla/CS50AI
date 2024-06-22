# CS50 AI Solutions

This repository contains my solutions to the exercises from the [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/) course offered by Harvard University.

## Table of Contents

- [Lecture 0: Search](#lecture-0-search)
  - [Degrees](#degrees)
  - [Tic-Tac-Toe](#tic-tac-toe)
- [Lecture 1: Knowledge](#lecture-1-knowledge)
  - [Knights](#knights)
  - [Minesweeper](#minesweeper)
- [Lecture 2: Uncertainty](#lecture-2-uncertainty)
  - [Heredity](#heredity)
  - [PageRank](#pagerank)
- [Lecture 3: Optimization](#lecture-3-optimization)
  - [Crossword](#crossword)
- [Lecture 4: Learning](#lecture-4-learning)
  - [Shopping](#shopping)
  - [Nim](#nim)

## Lecture 0: Search

### [Degrees](week0/degrees)

**Description**: This exercise involves implementing a program to determine the degree of separation between two actors using a shortest path algorithm. The method used is Breadth-First Search (BFS) to explore the shortest path in an unweighted graph where nodes represent actors and edges represent movies in which they have appeared together.

### [Tic-Tac-Toe](week0/tictactoe)

**Description**: Implement an AI to play Tic-Tac-Toe optimally using the minimax algorithm. The minimax algorithm is a recursive method used for decision-making and game theory, which minimizes the possible loss for a worst-case scenario.

## Lecture 1: Knowledge

### [Knights](week1/knights)

**Description**: This exercise involves implementing a knowledge base to solve the classic "Knights and Knaves" logic puzzles. The method involves constructing logical statements using propositional logic and employing a resolution algorithm to deduce the correct answers.

### [Minesweeper](week1/minesweeper)

**Description**: Implement an AI to play the game of Minesweeper optimally. The AI uses logical inference to deduce the locations of mines based on the numbers revealed in the adjacent cells. The implementation involves maintaining a knowledge base and applying constraint satisfaction techniques.

## Lecture 2: Uncertainty

### [Heredity](week2/heredity)

**Description**: Use Bayesian networks to compute the probability distribution for genetic traits within a family. The solution involves constructing a Bayesian network representing the heredity of traits and using probability theory to perform inference on the network.

### [PageRank](week2/pagerank)

**Description**: Implement the PageRank algorithm to rank web pages based on link structure. The PageRank algorithm uses an iterative approach to compute the rank of each page by considering the link structure of the web. It simulates the behavior of a random surfer who follows links randomly.

## Lecture 3: Optimization

### [Crossword](week3/crossword)

**Description**: Implement a crossword puzzle solver using constraint satisfaction. The solver uses backtracking search combined with constraint propagation to fill in the crossword puzzle. The algorithm ensures that all words fit the given constraints of the puzzle grid.

## Lecture 4: Learning

### [Shopping](week4/shopping)

**Description**: Build a machine learning model to predict whether online shopping customers will complete a purchase based on various features. The solution involves preprocessing the data, training a supervised learning model (e.g., decision tree, random forest), and evaluating its performance.

### [Nim](week4/nim)

**Description**: Implement an AI to play the game of Nim optimally using reinforcement learning. The AI learns the optimal strategy for playing Nim by interacting with the environment, updating its knowledge base, and using Q-learning to maximize its rewards.
