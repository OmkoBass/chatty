<script lang="ts">
  // FOR SOME REASON I CANNOT IMPORT TYPES, I GET AN ERROR 500 FROM SVELTE
  // NEXT.JS Is the best
  import { onMount } from "svelte";
  import { io } from "socket.io-client";

  import { joinRoom, leaveRoom, sendMessage } from "./utils/socketFunctions";
  import { validationMessages } from "./utils/constants";
  import { socketActions } from "./enums";

  import Header from "./lib/Header.svelte";
  import Button from "./lib/Button.svelte";
  import Chat from "./lib/Chat.svelte";
  import InputField from "./lib/InputField.svelte";
  import Error from "./lib/Error.svelte";

  const socket = io("http://localhost:5000");

  // These are all the errors that can trigger and be displayed to the user
  // I would group these up in an error object but typescript is being a pain
  let socketError = null
  let joinRoomError = null
  let messageError = null

  // On connection error display error
  socket.on(socketActions.connectionError, (e) => {
    socketError = {
      title: "Connection error",
      message: e.message,
    };
  });

  // On connection success let the user through
  socket.on(socketActions.connect, () => {
    socketError = null;
  });

  let roomName = "";
  let username = "";
  let isJoinedRoom = false;
  let messages = [];
  let isLoading = false;

  let isFormValid = false;
  let validationErrors = {
    username: "",
    roomName: "",
  };

  let dirtyFields = {
    username: false,
    roomName: false,
  };

  // Connect to the socket when the component mounts
  onMount(() => {
    socket.connect();
  });

  // This is a computed property that will run when the username or roomName changes.
  // It will validate the fields and set the errors and isFormValid
  $: {
    if (username === "" && dirtyFields.username) {
      validationErrors.username = validationMessages.required;
    } else {
      validationErrors.username = "";
    }

    if (roomName === "" && dirtyFields.roomName) {
      validationErrors.roomName = validationMessages.required;
    } else {
      validationErrors.roomName = "";
    }

    isFormValid = Object.values(validationErrors).every(
      (value) => value === ""
    );
  }

  // This is a computed property that will be true or false depending on the dirty fields
  $: fieldsUntouched = Object.values(dirtyFields).some(
    (value) => value === false
  );

  const handleJoinRoom = () => {
    if (fieldsUntouched) {
      Object.keys(dirtyFields).forEach((key) => {
        dirtyFields[key] = true;
      });

      return;
    }

    if (!isFormValid) {
      return;
    }

    const chatAction = {
      username,
      roomName,
    };

    joinRoom(socket, chatAction);
  };

  const handleLeaveRoom = () => leaveRoom(socket, { username, roomName });

  const handleSendMessage = (customEvent) => {
    isLoading = true;

    const message = customEvent.detail;

    sendMessage(socket, message);
    isLoading = false;
  };

  socket.on(socketActions.joinRoom, (message) => {
    if(message.errors) {
      joinRoomError = message.errors
      return
    }

    if (message.joined === true) {
      isJoinedRoom = true;
      joinRoomError = null
    }
  });

  socket.on(socketActions.leaveRoom, (message) => {
    if (message.left) {
      messages = [];
      isJoinedRoom = false;
    }
  });

  socket.on(socketActions.sendMessage, (message) => {
    if(message.error) {
      messageError = message.error
      return
    }
  });

  socket.on(socketActions.receiveMessage, (message) => {
    if (message.username === username) {
      isLoading = false;
    }

    const { leaver } = message;

    if (!leaver) {
      messages = [...messages, message];
      return;
    }

    const leaveMessage = {
      username: "",
      roomName,
      message: `${leaver} has left the room`,
    };

    messages = [...messages, leaveMessage];
    messageError = null
  });
</script>

<main
  class="flex flex-col min-h-screen h-full bg-gradient-to-r from-black to-gray-800"
>
  <Header />
  <div
    class="flex-1 flex flex-col justify-between max-w-screen-xl w-full h-full mx-auto p-4"
  >
    {#if socketError}
      <Error errorMessage={socketError} isVisible={!!socketError} />
    {/if}
    {#if !socketError}
      <div class="flex flex-col gap-4 mb-2">
        {#if !isJoinedRoom}
          <InputField
            bind:value={username}
            label="Username"
            placeholder="Someone"
            disabled={isJoinedRoom}
            error={validationErrors.username}
            on:becomeDirty={() => (dirtyFields.username = true)}
            id="username"
          />

          <InputField
            bind:value={roomName}
            label="Room Name"
            placeholder="SomeRoom45"
            disabled={isJoinedRoom}
            error={validationErrors.roomName}
            on:becomeDirty={() => (dirtyFields.roomName = true)}
            id={"room_name"}
          />
        {/if}

        <Button
          buttonText={isJoinedRoom ? "Leave" : "Join"}
          buttonHandler={isJoinedRoom ? handleLeaveRoom : handleJoinRoom}
        />

        <Error errorMessage={joinRoomError} isVisible={!!joinRoomError} />
      </div>

      {#if isJoinedRoom}
        <Error errorMessage={messageError} isVisible={!!messageError} />
        <Chat
          {username}
          {roomName}
          {messages}
          {isLoading}
          on:sendChatMessage={handleSendMessage}
        />
      {/if}
    {/if}
  </div>
</main>

<style global lang="postcss">
  @tailwind utilities;
  @tailwind components;
  @tailwind base;
</style>
