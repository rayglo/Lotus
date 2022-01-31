#!/usr/bin/env python3
import time
from sys import argv, stdout
from threading import Thread
import GameData
import socket
from constants import *
import os
import sys

sys.path.append(os.path.abspath("../"))
from LotusEngine import LotusEngine

if len(argv) < 4:
    print("You need the player name to start the game.")
    # exit(-1)
    playerName = "Test"  # For debug
    ip = HOST
    port = PORT
else:
    playerName = argv[3]
    ip = argv[1]
    port = int(argv[2])

run = True

statuses = ["Lobby", "Game", "GameHint"]

status = statuses[0]

firstSet = False

lotus_engine = LotusEngine(playerName)

hintState = ("", "")


def manageInput():
    global run
    global status
    while run:
        command = input()
        # Choose data to send
        if command == "exit":
            run = False
            os._exit(0)
        elif command == "ready" and status == statuses[0]:
            s.send(GameData.ClientPlayerStartRequest(playerName).serialize())
        elif command == "show" and status == statuses[1]:
            s.send(GameData.ClientGetGameStateRequest(playerName).serialize())
        elif command.split(" ")[0] == "discard" and status == statuses[1]:
            try:
                cardStr = command.split(" ")
                cardOrder = int(cardStr[1])
                s.send(GameData.ClientPlayerDiscardCardRequest(playerName, cardOrder).serialize())
            except:
                print("Maybe you wanted to type 'discard <num>'?")
                continue
        elif command.split(" ")[0] == "play" and status == statuses[1]:
            try:
                cardStr = command.split(" ")
                cardOrder = int(cardStr[1])
                s.send(GameData.ClientPlayerPlayCardRequest(playerName, cardOrder).serialize())
            except:
                print("Maybe you wanted to type 'play <num>'?")
                continue
        elif command.split(" ")[0] == "hint" and status == statuses[1]:
            try:
                destination = command.split(" ")[2]
                t = command.split(" ")[1].lower()
                if t != "colour" and t != "color" and t != "value":
                    print("Error: type can be 'color' or 'value'")
                    continue
                value = command.split(" ")[3].lower()
                if t == "value":
                    value = int(value)
                    if int(value) > 5 or int(value) < 1:
                        print("Error: card values can range from 1 to 5")
                        continue
                else:
                    if value not in ["green", "red", "blue", "yellow", "white"]:
                        print("Error: card color can only be green, red, blue, yellow or white")
                        continue
                s.send(GameData.ClientHintData(playerName, destination, t, value).serialize())
            except:
                print("Maybe you wanted to type 'hint <type> <destinatary> <value>'?")
                continue
        elif command.split(" ")[0] == "query" and status == statuses[1]:
            print(f"executing query {command.split(' ')[1]}")
            print(lotus_engine.query(command.split(' ')[1]))
            continue
        elif command == "":
            print("[" + playerName + " - " + status + "]: ", end="")
        else:
            print("Unknown command: " + command)
            continue
        stdout.flush()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    request = GameData.ClientPlayerAddData(playerName)
    s.connect((HOST, PORT))
    s.send(request.serialize())
    data = s.recv(DATASIZE)
    data = GameData.GameData.deserialize(data)
    if type(data) is GameData.ServerPlayerConnectionOk:
        print("Connection accepted by the server. Welcome " + playerName)
    print("[" + playerName + " - " + status + "]: ", end="")
    Thread(target=manageInput).start()
    while run:
        dataOk = False
        data = s.recv(DATASIZE)
        if not data:
            continue
        data = GameData.GameData.deserialize(data)
        print("\n================= " + type(data).__name__ + " received =================")
        if type(data) is GameData.ServerPlayerStartRequestAccepted:
            dataOk = True
            print("Ready: " + str(data.acceptedStartRequests) + "/" + str(data.connectedPlayers) + " players")
            data = s.recv(DATASIZE)
            data = GameData.GameData.deserialize(data)
        if type(data) is GameData.ServerStartGameData:  # Received when the game starts
            dataOk = True
            print("Game start!")
            s.send(GameData.ClientPlayerReadyData(playerName).serialize())
            status = statuses[1]
            time.sleep(1)
            s.send(GameData.ClientGetGameStateRequest(playerName).serialize())
        if type(data) is GameData.ServerGameStateData:  # Received everytime a "show" command is invoked
            dataOk = True
            if not firstSet:  # If this is the first time i'm requesting data
                for p in data.players:
                    if p.name == playerName:
                        continue
                    lotus_engine.add_player(p.name)
                    for i in range(len(p.hand)):
                        lotus_engine.draw_card(p.name, p.hand[i].color, p.hand[i].value, i)
                firstSet = True
            print("Current player: " + data.currentPlayer)
            print("Player hands: ")
            for p in data.players:
                print(p.toClientString())
            print("Cards in your hand: " + str(data.handSize))
            print("Table cards: ")
            for pos in data.tableCards:
                print(pos + ": [ ")
                for c in data.tableCards[pos]:
                    print(c.toClientString() + " ")
                print("]")
            print("Discard pile: ")
            for c in data.discardPile:
                print("\t" + c.toClientString())
            print("Note tokens used: " + str(data.usedNoteTokens) + "/8")
            print("Storm tokens used: " + str(data.usedStormTokens) + "/3")
            lotus_engine.set_current_player(data.currentPlayer)
        if type(data) is GameData.ServerActionInvalid:  # Called everytime an action is not allowed
            dataOk = True
            print("Invalid action performed. Reason:")
            print(data.message)
        if type(data) is GameData.ServerActionValid:  # Called everytime someone discards a card
            dataOk = True
            print(f"card to discard: ({data.card.color}, {data.card.value})")
            lotus_engine.discard_card(data.lastPlayer, data.cardHandIndex)

            data
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                s2.connect((HOST, PORT))
                s2.send(GameData.ClientGetGameStateRequest(playerName).serialize())
                data_inner = s2.recv(DATASIZE)
                data_inner = GameData.GameData.deserialize(data_inner)
                player = None
                for p in data_inner.players:
                    if p.name == data.lastPlayer:
                        player = p
                        break
                card = player.hand[4]
                lotus_engine.draw_card(data.lastPlayer, card.color, card.value, 4)
                stdout.flush()

            print("Action valid!")
            print("Current player: " + data.player)
        if type(data) is GameData.ServerPlayerMoveOk:  # Called everytime someone plays a card and the move is fine
            dataOk = True
            print("Nice move!")
            print("Current player: " + data.player)
        if type(data) is GameData.ServerPlayerThunderStrike:  # Called everytime someone plays a wrong card
            dataOk = True
            print("OH NO! The Gods are unhappy with you!")
        if type(data) is GameData.ServerHintData:  # Called every time a player gives/gets an hint
            dataOk = True
            print("Hint type: " + data.type)
            print("Player " + data.destination + " cards with value " + str(data.value) + " are:")
            for i in data.positions:
                print("\t" + str(i))
        if type(data) is GameData.ServerInvalidDataReceived:  # Called everytime a data package sent is badly formed
            dataOk = True
            print(data.data)
        if type(data) is GameData.ServerGameOver:  # Received whenever 3 red tokens are reached
            dataOk = True
            print(data.message)
            print(data.score)
            print(data.scoreMessage)
            stdout.flush()
            # run = False
            print("Ready for a new game!")
        if not dataOk:
            print("Unknown or unimplemented data type: " + str(type(data)))
        print("[" + playerName + " - " + status + "]: ", end="")
        stdout.flush()
