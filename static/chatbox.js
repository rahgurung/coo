var global_channel_list = [];
var global_user_list = [];
var global_current_channel;
var msgType = "PUBLIC";
let displayname = localStorage.getItem('displayname');;


// this function weighs and unweighs the channel
// chn means channel parameter here
function clickhandler(chn) {
  if (global_channel_list.includes(global_current_channel)) {
    document.getElementbyId(global_current_channel).style.fontWeight = "normal";
  }

  global_current_channel = chn;
  msgType = "PUBLIC";
  let header = document.getElementbyId("message_header");

  document.getElementbyId(global_current_channel).style.fontWeight = "bold";
  header.innerHTML = " Messages on " + global_current_channel + "channel";
  localStorage.setItem("channel", global_current_channel)
  configure_msgs(global_current_channel, msgType)
}


// this function weighs the new channel and unweighs the old channel
// chn means channel parameter here
function dm_clickhandler(usr) {
    let header = document.getElementById("message_header");
    msgType = "PRIVATE";

    document.getElementById(global_current_channel).style.fontWeight = "normal";

    global_current_channel = usr;
    document.getElementById(usr).style.fontWeight = "bold";

    hdr.innerHTML = "Conversations with " + usr;
    configure_msgs(usr, msgType);
}
