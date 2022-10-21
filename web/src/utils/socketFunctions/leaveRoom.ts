import { ChatAction } from "../../types";
import { socketActions } from "../../enums/index";

export function leaveRoom(socket, chatAction: ChatAction) {
  socket.emit(socketActions.leaveRoom, chatAction);
}
