
<!-- PROJECT LOGO -->

<p align="center">
  <h3 align="center">Multiplayer Chess Webapp</h3>
  <p align="center">
    <a href="https://github.com/Christian267/Chess-Web-App"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"></a>
    <a href="https://github.com/christian267/chess-web-app/issues">Report Bug</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#overview">Overview</a>
      <ul>
        <li><a href="#design">Design</a></li>
      </ul>
      <ul>
        <li><a href="#features">Features</a></li>
      </ul>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Overview
### Design

### Features
  <h3 align="center">Play live chess games with your friends!</h3>
<p align="center">
  <img src=".\images\chess_demo.gif" width=550>
</p>
  <h3 align="center">View and climb the leaderboards!</h3>
<p align="center">
  <img src=".\images\leaderboard.png" width=400>
</p>
  <h3 align="center">Review your performance through your personal match history</h3>
<p align="center">
  <img src=".\images\match_history.png" width=400>
</p>


### Built With
* [Bootstrap](https://getbootstrap.com)
* [Chessboard.js](https://chessboardjs.com/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [PostgreSQL](https://www.postgresql.org/)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The required python packages to run this application are found in requirements.txt

### Installation

<!-- 1. Get a free API Key at [https://example.com](https://example.com) -->
1. Clone the repo
   ```sh
   git clone https://github.com/Christian267/Chess-Web-App
   ```
2. Create and activate a virtual environment
   ```sh
   python3 -m venv venv

   venv\scripts\activate
   ```
3. Install required packages
   ```sh
   pip install requirements.txt
   ```
4. Initialize the database
   ```sh
   BASH
   $ export FLASK_APP=chessapp
   $ flask init-db
   ```
   CMD
   ```sh
   > set FLASK_APP=chessapp
   > flask init-db
   ```
   Powershell
   ```sh
   > $env:FLASK_APP = "flaskr"
   > flask init-db
   ```
  
5. Run the Flask application and copy/paste the url into your browser
   ```sh
   python3 main.py
   ```
<!-- CONTACT -->
## Contact

Christian Benitez - chrisbntz81@gmail.com

Project Link: [https://github.com/christian267/Chess-Web-App](https://github.com/christian267/Chess-Web-App)
