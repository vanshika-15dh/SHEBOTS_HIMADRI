# SheBots
# RoboGambit 2026–27 Project

---

## Table of Contents

- Overview  
- Repository Structure  
- Task 1: Autonomous Game Engine  
- Task 2: ArUco-Based Perception  
- Simulation in Gazebo  
- Conclusion  

---

# Overview

This repository contains our complete submission for **RoboGambit 2026–27**, a strategy-driven robotics competition organized by **Aries and the Robotics Club, IIT Delhi**.

The aim of this competition is to design a system that can understand a chess board and make intelligent decisions based on the current state of the game.

Our approach focuses on connecting perception and reasoning. The system first observes the board using a camera, identifies where the pieces are placed, and then determines the most suitable move using a game engine.

The project is divided into three main components:

- **Game Engine** – responsible for deciding the best move based on the board state  
- **Perception Module** – detects pieces on the board using computer vision techniques  
- **Simulation Environment** – used to test and validate the system using Gazebo  

Together, these components allow the system to interpret the board and reason about the game in an autonomous way.

---

# Repository Structure

The repository is organized into different modules corresponding to the tasks of the competition.

The main game logic is implemented in the file responsible for handling the board representation and move decisions. The perception module processes images captured from the camera and determines the position of the pieces on the board. In addition to these components, the repository also contains files related to Gazebo simulation, which were used to test the system in a virtual environment.

Sample images used during testing and experimentation are also included in the repository.

---

# Task 1: Autonomous Game Engine

The game engine is responsible for analyzing the board configuration and deciding the best possible move for the current player.

While developing this component, our main focus was to ensure that the system correctly follows the rules of the game and handles different board situations reliably. The engine examines the available moves from a given board position and evaluates the resulting positions to determine which option provides the most advantage.

We paid special attention to maintaining consistency in board representation and ensuring that each move correctly updates the board state. Different board configurations were tested during development to verify that the engine behaves correctly in a wide range of situations.

This component forms the decision-making part of the system.

---

# Task 2: ArUco-Based Perception

The perception module allows the system to understand the physical board setup from camera images.

To make detection reliable, we used **ArUco markers** placed on the board corners as well as on the pieces. These markers help the system identify important reference points in the image and determine the positions of the pieces relative to the board.

The perception process involves detecting the markers in the image, identifying the board boundaries, and converting the detected positions into board coordinates. Once this mapping is established, the system determines which square each piece occupies.

The result of this process is a board representation that can be directly used by the game engine.

This module essentially acts as the bridge between the **physical environment and the decision-making system**.

---

# Simulation in Gazebo

In addition to the perception and decision modules, we also worked on **Gazebo simulation** to test the setup in a virtual environment.

Gazebo allowed us to simulate the robotic setup and experiment with different scenarios without relying entirely on physical hardware. This helped us visualize how the system would behave and validate the perception process under controlled conditions.

The simulation includes a virtual representation of the board environment along with a camera perspective similar to the actual setup.

Working with simulation helped us refine the system before integrating it with real-world inputs.

---

# Conclusion

Through this project, we worked on building a complete pipeline that combines perception, reasoning, and simulation.

The perception module extracts the board configuration from the physical setup, while the game engine analyzes that configuration and determines a suitable move. The Gazebo simulation provided a useful environment for testing and validating our approach.

Overall, this project gave us valuable experience in combining computer vision, decision-making logic, and robotics simulation to create an autonomous system.
