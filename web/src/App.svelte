<script lang="ts">
  import { onMount } from "svelte";
  import { io } from "socket.io-client";

  import { joinRoom, leaveRoom, sendMessage } from "./utils/socketFunctions";
  import { socketActions } from "./enums";

  import Button from "./lib/Button.svelte";
  import Chat from "./lib/Chat.svelte";

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

  const handleJoinRoom = () => joinRoom(socket, { username, roomName });

  const handleLeaveRoom = () => leaveRoom(socket, { username, roomName });

  const handleSendMessage = (customEvent) => {
    isLoading = true;

    const message = customEvent.details;

    sendMessage(socket, message);
  };

  onMount(() => {
    socket.connect();
  });

  socket.on("join_chat", (message) => {
    if (message.joined) {
      isJoinedRoom = true;
    }
  });

  socket.on("leave_chat", (message) => {
    if (message.left) {
      isJoinedRoom = false;
    }
  });

  socket.on("recieve_message", (message) => {
    if (message.username === username) {
      isLoading = false;
    }

    messages = [...messages, message];
  });
</script>

<main class="flex flex-col justify-center max-w-screen-xl m-auto">
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
    <h1>Hello World</h1>

    <div>
      <label for="username">Enter your username</label>
      <input name="username" type="text" bind:value={username} />
    </div>

    <div>
      <label for="room-name">Enter the room you want to join</label>
      <input name="room-name" type="text" bind:value={roomName} />
    </div>

    <Button
      buttonText={isJoinedRoom ? "Leave" : "Join"}
      buttonHandler={isJoinedRoom ? handleLeaveRoom : handleJoinRoom}
    />

    {#if isJoinedRoom}
      <Chat
        {username}
        {roomName}
        {messages}
        {isLoading}
        on:sendChatMessage={handleSendMessage}
      />
    {/if}
  {/if}
</main>

<style global lang="postcss">
  @tailwind utilities;
  @tailwind components;
  @tailwind base;
</style>
