### HTTPs APIS Available

#### Web Pages -
- home:
    - URL: "/"

- login:
    - URL: "/login/"

- logout:
    - URL: "/logout/"

#### API -
- Access Token:
  - URL: "/api/token/"
  - Method: POST
  - body: 
    ```json
    {
        "username": "",
        "password": ""
    }
    ```
  - response:
    ```json
    {
        "access": "",
        "refresh": "",
    }
    ```

- Refresh Token:
  - URL: "/api/token/refresh/"
  - Method: POST
  - Body:
  ```json
  {
      "refresh": ""
  }
  ```
  - Response:
  ```json
  {
      "access": ""
  }
  ```

- Room List:
  - URL: "/api/room/"
  - Method: ["GET", "POST"]
  - GET: 
    ```json
    [{
        "id": 8,
        "student": {
            "id": 2,
            "first_name": "",
            "last_name": "",
            "email": "",
            "image": "http://127.0.0.1:8000/default.jpg.webp"
        },
        "teacher": {
            "id": 3,
            "first_name": "",
            "last_name": "",
            "email": "",
            "image": "http://127.0.0.1:8000/default.jpg_kopT5f1.webp"
        },
        "status": "closed",
        "timestamp": "2021-08-26T07:42:42.087078Z",
        "text": "hello",
        "image": ""
    }]
    ```
  - POST:
    - body:
        ```json
        {
            "text": "some text",
            "image": ""
        }
        ```
    - header:
        ```json
        Bearer {{token}}
        ```
    - response: Same as [GET](#api)

- Message List:
  - URL: "/api/<int:room>/messages/"
  - GET:
    ```json
    [
        {
            "id": 11,
            "text": "hello",
            "image": "",
            "seen": false,
            "timestamp": "2021-08-26T07:59:57.561146Z",
            "room": 11,
            "user": 2
        }
    ]
    ```

### Socket.io Events 
Base URL - "/"

#### Server Event (Events send to server from client):
- disconnect
- connect: Connect to socket.io server.

    auth:
    - access_token: Str
    - id: UserId

- join_room: Join the room having status active.

    Permission: Only Teacher

    data:
    - room: RoomId

- close_room: Close a room i.e. change status to closed.

    Permission: Only Teacher

    data:
    - room: RoomId

- message: Send message to all in room.

    Permission: all

    data:
    - text: Str
    - image: Str
    - room: RoomId

- seen: Mark message as seen for opposite user.

    Permission: all

    data:
    - room: RoomId

- new_room: Connect user to new room and send `new_room`
    event to teacher group

    Permission: student

    data:
    - room: RoomId


#### Client Event (Event send to client from server):
- room_joined: Emits when teacher joins the room first time. Room status changes active -> engaged.

    reciever: all

    @response:
    - room: RoomId
    - teacher: {"id": UserId, "first_name": Str, "last_name": Str, "image": Str}
    - status: Str ("engaged")

- room_closed: Emits when teacher close the room.
    Room status changes engaged -> closed.
    Disconnects both user from room its means no 
    more message will be accepted in the room.

    reciever: all

    @response:
    - status: Str ("closed")
    - room: RoomId

- message: Emits to all when user send message in room.

    reciever: all

    @response:
    - text: Str
    - image: Str
    - timestamp: Datetime(ISO Format)
    - user: UserId
    - room: RoomId

- online: Emits to all when a user come online in room.

    reciever: all

    @respose:
    - user: UserId

- offline: Emits to all when a user goes offline in room.

    reciever: all

    @response:
    - user: UserId

- seen: Emits when a user see all the message.

    reciever: all

    @response:
    - room: RoomId
    - user: UserId (Of opposite user)

- new_room: Emits when a new room is created.

    reciever: teacher

    @response: room API Response

#### Debug Events (ping/pong)
- rooms:
    return the rooms id to which a user connected.

    reciever: self

    @response:
    - rooms: RoomId[]
