import type { Message } from "../../types";
import { socketActions } from "../../enums";

export function sendMessage(socket, message: Message) {
  socket.emit(socketActions.sendMessage, message);
}
