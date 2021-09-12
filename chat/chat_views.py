import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from src.socket_server import sio

from .models import Message, Room
from .serializer import MessageSerializer, RoomSerializer

jwt_authentication = JWTAuthentication()


def _validate_token(token):
    validated_token = jwt_authentication.get_validated_token(token)
    user = jwt_authentication.get_user(validated_token)
    return user


def _get_token(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def _authenticate(data):
    token = data["access"]
    return _validate_token(token)


@login_required(login_url="login/")
def index(request):
    data = _get_token(request.user)
    return render(request, "index.html", context=data)


# utility function
def get_rooms_id(user) -> list:
    rooms = Room.objects.filter(Q(user1=user) | Q(user2=user)).values_list(
        "id", flat=True
    )
    return list([str(i) for i in rooms])


def leave_rooms(sid, rooms: list) -> None:
    for room in rooms:
        sio.leave_room(sid, room)


# events
@sio.event
def connect(sid, environ, data=None):
    """
    Feature:
    - Connect user.
    - Authenticate user.
    - Join user to rooms.
    - Save {user: User} to sio session.
    - Dispatch online event to connected rooms except self.

    Validation:
    - User identity (access_token).

    data:
    - access_token: Str (user access token)
    - id: UserId (user id) @TODO:
    """
    try:
        print(data)
        # authenticate user
        user = _authenticate(data)

        # save session data
        sio.save_session(sid, {"user": user})
        # print(sio.get_session(sid))

        # join rooms
        rooms = get_rooms_id(user)
        for room in rooms:
            sio.enter_room(sid, room)
        sio.enter_room(sid, user.id)

        sio.emit("online", {"user": user.id}, room=sio.rooms(sid), skip_sid=sid)
    except Exception as e:
        # raise e
        sio.emit("error", {"message": str(e)}, room=sid)
        sio.disconnect(sid)


@sio.event
def disconnect(sid):
    """
    Feature:
    - Dispatch offline event to connected rooms.
    - To disconnect the user.
    - Leave all room that joined @TODO:
    """
    print("Client disconnected", sid)
    try:
        user = sio.get_session(sid)["user"]
        sio.emit("offline", {"user": user.id}, room=sio.rooms(sid), skip_sid=sid)
    except Exception as e:
        # raise e
        sio.emit("error", {"message": str(e)}, room=sid)


@sio.event
def message(sid, message=None):
    """
    Main message event receiver

    Feature:
    - Save message to db.
    - Emit message to all user in the room.

    Validation:
    - User in current room id

    Message:
    - id: id
    - text: Str
    - image: Str
    - room: room.id
    """
    print("message--", sid, message)
    serializer = MessageSerializer(data=message)

    # TODO: Handle room validation in serializer context
    if serializer.is_valid() and message["room"] in sio.rooms(sid):
        user = sio.get_session(sid)["user"]
        serializer.save(user=user)
        data = serializer.data
        sio.send(data, room=str(data["room"]))
    else:
        sio.emit("error", serializer.errors, room=sid)


@sio.event
def seen(sid, message=None):
    """
    Mark message as seen in room

    Validation:
    - User in current room id

    message:
    - id: room.id
    """
    room_id = message.get("id")
    if room_id in sio.rooms(sid):
        user = sio.get_session(sid)["user"]
        Message.objects.filter(~Q(user=user), room=room_id, seen=False).update(
            seen=True
        )
        sio.emit("seen", {"id": room_id}, room=room_id, skip_sid=sid)


@sio.event
def new_room(sid, message=None):
    """
    Connect user to new room and send new_room
    event to opposite user

    Feature:
    - connect user to room.
    - Emit `new_room` event to opposite
    with room data.

    message:
    - id: room.id
    """
    room = Room.objects.filter(id=message["id"]).first()
    if room:
        data = RoomSerializer(room).data
        sio.enter_room(sid, room=message["id"])
        sio.emit("new_room", data, room=room.user1.id)


# DEBUG EVENTS
@sio.event
def rooms(sid, message=None):
    """returns rooms to which a user connected"""
    sio.emit("rooms", data=sio.rooms(sid), room=sid)
