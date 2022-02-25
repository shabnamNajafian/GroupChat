# GroupChat

This project is developed to study privacy concerns in generating explanations of group recommendations in the tourism domain using a chat-bot. For this purpose, we implemented a web-based chat-bot that we call Tourybot.
For the UI, we used a client in java (Vaadin AI Chat) - https://github.com/alejandro-du/vaadin-ai-chat, retrieved March 2021- and implemented in the Vaadin framework (an open platform for building web apps in Java (https://vaadin.com/), retrieved September 2021). The backend is written in python. SQLite was used for logging user interactions in the task.
Tourybot includes two chat windows, one for the chat between the system bot and individual members (see the first screenshot), and the other for the chat with the Group (see the second screenshot). Users can seamlessly switch between the two conversations to add system-generated recommendations and explanations to their discussions with other group members.

Following are two screenshots of the system in the _peer majority-competitive task_ scenario:

The screenshot of the chatbot represents the chat in the **peer majority and competitive task scenario** between an active user and his group. a) indicates two ongoing chats, one with a chat-bot and the group, b) indicates the Tourybot suggest a place (the Oriental City in this example) for the whole group, one active user (John) and his two group members (the two other group members, Bob and Alice, are hypothetical) in a group chat.

<img width="830" alt="group" src="https://user-images.githubusercontent.com/5775658/155727311-2ae231d1-2db8-4c79-a2f0-8cc386035188.png">


The following screenshot shows an example of chats where the active user is in the peer majority scenario means he agrees with the majority preference in this case with his peer and is given a competitive task. a) indicates that there are two chats, one with a chat-bot and the other with the group (the chat switches between the group and Tourybot), b) indicates an \textit{ongoing} chat with a chat-bot (TouryBot). Here the user can indicate how much information they want to share to convince the other group member (Bob) to visit the suggested POI.

<img width="819" alt="toury" src="https://user-images.githubusercontent.com/5775658/155727333-9e848fac-a569-457b-a265-75dae7f3a743.png">


