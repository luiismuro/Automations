# 🤖 SignupFormAutomation - Selenium + Java
This project executes the automation task of a user signup flow on the website
[Automation Exercise](https://automationexercise.com), 
by using Java, Selenium WebDriver and the design pattern Page Object Model (POM).


## 🔧 Tecnologies on this project
- Java 17+
- Maven
- Selenium WebDriver
- JUnit 5
- IntelliJ IDEA
- Git / GitHub

## 📁 Folder Structure:

SignupFormAutomation/
│
├── src/
│ ├── driver/ # Chromedriver
│ ├── main/ # currently empty
│ └── test/
│ ├── java/
│ │ ├── SignupTest.java
│ │ ├── SignupPage.java
│ │ └── utils/
│ │ ├── EmailGenerator.java
│ │ └── CredentialLoader.java
│
├── credentials.properties # ⚠️ Ignored on git
├── pom.xml
└── README.md


## 🔐 Credential Protection

The file `credentials.properties` contains sensitive data (email and password) **not versioned** on Git. 
It stores used password on the signup form;

## How to execute:

- Go to the folder src/test/java/
- Open file SignupTest.java
- Run
