<script lang="ts">
  import { onMount } from "svelte";
  import { io } from "socket.io-client";

  import { joinRoom, leaveRoom, sendMessage } from "./utils/socketFunctions";
  import { validationMessages } from "./utils/constants";
  import { socketActions } from "./enums";

  import Header from "./lib/Header.svelte";
  import Button from "./lib/Button.svelte";
  import Chat from "./lib/Chat.svelte";
  import InputField from "./lib/InputField.svelte";

  const socket = io("http://localhost:5000");

  let socketError = null;

  socket.on(socketActions.connectionError, (e) => {
    socketError = {
      title: "Connection error",
      message: e.message,
    };
  });

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
    username: '',
    roomName: '',
  }

  let dirtyFields = {
    username: false,
    roomName: false,
  }

  onMount(() => {
    socket.connect();
  });

  $: {
    if(username === '' && dirtyFields.username) {
        validationErrors.username = validationMessages.required;
    }
    else {
        validationErrors.username = '';
    }

    if (roomName === '' && dirtyFields.roomName) {
        validationErrors.roomName = validationMessages.required;
    }
    else {
        validationErrors.roomName = '';
    }

    isFormValid = Object.values(validationErrors).every((value) => value === '');
  }

  $: fieldsUntouched = Object.values(dirtyFields).some((value) => value === false);

  const handleJoinRoom = () => {
    if(fieldsUntouched) {
      Object.keys(dirtyFields).forEach((key) => {
          dirtyFields[key] = true;
      });

      return
    }


    if (!isFormValid) {
      return
    }

    const chatAction = {
      username,
      roomName,
    };

    joinRoom(socket, chatAction)
  };

  const handleLeaveRoom = () => leaveRoom(socket, { username, roomName });

  const handleSendMessage = (customEvent) => {
    isLoading = true;

    const message = customEvent.detail;

    sendMessage(socket, message);
    isLoading = false;
  };

  socket.on(socketActions.joinRoom, (message) => {
    if (message.joined) {
      isJoinedRoom = true;
    }
  });

  socket.on(socketActions.leaveRoom, (message) => {
    if (message.left) {
      messages = [];
      isJoinedRoom = false;
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
  });
</script>

<main
  class="flex flex-col justify-start h-screen bg-gradient-to-r from-black to-gray-800"
>
  <Header />
  <div
    class="flex-1 flex flex-col justify-between max-w-screen-xl w-full mx-auto p-4"
  >
    {#if socketError}
      <h1 class="text-5xl font-bold text-red-700 text-center">
        {socketError.title}
      </h1>
      <pre class="text-red-500">{JSON.stringify(
          socketError.message,
          null,
          4
        )}</pre>
    {:else}
      <div class="grid gap-6 mb-2">
        <InputField
          bind:value={username}
          label="Username"
          placeholder="Someone"
          disabled={isJoinedRoom}
          error="{validationErrors.username}"
          on:becomeDirty={() => dirtyFields.username = true}
          id="username"
        />

        <InputField
          bind:value={roomName}
          label="Room Name"
          placeholder="SomeRoom45"
          disabled={isJoinedRoom}
          error="{validationErrors.roomName}"
          on:becomeDirty={() => dirtyFields.roomName = true}
          id={"room_name"}
        />

        <Button
          buttonText={isJoinedRoom ? "Leave" : "Join"}
          buttonHandler={isJoinedRoom ? handleLeaveRoom : handleJoinRoom}
        />
      </div>

      {#if isJoinedRoom}
        <div class="flex-1">
          <Chat
            {username}
            {roomName}
            {messages}
            {isLoading}
            on:sendChatMessage={handleSendMessage}
          />
        </div>
      {/if}
    {/if}
  </div>
</main>

<style global lang="postcss">
  @tailwind utilities;
  @tailwind components;
  @tailwind base;
</style>
